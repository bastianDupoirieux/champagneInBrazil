from collections.abc import AsyncIterable
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlmodel import SQLModel

from models.sql.key_value import KeyValueModel
from models.sql.wine import Wine
from utils.db_utils import get_database_url_and_connect_args
from utils.get_env import get_database_url_env

database_url = get_database_url_env()

database_url, connect_args = get_database_url_and_connect_args(database_url)

sql_engine: AsyncEngine = create_async_engine(database_url, connect_args=connect_args)
async_session_maker = async_sessionmaker(sql_engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker as session:
        yield session

async def create_db_and_tables():
    async with sql_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.create_all(
                sync_conn,
                tables = [
                    KeyValueModel.__table__,
                    Wine.__table__,
                ],
            )
        )
