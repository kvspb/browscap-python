# browscap-python
Python Borwscap Libarry

```python
import browscap
from browscap.cache.redis import RedisCache
from browscap import IniLoader

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
bc = browscap.Browscap(cache=RedisCache(db=5))
bc.update(type=IniLoader.PHP_INI_FULL)
browser=bc.get_browser(ua)
```
