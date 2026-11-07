
from sqlalchemy import Column, Enum as SAEnum
from enum import Enum
from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.item_cardapio import ItemCardapio


class UserRole(str, Enum):
    CLIENTE = "CLIENTE"
    LOGISTA = "LOGISTA"


class ClienteBase(SQLModel):
    nome: str = Field(min_length=2, max_length=150)
    data_nascimento: date | None = Field(default=None)
    endereco: str = Field(min_length=3, max_length=255)
    cep: str = Field(min_length=8, max_length=10)
    numero: str = Field(min_length=1, max_length=20)
    telefone: str = Field(min_length=8, max_length=20)


class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"

    id: int | None = Field(default=None, primary_key=True)

    role: UserRole = Field(
        default=UserRole.CLIENTE,
        sa_column=Column(
            SAEnum(
                UserRole,
                native_enum=False,
                length=20,
                values_callable=lambda enum_cls: [e.value for e in enum_cls]
            ),
            nullable=False,
            server_default="CLIENTE"
        )
    )

    pedidos: list["Pedido"] = Relationship(
        back_populates="cliente",
        cascade_delete=True
    )

    itens_criados: list["ItemCardapio"] = Relationship(
        back_populates="criador"
    )


class ClienteCreate(SQLModel):
    nome: str
    data_nascimento: date | None = None
    endereco: str
    cep: str
    numero: str
    telefone: str


class ClienteUpdate(SQLModel):
    nome: str | None = None
    data_nascimento: date | None = None
    endereco: str | None = None
    cep: str | None = None
    numero: str | None = None
    telefone: str | None = None


class ClienteResponse(ClienteBase):
    id: int
    role: UserRole
