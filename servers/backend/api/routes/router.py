from fastapi import APIRouter

from api.routes.endpoints.product_overviews import OVERVIEW_ROUTER
from api.routes.endpoints.add import ADD_ROUTER
from api.routes.endpoints.wine import WINE_ROUTER

API_ROUTER = APIRouter()

API_ROUTER.include_router(OVERVIEW_ROUTER)
API_ROUTER.include_router(ADD_ROUTER)
API_ROUTER.include_router(WINE_ROUTER)
