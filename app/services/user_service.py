import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.models.tenant import Tenant

class UserService:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
        return await db.get(User, user_id)

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_tenant_id(db: AsyncSession, tenant_id: str) -> Tenant | None:
        return await db.get(Tenant, tenant_id)

    @staticmethod
    async def create(db: AsyncSession, **fields) -> User:
        user = User(**fields)
        db.add(user)
        await db.flush()
        return user






   

  