from pydantic import BaseModel
from typing import List, Optional

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    message: Optional[str]
    details: Optional[str]

class TasksResponse(BaseModel):
    tasks: List[TaskStatusResponse]