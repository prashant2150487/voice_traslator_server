import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.constants.errors import ERROR_HTTP_STATUS, ErrorCode

logger = logging.getLogger("app")


class AppException(Exception):
    """Raise this from controllers and services. The handler turns it into the standard error body."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: dict[str, Any] | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code or ERROR_HTTP_STATUS[code]
        self.headers = headers
        super().__init__(message)


def _error(status_code: int, code: ErrorCode, message: str, details=None, headers=None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content={
            "success": False,
            "error": {"code": code.value, "message": message, "details": details or {}},
        },
    )


_HTTP_TO_CODE = {
    400: ErrorCode.BAD_REQUEST,
    401: ErrorCode.AUTH_TOKEN_INVALID,
    403: ErrorCode.FORBIDDEN,
    404: ErrorCode.NOT_FOUND,
    405: ErrorCode.METHOD_NOT_ALLOWED,
    409: ErrorCode.CONFLICT,
    429: ErrorCode.RATE_LIMITED,
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exc(request: Request, exc: AppException):
        return _error(exc.status_code, exc.code, exc.message, exc.details, exc.headers)

    @app.exception_handler(StarletteHTTPException)
    async def http_exc(request: Request, exc: StarletteHTTPException):
        # Catches the plain HTTPException raised by older code and unknown routes (404/405).
        code = _HTTP_TO_CODE.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return _error(exc.status_code, code, message, headers=getattr(exc, "headers", None))

    @app.exception_handler(RequestValidationError)
    async def validation_exc(request: Request, exc: RequestValidationError):
        errors = [
            {"field": ".".join(str(p) for p in e["loc"][1:]) or str(e["loc"][0]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return _error(422, ErrorCode.VALIDATION_ERROR, "Invalid request", {"errors": errors})

    @app.exception_handler(Exception)
    async def unhandled_exc(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return _error(500, ErrorCode.INTERNAL_ERROR, "Something went wrong")