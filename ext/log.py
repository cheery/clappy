
import api
import api.ext.log
import host

ID = api.ext.log.EXT_LOG

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.log.host_log, "log")
def log_hook(c_host):
    return dispatch(c_host, "log")

this = api.ext.log.host_log(log_hook)

host_hooks = {
    "log",
}
