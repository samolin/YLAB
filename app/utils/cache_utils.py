from httpx import Request, Response
from redis import Redis

from app.core.config import settings


def id_key_builder(
    func,
    namespace: str = '',
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    path = request.url.path.split('/')
    ids = ':'.join(filter(lambda id: len(id) == 36, path))
    return ':'.join([
        namespace,
        ids,
    ])


def cache_deleter():
    redis = Redis.from_url(str(settings.redis.REDIS_URL))
    redis.flushdb()
