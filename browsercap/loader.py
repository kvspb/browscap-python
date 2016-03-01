import logging

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

logger = logging.getLogger(__name__)


class IniLoader(object):
    PHP_INI_LITE = 'Lite_PHP_BrowscapINI'
    PHP_INI_FULL = 'Full_PHP_BrowscapINI'
    PHP_INI = 'PHP_BrowscapINI'

    remote_ini_url = 'http://browscap.org/stream?q='
    remote_time_url = 'http://browscap.org/version'
    remote_version_url = 'http://browscap.org/version-number'

    def get_remote_version(self):
        with urlopen(self.remote_version_url) as response:
            return int(response.read())

    def get_version_time(self):
        with urlopen(self.remote_time_url) as response:
            return response.read()

    def get_ini(self, file_name=None, type=PHP_INI):
        url = self.remote_ini_url + type
        logger.info("Fetching %s." % url)
        with urlopen(url) as response:
            contents = response.read()

        logger.info("Fetched")

        if file_name is not None:
            with open(file_name, 'wb') as file:
                file.write(contents)
            logger.info("File %s saved." % file_name)
            return True
        else:
            return contents
