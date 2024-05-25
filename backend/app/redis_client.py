from redis import Redis

class RedisClient:
    def __init__(self):
        self.client = Redis(host='localhost', port=6379, db=0)

    def create_task(self, email: str):
        task_id = f"task:{email}"
        self.client.set(task_id, "processing")
        return task_id

    def get_all_tasks(self):
        keys = self.client.keys("task:*")
        tasks = {}
        for key in keys:
            task_id = key.decode('utf-8')
            status = self.client.get(task_id).decode('utf-8')
            tasks[task_id] = status
        return tasks

    def complete_task(self, email: str):
        task_id = f"task:{email}"
        self.client.set(task_id, "completed")
