from sqlmodel import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.sql.wine.wine_table import Wine

async def get_all_wines_from_cellar(
        sql_session: AsyncSession
):
    """
    Select all wines that are in the cellar
    :param sql_session:
    :return:
    """
    statement = select(Wine).where(Wine.in_cellar.is_(True))
    result = await sql_session.execute(statement)

    return result

async def get_all_wines_currently_in_cellar(
        sql_session: AsyncSession
):
    """
    Wines that are currently in the cellar still exist there
    :param sql_session:
    :return:
    """
    statement = select(Wine).where(Wine.in_cellar.is_(True), Wine.quantity > 0)
    result = await sql_session.execute(statement)

    return result

async def get_all_past_wines_from_cellar(
        sql_session: AsyncSession
):
    """
    Past wines from the cellar are wines that used to be there but now aren't anymore. Quantity == 0
    :param sql_session:
    :return:
    """
    statement = select(Wine).where(Wine.in_cellar.is_(True), Wine.quantity == 0)
    result = await sql_session.execute(statement)

    return result

async def get_all_wines_on_wishlist(
        sql_session: AsyncSession
):
    """
    Fetch all wines on wishlist
    :param sql_session:
    :return:
    """
    statement = select(Wine).where(Wine.on_wishlist.is_(True))
    result = await sql_session.execute(statement)

    return result

async def get_all_tasted_wines(
        sql_session: AsyncSession
):
    """
    Fetch all tasted wines
    :param sql_session:
    :return:
    """
    statement = select(Wine.has_been_tasted.is_(True))
    result = await sql_session.execute(statement)

    return result
