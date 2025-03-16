from ctypes import CDLL, cast, POINTER, byref, c_void_p, pointer
import api

class LoadError(Exception):
    """Covers all loading related errors"""

class Entry:
    def __init__(self, path, cdll, c):
        self.path = path
        self.cdll = cdll
        self.c = c

    def get_factory(self, factory_module):
        factory = self.c.get_factory(factory_module.ID)
        if not factory:
            raise LoadError(f"CLAP interface {repr(self.path)} doesn't have {repr(factory.module.ID.decode('utf-8'))}")
        factory = cast(factory, POINTER(factory_module.structure))
        return factory_module.Factory(factory)

    def deinit(self):
        self.c.deinit()

def load(path):
    try:
        cdll = CDLL(path)
        c_entry = api.plugin_entry.in_dll(cdll, 'clap_entry')
    except OSError:
        raise LoadError(f"cannot open CLAP interface {repr(path)}")
    except ValueError:
        raise LoadError(f"cannot retrieve 'clap_entry' symbol from CLAP interface {repr(path)}")
    else:
        if not c_entry.init(path.encode('utf-8')):
            raise LoadError(f"cannot initialize CLAP interface {repr(path)}")
    return Entry(path, cdll, c_entry)

