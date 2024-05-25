import csv
from .redis_client import RedisClient

redis_client = RedisClient()

def process_csv_task(email: str, csv_data: str):
    try:
        # Simulate processing
        rows = csv.reader(csv_data.splitlines())
        processed_data = [row for row in rows]

        # Store the result in Redis
        redis_client.complete_task(email)
    except Exception as e:
        # Handle processing error
        task_id = f"task:{email}"
        redis_client.client.set(task_id, "failed")
        raise e
