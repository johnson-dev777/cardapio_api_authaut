
"""Adiciona campo role à tabela clientes."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0004_role_clientes"

# Confira se 0003_clientes ainda é a última migration.
down_revision: Union[str, None] = "0003_clientes"

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Cria o ENUM antes de adicionar a coluna.
    userrole = postgresql.ENUM(
        "CLIENTE",
        "LOGISTA",
        name="userrole",
    )

    userrole.create(bind, checkfirst=True)

    # Adiciona role somente se ainda não existir.
    if inspector.has_table("clientes"):
        if not any(
            coluna["name"] == "role"
            for coluna in inspector.get_columns("clientes")
        ):
            op.add_column(
                "clientes",
                sa.Column(
                    "role",
                    userrole,
                    nullable=False,
                    server_default="CLIENTE",
                ),
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("clientes"):
        colunas = [
            coluna["name"]
            for coluna in inspector.get_columns("clientes")
        ]

        if "role" in colunas:
            op.drop_column("clientes", "role")

    userrole = postgresql.ENUM(
        "CLIENTE",
        "LOGISTA",
        name="userrole",
    )

    userrole.drop(bind, checkfirst=True)
