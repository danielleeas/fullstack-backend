"""create user table

Revision ID: 355ac51cc478
Revises: 
Create Date: 2025-03-27 06:23:15.511192

"""
from typing import Sequence, Union
import ulid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '355ac51cc478'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_ulid():
    return str(ulid.new())

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.String(26), primary_key=True, default=generate_ulid, unique=True, nullable=False),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
