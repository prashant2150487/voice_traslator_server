from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
# from app.bootstrap import run_bootstrap
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.core.database import engine
from app.middleware.request_logger import RequestLoggerMiddleware
from app.routes import api_router
from app.core.exceptions import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        print("Database connection: connected", flush=True)
    except SQLAlchemyError as exc:
        print(f"Database connection: failed ({type(exc).__name__})", flush=True)

    yield
    await engine.dispose()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
register_exception_handlers(app)

app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "ok"}