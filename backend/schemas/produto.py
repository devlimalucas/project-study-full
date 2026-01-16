from pydantic import BaseModel
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    estoque: int
    descricao: str | None = None


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoRead(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
