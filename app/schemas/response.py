from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: T
    pagination: dict[str, Any] | None = None


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = {}

class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorBody

def ok(
    data: Any,
    pagination: dict[str, Any] | None = None,
    message: str = "",
) -> dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": pagination,
    }
