from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.core.config import settings
from app.db.database import Base, engine
from app.routers.base import api_router

app = FastAPI()


def include_routers(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def redis():
    redis = aioredis.from_url(str(settings.redis.REDIS_URL), encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


def start_application():
    app = FastAPI(
        title=settings.app.PROJECT_NAME,
        description=settings.app.PROJECT_VERSION,
    )
    create_tables()
    redis()
    include_routers(app)
    return app


app = start_application()
