from fastapi import HTTPException, UploadFile, BackgroundTasks
from .task import save_file, process_csv_task
from .schemas import TasksResponse
from .redis_client import RedisClient
from sqlalchemy.orm import Session


class AppService:
    def __init__(self, redis_client: RedisClient, session_factory: Session):
        self.redis_client = redis_client
        self.session_factory = session_factory

    async def upload_csv(self, background_tasks: BackgroundTasks, email: str, file: UploadFile):
        try:
            # Salva o arquivo primeiro
            file_path = save_file(await file.read(), file.filename)

            # Cria a tarefa no Redis
            task_id = self.redis_client.create_task(email)

            # Adiciona a tarefa de processamento ao BackgroundTasks
            background_tasks.add_task(process_csv_task, file_path, email)

            return {"message": "CSV is being processed", "task_id": task_id}, 202
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o CSV: {str(e)}")

    async def get_tasks(self):
        try:
            tasks = self.redis_client.get_all_tasks()
            response = TasksResponse(tasks=tasks)
            return response, 200
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao recuperar as tarefas: {str(e)}")