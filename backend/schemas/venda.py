from pydantic import BaseModel, ConfigDict, condecimal, conint
from datetime import date
from decimal import Decimal


class VendaBase(BaseModel):
    data: date
    produto_id: int
    cliente_id: int
    vendedor_id: int
    quantidade: conint(gt=0)
    preco_unitario: condecimal(gt=0, max_digits=10, decimal_places=2)
    receita: Decimal | None = None  # calculada no backend


class VendaCreate(VendaBase):
    """Schema usado para criação de venda (POST)."""
    pass


class VendaRead(VendaBase):
    """Schema usado para leitura de venda (GET)."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class VendaUpdate(BaseModel):
    """Schema usado para atualização de venda (PUT/PATCH)."""
    data: date | None = None
    produto_id: int | None = None
    cliente_id: int | None = None
    vendedor_id: int | None = None
    quantidade: int | None = None
    preco_unitario: Decimal | None = None
    receita: Decimal | None = None
