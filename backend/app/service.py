from fastapi import HTTPException, UploadFile, Form, BackgroundTasks
from .tasks import save_file, process_csv_task
from .schemas import TasksResponse
from .redis_client import RedisClient

class AppService:
    def __init__(self, redis_client: RedisClient):
        """
        Inicializa a classe AppService com um cliente Redis.
        """
        self.redis_client = redis_client

    async def upload_csv(self, background_tasks: BackgroundTasks, email: str, file: UploadFile):
        """
        Faz o upload de um arquivo CSV e inicia o processamento em background.
        """
        try:
            file_content = await file.read()
            file_path = save_file(file_content, file.filename)

            # Armazena a tarefa no Redis como 'processing'
            task_id = self.redis_client.create_task(email)

            # Notifica o usuário que a tarefa está sendo processada
            background_tasks.add_task(process_csv_task, file_path, email)

            return {"message": "CSV is being processed", "task_id": task_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o CSV: {str(e)}")

    async def get_tasks(self):
        """
        Recupera todas as tarefas do Redis.
        """
        try:
            tasks = self.redis_client.get_all_tasks()
            return TasksResponse(tasks=tasks)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao recuperar as tarefas: {str(e)}")
