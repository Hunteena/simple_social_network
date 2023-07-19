from contextlib import asynccontextmanager

import aiopg

from app.settings import settings


@asynccontextmanager
async def postgres_connection():
    pool = await aiopg.create_pool(
        dsn=f"postgresql://"
            f"{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
            f"{settings.POSTGRES_DB}"
    )
    async with pool:
        async with pool.acquire() as conn:
            yield conn
