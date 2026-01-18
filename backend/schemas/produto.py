from pydantic import BaseModel, ConfigDict, field_serializer
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    estoque: int
    descricao: str | None = None

    @field_serializer("preco")
    def serialize_preco(self, value: Decimal) -> float:
        return float(value)


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoRead(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    preco: Decimal | None = None
    estoque: int | None = None
    descricao: str | None = None
