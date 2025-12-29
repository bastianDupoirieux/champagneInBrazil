from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from fastapi import HTTPException

from models.sql.wine.wine_table import Wine


async def select_wine_by_id(
        wine_id: uuid.UUID,
        sql_session: AsyncSession
):
    statement = select(Wine).where(Wine.id == wine_id)
    wine = await sql_session.execute(statement)

    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")

    return wine
