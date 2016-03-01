import re

unquote_replace_to = (
    "\\", "+", "*", "?", "[", "^", "]", "\$", "(", ")", "{", "}", "=", "!", "<", ">", "|", ":",
    "-", ".", "/", ' ', ','
)
unquote_replace_from = (
    "\\\\", "\\+", "\\*", "\\?", "\\[", "\\^", "\\]", "\\\$", "\\(", "\\)", "\\{", "\\}", "\\=",
    "\\!", "\\<", "\\>", "\\|", "\\:", "\\-", "\\.", "\\/", '\ ', '\,'
)


def preg_un_quote(pattern):
    unquoted = pattern

    if re.search('[^a-z\s]', pattern, flags=re.IGNORECASE) is not None:
        unquoted = re.sub('(?<!\\\\)\\.\\*', '\\*', unquoted)
        unquoted = re.sub('(?<!\\\\)\\.', '\\?', unquoted)
        unquoted = re.sub('(?<!\\\\)\\\\x', '\\x', unquoted)

        for i in range(0, len(unquote_replace_from)):
            unquoted = unquoted.replace(unquote_replace_from[i], unquote_replace_to[i])
        pass

    return unquoted


def regex_quote(string):
    tmp = re.escape(string)
    tmp = tmp.replace('\*', '.*').replace('\?', '.').replace('\\x', '\\\\x')
    return tmp