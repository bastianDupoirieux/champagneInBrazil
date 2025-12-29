from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from fastapi import HTTPException

from models.sql.wine.wine_table import Wine
from models.sql.wine.create.create_in_cellar import CreateInCellar
from models.sql.wine.create.create_in_tasting import CreateInTasting
from models.sql.wine.create.create_in_wishlist import CreateInWishlist


async def select_wine_by_id(
        wine_id: uuid.UUID,
        sql_session: AsyncSession
):
    statement = select(Wine).where(Wine.id == wine_id)
    wine = await sql_session.execute(statement)

    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")

    return wine


async def add_wine(
        wine_data: CreateInCellar | CreateInTasting | CreateInWishlist,
        sql_session: AsyncSession,
):
    wine_data.model_validate(wine_data.model_dump())
    new_wine = Wine(**wine_data.model_dump())

    sql_session.add(new_wine)
    await sql_session.commit()
    await sql_session.refresh(new_wine)

    return new_wine
