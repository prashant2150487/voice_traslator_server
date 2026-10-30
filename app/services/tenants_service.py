import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription
from app.models.tenant import Tenant
from app.models.plan import Plan
from sqlalchemy import func, select

from app.models.user import User


class TenantsService:
    @staticmethod
    async  def tenants_list(db,page,page_size,status,q):
        conditions = [Tenant.deleted_at.is_(None)]
        if status:
            conditions.append(Tenant.status == status)
        if q:
            safe = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            pattern = f"%{safe}%"
            conditions.append(Tenant.name.ilike(pattern, escape="\\") | Tenant.slug.ilike(pattern, escape="\\"))

        total = (await db.execute(select(func.count()).select_from(Tenant).where(*conditions))).scalar_one()
        rows = (await db.execute(
            select(Tenant).where(*conditions)
            .order_by(Tenant.created_at.desc(), Tenant.id)
            .offset((page - 1) * page_size).limit(page_size)
        )).scalars().all()
        return list(rows), total
    @staticmethod
    async  def user_counts(db:AsyncSession, tenant_ids:list[uuid.UUID]):
        if not tenant_ids:
            return {}
        rows = await db.execute(
            select(User.tenant_id, func.count())
            .where(User.tenant_id.in_(tenant_ids), User.is_guest.is_(False))
            .group_by(User.tenant_id)
        )
        return {tid: n for tid, n in rows.all()}

    @staticmethod
    async def latest_subscriptions(
        db: AsyncSession, tenant_ids: list[uuid.UUID]
    ) -> dict[uuid.UUID, tuple[Subscription, Plan]]:
        if not tenant_ids:
            return {}
        rows = (await db.execute(
            select(Subscription, Plan)
            .join(Plan, Subscription.plan_id == Plan.id)
            .where(Subscription.tenant_id.in_(tenant_ids))
            .order_by(Subscription.created_at.asc(), Subscription.id.asc())
        )).all()
        return {subscription.tenant_id: (subscription, plan) for subscription, plan in rows}

    @staticmethod
    async def get(db: AsyncSession, tenant_id: uuid.UUID):
        tenant = await db.get(Tenant,tenant_id)
        if not tenant or tenant.deleted_at is not None:
            return  None
        return  tenant
