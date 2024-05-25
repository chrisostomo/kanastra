import redis
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        """
        Inicializa o cliente Redis.
        """
        try:
            redis_host = os.getenv('REDIS_HOST', 'redis')
            redis_port = int(os.getenv('REDIS_PORT', 6379))
            redis_db = int(os.getenv('REDIS_DB', 0))
            self.client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
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
            self.client.set(f'{task_id}_message', '')
            return task_id
        except Exception as e:
            print(f"Erro ao criar a tarefa: {e}")
            raise

    def complete_task(self, task_id: str) -> None:
        """
        Marca uma tarefa como concluída no Redis.

        Args:
            task_id (str): O ID da tarefa.
        """
        try:
            self.client.set(task_id, 'completed')
        except Exception as e:
            print(f"Erro ao completar a tarefa: {e}")
            raise

    def get_all_tasks(self):
        """
        Recupera todas as tarefas armazenadas no Redis.

        Returns:
            list: Uma lista de dicionários contendo o ID, o status e a mensagem de cada tarefa.
        """
        try:
            task_ids = self.client.lrange('tasks', 0, -1)
            tasks = []
            for task_id in task_ids:
                task_status = self.client.get(task_id)
                task_message = self.client.get(f'{task_id}_message') or 'No message available'
                tasks.append({"id": task_id, "status": task_status, "message": task_message})
            return tasks
        except Exception as e:
            print(f"Erro ao recuperar as tarefas: {e}")
            raise

    def set(self, key: str, value: str) -> None:
        """
        Define um valor no Redis.

        Args:
            key (str): A chave.
            value (str): O valor.
        """
        try:
            self.client.set(key, value)
        except Exception as e:
            print(f"Erro ao definir a chave no Redis: {e}")
            raise

    def get(self, key: str) -> str:
        """
        Recupera um valor do Redis.

        Args:
            key (str): A chave.

        Returns:
            str: O valor.
        """
        try:
            return self.client.get(key)
        except Exception as e:
            print(f"Erro ao recuperar a chave do Redis: {e}")
            raise