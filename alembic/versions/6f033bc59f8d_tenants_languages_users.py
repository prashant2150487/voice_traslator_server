"""tenants languages users

Revision ID: 6f033bc59f8d
Revises: de7b088e6b6d
Create Date: 2026-10-07 17:00:28.677787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f033bc59f8d'
down_revision: Union[str, Sequence[str], None] = 'de7b088e6b6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()
    if connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM users)")).scalar():
        raise RuntimeError(
            "Cannot convert the legacy users table while it contains rows; "
            "migrate user IDs and fields explicitly first."
        )

    op.create_table('languages',
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('tenants',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('tenant_id', sa.UUID(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=False))
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('display_name', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('preferred_language', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('is_guest', sa.Boolean(), nullable=False))
    op.alter_column('users', 'id', server_default=None)
    op.execute('ALTER SEQUENCE users_id_seq OWNED BY NONE')
    op.execute('DROP SEQUENCE users_id_seq')
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False,
               postgresql_using='gen_random_uuid()')
    op.alter_column('users', 'id', server_default=sa.text('gen_random_uuid()'))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index(op.f('ix_users_tenant_id'), 'users', ['tenant_id'], unique=False)
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
    op.create_foreign_key('fk_users_tenant_id_tenants', 'users', 'tenants', ['tenant_id'], ['id'])
    op.create_foreign_key('fk_users_preferred_language_languages', 'users', 'languages', ['preferred_language'], ['code'])
    op.create_check_constraint('ck_users_role', 'users', "role IN ('super_admin','admin','user','guest')")
    op.create_check_constraint('ck_users_tenant_required', 'users', "role = 'super_admin' OR tenant_id IS NOT NULL")
    op.drop_column('users', 'name')


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    if connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM users)")).scalar():
        raise RuntimeError("Cannot downgrade the users schema while it contains rows.")

    op.drop_constraint('fk_users_tenant_id_tenants', 'users', type_='foreignkey')
    op.drop_constraint('fk_users_preferred_language_languages', 'users', type_='foreignkey')
    op.drop_constraint('ck_users_role', 'users', type_='check')
    op.drop_constraint('ck_users_tenant_required', 'users', type_='check')
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_index(op.f('ix_users_tenant_id'), table_name='users')
    op.add_column('users', sa.Column('name', sa.VARCHAR(length=100), nullable=False))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'id', server_default=None)
    op.execute('CREATE SEQUENCE users_id_seq')
    op.alter_column('users', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               postgresql_using="nextval('users_id_seq'::regclass)")
    op.alter_column('users', 'id', server_default=sa.text("nextval('users_id_seq'::regclass)"))
    op.execute('ALTER SEQUENCE users_id_seq OWNED BY users.id')
    op.drop_column('users', 'is_guest')
    op.drop_column('users', 'preferred_language')
    op.drop_column('users', 'display_name')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'role')
    op.drop_column('users', 'tenant_id')
    op.drop_table('tenants')
    op.drop_table('languages')
