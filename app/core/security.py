import uuid
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

_hasher = PasswordHash.recommended()  # argon2

def hash_password(password: str) -> str:
    return _hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return _hasher.verify(password, hashed)

def create_access_token(
    user_id: uuid.UUID,
    tenant_id: uuid.UUID | None,
    role: str,
    expires_at: datetime | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id) if tenant_id else None,
        "role": role,
        "iat": now,
        "exp": (
            expires_at
            if expires_at is not None
            else now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])