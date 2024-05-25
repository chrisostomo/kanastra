import pytest
from unittest.mock import patch, mock_open, Mock
from .tasks import save_file, TaskProcessor, process_csv_task
from .models import Debt
from .redis_client import RedisClient

# Teste para a função save_file
def test_save_file():
    file_content = b"test content"
    file_name = "test.csv"
    directory = "uploads"

    with patch("builtins.open", mock_open()) as mocked_file:
        file_path = save_file(file_content, file_name, directory)
        mocked_file.assert_called_once_with(f"{directory}/{file_name}", 'wb')
        mocked_file().write.assert_called_once_with(file_content)
        assert file_path == f"{directory}/{file_name}"

# Teste para a função send_email dentro de TaskProcessor
def test_send_email():
    email = "test@example.com"
    task_processor = TaskProcessor(redis_client=Mock(), session_factory=Mock())

    with patch("smtplib.SMTP") as mocked_smtp:
        task_processor.send_email(email)
        instance = mocked_smtp.return_value
        instance.login.assert_called_once_with('username', 'password')
        instance.send_message.assert_called_once()

# Teste para a função process_csv_task dentro de TaskProcessor
@pytest.fixture
def mock_session():
    with patch("tasks.SessionLocal") as MockSession:
        yield MockSession.return_value

@pytest.fixture
def mock_redis_client():
    with patch("tasks.RedisClient") as MockRedis:
        yield MockRedis.return_value

def test_process_csv_task(mock_session, mock_redis_client):
    mock_session.bulk_save_objects = Mock()
    mock_session.commit = Mock()
    mock_session.rollback = Mock()
    mock_session.close = Mock()

    mock_redis_client.complete_task = Mock()

    task_processor = TaskProcessor(redis_client=mock_redis_client, session_factory=lambda: mock_session)

    file_path = "test.csv"
    email = "test@example.com"
    file_content = """name,governmentId,email,debtAmount,debtDueDate,debtId
                      John Doe,11111111111,johndoe@kanastra.com.br,1000.00,2022-10-10,uuid-1234"""

    with patch("builtins.open", mock_open(read_data=file_content)):
        response = task_processor.process_csv_task(file_path, email)
        assert response["status"] == "success"
        assert response["message"] == "File processed successfully"
        mock_session.bulk_save_objects.assert_called()
        mock_session.commit.assert_called()
        mock_redis_client.complete_task.assert_called_once_with(email)
