import asyncio
from typing import AsyncGenerator

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from redis import asyncio as aioredis

from app.core.config import settings
from app.db.database import Base, engine
from app.main import app

pytest_plugins = ('tests.functional.fixtures')


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as c:
        yield c


@pytest.fixture(autouse=True, scope='session')
async def redis():
    redis = aioredis.from_url(str(settings.redis.REDIS_URL), encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache-test')


@pytest.fixture(scope='function', autouse=True)
async def cleanup_redis():
    yield
    redis = aioredis.from_url(str(settings.redis.REDIS_URL))
    await redis.flushdb()
