from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_AMBISONIC = b"clap.ambisonic/3"

AMBISONIC_ORDERING_FUMA = 0
AMBISONIC_ORDERING_ACN = 1

AMBISONIC_NORMALIZATION_MAXN = 0
AMBISONIC_NORMALIZATION_SN3D = 1
AMBISONIC_NORMALIZATION_N3D = 2
AMBISONIC_NORMALIZATION_SN2D = 3
AMBISONIC_NORMALIZATION_N2D = 4

class ambisonic_config(Structure):
    _fields_ = [
        ('ordering', c_uint32),
        ('normalization', c_uint32),
    ]

class plugin_ambisonic(Structure):
    _fields_ = [
        ('is_config_supported', ABI(c_bool,
                                    POINTER(api.plugin),
                                    POINTER(ambisonic_config))),
        ('get_config', ABI(c_bool,
                           POINTER(api.plugin),
                           c_uint32,
                           POINTER(ambisonic_config))),
    ]

class host_ambisonic(Structure):
    _fields_ = [
        ('changed', ABI(None, POINTER(api.host))),
    ]

