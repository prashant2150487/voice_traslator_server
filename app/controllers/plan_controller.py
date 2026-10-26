import uuid
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.plan_service import PlanService


class PlanController:

    @staticmethod
    async def get_all_plan(db:AsyncSession):
        plans = await  PlanService.get_all(db)
        if plans is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Plan not found")
        return plans

    @staticmethod
    async def get_plan(plan_id: uuid.UUID, db: AsyncSession) :
        plan=await PlanService.get_plan(plan_id , db)
        if plan is None :
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Plan not found")
        return plan

