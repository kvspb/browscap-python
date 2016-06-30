import asyncio

import msgpack
from browscap import Cache


class RedisAioCache(Cache):
    def __init__(self, connection, db=0):
        super().__init__()
        self.db = db
        self.connection = connection

    @asyncio.coroutine
    def set(self, key, value):
        yield from self.connection.select(self.db)
        result = yield from self.connection.set(key, msgpack.dumps(value))
        return result

    @asyncio.coroutine
    def get(self, key):
        yield from self.connection.select(self.db)
        data = yield from self.connection.get(key.encode())
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
