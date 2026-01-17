from sqlalchemy import Column, Integer, String, Date, DECIMAL
from infra.database import Base


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    Data = Column(Date)
    Produto = Column(String(100))
    Categoria = Column(String(100))
    Cliente = Column(String(100))
    Regiao = Column(String(100))
    Quantidade = Column(Integer)
    Preco_Unitario = Column(DECIMAL(10, 2))
    Receita = Column(DECIMAL(10, 2))
