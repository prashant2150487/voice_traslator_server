import uuid
from fastapi import APIRouter, Depends
from app.dependencies.auth import require_permission
from app.schemas.auth import UserOut
from app.models.user import User
from app.models.role import UserRoleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.role_controller import RoleController



router = APIRouter(prefix="/users", tags=["Isers"])

@router.patch("/{user_id}/role",response_model=UserOut)
async def change_user_role(user_id:uuid.UUID,data: UserRoleUpdate,actor: User=Depends(require_permission("user.manage")),db: AsyncSession=Depends(get_db)):
    return await RoleController.assign_user_role(db,actor,user_id,data)