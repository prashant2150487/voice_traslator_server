

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from app.constants.message import AuthMessages
from app.core.config import settings
from app.models.tenant import Tenant
from app.schemas.auth import RegisterUserRequest, TokenResponse , LoginRequest , UserOut
from app.services.user_service import UserService
from app.core.security import create_access_token, decode_access_token, verify_password
from starlette.concurrency import run_in_threadpool
from app.core.exceptions import AppException
from app.constants.errors import ErrorCode

def _token_response(user) -> TokenResponse:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = create_access_token(user.id, user.tenant_id, user.role, expires_at)
    return TokenResponse(
        access_token=token,
        expires_at=expires_at,
        user=UserOut.model_validate(user),
    )

class AuthController:
    password_hash = PasswordHash.recommended()

    @staticmethod
    async def register_user(db: AsyncSession, data: RegisterUserRequest) -> TokenResponse:
        if await UserService.get_by_email(db, data.email):
            raise HTTPException(status.HTTP_409_CONFLICT, AuthMessages.EMAIL_EXISTS)

        tenant = Tenant()
        db.add(tenant)
        await db.flush()

        user = await UserService.create(
            db,
            tenant_id=tenant.id,
            email=data.email,
            password_hash=AuthController.password_hash.hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            role="user",
            is_guest=False,
            is_active=True,
        )

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = jwt.encode(
            {
                "sub": str(user.id),
                "tenant_id": str(user.tenant_id),
                "role": user.role,
                "exp": expires_at,
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        return TokenResponse(access_token=access_token, expires_at=expires_at, user=user)

    @staticmethod
    async def login(db: AsyncSession , data: LoginRequest)-> TokenResponse:
        user = await UserService.get_by_email(db, data.email)
        invalid = AppException(ErrorCode.AUTH_INVALID_CREDENTIALS, AuthMessages.INVALID_CREDENTIALS)

        if not user or not user.password_hash:
            raise invalid
        if not await run_in_threadpool(verify_password, data.password, user.password_hash):
            raise invalid
        if not user.is_active:
            raise AppException(ErrorCode.ACCOUNT_DISABLED, AuthMessages.ACCOUNT_DISABLED)

        return _token_response(user)