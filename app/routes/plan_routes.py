import uuid

from fastapi import APIRouter, Depends , Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.plan_controller import PlanController
from app.dependencies import db
from app.dependencies.auth import require_permission
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.plan import PlanResponse, PlanOut, PlanCreate, PlanUpdate
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

@router.post("/", response_model = Envelope[PlanOut], status_code=201)
async def create_plan(
    data: PlanCreate,
    request: Request,
    actor: User = Depends(require_permission("plans.manage")),
    db: AsyncSession = Depends(get_db),
):
    new_plan = await PlanController.create_plan(data, db)
    return ok(new_plan)

@router.delete("/{plan_id}" , response_model=Envelope[PlanOut], status_code=201)
async def delete_plan(
    plan_id: uuid.UUID,
    actor: User = Depends(require_permission("plans.manage")),
    db: AsyncSession = Depends(get_db),
):
    deleted_plan = await PlanController.delete_plan(plan_id,db)
    return ok(deleted_plan,message="Plan deactivated successfully")

@router.post("/{plan_id}/activate" , response_model=Envelope[PlanOut], status_code=201)
async def activate_plan(
    plan_id: uuid.UUID,
    actor: User = Depends(require_permission("plans.manage")),
    db: AsyncSession = Depends(get_db),
):
    activated_plan= await PlanController.activate_plan(plan_id,db)
    return ok(activated_plan,message="Plan activated successfully")

@router.patch("/{plan_id", response_model=Envelope[PlanOut], status_code=200)
async def update_plan(
        plan_id: uuid.UUID,
        data: PlanUpdate,
        db: AsyncSession = Depends(get_db),
):
    plan= await PlanController.update_plan(plan_id, data, db)
    return ok(plan, message="Plan updated successfully")












