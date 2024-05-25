from pydantic import BaseModel
from typing import Dict

class TaskStatus(BaseModel):
    task_id: str
    status: str

class TasksResponse(BaseModel):
    tasks: Dict[str, str]
