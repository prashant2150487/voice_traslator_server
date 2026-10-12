"""allow role code updates

Revision ID: c8a41d7e2f10
Revises: f4bc7b4d99d1
Create Date: 2026-10-11 17:57:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c8a41d7e2f10"
down_revision: Union[str, Sequence[str], None] = "f4bc7b4d99d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("ck_users_role", "users", type_="check")

    op.drop_constraint(
        "role_permissions_role_code_fkey",
        "role_permissions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_role_permissions_role_code_roles",
        "role_permissions",
        "roles",
        ["role_code"],
        ["code"],
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    op.create_foreign_key(
        "fk_users_role_roles",
        "users",
        "roles",
        ["role"],
        ["code"],
        onupdate="CASCADE",
    )


def downgrade() -> None:
    connection = op.get_bind()
    has_custom_user_roles = connection.execute(
        sa.text(
            "SELECT EXISTS ("
            "SELECT 1 FROM users "
            "WHERE role NOT IN ('super_admin', 'admin', 'user', 'guest')"
            ")"
        )
    ).scalar()
    if has_custom_user_roles:
        raise RuntimeError(
            "Cannot restore the fixed user-role constraint while users have custom roles."
        )

    op.drop_constraint("fk_users_role_roles", "users", type_="foreignkey")
    op.drop_constraint(
        "fk_role_permissions_role_code_roles",
        "role_permissions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "role_permissions_role_code_fkey",
        "role_permissions",
        "roles",
        ["role_code"],
        ["code"],
        ondelete="CASCADE",
    )
    op.create_check_constraint(
        "ck_users_role",
        "users",
        "role IN ('super_admin','admin','user','guest')",
    )
