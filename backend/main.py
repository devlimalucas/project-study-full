import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from infra import Base, engine
import models  # garante que todas as models sejam registradas
from routers import produtos_router, usuarios_router, vendas_router

app = FastAPI()

# Configuração de CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Espera opcional pelo banco (apenas se ativar a flag WAIT_FOR_DB=true)
if os.getenv("WAIT_FOR_DB", "false").lower() == "true":
    for i in range(30):
        try:
            with engine.connect() as conn:
                print("✅ Banco pronto!")
                break
        except OperationalError:
            print("⏳ Banco ainda não está pronto, tentando novamente...")
            time.sleep(2)

# Cria todas as tabelas (se não usar Alembic para isso)
Base.metadata.create_all(bind=engine)

# Inclui rotas
app.include_router(produtos_router)
app.include_router(usuarios_router)
app.include_router(vendas_router)
