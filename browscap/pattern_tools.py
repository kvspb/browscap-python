import hashlib
import re


def get_hash_for_pattern(patern, variants=False):
    m = hashlib.md5()
    loc_patern = patern
    loc_patern = loc_patern[:32]

    matches = re.findall('^([^\.\*\?\s\r\n\\\\]+).*$', loc_patern)

    if not matches or matches[0] is None:
        m.update(b'')
        md5 = m.hexdigest()
        if variants:
            return [md5, ]
        else:
            return md5

    string = matches[0]
    if variants is True:
        pattern_starts = []
        for i in range(len(string), 0, -1):
            m = hashlib.md5()
            m.update(string[:i].encode('UTF-8'))
            pattern_starts.append(m.hexdigest())
        m = hashlib.md5()
        m.update(b'')
        pattern_starts.append(m.hexdigest())
        return pattern_starts

    m.update(string.encode('UTF-8'))
    return m.hexdigest()


def get_hash_for_prats(patern):
    m = hashlib.md5()
    m.update(patern.encode('UTF-8'))
    return m.hexdigest()


def get_pattern_length(pattern):
    tmp = pattern
    return len(tmp.replace('*', ''))
