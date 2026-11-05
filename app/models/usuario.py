# app/models/usuario.py
from enum import Enum
from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    CLIENTE = "cliente"
    LOGISTA = "logista" # O admin

class UsuarioBase(SQLModel):
    nome: str = Field(min_length=2, max_length=150)
    email: str = Field(unique=True, index=True)
    ativo: bool = Field(default=True)

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: int | None = Field(default=None, primary_key=True)
    senha_hash: str
    role: UserRole = Field(default=UserRole.CLIENTE)

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    role: UserRole