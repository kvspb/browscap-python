from .cache import Cache, FileCache
from .converter import Converter
from .browscap import Browser, Browscap
from .loader import IniLoader

__title__ = 'browscap'
__version__ = '0.0.12'
__author__ = "Valery Komarov"

VERSION = tuple(map(int, __version__.split('.')))

__all__ = [Browser, Browscap, IniLoader, Converter, FileCache, Cache]
