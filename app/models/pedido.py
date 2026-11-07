from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.item_pedido import ItemPedido

class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class PedidoBase(SQLModel):
    observacoes: str | None = Field(default=None, max_length=255)
    valor_total: float = Field(default=0.0, ge=0)

class Pedido(PedidoBase, table=True):
    __tablename__ = "pedidos"
    id: int | None = Field(default=None, primary_key=True)

    # N:1 → Cliente dono do pedido
    cliente_id: int = Field(foreign_key="clientes.id", ondelete="CASCADE")
    cliente: "Cliente" = Relationship(back_populates="pedidos")  # <-- AJUSTADO

    data_hora: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
)
    status: StatusPedido = Field(default=StatusPedido.CRIADO)

    # 1:N → Itens do pedido (composição)
    itens: list["ItemPedido"] = Relationship(back_populates="pedido", cascade_delete=True)  # <-- AJUSTADO

class PedidoCreate(SQLModel):
    observacoes: str | None = None
    itens: list["ItemPedidoCreateInline"] = []

class PedidoUpdateStatus(SQLModel):
    status: StatusPedido

class PedidoResponse(PedidoBase):
    id: int
    cliente_id: int
    data_hora: datetime
    status: StatusPedido
    itens: list["ItemPedidoResponse"] = []

class PedidoListResponse(SQLModel):
    id: int
    cliente_id: int
    data_hora: datetime
    status: StatusPedido
    valor_total: float
    total_itens: int