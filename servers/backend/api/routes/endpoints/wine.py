#@TODO Bastian Duporieux

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from models.sql.wine.wine_table import Wine
from models.sql.wine.wine_read import WineRead
from services.database import get_async_session
from services.wine import select_wine_by_id

WINE_ROUTER = APIRouter(prefix="/wine/{wine_id}", tags=["Wine"])

@WINE_ROUTER.get(path="/details", response_model=WineRead)
async def wine_details(
        wine_id: uuid.UUID,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await select_wine_by_id(wine_id, sql_session)

    return WineRead.model_validate(wine, from_attributes=True)

@WINE_ROUTER.post(path="/details", response_model=WineRead)
async def edit_wine(
        wine_id: uuid.UUID,
        sql_session: AsyncSession = Depends(get_async_session)
):
    wine = await select_wine_by_id(wine_id, sql_session)

    data = {}
    columns = [column.name for column in Wine.__table__.columns]
    for col in columns:
        pass





