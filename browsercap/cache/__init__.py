import os

import msgpack


class Cache(object):
    def set(self, key, value):
        pass

    def get(self, key):
        pass


class FileCache(object):
    def __init__(self, dirname):
        super().__init__()
        self.dirname = dirname

    def set(self, key, value):
        with open("%s/%s" % (self.dirname, key), 'wb') as file:
            file.write(msgpack.dumps(value))

    def get(self, key):
        file_path = "%s/%s" % (self.dirname, key)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                data = file.read()
            return msgpack.loads(data, encoding='utf-8')
        return None
