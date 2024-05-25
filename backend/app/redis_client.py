import redis
import uuid

class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

    def create_task(self, email):
        task_id = str(uuid.uuid4())
        self.client.set(task_id, 'processing')
        self.client.rpush('tasks', task_id)
        return task_id

    def complete_task(self, email):
        task_id = f"task:{email}"
        self.client.set(task_id, 'completed')

    def get_all_tasks(self):
        task_ids = self.client.lrange('tasks', 0, -1)
        tasks = [{"id": task_id, "status": self.client.get(task_id)} for task_id in task_ids]
        return tasks
