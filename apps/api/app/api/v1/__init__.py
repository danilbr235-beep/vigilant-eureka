from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.orders import router as orders_router
from app.api.v1.pricing import router as pricing_router
from app.api.v1.rates import router as rates_router
from app.api.v1.reports import router as reports_router
from app.api.v1.settings import router as settings_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(pricing_router)
api_router.include_router(inventory_router)
api_router.include_router(orders_router)
api_router.include_router(rates_router)
api_router.include_router(settings_router)
api_router.include_router(reports_router)
