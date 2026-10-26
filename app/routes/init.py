from fastapi import APIRouter
from app.routes.auth_routes import router as auth_router
from app.routes.role_routes import router as role_router
from app.routes.user_routes import router as user_router
from app.routes.plan_routes import router as plan_router
from app.routes.tenants_routes import router as tenants_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(role_router)
api_router.include_router(user_router)
api_router.include_router(plan_router)
api_router.include_router(tenants_router)
