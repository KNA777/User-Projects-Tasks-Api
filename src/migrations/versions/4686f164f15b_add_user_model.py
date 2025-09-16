"""add user model

Revision ID: 4686f164f15b
Revises:
Create Date: 2025-09-04 15:23:22.984476

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "4686f164f15b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("avatar_url", sa.String(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")

