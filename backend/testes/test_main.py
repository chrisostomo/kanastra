import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'input.csv')
    with open(csv_file_path, 'rb') as file:
        start_time = time.time()
        response = client.post(
            "/upload",
            files={"file": file},
            data={"email": "user@example.com"}
        )
        end_time = time.time()
        duration = end_time - start_time

        assert response.status_code == 201
        assert duration < 60, f"Processing took too long: {duration} seconds"
