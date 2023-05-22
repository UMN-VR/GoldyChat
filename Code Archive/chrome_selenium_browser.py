import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Use HybridPuppeteer.py instead
#bad bad bad
class ChromeSeleniumBrowser:
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
        self.driver = None

    def start_browser(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=chrome_options)

    def stop_browser(self):
        if self.driver:
            self.driver.quit()

    def visit_website(self, url):
        if self.driver:
            self.driver.get(url)

    def capture_screenshot(self, screenshot_path):
        if self.driver:
            self.driver.save_screenshot(screenshot_path)

    