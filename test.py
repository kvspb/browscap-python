import tempfile
import unittest

import gc
from functools import wraps
from pprint import pprint

import asyncio

import browscap
from browscap.aio import BrowscapAsync
from browscap.aio.cache.redis import RedisAioCache
from browscap.cache.redis import RedisCache


class TestCase(unittest.TestCase):
    def tearDown(self):
        result = gc.collect()


class BaseCache:
    def test_known(self):
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
        browser = self.bc.get_browser(ua)
        self.assertEqual(browser['Browser'], 'Chrome')
        self.assertEqual(browser['Version'], '48.0')
        self.assertEqual(browser['Platform'], 'MacOSX')
        self.assertEqual(browser['Platform_Version'], '10.11')

    def test_unknown(self):
        ua = "Fake browser"
        browser = self.bc.get_browser(ua)
        self.assertEqual(browser['Browser'], 'Default Browser')
        self.assertEqual(browser['Version'], '0.0')
        self.assertEqual(browser['Platform'], 'unknown')
        self.assertEqual(browser['Platform_Version'], 'unknown')


class FileCacheTest(unittest.TestCase, BaseCache):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.bc = browscap.Browscap(cache=browscap.FileCache(dirname=cls.temp_dir.name))
        cls.bc.update(file_name='./test.ini')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.temp_dir.cleanup()


class RedisCacheTest(unittest.TestCase, BaseCache):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bc = browscap.Browscap(cache=RedisCache())
        cls.bc.update(file_name='./test.ini')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


def run_until_complete(fun):
    if not asyncio.iscoroutinefunction(fun):
        fun = asyncio.coroutine(fun)

    @wraps(fun)
    def wrapper(test, *args, **kw):
        loop = test.loop
        ret = loop.run_until_complete(fun(test, *args, **kw))
        return ret
    return wrapper
