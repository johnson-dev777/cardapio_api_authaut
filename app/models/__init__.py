"""Módulo de modelos de dados e esquemas SQLModel organizados por entidade."""
from app.models.item_cardapio import (
    ItemCardapioBase,
    ItemCardapio,
    ItemCardapioCreate,
    ItemCardapioUpdate,
    ItemCardapioResponse,
)

from app.models.item_pedido import (
    ItemPedidoBase,
    ItemPedido,
    ItemPedidoCreate,
    ItemPedidoCreateInline,
    ItemPedidoUpdate,
    ItemPedidoResponse,
)
from app.models.pedido import (
    StatusPedido,
    PedidoBase,
    Pedido,
    PedidoCreate,
    PedidoUpdateStatus,
    PedidoResponse,
    PedidoListResponse,
)

# app/models/__init__.py
# ... (outros imports mantidos)
from app.models.cliente import (
    ClienteBase,
    Cliente,
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    UserRole,  # <-- ADICIONE AQUI
)
# ...

__all__ = [
    # ... (outros itens)
    # Cliente
    "ClienteBase",
    "Cliente",
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "UserRole",  # <-- ADICIONE AQUI
    # ...
]