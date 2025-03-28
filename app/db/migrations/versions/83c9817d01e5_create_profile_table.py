"""create profile table

Revision ID: 83c9817d01e5
Revises: 355ac51cc478
Create Date: 2025-03-27 06:45:47.388029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import ulid

# revision identifiers, used by Alembic.
revision: str = '83c9817d01e5'
down_revision: Union[str, None] = '355ac51cc478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_ulid():
    return str(ulid.new())

def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column('id', sa.String(26), primary_key=True, default=generate_ulid, unique=True, nullable=False),
        sa.Column('user_id', sa.String(26), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column("bio", sa.String(500), nullable=True),
        sa.Column("title", sa.String(100), nullable=True),
        sa.Column("avatar", sa.String(255), nullable=True),
        sa.Column("cover", sa.String(255), nullable=True),
        sa.Column("location", sa.String(100), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table("profiles")
