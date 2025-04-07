"""create token table

Revision ID: 78220b89765a
Revises: 83c9817d01e5
Create Date: 2025-04-07 18:03:18.225032

"""
from typing import Sequence, Union
import ulid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78220b89765a'
down_revision: Union[str, None] = '83c9817d01e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_ulid():
    return str(ulid.new())

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tokens",
        sa.Column("id", sa.String(26), primary_key=True, default=generate_ulid, unique=True, nullable=False),
        sa.Column("user_id", sa.String(26), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tokens")
