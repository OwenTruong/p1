FROM python:3.12-slim

WORKDIR /app

ARG FASTAPI_PORT

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $FASTAPI_PORT
# python -m uvicorn src.app:app --port 80 --host 0.0.0.0 --app-dir src
CMD ["python", "-m", "uvicorn", "src.app:app", "--port", "${FASTAPI_PORT}", "--host", "0.0.0.0", "--app-dir", "src"]