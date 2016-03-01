import msgpack
from ..cache import Cache


class RedisCache(Cache):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super().__init__()
        self.db = db
        self.port = port
        self.host = host
        self.connection = None

    def get_connection(self):
        import redis
        if self.connection is None:
            self.connection = redis.Redis(host=self.host, port=self.port, db=self.db)
        return self.connection

    def set(self, key, value):
        connection = self.get_connection()
        connection.set(key, msgpack.dumps(value))

    def get(self, key):
        connection = self.get_connection()
        data = connection.get(key)
        if data is not None:
            return msgpack.loads(data, encoding='utf-8')
        return None
