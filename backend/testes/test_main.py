import os
import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Debt
import shutil

# Definindo URL do banco de dados de teste
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup e teardown do banco de dados de teste
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Setup e teardown do diretório de uploads
@pytest.fixture(scope="module")
def setup_upload_dir():
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    yield
    shutil.rmtree(upload_dir)

# Fixture do cliente de teste
@pytest.fixture(scope="module")
def client(test_db, setup_upload_dir):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# Teste para upload de arquivo
def test_upload_file(client):
    file_path = "test.csv"
    with open(file_path, "w") as f:
        f.write("name,governmentId,email,debtAmount,debtDueDate,debtID\n")
        f.write("John Doe,123456789,john.doe@example.com,1000,2024-05-01,1\n")

    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": f}, data={"email": "test@example.com"})

    os.remove(file_path)

    assert response.status_code == 201
    assert response.json() == {"message": "File uploaded and processing started"}

# Teste para obtenção de arquivos
def test_get_files(client):
    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["email"] == "john.doe@example.com"
