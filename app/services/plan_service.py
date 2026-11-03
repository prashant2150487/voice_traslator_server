import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.plan import Plan


class PlanService:
    @staticmethod
    async def get_all(db:AsyncSession):
        result = await db.execute(select(Plan))
        return list(result.scalars().all())

    @staticmethod
    async def get_plan(plan_id: uuid.UUID, db: AsyncSession) -> Plan | None:
        return await db.get(Plan, plan_id)

    @staticmethod
    async def get_plan_by_code(code: str, db: AsyncSession) -> Plan | None:
        result = await db.execute(select(Plan).where(Plan.code == code))
        return result.scalar_one_or_none()


    @staticmethod
    async def create_plan(data, db: AsyncSession) -> Plan | None:
        new_plan = Plan(
            code=data.code,
            name=data.name,
            price_monthly=data.price_monthly,
            price_yearly=data.price_yearly,
            currency=data.currency,
            limits=data.limits.dict(),
            external_price_id=data.external_price_id,
            is_active=data.is_active
        )
        db.add(new_plan)
        await db.commit()
        await db.refresh(new_plan)
        return new_plan

    # @staticmethod
    # async def update(plan_id: uuid.UUID, data: ):
