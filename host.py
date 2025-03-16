from ctypes import CDLL, cast, POINTER, byref, c_void_p, pointer, pythonapi, py_object
import api

class MetaHost(type):
    def __new__(cls, clsname, bases, clsdict):
        registry = {}
        extensions = {}
        for name, obj in clsdict.items():
            if hasattr(obj, "hook"):
                ext, method = obj.hook
                registry.setdefault(ext.ID, {})[method] = obj
                extensions[ext.ID] = ext
        clsdict['available_extensions'] = extensions
        clsdict['registry'] = registry
        for ID, ext in extensions.items():
            implemented = set(registry.get(ID).keys())
            if ext.host_hooks ^ implemented:
                raise Exception(f"extension {ID} not completely implemented")
        return super().__new__(cls, clsname, bases, clsdict)

class Host(metaclass=MetaHost):
    clap_version = api.version(
        api.VERSION_MAJOR,
        api.VERSION_MINOR,
        api.VERSION_REVISION)
    def __init__(self, plugin):
        self.plugin = plugin
        self.requested_extensions = set()

    def get_extension(self, extension):
        self.requested_extensions.add(extension)
        try:
            ext = self.available_extensions[extension]
        except KeyError:
            return None
        ext = cast(pointer(ext.this), c_void_p).value
        return ext

    def release(self):
        pythonapi.Py_DecRef(py_object(self))

def create_instance(constructor, plugin, *args):
    host = constructor(plugin, *args)
    pythonapi.Py_NewRef(py_object(host))
    host.c = api.host(
        host.clap_version,
        cast(pointer(py_object(host)), c_void_p),
        host.name,
        host.vendor,
        host.url,
        host.version,
        get_extension_hook,
        request_restart_hook,
        request_process_hook,
        request_callback_hook,
    )
    return pointer(host.c)

def to_host(c_host):
    return cast(c_host[0].host_data, POINTER(py_object))[0]

@api.hook(api.host, 'get_extension')
def get_extension_hook(c_host, extension):
    return to_host(c_host).get_extension(extension)

@api.hook(api.host, 'request_restart')
def request_restart_hook(c_host):
    to_host(c_host).request_restart()

@api.hook(api.host, 'request_process')
def request_process_hook(c_host):
    to_host(c_host).request_process()

@api.hook(api.host, 'request_callback')
def request_callback_hook(c_host):
    to_host(c_host).request_callback()

def hook(ext_module, function):
    def _decorator_(fn):
        fn.hook = ext_module, function
        return fn
    return _decorator_
