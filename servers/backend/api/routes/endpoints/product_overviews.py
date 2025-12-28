#Contains the routes to the "my cellar" and "experienced wines" pages
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from sqlmodel import select

from models.sql.wine import Wine


OVERVIEW_ROUTER = APIRouter(prefix="/overview", tags=["overview"])

OVERVIEW_ROUTER.get("/cellar")
async def get_wines_in_cellar(sql_session: AsyncSession):
    not_drank_wines_statement = select(Wine).where(Wine.has_been_drunk.is_not(True))
    wines = await sql_session.execute(not_drank_wines_statement)

    return wines


@OVERVIEW_ROUTER.get("/experienced_wines")
async def get_wines_not_in_cellar(sql_session: AsyncSession)
    statement = select(Wine).where(Wine.has_been_drunk.is_(True))
    wines = await sql_session.execute(statement)

    return wines
