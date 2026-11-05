from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.item_pedido import ItemPedido
    from app.models.cliente import Cliente

class ItemCardapioBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    descricao: str | None = Field(default=None, max_length=255)
    preco: float = Field(gt=0)
    categoria: str = Field(default="Lanches")
    disponivel: bool = Field(default=True)
    tempo_preparo_minutos: int | None = Field(default=None, ge=1)

class ItemCardapio(ItemCardapioBase, table=True):
    __tablename__ = "itens_cardapio"
    id: int | None = Field(default=None, primary_key=True)

    # N:1 → Logista que criou o item
    criador_id: int | None = Field(default=None, foreign_key="clientes.id")
    criador: "Cliente" = Relationship(back_populates="itens_criados")  # <-- NOVO

    # 1:N → Itens de pedido que referenciam este prato
    itens_pedido: list["ItemPedido"] = Relationship(back_populates="item_cardapio")

class ItemCardapioCreate(ItemCardapioBase):
    pass

class ItemCardapioUpdate(SQLModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    categoria: str | None = None
    disponivel: bool | None = None
    tempo_preparo_minutos: int | None = None

class ItemCardapioResponse(ItemCardapioBase):
    id: int
    criador_id: int | None = None