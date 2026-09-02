"""Owns the asynchronous PostgreSQL engine and request-scoped session factory.
Database consumers receive one transaction-capable session without managing the pool."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.database_url, pool_pre_ping=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_database_session() -> AsyncIterator[AsyncSession]:
    """Yield an isolated asynchronous session for one application operation."""
    async with session_factory() as session:
        yield session


async def close_database() -> None:
    """Dispose pooled database connections during application shutdown."""
    await engine.dispose()
