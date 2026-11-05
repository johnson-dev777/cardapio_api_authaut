from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.item_cardapio import ItemCardapio

class ItemPedidoBase(SQLModel):
    quantidade: int = Field(ge=1)
    observacao: str | None = Field(default=None, max_length=150)
    preco_unitario: float = Field(gt=0)

class ItemPedido(ItemPedidoBase, table=True):
    __tablename__ = "itens_pedido"
    id: int | None = Field(default=None, primary_key=True)

    # N:1 → Pedido ao qual pertence
    pedido_id: int = Field(foreign_key="pedidos.id", ondelete="CASCADE")
    pedido: "Pedido" = Relationship(back_populates="itens")  # <-- AJUSTADO

    # N:1 → Item do cardápio referenciado
    item_cardapio_id: int = Field(foreign_key="itens_cardapio.id")
    item_cardapio: "ItemCardapio" = Relationship(back_populates="itens_pedido")  # <-- AJUSTADO

class ItemPedidoCreate(SQLModel):
    item_cardapio_id: int
    quantidade: int
    observacao: str | None = None

class ItemPedidoCreateInline(ItemPedidoCreate):
    pass

class ItemPedidoUpdate(SQLModel):
    quantidade: int | None = None
    observacao: str | None = None

class ItemPedidoResponse(ItemPedidoBase):
    id: int
    pedido_id: int
    item_cardapio_id: int