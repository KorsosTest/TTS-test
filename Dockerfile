FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "app.tts_api:app", "--host", "0.0.0.0", "--port", "10000"]
