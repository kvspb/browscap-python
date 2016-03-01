try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import logging

from .parser import IniParser

logger = logging.getLogger(__name__)


class Converter(object):
    def __init__(self, cache=None):
        super().__init__()
        self.cache = cache

    def convert_file(self, file_name):
        with open(file_name) as file:
            contents = file.read()
        self.convert_string(contents)

    def convert_string(self, contents):

        logger.info("Loading config file")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read_string(contents)
        logger.info("Config file loaded")
        version = config.get('GJK_Browscap_Version', 'Version')

        self.cache.set('browscap.version', version)

        parser = IniParser()

        paterns = parser.create_patterns(string=contents)
        logger.info("Get paterns")
        for subkey in sorted(paterns.keys()):
            value = paterns[subkey]
            self.cache.set('browscap.patterns.%s' % subkey, value)
        logger.info("Patterns saved")

        parts = parser.create_ini_parts(config=config)
        logger.info("Get parts")
        for (subkey, value) in sorted(parts.items()):
            self.cache.set('browscap.iniparts.%s' % subkey, value)
        logger.info("Parts saved")
