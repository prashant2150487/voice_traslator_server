import uuid
from dataclasses import field

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import audit
from app.constants.message import PlanMessages
from app.services.plan_service import PlanService
from app.schemas.plan import PlanUpdate


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
    

    @staticmethod
    async def create_plan(data, db: AsyncSession):
        if await PlanService.get_plan_by_code(data.code, db) is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, PlanMessages.CODE_EXISTS)

        try:
            new_plan = await PlanService.create_plan(data, db)
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status.HTTP_409_CONFLICT, PlanMessages.CODE_EXISTS) from exc

        if new_plan is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Failed to create plan")
        return new_plan

    @staticmethod
    async def delete_plan(plan_id: uuid.UUID, db: AsyncSession):
        plan = await PlanService.get_plan(plan_id, db)
        if plan is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Plan not found")
        if not plan.is_active:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Plan is already inactive")

        plan.is_active = False
        await db.commit()
        await db.refresh(plan)
        return plan

    @staticmethod
    async def activate_plan(plan_id: uuid.UUID, db: AsyncSession):
        plan = await PlanService.get_plan(plan_id,db)
        if plan is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Plan not found")
        if plan.is_active:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Plan already activated")
        plan.is_active = True
        await db.commit()
        await db.refresh(plan)
        return plan

    @staticmethod
    async def update_plan(plan_id: uuid.UUID, data: PlanUpdate, db: AsyncSession):
        plan = await PlanController.get_plan(plan_id, db)

        fields =  { k : v for k,v in data.model_dump(exclude_unset=True).items()
                    if v is not None or k== 'external_price_id'

                    }
        # if data.limits is not None:
        #     await _check_languages(db, data.limits)
        #
        # for k , v in fields.items():
        #     setattr(plan, k, v)
        # AuditService.record(db,)


        plan  = await PlanService.update(plan_id, data, db)
        await db.commit()
        await db.refresh(plan)
        return plan


