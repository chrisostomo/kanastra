from pydantic import BaseModel
from typing import Dict

class TaskStatus(BaseModel):
    """
    Model representing the status of a task.
    """
    task_id: str
    status: str

class TasksResponse(BaseModel):
    """
    Model representing a response with multiple task statuses.
    """
    tasks: Dict[str, str]
