from contextlib import asynccontextmanager

import aiopg

from app.settings import settings


class Database:
    _pool = None
    dsn = (
        f"postgresql://"
        f"{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await aiopg.create_pool(dsn=cls.dsn)
        return cls._pool


@asynccontextmanager
async def get_db_conn():
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        yield conn
