import tempfile
import unittest

import gc
from pprint import pprint

import browsercap


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.bc = browsercap.Browscap(cache=browsercap.FileCache(dirname=cls.temp_dir.name))
        cls.bc.update(file_name='./test.ini')


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.temp_dir.cleanup()

    def tearDown(self):
        result = gc.collect()


class FileCache(TestCase):
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
