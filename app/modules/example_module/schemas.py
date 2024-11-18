from pydantic import BaseModel

class ExampleRequest(BaseModel):
    url: str
    selector: str

class ExampleResponse(BaseModel):
    title: str
    performance_metrics: dict

class TaskResponse(BaseModel):
    task_id: str 