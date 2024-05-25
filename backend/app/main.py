from fastapi import FastAPI, BackgroundTasks, HTTPException
from .tasks import process_csv_task, save_file
from .schemas import ProcessCSVRequest, TasksResponse
from .redis_client import RedisClient

app = FastAPI()
redis_client = RedisClient()

@app.post("/upload_csv/")
async def upload_csv(request: ProcessCSVRequest, background_tasks: BackgroundTasks):
    email = request.email
    csv_data = request.csv_data

    try:
        # Save file to disk
        file_path = save_file(csv_data.encode(), f"{email}.csv")

        # Store the task in Redis as 'processing'
        task_id = redis_client.create_task(email)

        # Notify the user that the task is being processed
        process_csv_task.delay(file_path, email)

        return {"message": "CSV is being processed", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/", response_model=TasksResponse)
async def get_tasks():
    try:
        tasks = redis_client.get_all_tasks()
        return TasksResponse(tasks=tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
