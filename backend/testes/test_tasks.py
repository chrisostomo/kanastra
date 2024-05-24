from app.tasks import process_csv, send_email
from unittest.mock import patch
import unittest

class TestTasks(unittest.TestCase):

    @patch('app.tasks.SessionLocal')
    def test_process_csv(self, mock_session):
        csv_content = "name,governmentId,email,debtAmount,debtDueDate,debtID\nJohn Doe,11111111111,johndoe@example.com,1000.00,2022-10-01,123e4567-e89b-12d3-a456-426614174000"
        process_csv(csv_content, "user@example.com")
        self.assertTrue(mock_session().add.called)
        self.assertTrue(mock_session().commit.called)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        send_email("user@example.com")
        self.assertTrue(mock_smtp.return_value.send_message.called)

if __name__ == "__main__":
    unittest.main()
