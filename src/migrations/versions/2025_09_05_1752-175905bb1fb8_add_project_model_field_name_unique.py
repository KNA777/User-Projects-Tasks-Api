"""add project model field name unique

Revision ID: 175905bb1fb8
Revises: ec09d261cf77
Create Date: 2025-09-05 17:52:54.343236

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "175905bb1fb8"
down_revision: Union[str, Sequence[str], None] = "ec09d261cf77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_unique_constraint(None, "projects", ["name"])



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(None, "projects", type_="unique")

