from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_PRESET_LOAD = b"clap.preset-load/2"

class plugin_preset_load(Structure):
    _fields_ = [
        ('from_location', ABI(c_bool,
                              POINTER(api.plugin),
                              c_uint32,
                              c_char_p,
                              c_char_p)),
    ]

class host_preset_load(Structure):
    _fields_ = [
        ('on_error', ABI(None,
                         POINTER(api.host),
                         c_uint32,
                         c_char_p,
                         c_char_p,
                         c_int32,
                         c_char_p)),
        ('loaded', ABI(None,
                       POINTER(api.host),
                       c_char_p,
                       c_char_p)),
    ]

