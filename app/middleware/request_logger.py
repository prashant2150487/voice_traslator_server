import time, logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        ms = (time.perf_counter() - start) * 1000
        logger.info("%s %s -> %s (%.1fms)", request.method, request.url.path, response.status_code, ms)
        return response