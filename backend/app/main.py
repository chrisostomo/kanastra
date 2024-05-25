from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .service import AppService
from .schemas import TasksResponse
from .redis_client import RedisClient
from .db import init_db
from .celery import celery

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

# Inicialização do banco de dados
init_db()

# Criação da aplicação FastAPI
app = create_app()

# Entry point for Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
