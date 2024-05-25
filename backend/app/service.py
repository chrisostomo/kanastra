from fastapi import HTTPException, UploadFile, Form, BackgroundTasks
from .tasks import save_file, process_csv_task
from .schemas import TasksResponse
from .redis_client import RedisClient

from .redis_client import RedisClient
from .db import SessionLocal

class AppService:
    def __init__(self, redis_client: RedisClient, session_factory):
        """
        Inicializa a classe AppService com um cliente Redis e uma fábrica de sessões.

        Args:
            redis_client (RedisClient): O cliente Redis.
            session_factory (sessionmaker): A fábrica de sessões do SQLAlchemy.
        """
        self.redis_client = redis_client
        self.session_factory = session_factory

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

        Returns:
            tuple: (TasksResponse, int) - Uma lista de tarefas com seus status e o código de status HTTP.
        """
        try:
            tasks = self.redis_client.get_all_tasks()
            response = TasksResponse(tasks=tasks)
            return response, 200
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao recuperar as tarefas: {str(e)}")

