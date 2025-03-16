from ctypes import CDLL, cast, POINTER, byref, c_void_p, pointer
import api
import host
import plugin

ID = api.PLUGIN_FACTORY_ID
structure = api.plugin_factory

class PluginFactory:
    def __init__(self, c):
        self.c = c

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return self.c[0].get_plugin_count(self.c)

    def __getitem__(self, index):
        d = self.c[0].get_plugin_descriptor(self.c, index)
        if not d:
            raise IndexError("plugin descriptor index out of range")
        return dict(
            id = d[0].id,
            name = d[0].name,
            vendor = d[0].vendor,
            url = d[0].url,
            manual_url = d[0].manual_url,
            support_url = d[0].support_url,
            version = d[0].version,
            description = d[0].description,
            features = api.nt_list(d[0].features)
        )

    def create(self, host_constructor, id, *args):
        plug = plugin.Plugin()
        c_host = host.create_instance(host_constructor, plug, *args)
        plug.c = self.c[0].create_plugin(self.c, c_host, id)
        if not plug.c:
            raise Exception(f"creation of plugin {repr(id.decode('utf-8'))} failed")
        if not plug.c[0].init(plug.c):
            raise Exception(f"could not initialize plugin {repr(id.decode('utf-8'))}") 
        plug.host = host.to_host(c_host)
        return plug

Factory = PluginFactory
