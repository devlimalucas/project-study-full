from pydantic import BaseModel, EmailStr, constr
from typing import Literal


class UsuarioBase(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    role: Literal["admin", "cliente", "vendedor"]


class UsuarioCreate(UsuarioBase):
    senha: constr(min_length=6, max_length=255)


class UsuarioRead(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    """Schema usado para atualização parcial de usuário (PUT/PATCH)."""
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    role: Literal["admin", "cliente", "vendedor"] | None = None
