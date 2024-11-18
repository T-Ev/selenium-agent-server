from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumManager:
    def __init__(self):
        self.options = self._setup_chrome_options()
        self.command_executor = 'http://localhost:4444/wd/hub'
        
    def _setup_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Enable performance logs
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {
            'browser': 'ALL',
            'performance': 'ALL'
        }
        
        return chrome_options
    
    @contextmanager
    def get_driver(self):
        driver = webdriver.Remote(
            command_executor=self.command_executor,
            options=self.options
        )
        try:
            yield driver
        finally:
            driver.quit() 