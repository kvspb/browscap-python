import asyncio

import browscap.quote
from ..subkey_tools import INI_PART_CACHE_KEY_LEN, PATTERN_CACHE_KEY_LEN
from .. import pattern_tools, Browser
from ..browscap import BrowscapBase, SettingsHelper, GetPattern
from ..pattern_tools import get_hash_for_pattern
from ..quote import preg_un_quote


class SettingsHelperAsync(SettingsHelper):
    @asyncio.coroutine
    def get_settings(self, quoted_pattern, settings=None):
        parent = None
        unquoted_pattern = preg_un_quote(quoted_pattern)
        pattern = unquoted_pattern.lower()
        patternhash = pattern_tools.get_hash_for_prats(pattern)
        subkey = patternhash[:INI_PART_CACHE_KEY_LEN]

        buffer = yield from self.cache.get('browscap.iniparts.%s' % subkey)
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
                settings = yield from self.get_settings(browscap.quote.regex_quote(parent), settings)

        return settings


class GetPatternAsync(GetPattern):
    @asyncio.coroutine
    def get_cache_patterns(self, subkey):
        if subkey not in self.local_cache:
            self.local_cache[subkey] = yield from self.cache.get('browscap.patterns.%s' % subkey)
        return self.local_cache[subkey]

    @asyncio.coroutine
    def get_patterns(self, ua):
        starts = get_hash_for_pattern(ua, True)
        length = len(ua)
        starts.append('z' * 32)

        contents = []
        for tmp_start in starts:
            patterns = yield from self.get_cache_patterns(tmp_start[:PATTERN_CACHE_KEY_LEN])

            if patterns is None:
                continue

            found = False
            for buffer in patterns:
                if buffer[0] == tmp_start:
                    if buffer[1] <= length:
                        contents.append(buffer[2])
                    found = True
                elif found is True:
                    break

        return contents


class BrowscapAsync(BrowscapBase):
    def __init__(self, cache=None):
        super().__init__(cache)
        self.pattern_helper = GetPatternAsync(cache=cache)
        self.setting_helper = SettingsHelperAsync(cache=cache)

    @asyncio.coroutine
    def get_browser(self, ua):
        ua_lower = ua.lower()
        patterns_block = yield from self.pattern_helper.get_patterns(ua_lower)

        for pattern in self.find_settings(patterns_block, ua_lower):
            sett = yield from self.setting_helper.get_settings(pattern)
            if sett is not None:
                return Browser(sett)

        return Browser()
