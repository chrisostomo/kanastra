from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .service import AppService
from .schemas import TasksResponse, TaskStatusResponse
from .redis_client import RedisClient
from .db import init_db, SessionLocal
from starlette.responses import JSONResponse

def create_app() -> FastAPI:
    app = FastAPI()

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
        response, status_code = await app_service.upload_csv(background_tasks, email, file)
        return JSONResponse(content=response, status_code=status_code)

    @app.get("/tasks/", response_model=TasksResponse)
    async def get_tasks():
        response, status_code = await app_service.get_tasks()
        return JSONResponse(content=response.dict(), status_code=status_code)

    @app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
    async def get_task_status(task_id: str):
        try:
            task_status = app_service.get_task_status(task_id)
            return JSONResponse(content=task_status.dict(), status_code=200)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    return app

init_db()

app = create_app()