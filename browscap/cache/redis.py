import msgpack
from ..cache import Cache


class RedisCache(Cache):
    def __init__(self, connection, db=0):
        super().__init__()
        self.db = db
        self.connection = connection

    def set(self, key, value):
        # self.connection.db(self.db)
        self.connection.set(key, msgpack.dumps(value))

    def get(self, key):
        # self.connection.db(self.db)
        data = self.connection.get(key)
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
