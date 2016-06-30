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
        transaction = yield from self.connection.multi()
        yield from transaction.select(self.db)
        f = yield from transaction.set(key, msgpack.dumps(value))
        yield from transaction.exec()
        data = yield from f

        return data

    @asyncio.coroutine
    def get(self, key):
        transaction = yield from self.connection.multi()
        yield from transaction.select(self.db)
        f = yield from transaction.get(key.encode())
        yield from transaction.exec()
        data = yield from f

        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
