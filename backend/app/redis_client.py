import redis
import uuid


class RedisClient:
    def __init__(self):
        """
        Inicializa o cliente Redis.
        """
        try:
            self.client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
        except Exception as e:
            print(f"Erro ao inicializar o cliente Redis: {e}")
            raise

    def create_task(self, email: str) -> str:
        """
        Cria uma nova tarefa e a armazena no Redis.

        Args:
            email (str): O email associado à tarefa.

        Returns:
            str: O ID da tarefa criada.
        """
        try:
            task_id = str(uuid.uuid4())
            self.client.set(task_id, 'processing')
            self.client.rpush('tasks', task_id)
            return task_id
        except Exception as e:
            print(f"Erro ao criar a tarefa: {e}")
            raise

    def complete_task(self, email: str) -> None:
        """
        Marca uma tarefa como concluída no Redis.

        Args:
            email (str): O email associado à tarefa.
        """
        try:
            task_id = f"task:{email}"
            self.client.set(task_id, 'completed')
        except Exception as e:
            print(f"Erro ao completar a tarefa: {e}")
            raise

    def get_all_tasks(self):
        """
        Recupera todas as tarefas armazenadas no Redis.

        Returns:
            list: Uma lista de dicionários contendo o ID e o status de cada tarefa.
        """
        try:
            task_ids = self.client.lrange('tasks', 0, -1)
            tasks = [{"id": task_id, "status": self.client.get(task_id)} for task_id in task_ids]
            return tasks
        except Exception as e:
            print(f"Erro ao recuperar as tarefas: {e}")
            raise
