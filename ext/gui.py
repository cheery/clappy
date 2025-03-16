import api
import api.ext.gui
import host
from ctypes import c_uint32, byref

ID = api.ext.gui.EXT_GUI

plugin_structure = api.ext.gui.plugin_gui

class PluginGUI:
    def __init__(self, c, e):
        self.c = c
        self.e = e

    def is_api_supported(self, api, is_floating):
        return self.e[0].is_api_supported(self.c, api, is_floating)

    def get_preferred_api(self):
        result = c_char_p(0)
        is_floating = c_bool(False)
        if not self.e[0].get_preferred_api(self.c, byref(result), port_index, byref(is_floating)):
            raise Exception("could not get preferred GUI api")
        return result.value, is_floating.value

    def create(self, api, is_floating):
        if not self.e[0].create(self.c, api, is_floating):
            raise Exception("could not create GUI")

    def destroy(self):
        self.e[0].destroy(self.c)

    def set_scale(self, scale):
        if not self.e[0].set_scale(self.c, scale):
            raise Exception("could not apply GUI scaling")

    def get_size(self):
        width = c_uint32()
        height = c_uint32()
        if not self.e[0].get_size(self.c, byref(width), byref(height)):
            raise Exception("could not get current size of a GUI")
        return width.value, height.value

    def can_resize(self):
        return self.e[0].can_resize(self.c)

    def get_resize_hints(self):
        hints = api.ext.gui.resize_hints()
        if not self.e[0].get_resize_hints(self.c, byref(hints)):
            raise Exception("could not get resize hints")
        return hints

    def adjust_size(self, c_width, c_height):
        if not self.e[0].get_size(self.c, byref(c_width), byref(c_height)):
            raise Exception("could not adjust size of a GUI")

    def set_size(self, width, height):
        if not self.e[0].set_size(self.c, width, height):
            raise Exception("could not set size of a GUI")
        return hints

    def set_parent(self, window):
        if not self.e[0].set_parent(self.c, to_c_window(window)):
            raise Exception("could not embed plugin window")

    def set_transient(self, window):
        if not self.e[0].set_parent(self.c, to_c_window(window)):
            raise Exception("could not set transient")

    def suggest_title(self, title):
        self.e[0].suggest_title(self.c, title)

    def show(self):
        if not self.e[0].show(self.c):
            raise Exception("could not show GUI")

    def hide(self):
        if not self.e[0].hide(self.c):
            raise Exception("could not hide GUI")

PluginExtension = PluginGUI

def to_c_window(window):
    a, handle = window
    w = api.ext.gui.window(a)
    match a:
        case 'cocoa':
            w.ptr.cocoa = handle
        case 'x11':
            w.ptr.x11 = handle
        case 'win32':
            w.ptr.win32 = handle
        case _:
            w.ptr.ptr = handle
    return w

def dispatch(c_host, method, *args):
    h = host.to_host(c_host)
    return h.registry[ID][method](h, *args)

@api.hook(api.ext.gui.host_gui, "resize_hints_changed")
def resize_hints_changed_hook(c_host):
    return dispatch(c_host, "resize_hints_changed")

@api.hook(api.ext.gui.host_gui, "request_resize")
def request_resize_hook(c_host, width, height):
    return dispatch(c_host, "request_resize", width, height)

@api.hook(api.ext.gui.host_gui, "request_show")
def request_show_hook(c_host):
    return dispatch(c_host, "request_show")

@api.hook(api.ext.gui.host_gui, "request_hide")
def request_hide_hook(c_host):
    return dispatch(c_host, "request_hide")

@api.hook(api.ext.gui.host_gui, "closed")
def closed_hook(c_host, was_destroyed):
    return dispatch(c_host, "closed", was_destroyed)

this = api.ext.gui.host_gui(
    resize_hints_changed_hook,
    request_resize_hook,
    request_show_hook,
    request_hide_hook,
    closed_hook,
    )

host_hooks = {
    "resize_hints_changed",
    "request_resize",
    "request_show",
    "request_hide",
    "closed"
}
