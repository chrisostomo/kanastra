from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: str
    status: str

class TasksResponse(BaseModel):
    tasks: List[Task]
