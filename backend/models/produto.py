from sqlalchemy import Column, Integer, String, DECIMAL
from infra import Base  # agora importado direto do __init__.py

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, unique=True)  # nome único
    preco = Column(DECIMAL(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)  # estoque padrão 0
    descricao = Column(String(255), nullable=True)
