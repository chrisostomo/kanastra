from pydantic import BaseModel
from typing import List

class TaskResponse(BaseModel):
    id: str
    status: str
    message: str

class TasksResponse(BaseModel):
    tasks: List[TaskResponse]