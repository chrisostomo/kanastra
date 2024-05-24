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
