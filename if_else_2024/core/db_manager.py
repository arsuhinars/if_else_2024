# flake8: noqa: E402
import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# isort: off
from if_else_2024.accounts.models import Account
from if_else_2024.auth.models import AuthSession
from if_else_2024.regions.models import RegionType, Region


class DatabaseManager:
    def __init__(self, db_url: str):
        self._engine = create_async_engine(
            db_url,
        )
        self._sessionmaker = async_sessionmaker(
            self._engine, expire_on_commit=False, autoflush=False
        )

    async def initialize(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
            logger.info("Database was successfully initialized")

    async def dispose(self):
        await self._engine.dispose()
        logger.info("Closed connection with database")

    @asynccontextmanager
    async def create_session(self):
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as ex:
                logger.error(
                    "Exception was thrown during database session. Rollback",
                    exc_info=ex,
                )
                await session.rollback()
                raise ex
