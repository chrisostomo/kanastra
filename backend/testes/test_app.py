import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.db import Base
from app.models import Debt
import os

# Configurações do banco de dados para testes
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuração do app para testes
app = create_app()
client = TestClient(app)

# Criando as tabelas no banco de dados de teste
@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_upload_csv(setup_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        file_path = os.path.join(os.path.dirname(__file__), "test_files/input.csv")
        with open(file_path, "rb") as file:
            response = await ac.post("/upload_csv/", data={"email": "test@example.com"}, files={"file": file})
        assert response.status_code == 202
        json_response = response.json()
        assert "task_id" in json_response

@pytest.mark.asyncio
async def test_get_tasks(setup_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/files/")
        assert response.status_code == 200
        json_response = response.json()
        assert "tasks" in json_response