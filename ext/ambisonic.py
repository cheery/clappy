import api
import api.ext.ambisonic
import host

ID = api.ext.ambisonic.EXT_AMBISONIC

plugin_structure = api.ext.ambisonic.plugin_ambisonic

class PluginAmbisonic:
    def __init__(self, c, e):
        self.c = c
        self.e = e

    def is_config_supported(self, c_config):
        return self.e[0].is_config_supported(self.c, byref(c_config))

    def get_config(self, is_input, port_index, c_config):
        if not self.e[0].get_config(self.c, is_input, port_index, byref(c_config)):
            raise Exception("could not get ambisonic config")

PluginExtension = PluginAmbisonic

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.ambisonic.host_ambisonic, "changed")
def changed_hook(c_host):
    return dispatch(c_host, "changed")

this = api.ext.ambisonic.host_ambisonic(changed_hook)

host_hooks = {
    "changed",
}
