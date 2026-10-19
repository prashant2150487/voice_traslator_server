
from fastapi import APIRouter , Depends
from app.dependencies.db import get_db
from app.schemas.roles import ( PermissionOut, RoleOut,RolePermissionsUpdate, RoleSummary, RoleUpdate)
from app.dependencies.auth import require_permission
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.role_controller import RoleController
from app.schemas.response import Envelope , ok





router = APIRouter(prefix="/roles",tags=['Roles'])

@router.get("",response_model=Envelope[list[RoleSummary]],dependencies=[Depends(require_permission("roles.view"))])
async def list_roles(db: AsyncSession = Depends(get_db)):
    roles = await RoleController.list_roles(db)
    return ok([RoleSummary.model_validate(role) for role in roles])

@router.get("/permissions", response_model=Envelope[list[PermissionOut]],dependencies=[Depends(require_permission("roles.view"))])
async def list_permissions(db: AsyncSession=Depends(get_db)):
    permissions = await RoleController.list_permissions(db)
    return  ok([PermissionOut.model_validate(p) for p in permissions])

@router.get("/{code}",response_model=Envelope[RoleOut],dependencies=[Depends(require_permission("roles.view"))])
async def get_role(code:str,db:AsyncSession=Depends(get_db)):
    role= await RoleController.get_role(db,code)
    return ok(RoleOut.model_validate(role))

@router.patch("/{code}", response_model=Envelope[RoleOut], dependencies=[Depends(require_permission("roles.manage"))])
async def update_role(code: str, data: RoleUpdate, db: AsyncSession = Depends(get_db)):
    role = await RoleController.update_role(db,code,data)
    return ok(RoleOut.model_validate(role))

@router.patch(
    "/{code}/permissions",
    response_model=RoleOut,
    dependencies=[Depends(require_permission("roles.manage"))],
)
async def set_role_permissions(
    code: str, data: RolePermissionsUpdate, db: AsyncSession = Depends(get_db)
):
    return await RoleController.set_permissions(db, code, data)
