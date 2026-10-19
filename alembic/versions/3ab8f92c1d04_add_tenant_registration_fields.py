"""Add tenant registration fields.

Revision ID: 3ab8f92c1d04
Revises: da185c8a0551
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "3ab8f92c1d04"
down_revision: Union[str, Sequence[str], None] = "da185c8a0551"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tenants", sa.Column("name", sa.String(length=150), nullable=True))
    op.add_column("tenants", sa.Column("slug", sa.String(length=63), nullable=True))
    op.add_column("tenants", sa.Column("status", sa.String(length=15), nullable=True))
    op.add_column("tenants", sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("tenants", sa.Column("default_language", sa.String(length=10), nullable=True))
    op.add_column(
        "tenants",
        sa.Column("data_region", sa.String(length=20), nullable=True),
    )
    op.add_column("tenants", sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column(
        "tenants",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        """
        UPDATE tenants
        SET name = 'Workspace',
            slug = 'workspace-' || replace(id::text, '-', ''),
            status = CASE WHEN is_active THEN 'active' ELSE 'suspended' END,
            data_region = 'default',
            settings = '{}'::jsonb
        """
    )

    op.alter_column("tenants", "name", nullable=False)
    op.alter_column("tenants", "slug", nullable=False)
    op.alter_column(
        "tenants",
        "status",
        existing_type=sa.String(length=15),
        server_default="active",
        nullable=False,
    )
    op.alter_column(
        "tenants",
        "data_region",
        existing_type=sa.String(length=20),
        server_default="default",
        nullable=False,
    )
    op.alter_column(
        "tenants",
        "settings",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        server_default=sa.text("'{}'::jsonb"),
        nullable=False,
    )

    op.create_unique_constraint("uq_tenants_slug", "tenants", ["slug"])
    op.create_check_constraint(
        "ck_tenants_status",
        "tenants",
        "status IN ('trial','active','past_due','suspended','cancelled')",
    )
    op.create_check_constraint(
        "ck_tenants_slug",
        "tenants",
        r"slug ~ '^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$'",
    )
    op.create_foreign_key(
        "fk_tenants_owner_user",
        "tenants",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_tenants_default_language_languages",
        "tenants",
        "languages",
        ["default_language"],
        ["code"],
    )
    op.drop_column("tenants", "is_active")


def downgrade() -> None:
    op.add_column(
        "tenants",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=True),
    )
    op.execute("UPDATE tenants SET is_active = status = 'active'")
    op.alter_column("tenants", "is_active", nullable=False)

    op.drop_constraint("fk_tenants_default_language_languages", "tenants", type_="foreignkey")
    op.drop_constraint("fk_tenants_owner_user", "tenants", type_="foreignkey")
    op.drop_constraint("ck_tenants_slug", "tenants", type_="check")
    op.drop_constraint("ck_tenants_status", "tenants", type_="check")
    op.drop_constraint("uq_tenants_slug", "tenants", type_="unique")

    op.drop_column("tenants", "deleted_at")
    op.drop_column("tenants", "settings")
    op.drop_column("tenants", "data_region")
    op.drop_column("tenants", "default_language")
    op.drop_column("tenants", "owner_user_id")
    op.drop_column("tenants", "status")
    op.drop_column("tenants", "slug")
    op.drop_column("tenants", "name")
