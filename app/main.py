from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.core.config import settings
from app.db.database import Base, engine
from app.routers.base import api_router

app = FastAPI(title=settings.app.PROJECT_NAME,
              description=settings.app.PROJECT_VERSION,)


app.include_router(api_router)

print(settings.rabbit.RABBIT_URL)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(str(settings.redis.REDIS_URL), encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
