#!/bin/bash
set -e

echo "🚀 Aplicando migrations Alembic..."
alembic upgrade head

echo "🌱 Rodando seeds..."
python -m seeds.seeds || echo "Nenhum seed configurado ainda"

echo "🔥 Subindo servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
