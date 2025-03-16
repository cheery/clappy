import api
import api.ext.audio_ports
import host
from ctypes import byref

ID = api.ext.audio_ports.EXT_AUDIO_PORTS

plugin_structure = api.ext.audio_ports.plugin_audio_ports

class PluginAudioPorts:
    def __init__(self, c, e):
        self.c = c
        self.e = e
        self.inputs = Ports(self.c, self.e, True)
        self.outputs = Ports(self.c, self.e, False)

class Ports:
    def __init__(self, c, e, is_input):
        self.c = c
        self.e = e
        self.is_input = is_input

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return self.e[0].count(self.c, self.is_input)

    def __getitem__(self, index):
        c_info = api.ext.audio_ports.audio_port_info()
        if not self.e[0].get(self.c, index, self.is_input, byref(c_info)):
            raise Exception("could not get audio port info")
        return dict(
            id = c_info.id,
            name = c_info.name,
            flags = c_info.flags,
            channel_count = c_info.channel_count,
            port_type = c_info.port_type,
            in_place_pair = c_info.in_place_pair,
        )

PluginExtension = PluginAudioPorts

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.audio_ports.host_audio_ports, "is_rescan_flag_supported")
def is_rescan_flag_supported_hook(c_host, flags):
    return dispatch(c_host, "is_rescan_flag_supported", flags)

@api.hook(api.ext.audio_ports.host_audio_ports, "rescan")
def rescan_hook(c_host, flags):
    return dispatch(c_host, "rescan", flags)

this = api.ext.audio_ports.host_audio_ports(
    is_rescan_flag_supported_hook,
    rescan_hook,
)

host_hooks = {
    "is_rescan_flag_supported",
    "rescan",
}
