from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .tasks import task_processor, save_file, process_csv_task
from .schemas import TasksResponse
from .redis_client import RedisClient

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.
    """
    app = FastAPI()

    # Configuração do CORS
    origins = [
        "http://localhost:8888",
        "http://127.0.0.1:8888",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inicialização das dependências
    redis_client = RedisClient()
    app_service = AppService(redis_client=redis_client)

    @app.post("/upload_csv/")
    async def upload_csv(background_tasks: BackgroundTasks, email: str = Form(...), file: UploadFile = File(...)):
        """
        Endpoint para upload de CSV.
        """
        return await app_service.upload_csv(background_tasks, email, file)

    @app.get("/files/", response_model=TasksResponse)
    async def get_tasks():
        """
        Endpoint para listar tarefas.
        """
        return await app_service.get_tasks()

    return app

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
