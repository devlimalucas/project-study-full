from sqlalchemy import Column, Integer, String, DECIMAL
from infra.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=True)
