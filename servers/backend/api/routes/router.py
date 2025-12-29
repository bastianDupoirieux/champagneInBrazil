from fastapi import APIRouter

from api.routes.endpoints.product_overviews import OVERVIEW_ROUTER

API_ROUTER = APIRouter(prefix="/api")

API_ROUTER.include_router(OVERVIEW_ROUTER)