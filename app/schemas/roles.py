import uuid
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator



class PermissionOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    code: str
    description: str

class RoleSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    scope: str
    description: str



class RoleOut(RoleSummary):
    permissions: list[PermissionOut]

class RoleUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=20, pattern=r"^[a-z][a-z0-9_]*$")
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    scope: Literal["platform", "tenant", "room"] | None = None

    @field_validator("code", "name", "description", "scope", mode="before")
    @classmethod
    def reject_null_updates(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value

class RolePermissionsUpdate(BaseModel):
    permissions: list[str]

class UserRoleUpdate(BaseModel):
    role: str
