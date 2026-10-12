"""replace display names and remove tenant names

Revision ID: 8d4b6a1c2f90
Revises: 6f033bc59f8d
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8d4b6a1c2f90"
down_revision: Union[str, Sequence[str], None] = "6f033bc59f8d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(length=100), nullable=True))
    op.execute(
        """
        UPDATE users
        SET first_name = split_part(btrim(display_name), ' ', 1),
            last_name = CASE
                WHEN strpos(btrim(display_name), ' ') = 0 THEN ''
                ELSE btrim(substr(btrim(display_name), strpos(btrim(display_name), ' ') + 1))
            END
        """
    )
    op.alter_column("users", "first_name", nullable=False)
    op.alter_column("users", "last_name", nullable=False)
    op.drop_column("users", "display_name")
    op.drop_column("tenants", "name")


def downgrade() -> None:
    op.add_column("tenants", sa.Column("name", sa.String(length=150), nullable=True))
    op.execute("UPDATE tenants SET name = ''")
    op.alter_column("tenants", "name", nullable=False)

    op.add_column("users", sa.Column("display_name", sa.String(length=100), nullable=True))
    op.execute(
        """
        UPDATE users
        SET display_name = CASE
            WHEN last_name = '' THEN first_name
            ELSE first_name || ' ' || last_name
        END
        """
    )
    op.alter_column("users", "display_name", nullable=False)
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
