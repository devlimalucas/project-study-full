FROM python:3.11-slim

WORKDIR /app

# Instalar cliente MySQL, netcat e compiladores básicos
RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd gcc && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
