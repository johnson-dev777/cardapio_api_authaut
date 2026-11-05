"""0005_adiciona_role_clientes

Revision ID: 0005_role
Revises: 0004_pedidos
Create Date: 2026-11-05 16:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0005_role'
down_revision: Union[str, None] = '0004_pedidos'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona a coluna role na tabela clientes."""
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('role', sa.String(length=20), nullable=False, server_default='CLIENTE')
        )


def downgrade() -> None:
    """Remove a coluna role da tabela clientes."""
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.drop_column('role')