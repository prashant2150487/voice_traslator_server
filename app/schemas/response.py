from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Evelope(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta : dict[str,any] | None = None

class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = {}

class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorBody

def ok(data:any,meta:dict[str,Any] | None = None) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": meta
    }

