import pytest
from fastapi.testclient import TestClient
from main import app, AppDependencies, AppService
from redis_client import RedisClient
from models import TasksResponse
from unittest.mock import Mock, patch

# Fixture para o cliente de testes do FastAPI
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Fixture para injetar dependências mockadas
@pytest.fixture
def app_dependencies():
    mock_redis_client = Mock(spec=RedisClient)
    dependencies = AppDependencies(redis_client=mock_redis_client)
    return dependencies

# Teste para o endpoint /process_file/
def test_upload_csv(client, app_dependencies):
    # Mock da resposta do RedisClient
    app_dependencies.redis_client.create_task.return_value = "mock-task-id"

    # Mock da função save_file
    with patch('tasks.save_file', return_value="/mock/path/to/file.csv"):
        response = client.post(
            "/process_file/",
            data={"email": "test@example.com"},
            files={"file": ("test.csv", "name,governmentId,email,debtAmount,debtDueDate,debtId\nJohn Doe,11111111111,johndoe@kanastra.com.br,1000.00,2022-10-10,uuid-1234")}
        )

    assert response.status_code == 200
    assert response.json() == {"message": "CSV is being processed", "task_id": "mock-task-id"}

# Teste para o endpoint /files/
def test_get_tasks(client, app_dependencies):
    # Mock da resposta do RedisClient
    mock_tasks = [{"id": "mock-task-id", "status": "processing"}]
    app_dependencies.redis_client.get_all_tasks.return_value = mock_tasks

    response = client.get("/files/")

    assert response.status_code == 200
    assert response.json() == {"tasks": mock_tasks}
