"""
启信宝爬虫核心模块
"""
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from browser import BrowserManager
from utils import (
    load_config,
    parse_cookie_string,
    random_delay,
    human_like_typing,
    extract_text_content
)


class QixinbaoCrawler:
    """启信宝爬虫类"""

    def __init__(self, config_path: str = 'config.json'):
        """
        初始化爬虫

        Args:
            config_path: 配置文件路径
        """
        self.config = load_config(config_path)
        self.browser_manager = BrowserManager(self.config)
        self.cookie = parse_cookie_string(
            self.config.get('cookie', ''),
            domain='.qixin.com'
        )
        self.delays = self.config.get('delays', {'min': 1.0, 'max': 3.0})
        self.base_url = "https://www.qixin.com"

    async def search_company(self, page: Page, company_name: str) -> bool:
        """
        搜索公司

        Args:
            page: 页面对象
            company_name: 公司名称

        Returns:
            是否成功搜索到结果
        """
        try:
            # 访问首页（等待网络空闲，确保反爬JS执行完毕）
            print(f"正在搜索: {company_name}")
            await page.goto(
                f"{self.base_url}/",
                wait_until='networkidle',
                timeout=30000
            )
            await random_delay(*self.delays.values())

            # 查找搜索框（尝试多个可能的选择器）
            search_selectors = [
                'input[placeholder*="搜索"]',
                'input[placeholder*="企业名称"]',
                'input.search-input',
                '#search-input',
                '.search-box input',
                'input[name="key"]',
                '.qixin-search-input'  # 备用选择器
            ]

            search_input = None
            used_selector = None
            for selector in search_selectors:
                try:
                    search_input = await page.wait_for_selector(
                        selector,
                        timeout=3000
                    )
                    if search_input:
                        used_selector = selector
                        print(f"[调试] 使用搜索框选择器: {selector}")
                        break
                except:
                    continue

            if not search_input:
                print("未找到搜索框，尝试直接搜索URL")
                # 构造搜索URL
                search_url = f"{self.base_url}/search?key={company_name}"
                await page.goto(
                    search_url,
                    wait_until='networkidle',
                    timeout=30000
                )
            else:
                # 输入公司名称（直接填充，不用模拟打字）
                print("[调试] 正在输入公司名称...")
                try:
                    await page.fill(used_selector, company_name)
                    print(f"[调试] 公司名称已输入: {company_name}")
                except Exception as e:
                    print(f"[调试] 输入公司名称失败: {e}")
                    raise
                await random_delay(0.5, 1.0)

                # 点击搜索按钮
                search_button_selectors = [
                    'button[type="submit"]',
                    '.search-button',
                    '.search-btn',
                    'button:has-text("搜索")',
                    '.icon-search',  # 图标按钮
                    'a.search-btn',   # 链接按钮
                    '.search-icon',    # 搜索图标
                    'i.search'         # 图标元素
                ]

                button_clicked = False
                print("[调试] 尝试点击搜索按钮...")
                for idx, selector in enumerate(search_button_selectors):
                    try:
                        print(f"[调试] 尝试选择器 {idx + 1}/{len(search_button_selectors)}: {selector}")
                        await page.click(selector, timeout=2000)
                        print(f"[调试] 成功点击搜索按钮: {selector}")
                        button_clicked = True
                        break
                    except Exception as e:
                        print(f"[调试] 选择器 {selector} 失败: {str(e)[:50]}")
                        continue

                # 如果没有找到搜索按钮，尝试按 Enter 键
                if not button_clicked:
                    print("[调试] 所有搜索按钮选择器都失败，尝试按 Enter 键")
                    try:
                        await page.press(used_selector, 'Enter')
                        print("[调试] 已按 Enter 键")
                    except Exception as e:
                        print(f"[调试] 按 Enter 键失败: {e}")

            # 等待搜索结果加载（增强等待机制）
            print("[调试] 等待搜索结果加载...")
            print(f"[调试] 当前 URL: {page.url}")

            # 关键改进：先等待 3-5 秒，让搜索结果列表完全渲染
            print("[调试] 等待 3 秒让搜索结果列表渲染...")
            await asyncio.sleep(3)

            try:
                # 先等待 URL 变化（搜索通常会跳转）
                await page.wait_for_url('*search*', timeout=5000)
                print(f"[调试] URL 已变化到搜索页面: {page.url}")
            except:
                print(f"[调试] URL 没有变化，当前仍是: {page.url}")

            # 等待关键元素出现（查询结果容器）
            print("[调试] 等待搜索结果容器出现...")
            result_indicators = [
                '.search-result-list',
                '.company-list',
                '.result-list',
                'text=查询结果',
                'text=搜索结果',
                'text=共',
                '[class*="result"]'
            ]

            indicator_found = False
            for indicator in result_indicators:
                try:
                    await page.wait_for_selector(indicator, timeout=3000)
                    print(f"[调试] 找到结果指示器: {indicator}")
                    indicator_found = True
                    break
                except:
                    continue

            if not indicator_found:
                print("[调试] 未找到结果指示器，但继续执行...")

            # 等待网络空闲（加载完成）
            print("[调试] 等待网络空闲...")
            await page.wait_for_load_state('networkidle', timeout=15000)
            print("[调试] 页面加载完成")

            # 再次等待，确保动态内容渲染完成
            print("[调试] 额外等待 2 秒确保动态内容渲染...")
            await asyncio.sleep(2)

            return True

        except Exception as e:
            print(f"搜索失败: {e}")
            return False

    async def click_first_result(self, page: Page) -> bool:
        """
        点击第一个搜索结果

        Args:
            page: 页面对象

        Returns:
            是否成功点击
        """
        try:
            print("[调试] 等待搜索结果列表渲染...")
            # 等待搜索结果列表完全渲染（关键改进）
            await asyncio.sleep(3)  # 初始等待 3 秒

            # 等待包含"查询结果"或类似文字的容器出现
            result_container_selectors = [
                '.search-result-list',
                '.company-list',
                '.result-list',
                '[class*="result"]',
                '[class*="list"]'
            ]

            container_found = False
            for container_selector in result_container_selectors:
                try:
                    await page.wait_for_selector(container_selector, timeout=3000)
                    print(f"[调试] 找到结果容器: {container_selector}")
                    container_found = True
                    break
                except:
                    continue

            if not container_found:
                print("[调试] 未找到结果容器，尝试直接查找第一条结果")

            # 尝试多个可能的结果选择器（按优先级排序）
            result_selectors = [
                'a.company-name',                    # 方案 A: 最直接
                '.search-result-list .item:first-child a',  # 方案 B: 列表容器
                'a[href*="/company/"]',              # 方案 C: 属性选择器
                '.company-item a',                   # 备用 1
                '.search-result-item a',             # 备用 2
                '.company-list-item:first-child a',  # 备用 3
                '.result-item:first-child a',        # 备用 4
                'div[class*="item"] a:first-child',  # 备用 5: 模糊匹配
                'a[class*="company"]'                # 备用 6: 模糊匹配
            ]

            link_element = None
            used_selector = None

            for idx, selector in enumerate(result_selectors):
                try:
                    print(f"[调试] 尝试选择器 {idx + 1}/{len(result_selectors)}: {selector}")
                    link_element = await page.wait_for_selector(selector, timeout=3000)
                    if link_element:
                        used_selector = selector
                        print(f"[调试] 找到链接元素: {selector}")
                        break
                except Exception as e:
                    print(f"[调试] 选择器 {selector} 未找到: {str(e)[:50]}")
                    continue

            if not link_element:
                print("[!] 未找到搜索结果链接")
                # 截图保存当前页面状态，方便调试
                await page.screenshot(path="search_page_debug.png")
                print("[调试] 已保存搜索页面截图: search_page_debug.png")
                return False

            # 处理新窗口打开问题（关键改进）
            print("[调试] 检测链接是否会在新窗口打开...")

            # 使用 JavaScript 强制在当前窗口打开
            try:
                await page.evaluate(
                    f'''
                    () => {{
                        const links = document.querySelectorAll("{used_selector}");
                        links.forEach(link => {{
                            link.target = "_self";
                            link.setAttribute("target", "_self");
                        }});
                    }}
                    '''
                )
                print("[调试] 已强制链接在当前窗口打开")
            except Exception as e:
                print(f"[调试] JS 执行失败（非致命）: {e}")

            # 记录当前 URL，用于后续验证跳转
            old_url = page.url
            print(f"[调试] 点击前 URL: {old_url}")

            # 点击链接
            print(f"[调试] 正在点击链接: {used_selector}")
            await link_element.click(timeout=5000)

            # 等待页面跳转或加载（关键改进）
            print("[调试] 等待页面跳转...")

            # 等待 URL 变化（通常会跳转到详情页）
            try:
                await page.wait_for_url(
                    lambda url: url != old_url and "/company/" in url,
                    timeout=8000
                )
                print(f"[调试] URL 已变化: {old_url} -> {page.url}")
            except:
                print("[调试] URL 未变化，检查是否弹出新窗口...")

                # 检查是否有新窗口打开
                try:
                    contexts = page.context.pages
                    if len(contexts) > 1:
                        print(f"[调试] 检测到 {len(contexts)} 个标签页，切换到新标签页")
                        # 切换到新打开的页面
                        new_page = contexts[-1]
                        # 关闭旧页面，使用新页面
                        await page.close()
                        # 更新 page 引用（这里需要特殊处理，暂时只记录）
                        print(f"[调试] 新页面 URL: {new_page.url}")
                        return True
                except:
                    print("[调试] 没有检测到新窗口")

            # 等待详情页加载完成（关键改进）
            await asyncio.sleep(2)
            print("[调试] 等待详情页网络空闲...")
            try:
                await page.wait_for_load_state('networkidle', timeout=10000)
                print("[调试] 详情页加载完成")
            except:
                print("[调试] 网络未完全空闲，继续执行...")

            # 验证是否真的进入了详情页
            current_url = page.url
            print(f"[调试] 当前页面 URL: {current_url}")

            # 检查 URL 是否包含公司详情页的特征
            if '/company/' in current_url or '/firm/' in current_url or '/ent/' in current_url:
                print("[OK] 成功进入公司详情页")
                return True
            else:
                print("[!] 警告: URL 不像详情页，但继续尝试提取数据")

                # 截图保存当前状态
                await page.screenshot(path="after_click_debug.png")
                print("[调试] 已保存点击后截图: after_click_debug.png")

                return True  # 继续尝试提取

        except Exception as e:
            print(f"[X] 点击结果失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def click_first_result_with_page_switch(self, page: Page) -> Optional[Page]:
        """
        点击第一个搜索结果并切换到详情页（处理新窗口）

        Args:
            page: 搜索结果页面对象

        Returns:
            详情页的 Page 对象（可能是新窗口，也可能是原页面）
        """
        try:
            print("[调试] 等待搜索结果列表渲染...")
            # 等待搜索结果列表完全渲染（关键改进）
            await asyncio.sleep(3)

            # 等待包含"查询结果"或类似文字的容器出现
            result_container_selectors = [
                '.search-result-list',
                '.company-list',
                '.result-list',
                '[class*="result"]',
                '[class*="list"]'
            ]

            container_found = False
            for container_selector in result_container_selectors:
                try:
                    await page.wait_for_selector(container_selector, timeout=3000)
                    print(f"[调试] 找到结果容器: {container_selector}")
                    container_found = True
                    break
                except:
                    continue

            if not container_found:
                print("[调试] 未找到结果容器，尝试直接查找第一条结果")

            # 尝试多个可能的结果选择器（按优先级排序）
            result_selectors = [
                'a.company-name',
                '.search-result-list .item:first-child a',
                'a[href*="/company/"]:first-child',      # 只选择第一个
                'a[href*="/company/"]:nth-of-type(1)',  # 另一种选择第一个的方式
                '.company-item a',
                '.search-result-item a',
                '.company-list-item:first-child a',
                '.result-item:first-child a',
                'div[class*="item"] a:first-child',
                'a[class*="company"]'
            ]

            link_element = None
            used_selector = None

            for idx, selector in enumerate(result_selectors):
                try:
                    print(f"[调试] 尝试选择器 {idx + 1}/{len(result_selectors)}: {selector}")

                    # 先尝试获取所有匹配的元素
                    elements = await page.query_selector_all(selector)

                    if elements:
                        # 选择第一个元素
                        link_element = elements[0]
                        used_selector = selector
                        print(f"[调试] 找到 {len(elements)} 个链接，选择第一个")
                        break
                    else:
                        print(f"[调试] 选择器 {selector} 未找到元素")
                except Exception as e:
                    print(f"[调试] 选择器 {selector} 出错: {str(e)[:50]}")
                    continue

            if not link_element:
                print("[!] 未找到搜索结果链接")
                await page.screenshot(path="search_page_debug.png")
                print("[调试] 已保存搜索页面截图: search_page_debug.png")
                return None

            # 记录点击前的标签页数量
            old_page_count = len(page.context.pages)
            print(f"[调试] 点击前标签页数量: {old_page_count}")

            # 使用 JavaScript 强制在当前窗口打开
            try:
                await page.evaluate(
                    f'''
                    () => {{
                        const links = document.querySelectorAll("{used_selector}");
                        links.forEach(link => {{
                            link.target = "_self";
                            link.setAttribute("target", "_self");
                        }});
                    }}
                    '''
                )
                print("[调试] 已强制链接在当前窗口打开")
            except Exception as e:
                print(f"[调试] JS 执行失败（非致命）: {e}")

            # 点击链接
            print(f"[调试] 正在点击链接: {used_selector}")
            await link_element.click(timeout=5000)

            # 等待新窗口打开或页面跳转
            await asyncio.sleep(2)

            # 检查是否有新窗口打开
            new_page_count = len(page.context.pages)
            print(f"[调试] 点击后标签页数量: {new_page_count}")

            if new_page_count > old_page_count:
                # 有新窗口打开，切换到新窗口
                print(f"[调试] 检测到新窗口打开，切换到最新标签页")
                detail_page = page.context.pages[-1]  # 获取最后一个（最新的）页面

                # 等待新页面加载
                try:
                    await detail_page.wait_for_load_state('networkidle', timeout=10000)
                except:
                    pass

                print(f"[调试] 新页面 URL: {detail_page.url}")

                # 验证是否是详情页
                if '/company/' in detail_page.url or '/firm/' in detail_page.url:
                    print("[OK] 成功切换到详情页")
                    return detail_page
                else:
                    print(f"[!] 新窗口 URL 不像详情页: {detail_page.url}")
                    return detail_page  # 仍然返回新页面
            else:
                # 没有新窗口，在原页面跳转
                print("[调试] 在原页面跳转")
                await page.wait_for_load_state('networkidle', timeout=10000)
                print(f"[调试] 当前页面 URL: {page.url}")

                if '/company/' in page.url or '/firm/' in page.url:
                    print("[OK] 成功进入详情页")
                    return page
                else:
                    print(f"[!] URL 不像详情页: {page.url}")
                    return page

        except Exception as e:
            print(f"[X] 点击结果失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def extract_basic_info(self, page: Page) -> Dict:
        """
        提取公司基本信息

        Args:
            page: 页面对象

        Returns:
            基本信息字典
        """
        info = {}

        # 先等待页面加载
        await asyncio.sleep(1)

        # 定义要提取的字段和对应的选择器（增加了更多备选选择器）
        fields = {
            'company_name': [
                'h1',                                # 最直接
                '.company-name h1',
                'h1.company-title',
                '.detail-title h1',
                '.ent-name',
                '[class*="company-name"]',
                '[class*="ent-name"]',
                'title'                              # 最后备选：页面标题
            ],
            'legal_person': [
                '[data-key="legalPerson"]',
                '.legal-person',
                '.faren',
                'td:has-text("法定代表人") + td',
                'td:has-text("法人") + td',
                'div:has-text("法定代表人") + div',
                '[class*="legal-person"]',
                '[class*="faren"]'
            ],
            'registered_capital': [
                '[data-key="capital"]',
                '.registered-capital',
                '.zhuceziben',
                'td:has-text("注册资本") + td',
                'td:has-text("资本") + td',
                'div:has-text("注册资本") + div',
                '[class*="capital"]'
            ],
            'establish_date': [
                '[data-key="establishDate"]',
                '.establish-date',
                '.chengliriqi',
                'td:has-text("成立日期") + td',
                'td:has-text("成立时间") + td',
                'div:has-text("成立日期") + div',
                '[class*="establish"]'
            ],
            'status': [
                '.company-status',
                '.status',
                '.jingyingzhuangtai',
                'td:has-text("经营状态") + td',
                'td:has-text("状态") + td',
                '[class*="status"]',
                '[class*="state"]'
            ],
            'organization_code': [
                '.organization-code',
                '.tyshxydm',
                'td:has-text("统一社会信用代码") + td',
                'td:has-text("信用代码") + td',
                'td:has-text("税号") + td',
                '[class*="code"]'
            ],
            'business_scope': [
                '.business-scope',
                '.jingyingfanwei',
                'td:has-text("经营范围") + td',
                'div:has-text("经营范围") + div',
                '[class*="scope"]'
            ],
            'industry': [
                '.industry',
                '.hangye',
                'td:has-text("所属行业") + td',
                'td:has-text("行业") + td',
                '[class*="industry"]'
            ],
            'taxpayer_type': [
                '.taxpayer-type',
                '.nsrhzz',
                'td:has-text("纳税人资质") + td',
                'td:has-text("纳税人") + td',
                '[class*="taxpayer"]'
            ]
        }

        # 尝试每个字段的多个选择器
        for field_name, selectors in fields.items():
            value = "N/A"
            for idx, selector in enumerate(selectors):
                try:
                    element = await page.query_selector(selector)
                    if element:
                        value = await element.text_content()
                        if value:
                            value = value.strip()
                            if value and value != "N/A":
                                print(f"[调试] {field_name}: 使用选择器 {idx + 1}/{len(selectors)}: {selector}")
                                break
                except Exception as e:
                    continue

            info[field_name] = value if value else "N/A"

        print(f"[OK] 基本信息: {info.get('company_name', 'Unknown')}")
        return info

    async def extract_contact_info(self, page: Page) -> Dict:
        """
        提取联系方式

        Args:
            page: 页面对象

        Returns:
            联系方式字典
        """
        contacts = {}

        # 检查是否需要VIP权限才能查看
        vip_selectors = [
            '.vip-lock',
            '.need-vip',
            '[data-vip-required="true"]',
            'text=开通VIP查看'
        ]

        for selector in vip_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    print("[!] 联系方式需要VIP权限")
                    return {
                        'phone': '需要VIP',
                        'email': '需要VIP',
                        'address': '需要VIP'
                    }
            except:
                continue

        # 提取联系方式
        contact_fields = {
            'phone': [
                '.phone-number',
                '.contact-phone',
                'td:has-text("电话") + td',
                '[data-key="phone"]'
            ],
            'email': [
                '.email',
                '.contact-email',
                'td:has-text("邮箱") + td',
                '[data-key="email"]'
            ],
            'address': [
                '.address',
                '.company-address',
                'td:has-text("地址") + td',
                '[data-key="address"]'
            ]
        }

        for field_name, selectors in contact_fields.items():
            value = "N/A"
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        value = await element.text_content()
                        if value:
                            value = value.strip()
                            if value:
                                break
                except:
                    continue

            contacts[field_name] = value if value else "N/A"

        print(f"[OK] 联系方式: {contacts.get('phone', 'N/A')}")
        return contacts

    async def extract_shareholders(self, page: Page) -> List[str]:
        """
        提取股东信息

        Args:
            page: 页面对象

        Returns:
            股东信息列表
        """
        shareholders = []

        try:
            # 点击股东信息标签
            tab_selectors = [
                'text=股东信息',
                'a:has-text("股东")',
                '[data-tab="shareholders"]',
                '.tab-shareholders'
            ]

            for selector in tab_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    await random_delay(1, 2)
                    break
                except:
                    continue

            # 提取股东列表
            shareholder_selectors = [
                '.shareholder-item',
                '.shareholder-row',
                'tr.shareholder',
                '.shareholder-list li'
            ]

            for selector in shareholder_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        for element in elements:
                            text = await element.text_content()
                            if text:
                                shareholders.append(text.strip())
                        if shareholders:
                            break
                except:
                    continue

            print(f"[OK] 股东信息: {len(shareholders)} 条")

        except Exception as e:
            print(f"提取股东信息失败: {e}")

        return shareholders

    async def extract_executives(self, page: Page) -> List[str]:
        """
        提取主要人员信息

        Args:
            page: 页面对象

        Returns:
            高管信息列表
        """
        executives = []

        try:
            # 点击主要人员标签
            tab_selectors = [
                'text=主要人员',
                'text=高管信息',
                'a:has-text("人员")',
                '[data-tab="executives"]',
                '.tab-executives'
            ]

            for selector in tab_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    await random_delay(1, 2)
                    break
                except:
                    continue

            # 提取高管列表
            executive_selectors = [
                '.executive-item',
                '.executive-row',
                'tr.executive',
                '.executive-list li'
            ]

            for selector in executive_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        for element in elements:
                            text = await element.text_content()
                            if text:
                                executives.append(text.strip())
                        if executives:
                            break
                except:
                    continue

            print(f"[OK] 高管信息: {len(executives)} 条")

        except Exception as e:
            print(f"提取高管信息失败: {e}")

        return executives

    async def crawl_single_company(self, company_name: str) -> Optional[Dict]:
        """
        爬取单个公司的完整信息

        Args:
            company_name: 公司名称

        Returns:
            公司数据字典
        """
        page = None

        try:
            # 创建页面
            page = await self.browser_manager.create_page(cookies=self.cookie)

            # 搜索公司
            if not await self.search_company(page, company_name):
                return None

            # 点击第一个结果（可能会打开新窗口）
            # 注意：click_first_result 现在会返回一个可能的新页面
            detail_page = await self.click_first_result_with_page_switch(page)

            if not detail_page:
                return None

            # 执行类人操作
            await self.browser_manager.human_like_actions(detail_page)

            # 提取各类信息（使用详情页）
            basic_info = await self.extract_basic_info(detail_page)
            await random_delay(1, 2)

            contact_info = await self.extract_contact_info(detail_page)
            await random_delay(1, 2)

            shareholders = await self.extract_shareholders(detail_page)
            await random_delay(1, 2)

            executives = await self.extract_executives(detail_page)

            # 合并数据
            company_data = {
                **basic_info,
                **contact_info,
                'shareholders': '; '.join(shareholders) if shareholders else 'N/A',
                'executives': '; '.join(executives) if executives else 'N/A',
                'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(f"[OK] 成功爬取: {company_name}")

            # 关闭详情页（如果不同于搜索页）
            if detail_page != page:
                await detail_page.close()

            return company_data

        except Exception as e:
            print(f"[X] 爬取失败 {company_name}: {e}")
            return None

        finally:
            if page:
                await self.browser_manager.close_page(page)

    async def crawl_batch(self, company_names: List[str], progress_callback=None):
        """
        批量爬取公司信息

        Args:
            company_names: 公司名称列表
            progress_callback: 进度回调函数
        """
        results = []
        total = len(company_names)

        for i, company_name in enumerate(company_names, 1):
            print(f"\n[{i}/{total}] 正在处理: {company_name}")

            data = await self.crawl_single_company(company_name)

            if data:
                results.append(data)

            # 调用进度回调
            if progress_callback:
                await progress_callback(i, total, company_name, data is not None)

            # 增加延迟，避免频繁请求
            if i < total:
                await random_delay(3, 6)

        return results

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.browser_manager.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.browser_manager.stop()
