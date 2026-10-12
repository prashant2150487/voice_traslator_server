from app.models.role import Permission, Role,role_permissions
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class RoleService:
    @staticmethod
    async def list_roles(db: AsyncSession)-> list[Role]:
        result = await db.execute(select(Role).order_by(Role.code))
        return list(result.scalars().all())

    @staticmethod
    async def has_permission(db: AsyncSession, role_code: str, permission: str) -> bool:
        result = await db.execute(
            select(role_permissions.c.permission_code).where(
                role_permissions.c.role_code == role_code,
                role_permissions.c.permission_code == permission,
            )
        )
        return result.first() is not None

    @staticmethod
    async def list_permissions(db:AsyncSession)-> list[Permission]:
        resut= await db.execute(select(Permission).order_by(Permission.code))
        return list(resut.scalars().all())

    @staticmethod
    async def get_permissions(db: AsyncSession, codes: list[str]) -> list[Permission]:
        if not codes:
            return []
        result = await db.execute(
            select(Permission).where(Permission.code.in_(codes)).order_by(Permission.code)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_role(db:AsyncSession,code:str)-> Role | None:
        return await db.get(Role,code)
    
    @staticmethod
    async def update_role(db:AsyncSession,role:Role , fields:dict)->Role:
        for k , v in fields.items():
            setattr(role,k,v)
        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def set_permissions(db:AsyncSession, role:Role,perms: list[Permission])->Role:
        role.permissions = perms
        await db.commit()
        await db.refresh(role)
        return role




    