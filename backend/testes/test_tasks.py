import os
import pytest
from tasks import process_file_task, save_file

@pytest.fixture
def sample_file(tmpdir):
    content = b"name,governmentId,email,debtAmount,debtDueDate,debtId\nJohn Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-10,1"
    file_path = os.path.join(tmpdir, "test.csv")
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path

def test_save_file(sample_file):
    content = b"sample content"
    file_path = save_file(content, "sample.txt", directory=os.path.dirname(sample_file))
    assert os.path.exists(file_path)
    with open(file_path, 'rb') as f:
        assert f.read() == content

def test_process_file_task(sample_file):
    result = process_file_task(sample_file)
    assert result["status"] == "success"
    assert "File processed successfully" in result["message"]
