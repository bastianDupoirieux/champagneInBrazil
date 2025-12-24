#Contains the routes to the "my cellar" and "experienced wines" pages
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter


OVERVIEW_ROUTER = APIRouter(prefix="/overview", tags=["overview"])

