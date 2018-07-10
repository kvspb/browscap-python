import logging
import os
import re2
import tempfile

import browscap.quote
from . import pattern_tools
from .pattern_tools import get_hash_for_pattern
from .quote import preg_un_quote
from .subkey_tools import INI_PART_CACHE_KEY_LEN, PATTERN_CACHE_KEY_LEN

from .converter import Converter
from .loader import IniLoader

logger = logging.getLogger(__name__)


class Browser(dict):
    def __init__(self, iterable=None, **kwargs):
        default_properties = {
            'browser_name_regex': None,
            'browser_name_pattern': None,
            'Parent': None,
            'Comment': 'Default Browser',
            'Browser': 'Default Browser',
            'Browser_Type': 'unknown',
            'Browser_Bits': '0',
            'Browser_Maker': 'unknown',
            'Browser_Modus': 'unknown',
            'Version': '0.0',
            'MajorVer': '0',
            'MinorVer': '0',
            'Platform': 'unknown',
            'Platform_Version': 'unknown',
            'Platform_Description': 'unknown',
            'Platform_Bits': '0',
            'Platform_Maker': 'unknown',
            'Alpha': False,
            'Beta': False,
            'Win16': False,
            'Win32': False,
            'Win64': False,
            'Frames': False,
            'IFrames': False,
            'Tables': False,
            'Cookies': False,
            'BackgroundSounds': False,
            'JavaScript': False,
            'VBScript': False,
            'JavaApplets': False,
            'ActiveXControls': False,
            'isMobileDevice': False,
            'isTablet': False,
            'isSyndicationReader': False,
            'Crawler': False,
            'CssVersion': '0',
            'AolVersion': '0',
            'Device_Name': 'unknown',
            'Device_Maker': 'unknown',
            'Device_Type': 'unknown',
            'Device_Pointing_Method': 'unknown',
            'Device_Code_Name': 'unknown',
            'Device_Brand_Name': 'unknown',
            'RenderingEngine_Name': 'unknown',
            'RenderingEngine_Version': 'unknown',
            'RenderingEngine_Description': 'unknown',
            'RenderingEngine_Maker': 'unknown',
        }
        super().__init__(default_properties, **kwargs)
        if iterable is not None:
            for item in iterable:
                self[item] = iterable[item]


class BrowscapBase(object):
    def __init__(self, cache=None):
        super().__init__()
        self.cache = cache

    def get_version(self):
        return self.cache.get('browscap.version')

    def update(self, type=IniLoader.PHP_INI_FULL, file_name=None):

        if file_name is None:
            f_name = tempfile.gettempdir() + '/browscap_tmp.ini'
            loader = IniLoader()
            if loader.get_ini(file_name=f_name, type=type) is False:
                return False
        else:
            f_name = file_name

        converter = Converter(cache=self.cache)
        converter.convert_file(file_name=f_name)

        if file_name is None:
            os.unlink(f_name)

    def find_settings(self, patterns_block, ua_lower):
        for patterns in patterns_block:

            pattern = re2.compile('^(?:%s)$' % ')|(?:'.join(patterns))
            if pattern.search(ua_lower) is None:
                continue

            for pattern in patterns:
                pattern = pattern.replace('[\d]', '(\d)')
                match_result = re2.search("^%s$" % pattern, ua_lower)

                if match_result is not None:
                    matches = match_result.groups()
                    for match in matches:
                        pattern = pattern.replace('(\d)', match, 1)

                    yield pattern


class Browscap(BrowscapBase):
    def __init__(self, cache=None):
        super().__init__(cache)
        self.pattern_helper = GetPattern(cache=cache)
        self.setting_helper = SettingsHelper(cache=cache)

    def get_browser(self, ua):
        ua_lower = ua.lower()
        patterns_block = self.pattern_helper.get_patterns(ua_lower)

        for pattern in self.find_settings(patterns_block, ua_lower):
            sett = self.setting_helper.get_settings(pattern)

            if sett is not None:
                return Browser(sett)

        return Browser()


class SettingsHelper(object):
    def __init__(self, cache=None):
        super().__init__()
        self.cache = cache

    def get_settings(self, quoted_pattern, settings=None):
        parent = None
        unquoted_pattern = preg_un_quote(quoted_pattern)
        pattern = unquoted_pattern.lower()
        patternhash = pattern_tools.get_hash_for_prats(pattern)
        subkey = patternhash[:INI_PART_CACHE_KEY_LEN]

        buffer = self.cache.get('browscap.iniparts.%s' % subkey)

        if buffer is not None:
            if patternhash in buffer:
                added_settings = buffer[patternhash]

                if settings is None:
                    settings = added_settings
                    settings['browser_name_regex'] = '^%s$' % pattern
                    settings['browser_name_pattern'] = unquoted_pattern
                else:
                    for (key, value) in added_settings.items():
                        if key not in settings:
                            settings[key] = value

                if 'Parent' in settings:
                    parent = settings['Parent']
                    del settings['Parent']

                if parent is not None:
                    settings = self.get_settings(browscap.quote.regex_quote(parent), settings)

        return settings


class GetPattern(object):
    local_cache = {}

    @classmethod
    def purge_cache(cls):
        cls.local_cache.clear()

    def __init__(self, cache=None):
        super().__init__()
        self.cache = cache

    def get_cache_patterns(self, subkey):
        if subkey not in self.local_cache:
            self.local_cache[subkey] = self.cache.get('browscap.patterns.%s' % subkey)
        return self.local_cache[subkey]

    def get_patterns(self, ua):
        starts = get_hash_for_pattern(ua, True)
        length = len(ua)
        starts.append('z' * 32)

        for tmp_start in starts:
            patterns = self.get_cache_patterns(tmp_start[:PATTERN_CACHE_KEY_LEN])

            if patterns is None or len(patterns) == 0:
                continue

            found = False
            for buffer in patterns:
                if buffer[0] == tmp_start:
                    if buffer[1] <= length:
                        yield buffer[2]
                    found = True
                elif found is True:
                    break
