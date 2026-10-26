from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.tenants_controller import TenantsController
from app.dependencies.auth import require_permission
from app.dependencies.db import get_db
from app.schemas.response import Envelope, ok
from app.schemas.tenants import TenantsListItem
from app.models.user import User

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("", response_model=Envelope[list[TenantsListItem]])
async def list_tenants(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    status: str | None = Query(None, max_length=100),
    _: User = Depends(require_permission("tenants.manage")),
    db: AsyncSession = Depends(get_db),
):
    items, pagination = await TenantsController.list(db, page, page_size, status, q)
    return ok(items, pagination=pagination)
