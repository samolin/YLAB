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


async def cache_deleter(path: str):

    #  ['70a4e126-bf98-4d80-a176-4e3b72b76904', 'c7ffdc80-aae7-451c-8f9e-2ed1da167a0a', 'a8e4d128-b4a3-4b96-8001-d2fc5fb8f212']
    ''' menu: - del everytime
        menu:70a4e126-bf98-4d80-a176-4e3b72b76904
        submenu:70a4e126-bf98-4d80-a176-4e3b72b76904 - del everytime
        submenu:70a4e126-bf98-4d80-a176-4e3b72b76904:c7ffdc80-aae7-451c-8f9e-2ed1da167a0a
        dish:70a4e126-bf98-4d80-a176-4e3b72b76904:c7ffdc80-aae7-451c-8f9e-2ed1da167a0a - del everytime
        dish:70a4e126-bf98-4d80-a176-4e3b72b76904:c7ffdc80-aae7-451c-8f9e-2ed1da167a0a:a8e4d128-b4a3-4b96-8001-d2fc5fb8f212

    '''

    path = path.split('/')
    ids = list(filter(lambda id: len(id) == 36, path))
    cache_keys = []
    id = ''
    for i in ids:
        id += f':{i}'
        cache_keys.append(id[1:])
    to_delete = []
    if len(cache_keys) == 3:
        to_delete.append('dish:' + cache_keys.pop())
    if len(cache_keys) == 2:
        two_ids = cache_keys.pop()
        to_delete.append('dish:' + two_ids)
        to_delete.append('submenu:' + two_ids)
    if len(cache_keys) == 1:
        id = cache_keys.pop()
        to_delete.append('submenu:' + id)
        to_delete.append('menu:' + id)
    to_delete.append('menu:')
    print('CACHE_KEYS:  ', cache_keys)
    print('TO_DELETE: ', to_delete)
    redis = Redis.from_url(str(settings.redis.REDIS_URL))
    redis.delete(*to_delete)
