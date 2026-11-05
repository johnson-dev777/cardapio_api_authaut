"""0006_adiciona_criador_id_itens_cardapio

Revision ID: 0006_criador
Revises: 0005_role
Create Date: 2026-11-05 16:34:05.366708
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0006_criador'
down_revision: Union[str, None] = '0005_role'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona a coluna criador_id e a FK na tabela itens_cardapio."""
    with op.batch_alter_table('itens_cardapio', schema=None) as batch_op:
        # 1. Adiciona a coluna
        batch_op.add_column(sa.Column('criador_id', sa.Integer(), nullable=True))
        
        # 2. Cria a chave estrangeira (nomeada para evitar problemas no downgrade)
        batch_op.create_foreign_key(
            'fk_itens_cardapio_criador_id', 
            'clientes', 
            ['criador_id'], 
            ['id']
        )


def downgrade() -> None:
    """Reverte a criação da FK e da coluna."""
    with op.batch_alter_table('itens_cardapio', schema=None) as batch_op:
        batch_op.drop_constraint('fk_itens_cardapio_criador_id', type_='foreignkey')
        batch_op.drop_column('criador_id')