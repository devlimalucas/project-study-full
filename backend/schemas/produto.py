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
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    preco: Decimal | None = None
    estoque: int | None = None
    descricao: str | None = None
