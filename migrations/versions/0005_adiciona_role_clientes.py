
"""Adiciona role à tabela clientes."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_role"
down_revision: Union[str, None] = "0004_pedidos"

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table("clientes"):
        colunas = [
            coluna["name"]
            for coluna in inspector.get_columns("clientes")
        ]

        if "role" not in colunas:
            op.add_column(
                "clientes",
                sa.Column(
                    "role",
                    sa.String(length=20),
                    nullable=False,
                    server_default="CLIENTE"
                )
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
