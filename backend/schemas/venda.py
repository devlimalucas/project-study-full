from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class VendaBase(BaseModel):
    Data: date
    Produto: str
    Categoria: str
    Cliente: str
    Regiao: str
    Quantidade: int
    Preco_Unitario: Decimal
    Receita: Decimal


class VendaRead(VendaBase):
    id: int

    class Config:
        from_attributes = True
