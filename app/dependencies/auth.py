import uuid
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.dependencies.db import get_db
from app.models.user import User
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.core.exceptions import AppException
from app.constants.errors import ErrorCode
from app.constants.message import AuthMessages


bearer = HTTPBearer(auto_error=False)
_WWW = {"WWW-Authenticate": "Bearer"}

async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED, AuthMessages.INVALID_TOKEN, headers={"WWW-Authenticate": "Bearer"}
    )
    if not creds:
        raise AppException(ErrorCode.AUTH_REQUIRED, AuthMessages.NOT_AUTHENTICATED, headers=_WWW)
    try:
        payload = decode_access_token(creds.credentials)
        user_id = uuid.UUID(payload["sub"])
    except jwt.ExpiredSignatureError:  # must come before InvalidTokenError (it is a subclass)
        raise AppException(ErrorCode.AUTH_TOKEN_EXPIRED, AuthMessages.TOKEN_EXPIRED, headers=_WWW)
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise AppException(ErrorCode.AUTH_TOKEN_INVALID, AuthMessages.INVALID_TOKEN, headers=_WWW)

    user = await UserService.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise AppException(ErrorCode.AUTH_TOKEN_INVALID, AuthMessages.INVALID_TOKEN, headers=_WWW)
    return user

def require_roles(*roles: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to do this")
        return user
    return checker


def require_permission(code: str):
    async def checker(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        if not await RoleService.has_permission(db, user.role, code):
            raise AppException(ErrorCode.FORBIDDEN, "You do not have permission to do this")
        return user
    return checker