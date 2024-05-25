from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: str
    status: str

    class Config:
        orm_mode = True
        """
        Permite a compatibilidade com objetos ORM.
        """

class TasksResponse(BaseModel):
    tasks: List[Task]

    class Config:
        orm_mode = True
        """
        Permite a compatibilidade com objetos ORM.
        """
