from fastapi import APIRouter, BackgroundTasks
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from app.modules.base import BaseModule
from app.modules.example_module.schemas import ExampleRequest, ExampleResponse, TaskResponse
from fastapi_cache.decorator import cache
from app.core.config import settings

class ExampleModule(BaseModule):
    @property
    def name(self) -> str:
        return "example"
    
    def setup_routes(self) -> None:
        task = self.create_celery_task()
        
        @self.router.post("/example", response_model=TaskResponse)
        async def example_endpoint(request: ExampleRequest):
            # Start Celery task
            celery_task = task.delay(
                url=request.url,
                selector=request.selector
            )
            return {"task_id": celery_task.id}
        
        @self.router.get("/example/{task_id}", response_model=ExampleResponse)
        @cache(expire=settings.CACHE_TTL)
        async def get_task_result(task_id: str):
            result = task.AsyncResult(task_id)
            if result.ready():
                return result.get()
            raise HTTPException(status_code=202, detail="Task still processing")
    
    async def selenium_workflow(self, driver: WebDriver, **kwargs) -> dict:
        url = kwargs.get('url')
        selector = kwargs.get('selector')
        
        driver.get(url)
        element = driver.find_element(By.CSS_SELECTOR, selector)
        
        # Get performance logs
        performance_logs = driver.get_log('performance')
        
        return {
            'title': element.text,
            'performance_logs': performance_logs
        }
    
    async def parse_result(self, raw_data: dict) -> dict:
        return {
            'title': raw_data['title'],
            'performance_metrics': {
                log['message'] for log in raw_data['performance_logs']
                if 'Network.responseReceived' in log['message']
            }
        } 