import re
import itertools

import browscap.quote
from . import pattern_tools
from .property import PropertyFormatter, PropertyHolder
from .subkey_tools import INI_PART_CACHE_KEY_LEN, PATTERN_CACHE_KEY_LEN


def array_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(itertools.islice(it, size)), ())


def strpbrk(haystack, char_list):
    try:
        pos = next(i for i, x in enumerate(haystack) if x in char_list)
        return haystack[pos:]
    except:
        return None


class IniParser(object):
    def __init__(self):
        super().__init__()

    def create_patterns(self, string):
        regexp = re.compile('(?<=\[)(?:[^\r\n]*[?*][^\r\n]*)(?=\])|(?<=\[)(?:[^\r\n*?]+)(?=\])(?![^\[]*Comment=)')
        matches = regexp.findall(string)

        data = {}

        for pattern in matches:
            if 'GJK_Browscap_Version' == pattern:
                continue

            pattern = pattern.lower()
            patternhash = pattern_tools.get_hash_for_pattern(pattern)
            tmp_length = pattern_tools.get_pattern_length(pattern)

            if tmp_length == 0:
                patternhash = 'z' * 32

            if patternhash not in data:
                data[patternhash] = {}

            if tmp_length not in data[patternhash]:
                data[patternhash][tmp_length] = set()

            pattern = browscap.quote.regex_quote(pattern)

            if re.search('\d', pattern) is not None:
                compressed_patern = re.sub('\d', '[\d]', pattern)
                if compressed_patern not in data[patternhash][tmp_length]:
                    data[patternhash][tmp_length].add(compressed_patern)
            else:
                data[patternhash][tmp_length].add(pattern)

        del matches

        contents = {}
        for patternhash in sorted(data.keys()):
            tmp_entries = data[patternhash]
            if len(tmp_entries) == 0:
                continue

            subkey = patternhash[:PATTERN_CACHE_KEY_LEN]
            if subkey not in contents:
                contents[subkey] = []

            for tmp_length in sorted(tmp_entries.keys(), reverse=True):
                tmp_patterns = tmp_entries[tmp_length]
                if len(tmp_patterns) == 0:
                    continue
                chunks = array_chunk(tmp_patterns, 50)
                for chunk in chunks:
                    contents[subkey].append([patternhash, tmp_length, chunk])

        del data

        return contents

    def create_ini_parts(self, config):
        property_formatter = PropertyFormatter(PropertyHolder())
        contents = {}
        contents2 = {}
        for section in config:
            pattern = section.lower()
            patternhash = pattern_tools.get_hash_for_prats(pattern)
            subkey = patternhash[:INI_PART_CACHE_KEY_LEN]

            if subkey not in contents:
                contents[subkey] = []
                contents2[subkey] = {}

            properties = {}
            for property_name in config[section]:
                property_value = config.get(section, property_name).strip('\"')
                properties[property_name] = property_formatter.formatPropertyValue(property_name, property_value)

            contents[subkey].append([patternhash, properties])
            contents2[subkey][patternhash] = properties

        return contents2
