from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from selenium.webdriver.remote.webdriver import WebDriver
from fastapi_cache.decorator import cache
from app.core.celery_app import celery_app
from app.core.config import settings

class BaseModule(ABC):
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the module name"""
        pass
    
    @abstractmethod
    def setup_routes(self) -> None:
        """Setup FastAPI routes for this module"""
        pass
    
    @abstractmethod
    async def selenium_workflow(self, driver: WebDriver, **kwargs) -> Any:
        """Execute the Selenium workflow"""
        pass
    
    @abstractmethod
    async def parse_result(self, raw_data: Any) -> Dict:
        """Parse the raw data from selenium workflow into structured format"""
        pass
    
    def create_celery_task(self):
        """Create a Celery task for this module's workflow"""
        @celery_app.task(name=f"{self.name}_task")
        def execute_workflow(**kwargs):
            from app.core.selenium_manager import SeleniumManager
            selenium_manager = SeleniumManager()
            selenium_manager.command_executor = 'http://selenium:4444/wd/hub'
            
            with selenium_manager.get_driver() as driver:
                raw_data = self.selenium_workflow(driver, **kwargs)
                return self.parse_result(raw_data)
        
        return execute_workflow 