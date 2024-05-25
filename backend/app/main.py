from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .tasks import process_csv_task, save_file
from .schemas import TasksResponse
from .redis_client import RedisClient

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

@app.post("/process_file/")
async def upload_csv(background_tasks: BackgroundTasks, email: str = Form(...), file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_path = save_file(file_content, file.filename)

        # Store the task in Redis as 'processing'
        task_id = redis_client.create_task(email)

        # Notify the user that the task is being processed
        process_csv_task.delay(file_path, email)

        return {"message": "CSV is being processed", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/", response_model=TasksResponse)
async def get_tasks():
    try:
        tasks = redis_client.get_all_tasks()
        return TasksResponse(tasks=tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
