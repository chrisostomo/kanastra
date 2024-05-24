import os
import pytest
from unittest.mock import patch
from tasks import process_file_task, save_file, send_email

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

@patch('tasks.send_email')
def test_process_file_task(mock_send_email, sample_file):
    mock_send_email.return_value = True
    result = process_file_task(sample_file)
    assert result["status"] == "success"
    assert "File processed successfully" in result["message"]
    mock_send_email.assert_called_once_with("johndoe@kanastra.com.br")

@patch('smtplib.SMTP')
def test_send_email(mock_smtp):
    send_email("user@example.com")
    assert mock_smtp.return_value.send_message.called
