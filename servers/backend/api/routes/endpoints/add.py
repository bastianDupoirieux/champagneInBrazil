from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.sql.wine.wine_read import WineRead
from models.sql.wine.create.create_in_cellar import CreateInCellar
from models.sql.wine.create.create_in_tasting import CreateInTasting
from models.sql.wine.create.create_in_wishlist import CreateInWishlist

from services.database import get_async_session
from services.wine import add_wine

ADD_ROUTER = APIRouter()

@ADD_ROUTER.post(path="/add", response_model=WineRead)
async def add_wine(
        payload: CreateInCellar | CreateInTasting | CreateInWishlist,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await add_wine(payload, sql_session)

    return WineRead.model_validate(wine, from_attributes=True)

'''
@ADD_ROUTER.post(path="/cellar/add", response_model=WineRead)
async def add_wine_to_cellar(
        payload: CreateInCellar,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await add_wine(payload, sql_session)

    return WineRead.model_validate(wine, from_attributes=True)


@ADD_ROUTER.post(path="/tasted/add", response_model=WineRead)
async def add_wine_to_tasted(
        payload: CreateInTasting,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await add_wine(payload, sql_session)

    return WineRead.model_validate(wine, from_attributes=True)


@ADD_ROUTER.post(path="/wishlist/add", response_model=WineRead)
async def add_wine_to_wishlist(
        payload: CreateInWishlist,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await add_wine(payload, sql_session)

    return WineRead.model_validate(wine, from_attributes=True)
'''
