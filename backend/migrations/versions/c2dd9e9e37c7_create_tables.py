"""create tables

Revision ID: c2dd9e9e37c7
Revises:
Create Date: 2026-01-20 21:35:29.259956
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c2dd9e9e37c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'produtos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('preco', sa.Float, nullable=False),
        sa.Column('estoque', sa.Integer, nullable=False),
        sa.Column('descricao', sa.Text),
    )

    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('senha_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=True),
    )

    op.create_table(
        'vendas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('produto_id', sa.Integer, sa.ForeignKey('produtos.id')),
        sa.Column('usuario_id', sa.Integer, sa.ForeignKey('usuarios.id')),
        sa.Column('quantidade', sa.Integer, nullable=False),
        sa.Column('data', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('vendas')
    op.drop_table('usuarios')
    op.drop_table('produtos')
