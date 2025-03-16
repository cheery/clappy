import api
import api.ext.thread_check
import host

ID = api.ext.thread_check.EXT_THREAD_CHECK

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.thread_check.host_thread_check, "is_main_thread")
def is_main_thread_hook(c_host):
    return dispatch(c_host, "is_main_thread")

@api.hook(api.ext.thread_check.host_thread_check, "is_audio_thread")
def is_audio_thread_hook(c_host):
    return dispatch(c_host, "is_audio_thread")

this = api.ext.thread_check.host_thread_check(is_main_thread_hook, is_audio_thread_hook)

host_hooks = {
    "is_main_thread",
    "is_audio_thread"
}
