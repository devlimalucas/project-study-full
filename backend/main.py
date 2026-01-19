import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from infra import Base, engine  # agora importado direto do __init__.py
import models  # importa todos os models via __init__.py
from routers import produtos_router, usuarios_router  # routers expostos no __init__.py

app = FastAPI()

# Configuração de CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Espera o banco ficar pronto
for i in range(30):
    try:
        with engine.connect() as conn:
            print("✅ Banco pronto!")
            break
    except OperationalError:
        print("⏳ Banco ainda não está pronto, tentando novamente...")
        time.sleep(2)

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)

# Inclui todas as rotas
app.include_router(produtos_router)
app.include_router(usuarios_router)
# app.include_router(vendas_router)
