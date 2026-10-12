"""remove preferred language from users

Revision ID: a21c09ef437b
Revises: 8d4b6a1c2f90
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a21c09ef437b"
down_revision: Union[str, Sequence[str], None] = "2f21014cddc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("fk_users_preferred_language_languages", "users", type_="foreignkey")
    op.drop_column("users", "preferred_language")


def downgrade() -> None:
    op.add_column("users", sa.Column("preferred_language", sa.String(length=10), nullable=True))
    op.create_foreign_key(
        "fk_users_preferred_language_languages",
        "users",
        "languages",
        ["preferred_language"],
        ["code"],
    )
