"""
测试脚本 - 用于验证配置和选择器
"""
import asyncio
import sys
import io
from playwright.async_api import async_playwright
from utils import load_config, parse_cookie_string

# 设置 stdout 为 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


async def test_cookie():
    """测试 Cookie 是否有效"""
    print("=" * 60)
    print("测试 1: 验证 Cookie 配置")
    print("=" * 60)

    config = load_config()

    if config.get('cookie') == 'your_cookie_string_here':
        print("[X] Cookie 未配置")
        print("\n请在 config.json 中配置你的启信宝 VIP Cookie")
        return False

    print("[OK] Cookie 已配置")
    return True


async def test_browser_launch():
    """测试浏览器启动"""
    print("\n" + "=" * 60)
    print("测试 2: 浏览器启动")
    print("=" * 60)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            print("[OK] 浏览器启动成功")

            # 访问启信宝
            await page.goto("https://www.qixin.com/")
            print("[OK] 成功访问启信宝首页")

            # 检查是否登录
            config = load_config()
            cookies = parse_cookie_string(config['cookie'])
            await context.add_cookies(cookies)

            await page.reload()
            await asyncio.sleep(2)

            # 检查登录状态（根据页面元素判断）
            try:
                # 可能的登录后元素
                login_indicators = [
                    '.user-info',
                    '.vip-icon',
                    '[data-logged-in="true"]',
                    'text=我的',
                    'text=VIP'
                ]

                logged_in = False
                for indicator in login_indicators:
                    try:
                        element = await page.query_selector(indicator)
                        if element:
                            logged_in = True
                            print("[OK] Cookie 有效，已成功登录 VIP 账号")
                            break
                    except:
                        continue

                if not logged_in:
                    print("[!] 无法确认登录状态，请手动检查浏览器窗口")

            except Exception as e:
                print(f"[!] 登录检查失败: {e}")

            print("\n按 Ctrl+C 关闭浏览器...")
            await asyncio.sleep(10)  # 显示10秒供检查

            await browser.close()

        return True

    except Exception as e:
        print(f"[X] 浏览器启动失败: {e}")
        return False


async def test_search():
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("测试 3: 搜索功能")
    print("=" * 60)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            # 设置 Cookie
            config = load_config()
            cookies = parse_cookie_string(config['cookie'])
            await context.add_cookies(cookies)

            page = await context.new_page()

            # 访问首页
            await page.goto("https://www.qixin.com/")
            await asyncio.sleep(2)
            print("[OK] 访问首页成功")

            # 查找搜索框
            search_selectors = [
                'input[placeholder*="搜索"]',
                'input[placeholder*="企业名称"]',
                'input.search-input'
            ]

            search_found = False
            for selector in search_selectors:
                try:
                    search_box = await page.wait_for_selector(selector, timeout=3000)
                    if search_box:
                        print(f"[OK] 找到搜索框: {selector}")
                        search_found = True

                        # 测试输入
                        await search_box.fill("腾讯")
                        await asyncio.sleep(1)
                        print("[OK] 成功输入测试文本")
                        break
                except:
                    continue

            if not search_found:
                print("[!] 未找到搜索框，请手动检查页面")

            print("\n按 Ctrl+C 关闭浏览器...")
            await asyncio.sleep(10)

            await browser.close()

        return True

    except Exception as e:
        print(f"[X] 搜索测试失败: {e}")
        return False


async def test_selectors():
    """测试页面选择器"""
    print("\n" + "=" * 60)
    print("测试 4: 选择器验证")
    print("=" * 60)
    print("\n此测试将打开浏览器并进入一个公司页面")
    print("请手动查找并记录下各类元素的 CSS 选择器")
    print("\n建议测试公司: 腾讯科技（深圳）有限公司")

    input("\n按 Enter 继续...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            # 设置 Cookie
            config = load_config()
            cookies = parse_cookie_string(config['cookie'])
            await context.add_cookies(cookies)

            page = await context.new_page()

            # 搜索并进入
            await page.goto("https://www.qixin.com/")
            await asyncio.sleep(2)

            print("\n已打开浏览器，请：")
            print("1. 手动搜索一个公司")
            print("2. 进入公司详情页")
            print("3. 使用 F12 开发者工具检查元素")
            print("4. 记录下需要的 CSS 选择器")
            print("\n常用查找方法:")
            print("- 右键点击元素 → Copy → Copy selector")

            print("\n按 Ctrl+C 关闭浏览器...")
            await asyncio.sleep(60)

            await browser.close()

        return True

    except KeyboardInterrupt:
        print("\n测试结束")
        return True
    except Exception as e:
        print(f"[X] 选择器测试失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("       启信宝爬虫 - 配置测试")
    print("=" * 60)

    tests = [
        ("Cookie 配置", test_cookie),
        ("浏览器启动", test_browser_launch),
        ("搜索功能", test_search),
        ("选择器验证", test_selectors)
    ]

    print("\n请选择要运行的测试:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"{i}. {name}")
    print("0. 运行所有测试")

    choice = input("\n请选择 (0-{}): ".format(len(tests)))

    if choice == '0':
        for name, test_func in tests:
            try:
                result = await test_func()
                if not result:
                    print(f"\n[!] {name} 测试失败，请检查配置")
                    break
            except KeyboardInterrupt:
                print("\n\n测试中断")
                break
            except Exception as e:
                print(f"\n[X] {name} 测试出错: {e}")
                import traceback
                traceback.print_exc()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tests):
                _, test_func = tests[idx]
                await test_func()
            else:
                print("无效选择")
        except ValueError:
            print("无效选择")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n测试中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
