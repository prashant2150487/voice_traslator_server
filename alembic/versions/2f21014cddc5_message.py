"""message

Revision ID: 2f21014cddc5
Revises: 8d4b6a1c2f90
Create Date: 2026-10-07 20:38:06.204906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f21014cddc5'
down_revision: Union[str, Sequence[str], None] = '8d4b6a1c2f90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
