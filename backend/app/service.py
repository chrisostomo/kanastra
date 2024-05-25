from fastapi import HTTPException, UploadFile, Form, BackgroundTasks
from .task import save_file, process_csv_task, Task
from .schemas import TasksResponse
from .redis_client import RedisClient

class AppService:
    def __init__(self, redis_client: RedisClient, session_factory):
        self.redis_client = redis_client
        self.session_factory = session_factory

    async def upload_csv(self, background_tasks: BackgroundTasks, email: str, file: UploadFile):
        try:
            file_content = await file.read()
            file_path = save_file(file_content, file.filename)

            task_id = self.redis_client.create_task(email)

            background_tasks.add_task(process_csv_task, file_path, email)

            return {"message": "CSV is being processed", "task_id": task_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o CSV: {str(e)}")

    async def get_tasks(self):
        try:
            tasks = self.redis_client.get_all_tasks()
            response = TasksResponse(tasks=tasks)
            return response, 200
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao recuperar as tarefas: {str(e)}")
