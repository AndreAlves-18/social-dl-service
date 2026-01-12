FROM python:3.9-slim

# Instala ffmpeg (Essencial para yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY cookies.txt .

# Cria diretório de downloads
RUN mkdir -p /app/downloads && chmod 777 /app/downloads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
