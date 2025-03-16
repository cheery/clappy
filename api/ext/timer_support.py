from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_TIMER_SUPPORT = b"clap.timer-support"

class plugin_timer_support(Structure):
    _fields_ = [
        ('on_timer', ABI(None, POINTER(api.plugin), api.id)),
    ]

class host_timer_support(Structure):
    _fields_ = [
        ('register_timer', ABI(c_bool,
                               POINTER(api.host),
                               c_uint32,
                               POINTER(api.id))),
        ('unregister_timer', ABI(c_bool,
                                 POINTER(api.host),
                                 api.id)),
    ]

