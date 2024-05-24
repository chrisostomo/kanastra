FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-asyncio

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
