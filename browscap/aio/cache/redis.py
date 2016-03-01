import asyncio

import msgpack
from asyncio_redis.encoders import BytesEncoder
from browscap import Cache


class RedisAioCache(Cache):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super().__init__()
        self.db = db
        self.port = port
        self.host = host
        self.connection = None

    def __del__(self):
        self.close_connection()

    @asyncio.coroutine
    def get_connection(self):
        import asyncio_redis
        if self.connection is None:
            self.connection = yield from asyncio_redis.Pool.create(host=self.host, port=self.port, db=self.db,
                                                                   encoder=BytesEncoder())
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    @asyncio.coroutine
    def set(self, key, value):
        connection = yield from self.get_connection()
        result = yield from connection.set(key, msgpack.dumps(value))
        return result

    @asyncio.coroutine
    def get(self, key):
        connection = yield from self.get_connection()
        data = yield from connection.get(key.encode())
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
