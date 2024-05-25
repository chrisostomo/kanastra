from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .tasks import process_csv_task, save_file
from .models import TasksResponse
from .redis_client import RedisClient

class AppDependencies:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

class AppService:
    def __init__(self, dependencies: AppDependencies):
        self.redis_client = dependencies.redis_client

    async def upload_csv(self, background_tasks: BackgroundTasks, email: str, file: UploadFile):
        try:
            file_content = await file.read()
            file_path = save_file(file_content, file.filename)

            # Store the task in Redis as 'processing'
            task_id = self.redis_client.create_task(email)

            # Notify the user that the task is being processed
            background_tasks.add_task(process_csv_task, file_path, email)

            return {"message": "CSV is being processed", "task_id": task_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_tasks(self):
        try:
            tasks = self.redis_client.get_all_tasks()
            return TasksResponse(tasks=tasks)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Inicialização da aplicação e dependências
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

# Inicialização de dependências
redis_client = RedisClient()
dependencies = AppDependencies(redis_client=redis_client)
app_service = AppService(dependencies=dependencies)

@app.post("/process_file/")
async def upload_csv(background_tasks: BackgroundTasks, email: str = Form(...), file: UploadFile = File(...)):
    return await app_service.upload_csv(background_tasks, email, file)

@app.get("/files/", response_model=TasksResponse)
async def get_tasks():
    return await app_service.get_tasks()
