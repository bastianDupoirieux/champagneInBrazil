#Contains the routes to the "my cellar" and "experienced wines" pages
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from models.sql.wine.wine_table import Wine
from models.sql.wine.wine_read import WineRead

from services.database import get_async_session
from services.wine_lists import (
get_all_wines_from_cellar,
get_all_wines_currently_in_cellar,
get_all_past_wines_from_cellar,
get_all_wines_on_wishlist,
get_all_tasted_wines,
)

from utils.orm import convert_orm_to_tuple


OVERVIEW_ROUTER = APIRouter(prefix="/overview", tags=["overview"])

@OVERVIEW_ROUTER.get(path="/cellar", response_model=list[WineRead])
async def get_wines_in_cellar(
        sql_session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_wines_from_cellar(sql_session)
    wines = convert_orm_to_tuple(result)

    return wines

@OVERVIEW_ROUTER.get(path="/cellar/current", response_model=list[WineRead])
async def get_wines_currently_in_cellar(
        sql_session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_wines_currently_in_cellar(sql_session)
    wines = convert_orm_to_tuple(result)

    return wines

@OVERVIEW_ROUTER.get(path="/cellar/past", response_model=list[WineRead])
async def get_past_wines_from_cellar(
        sql_session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_past_wines_from_cellar(sql_session)
    wines = convert_orm_to_tuple(result)

    return wines

@OVERVIEW_ROUTER.get(path="/tasted", response_model=list[WineRead])
async def get_tasted_wines(
        sql_session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_tasted_wines(sql_session)
    wines = convert_orm_to_tuple(result)

    return wines

@OVERVIEW_ROUTER.get(path="/wishlist", response_model=list[WineRead])
async def get_wines_on_wishlist(
        sql_session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_wines_on_wishlist(sql_session)
    wines = convert_orm_to_tuple(result)

    return wines
