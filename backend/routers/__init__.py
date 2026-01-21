from .produtos import router as produtos_router
from .usuarios import router as usuarios_router
from .vendas import router as vendas_router

__all__ = ["produtos_router", "usuarios_router", "vendas_router"]
