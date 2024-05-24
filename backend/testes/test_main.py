import os
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'input.csv')
    assert os.path.exists(csv_file_path), f"Arquivo CSV não encontrado: {csv_file_path}"
    with open(csv_file_path, 'rb') as file:
        start_time = time.time()
        response = client.post(
            "/process_file/",
            files={"file": ("input.csv", file, "text/csv")}
        )
        end_time = time.time()
    assert response.status_code == 200
    assert "task_id" in response.json()
    print(f"Upload e processamento do arquivo CSV concluídos em {end_time - start_time} segundos.")

def test_list_files():
    response = client.get("/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_user_already_registered():
    client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
