from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager

class SeleniumManager:
    def __init__(self):
        self.options = self._setup_chrome_options()
    
    def _setup_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Enable performance logs
        chrome_options.set_capability('goog:loggingPrefs', {
            'browser': 'ALL',
            'performance': 'ALL'
        })
        
        return chrome_options
    
    @contextmanager
    def get_driver(self):
        driver = webdriver.Chrome(options=self.options)
        try:
            yield driver
        finally:
            driver.quit() 