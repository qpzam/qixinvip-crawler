"""
浏览器管理模块
"""
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Dict, List, Optional
from utils import random_delay, random_mouse_move, random_scroll


class BrowserManager:
    """浏览器管理器"""

    def __init__(self, config: Dict):
        """
        初始化浏览器管理器

        Args:
            config: 配置字典
        """
        self.config = config
        self.browser_config = config.get('browser', {})
        self.anti_detection = config.get('anti_detection', {})
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    async def start(self):
        """启动浏览器"""
        self.playwright = await async_playwright().start()

        # 浏览器启动参数
        launch_options = {
            'headless': self.browser_config.get('headless', False),
            'timeout': self.browser_config.get('timeout', 30000),
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-size=1920,1080'
            ]
        }

        # 启动Chromium浏览器
        self.browser = await self.playwright.chromium.launch(**launch_options)

        # 创建浏览器上下文
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=self.browser_config.get('user_agent'),
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )

        # 如果启用隐身模式
        if self.anti_detection.get('stealth_mode', True):
            await self._init_stealth_mode()

        print("浏览器启动成功")

    async def _init_stealth_mode(self):
        """初始化隐身模式，绕过自动化检测"""
        # 注入脚本隐藏自动化特征
        await self.context.add_init_script("""
            // 覆盖navigator.webdriver属性
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // 覆盖chrome对象
            window.chrome = {
                runtime: {}
            };

            // 覆盖permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );

            // 覆盖plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // 覆盖languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en']
            });
        """)

    async def create_page(self, cookies: List[Dict] = None) -> Page:
        """
        创建新页面

        Args:
            cookies: Cookie列表

        Returns:
            页面对象
        """
        page = await self.context.new_page()

        # 设置默认超时
        page.set_default_timeout(self.browser_config.get('timeout', 30000))

        # 如果提供了Cookie，设置到页面
        if cookies:
            await self.context.add_cookies(cookies)

        return page

    async def close_page(self, page: Page):
        """关闭页面"""
        try:
            await page.close()
        except:
            pass

    async def human_like_actions(self, page):
        """执行类人操作，随机移动鼠标和滚动"""
        if self.anti_detection.get('random_mouse_move', True):
            await random_mouse_move(page)

        if self.anti_detection.get('random_scroll', True):
            await random_scroll(page)

        await random_delay(0.5, 1.5)

    async def stop(self):
        """停止浏览器"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("浏览器已关闭")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.stop()
