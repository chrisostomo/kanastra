import pytest
from fastapi import BackgroundTasks, UploadFile
from app.service import AppService
from app.redis_client import RedisClient
from sqlalchemy.orm import sessionmaker
from app.db import Base, engine
from unittest.mock import AsyncMock, MagicMock

# Configurações do banco de dados para testes
DATABASE_URL = "sqlite:///./test_service.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando as tabelas no banco de dados de teste
@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_upload_csv(setup_db):
    redis_client = RedisClient()
    session_factory = TestingSessionLocal
    app_service = AppService(redis_client, session_factory)

    file_path = os.path.join(os.path.dirname(__file__), "test_files/input.csv")
    with open(file_path, "rb") as f:
        mock_file = MagicMock(spec=UploadFile)
        mock_file.read = AsyncMock(return_value=f.read())
        mock_file.filename = "input.csv"

    background_tasks = BackgroundTasks()
    email = "test@example.com"
    response, status_code = await app_service.upload_csv(background_tasks, email, mock_file)

    assert status_code == 202
    assert "task_id" in response

@pytest.mark.asyncio
async def test_get_tasks(setup_db):
    redis_client = RedisClient()
    session_factory = TestingSessionLocal
    app_service = AppService(redis_client, session_factory)

    response, status_code = await app_service.get_tasks()

    assert status_code == 200
    assert "tasks" in response