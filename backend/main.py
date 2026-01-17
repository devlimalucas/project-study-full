import time
import models.produto
import models.venda
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from infra.database import Base, engine
from routes import produtos


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for i in range(30):
    try:
        with engine.connect() as conn:
            print("✅ Banco pronto!")
            break
    except OperationalError:
        print("⏳ Banco ainda não está pronto, tentando novamente...")
        time.sleep(2)

Base.metadata.create_all(bind=engine)

app.include_router(produtos.router)
