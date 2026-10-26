import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.plan_controller import PlanController
from app.dependencies.auth import require_permission
from app.dependencies.db import get_db
from app.schemas.plan import PlanResponse
from app.schemas.response import Envelope , ok


router = APIRouter(prefix ="/plan",tags = ["Plan"])

@router.get("", response_model=Envelope[list[PlanResponse]], dependencies=[Depends(require_permission("plans.manage"))])
async def get_all_plans(db: AsyncSession = Depends(get_db)):
    plans = await PlanController.get_all_plan(db)
    return ok(plans)

@router.get("/{plan_id}", response_model=Envelope[PlanResponse], dependencies=[Depends(require_permission("plans.manage"))])
async def get_plan(plan_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    plan = await PlanController.get_plan(plan_id, db)
    return ok(plan)








