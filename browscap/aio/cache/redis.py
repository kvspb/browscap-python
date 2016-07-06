import asyncio

import msgpack
from browscap import Cache


class RedisAioCache(Cache):
    def __init__(self, redis):
        super().__init__()
        self.redis = redis

    @asyncio.coroutine
    def set(self, key, value):
        result = yield from self.redis.set(key, msgpack.dumps(value))
        return result

    @asyncio.coroutine
    def get(self, key):
        data = yield from self.redis.get(key.encode())
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None


class RedisPoolAioCache(Cache):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    @asyncio.coroutine
    def set(self, key, value):
        with (yield from self.pool) as redis:
            result = yield from redis.set(key, msgpack.dumps(value))
        return result

    @asyncio.coroutine
    def get(self, key):
        with (yield from self.pool) as redis:
            data = yield from redis.get(key.encode())
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
