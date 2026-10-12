import uuid
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.message import AuthMessages
from app.core.security import decode_access_token
from app.dependencies.db import get_db
from app.models.user import User
from app.services.user_service import UserService
from app.services.role_service import RoleService
bearer = HTTPBearer(auto_error=False)

async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED, AuthMessages.INVALID_TOKEN, headers={"WWW-Authenticate": "Bearer"}
    )
    if not creds:
        raise unauthorized
    try:
        payload = decode_access_token(creds.credentials)
        user_id = uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorized

    user = await UserService.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise unauthorized
    return user

def require_roles(*roles: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
        return user
    return checker


def require_permission(code: str):
    async def checker(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        if not await RoleService.has_permission(db, user.role, code):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
        return user
    return checker