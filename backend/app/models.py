from pydantic import BaseModel
from typing import Dict

class TaskStatus(BaseModel):
    """
    Model representing the status of a task.

    Attributes:
        task_id (str): The unique identifier of the task.
        status (str): The status of the task (e.g., 'processing', 'completed', 'failed').
    """
    task_id: str
    status: str

class TasksResponse(BaseModel):
    """
    Model representing a response with multiple task statuses.

    Attributes:
        tasks (Dict[str, str]): A dictionary mapping task IDs to their statuses.
    """
    tasks: Dict[str, str]
