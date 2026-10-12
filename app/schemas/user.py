from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime