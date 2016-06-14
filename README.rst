Python Browscap Library
=======================


Detect browser
--------------

.. code:: python

    import browscap
    from browscap.cache.redis import RedisCache

    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
    bc = browscap.Browscap(cache=RedisCache(db=5))
    browser=bc.get_browser(ua)

Detect browser with asyncio
---------------------------

.. code:: python

    from pprint import pprint
    import asyncio
    from browscap.aio import BrowscapAsync
    from browscap.aio.cache.redis import RedisAioCache

    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def get_browser():
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
        cache = RedisAioCache(db=5)

        bc = BrowscapAsync(cache=cache)
        browser = yield from bc.get_browser(ua)

        cache.close_connection()
        return browser


    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        browser = loop.run_until_complete(get_browser())
        pprint(browser)


Update base
-----------

.. code:: python

    import browscap
    from browscap.cache.redis import RedisCache
    from browscap import IniLoader

    bc = browscap.Browscap(cache=RedisCache(db=5))
    bc.update(type=IniLoader.PHP_INI_FULL)
