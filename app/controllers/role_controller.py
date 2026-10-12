from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.services.role_service import RoleService
from app.constants.message import RoleMessages
from app.schemas.roles import RolePermissionsUpdate, RoleUpdate, UserRoleUpdate
from app.constants.rbac import Roles





class RoleController:
    @staticmethod
    async def list_roles(db:AsyncSession):
        return await RoleService.list_roles(db)

    @staticmethod
    async def list_permissions(db: AsyncSession):
        return await RoleService.list_permissions(db)

    @staticmethod
    async def get_role(db: AsyncSession,code:str):
        role = await RoleService.get_role(db,code)
        if not role : 
            raise HTTPException(status.HTTP_404_NOT_FOUND, RoleMessages.NOT_FOUND)
        return role

    @staticmethod
    async def update_role(db: AsyncSession, code: str , data: RoleUpdate ):
        role = await RoleService.get_role(db, code)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, RoleMessages.NOT_FOUND)

        old_code = role.code
        fields = data.model_dump(exclude_unset=True)
        new_code = fields.get("code")
        if new_code is not None and new_code != old_code:
            if old_code == "super_admin":
                raise HTTPException(status.HTTP_403_FORBIDDEN, RoleMessages.CODE_LOCKED)
            if await RoleService.get_role(db, new_code) is not None:
                raise HTTPException(status.HTTP_409_CONFLICT, RoleMessages.CODE_EXISTS)

        try:
            return await RoleService.update_role(db, role, fields)
        except IntegrityError as exc:
            await db.rollback()
            if new_code is not None and new_code != old_code:
                raise HTTPException(status.HTTP_409_CONFLICT, RoleMessages.CODE_EXISTS) from exc
            raise

    @staticmethod
    async def set_permissions(db: AsyncSession, code: str, data: RolePermissionsUpdate):
        role = await RoleController.get_role(db, code)
        if role.code == Roles.SUPER_ADMIN:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, RoleMessages.SUPER_ADMIN_LOCKED)

        wanted = set(data.permissions)
        found = await RoleService.get_permissions(db, list(wanted))
        missing = wanted - {p.code for p in found}
        if missing:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                RoleMessages.UNKNOWN_PERMISSIONS.format(codes=", ".join(sorted(missing))),
            )
        return await RoleService.set_permissions(db, role, found)