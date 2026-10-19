import uuid
from fastapi import APIRouter, Depends
from app.dependencies.auth import require_permission
from app.schemas.auth import UserOut 
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.role_controller import RoleController
from app.schemas.roles import UserRoleUpdate
from app.dependencies.db import get_db
from app.schemas.response import ok, Envelope



router = APIRouter(prefix="/users", tags=["Users"])

@router.patch("/{user_id}/role",response_model = Envelope[UserOut])
async def change_user_role(user_id:uuid.UUID,data: UserRoleUpdate,actor: User=Depends(require_permission("users.manage")),db: AsyncSession=Depends(get_db)):
    user = await RoleController.assign_user_role(db,actor,user_id , data)
    return ok(UserOut.model_validate(user))
