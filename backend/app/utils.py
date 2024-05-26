import os
import uuid

def save_file(file_content: bytes, file_name: str, directory: str = 'uploads') -> tuple:
    try:
        os.makedirs(directory, exist_ok=True)
        task_id = str(uuid.uuid4())
        file_path = os.path.join(directory, f"{task_id}_{file_name}")
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return task_id, file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")
