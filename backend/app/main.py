from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .service import AppService
from .schemas import TasksResponse
from .redis_client import RedisClient
from .db import init_db, SessionLocal

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.

    Returns:
        FastAPI: Instância da aplicação FastAPI.
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

    redis_client = RedisClient()
    session_factory = SessionLocal
    app_service = AppService(redis_client, session_factory)

    @app.post("/upload_csv/")
    async def upload_csv(background_tasks: BackgroundTasks, email: str = Form(...), file: UploadFile = File(...)):
        """
        Endpoint para upload de arquivo CSV.

        Args:
            background_tasks (BackgroundTasks): Tarefas em segundo plano.
            email (str): Email do usuário.
            file (UploadFile): Arquivo CSV enviado.

        Returns:
            dict: Mensagem de status e ID da tarefa.
            int: Código de status HTTP.
        """
        response, status_code = await app_service.upload_csv(background_tasks, email, file)
        return response, status_code

    @app.get("/files/", response_model=TasksResponse)
    async def get_tasks():
        """
        Endpoint para listar tarefas.

        Returns:
            TasksResponse: Lista de tarefas com seus status.
            int: Código de status HTTP.
        """
        response, status_code = await app_service.get_tasks()
        return response, status_code

    return app

# Inicializa o banco de dados
init_db()

# Cria a aplicação FastAPI
app = create_app()
