<<<<<<< Updated upstream
from pydantic import BaseModel
=======
from pydantic import BaseModel, ConfigDict, field_serializer, constr, condecimal, conint
>>>>>>> Stashed changes
from decimal import Decimal


class ProdutoBase(BaseModel):
    nome: constr(min_length=3, max_length=255)
    preco: condecimal(gt=0, max_digits=10, decimal_places=2)
    estoque: conint(ge=0)
    descricao: str | None = None

<<<<<<< Updated upstream
=======
    # Serializa Decimal -> float para saída JSON
    @field_serializer("preco")
    def serialize_preco(self, value: Decimal) -> float:
        return float(value)

>>>>>>> Stashed changes

class ProdutoCreate(ProdutoBase):
    """Schema usado para criação de produto (POST)."""
    pass


class ProdutoRead(ProdutoBase):
    """Schema usado para leitura de produto (GET)."""
    id: int

<<<<<<< Updated upstream
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }
=======
    model_config = ConfigDict(from_attributes=True)  # ORM -> Pydantic
>>>>>>> Stashed changes


class ProdutoUpdate(BaseModel):
    """Schema usado para atualização de produto (PUT/PATCH)."""
    nome: str | None = None
    preco: Decimal | None = None
    estoque: int | None = None
    descricao: str | None = None
