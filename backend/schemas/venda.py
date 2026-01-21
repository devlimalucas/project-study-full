from pydantic import BaseModel, ConfigDict, conint
from datetime import date
from decimal import Decimal

class VendaBase(BaseModel):
    data: date
    produto_id: int
    cliente_id: int
    vendedor_id: int
    quantidade: conint(gt=0)

class VendaCreate(VendaBase):
    """Schema usado para criação de venda (POST)."""
    pass

class VendaRead(VendaBase):
    """Schema usado para leitura de venda (GET)."""
    id: int
    preco_unitario: Decimal
    receita: Decimal

    model_config = ConfigDict(from_attributes=True)

class VendaUpdate(BaseModel):
    """Schema usado para atualização de venda (PUT/PATCH)."""
    data: date | None = None
    produto_id: int | None = None
    cliente_id: int | None = None
    vendedor_id: int | None = None
    quantidade: int | None = None
