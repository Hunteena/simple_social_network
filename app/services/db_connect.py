from contextlib import asynccontextmanager

import aiopg

from app.settings import settings


class Database:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await aiopg.create_pool(dsn=settings.dsn)
        return cls._pool


@asynccontextmanager
async def get_db_conn():
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        yield conn
