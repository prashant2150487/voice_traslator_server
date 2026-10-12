
from fastapi import APIRouter , Depends
from app.dependencies.db import get_db
from app.schemas.roles import ( PermissionOut, RoleOut,RolePermissionsUpdate, RoleSummary, RoleUpdate)
from app.dependencies.auth import require_permission
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.role_controller import RoleController





router = APIRouter(prefix="/roles")
@router.get("",
        response_model=list[RoleSummary],
        dependencies=[Depends(require_permission("roles.view"))]
    )
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await RoleController.list_roles(db)

@router.get("/permissions", response_model=list[PermissionOut],dependencies=[Depends(require_permission("roles.view"))])
async def list_permissions(db: AsyncSession=Depends(get_db)):
    return await RoleController.list_permissions(db)

@router.get("/{code}",response_model=RoleOut,dependencies=[Depends(require_permission("roles.view"))])
async def get_role(code:str,db:AsyncSession=Depends(get_db)):
    return await RoleController.get_role(db , code)

@router.patch("/{code}", response_model=RoleOut, dependencies=[Depends(require_permission("roles.manage"))])
async def update_role(code: str, data: RoleUpdate, db: AsyncSession = Depends(get_db)):
    return await RoleController.update_role(db, code, data)

@router.patch(
    "/{code}/permissions",
    response_model=RoleOut,
    dependencies=[Depends(require_permission("roles.manage"))],
)
async def set_role_permissions(
    code: str, data: RolePermissionsUpdate, db: AsyncSession = Depends(get_db)
):
    return await RoleController.set_permissions(db, code, data)
