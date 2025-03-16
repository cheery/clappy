from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, Union, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_GUI = b"clap.gui"

clap_hwnd = c_void_p
clap_nsview = c_void_p
clap_xwnd = c_ulong

class window_reference(Union):
    _fields_ = [
        ('cocoa', c_void_p),
        ('x11', c_ulong),
        ('win32', c_void_p),
        ('ptr', c_void_p),
    ]

class window(Structure):
    _fields_ = [
        ('api', c_char_p),
        ('ptr', window_reference),
    ]

class gui_resize_hints(Structure):
    _fields_ = [
        ('can_resize_horizontally', c_bool),
        ('can_resize_vertically', c_bool),
        ('preserve_aspect_ratio', c_bool),
        ('aspect_ratio_width', c_uint32),
        ('aspect_ratio_height', c_uint32),
    ]

class plugin_gui(Structure):
    pass

plugin_gui._fields_ = [
    ('is_api_supported', ABI(c_bool,
                             POINTER(api.plugin),
                             c_char_p,
                             c_bool)),
    ('get_preferred_api', ABI(c_bool,
                              POINTER(api.plugin),
                              POINTER(c_char_p),
                              c_bool)),
    ('create', ABI(c_bool,
                   POINTER(api.plugin),
                   c_char_p,
                   c_bool)),
    ('destroy', ABI(None, POINTER(api.plugin))),
    ('set_scale', ABI(c_bool, POINTER(api.plugin), c_double)),
    ('get_size', ABI(c_bool, POINTER(api.plugin), POINTER(c_uint32), POINTER(c_uint32))),
    ('can_resize', ABI(c_bool, POINTER(api.plugin))),
    ('get_resize_hints', ABI(c_bool, POINTER(api.plugin), POINTER(gui_resize_hints))),
    ('adjust_size', ABI(c_bool, POINTER(api.plugin), POINTER(c_uint32), POINTER(c_uint32))),
    ('set_size', ABI(c_bool, POINTER(api.plugin), c_uint32, c_uint32)),
    ('set_parent', ABI(c_bool, POINTER(api.plugin), POINTER(window))),
    ('set_transient', ABI(c_bool, POINTER(api.plugin), POINTER(window))),
    ('suggest_title', ABI(None, POINTER(api.plugin), c_char_p)),
    ('show', ABI(c_bool, POINTER(api.plugin))),
    ('hide', ABI(c_bool, POINTER(api.plugin))),
]

class host_gui(Structure):
    pass

host_gui._fields_ = [
    ('resize_hints_changed', ABI(None, POINTER(api.host))),
    ('request_resize', ABI(c_bool, POINTER(api.host), c_uint32, c_uint32)),
    ('request_show', ABI(c_bool, POINTER(api.host))),
    ('request_hide', ABI(c_bool, POINTER(api.host))),
    ('closed', ABI(None, POINTER(api.host), c_bool)),
]
