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
