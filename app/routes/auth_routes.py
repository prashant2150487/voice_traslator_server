
from app.models.user import User
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.auth_controller import AuthController
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.auth import RegisterUserRequest, TokenEnvelope, TokenResponse , LoginRequest , UserOut
from app.schemas.response import ok , Envelope

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenEnvelope, status_code=status.HTTP_201_CREATED)
async def register_user(data: RegisterUserRequest, db: AsyncSession = Depends(get_db)):
    return TokenEnvelope(data=await AuthController.register_user(db, data))

@router.post("/login", response_model=Envelope[TokenResponse], status_code=status.HTTP_200_OK)
async def login(dataLogin: LoginRequest, db: AsyncSession = Depends(get_db)):
    return ok(await AuthController.login(db, dataLogin))

@router.get("/getme", response_model=Envelope[UserOut], status_code=status.HTTP_200_OK)
async def me(user: User = Depends(get_current_user)):
    return ok(UserOut.model_validate(user))

