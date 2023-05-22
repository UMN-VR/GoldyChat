# pypuppeteer.py
import asyncio

from pyppeteer import launch
from text_colors import Colors

#bad use HybridPuppeteerWrapper instead
class PuppeteerWrapper:
    def __init__(self):
        print(f"{Colors.BRIGHT_MAGENTA}Initializing Puppeteer...{Colors.RESET}")
        #self.profile = "snap/chromium/common/chromium/Profile 1"
        self.browser = None
        self.page = None

    async def start_browser(self):
        self.browser = await launch(executablePath="/usr/bin/chromium-browser", userDataDir="snap/chromium/common/chromium/Profile 1", dumpio=True) # this is the correct path
        self.page = await self.browser.newPage()
    
    async def navigate(self, url):
        if not self.browser:
            await self.start_browser()
        await self.page.goto(url)

    async def get_content(self, selector):
        if not self.browser:
            raise Exception('Browser not started')
        element = await self.page.querySelector(selector)
        return await self.page.evaluate('(element) => element.textContent', element)

    async def close(self):
        if self.browser:
            await self.browser.close()

    async def take_screenshot(self, url, screenshot_path):
        page = await self.browser.newPage()
        await page.goto(url)
        await page.screenshot({'path': screenshot_path})
        await page.close()
