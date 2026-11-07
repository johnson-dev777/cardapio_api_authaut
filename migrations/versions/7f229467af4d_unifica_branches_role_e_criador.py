"""unifica branches role e criador

Revision ID: 7f229467af4d
Revises: 0004_role_clientes, 0006_criador
Create Date: 2026-11-07 10:36:16.231963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f229467af4d'
down_revision: Union[str, Sequence[str], None] = ('0004_role_clientes', '0006_criador')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
