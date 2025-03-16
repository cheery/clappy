import api
import api.ext.timer_support
import host

ID = api.ext.timer_support.EXT_TIMER_SUPPORT

plugin_structure = api.ext.timer_support.plugin_timer_support

class PluginTimer:
    def __init__(self, c, e):
        self.c = c
        self.e = e

    def on_timer(self, timer_id):
        self.e[0].on_timer(self.c, timer_id)

PluginExtension = PluginTimer

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.timer_support.host_timer_support, "register_timer")
def register_timer_hook(c_host, freqms, c_ref):
    return dispatch(c_host, "register_timer", freqms, c_ref)

@api.hook(api.ext.timer_support.host_timer_support, "unregister_timer")
def unregister_timer_hook(c_host, timer_id):
    return dispatch(c_host, "unregister_timer", timer_id)

this = api.ext.timer_support.host_timer_support(
    register_timer_hook,
    unregister_timer_hook)

host_hooks = {
    "register_timer",
    "unregister_timer"
}
