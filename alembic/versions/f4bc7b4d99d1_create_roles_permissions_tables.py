"""create roles permissions tables

Revision ID: f4bc7b4d99d1
Revises: a21c09ef437b
Create Date: 2026-10-09 14:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f4bc7b4d99d1"
down_revision: Union[str, Sequence[str], None] = "a21c09ef437b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("code", sa.String(length=60), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("code"),
    )

    op.create_table(
        "roles",
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("scope", sa.String(length=20), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_check_constraint(
        "ck_roles_scope",
        "roles",
        "scope IN ('platform', 'tenant', 'room')",
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_code", sa.String(length=20), nullable=False),
        sa.Column("permission_code", sa.String(length=60), nullable=False),
        sa.ForeignKeyConstraint(["role_code"], ["roles.code"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_code"], ["permissions.code"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_code", "permission_code"),
    )

    permissions = [
        {"code": "tenants.manage", "description": "Create, edit and suspend tenants"},
        {"code": "plans.manage", "description": "Manage plans"},
        {"code": "providers.manage", "description": "Manage platform provider profiles"},
        {"code": "platform.usage.view", "description": "View platform usage and billing status"},
        {"code": "support.access", "description": "Explicit, time-limited, audited support access"},
        {"code": "roles.view", "description": "View roles and permissions"},
        {"code": "roles.manage", "description": "Edit role permissions"},
        {"code": "company.settings", "description": "Manage company settings"},
        {"code": "users.manage", "description": "Manage users, roles and invitations"},
        {"code": "billing.manage", "description": "Manage plan and billing"},
        {"code": "usage.view", "description": "View tenant usage"},
        {"code": "audit.view", "description": "View audit log"},
        {"code": "rooms.view_all", "description": "View all company rooms"},
        {"code": "transcripts.view_all", "description": "View all company transcripts"},
        {"code": "rooms.create", "description": "Create rooms"},
        {"code": "rooms.join", "description": "Join rooms"},
        {"code": "profile.edit", "description": "Set own language and voice"},
        {"code": "transcripts.view_own", "description": "View transcripts of joined rooms"},
        {"code": "guests.invite", "description": "Invite guests to hosted rooms"},
        {"code": "room.join_invited", "description": "Join the invited room only"},
        {"code": "room.speak_listen", "description": "Speak and listen in the room"},
        {"code": "transcript.live", "description": "See the live transcript"},
    ]
    op.bulk_insert(sa.table("permissions", sa.column("code", sa.String), sa.column("description", sa.String)), permissions)

    roles = [
        {
            "code": "super_admin",
            "name": "Super Admin",
            "scope": "platform",
            "description": "Whole platform, no tenant. Your own team. Manages tenants, plans, suspension, provider profiles, platform usage and billing status. Does not read transcripts; support access is explicit, time-limited and audited.",
            "is_system": True,
        },
        {
            "code": "admin",
            "name": "Admin",
            "scope": "tenant",
            "description": "One tenant. The person who bought the plan and anyone they promote. Company settings, users and invitations, plan and billing, usage, audit log, all company rooms and transcripts.",
            "is_system": True,
        },
        {
            "code": "user",
            "name": "User",
            "scope": "tenant",
            "description": "One tenant. Company employees. Create and join rooms, set own language and voice, see transcripts of rooms they joined, invite guests to rooms they host.",
            "is_system": True,
        },
        {
            "code": "guest",
            "name": "Guest",
            "scope": "room",
            "description": "One room. External invitee. Join the invited room only, speak, listen and see the live transcript. No access to company data. History after leaving is off by default.",
            "is_system": True,
        },
    ]
    op.bulk_insert(sa.table("roles", sa.column("code", sa.String), sa.column("name", sa.String), sa.column("scope", sa.String), sa.column("description", sa.Text), sa.column("is_system", sa.Boolean)), roles)

    role_permission_rows = [
        ("super_admin", "tenants.manage"),
        ("super_admin", "plans.manage"),
        ("super_admin", "providers.manage"),
        ("super_admin", "platform.usage.view"),
        ("super_admin", "support.access"),
        ("super_admin", "roles.view"),
        ("super_admin", "roles.manage"),
        ("admin", "company.settings"),
        ("admin", "users.manage"),
        ("admin", "billing.manage"),
        ("admin", "usage.view"),
        ("admin", "audit.view"),
        ("admin", "rooms.view_all"),
        ("admin", "transcripts.view_all"),
        ("admin", "rooms.create"),
        ("admin", "rooms.join"),
        ("admin", "profile.edit"),
        ("admin", "guests.invite"),
        ("admin", "roles.view"),
        ("user", "rooms.create"),
        ("user", "rooms.join"),
        ("user", "profile.edit"),
        ("user", "transcripts.view_own"),
        ("user", "guests.invite"),
        ("guest", "room.join_invited"),
        ("guest", "room.speak_listen"),
        ("guest", "transcript.live"),
    ]
    op.bulk_insert(
        sa.table("role_permissions", sa.column("role_code", sa.String), sa.column("permission_code", sa.String)),
        [{"role_code": role_code, "permission_code": permission_code} for role_code, permission_code in role_permission_rows],
    )


def downgrade() -> None:
    op.drop_table("role_permissions")
    op.drop_table("roles")
    op.drop_table("permissions")
