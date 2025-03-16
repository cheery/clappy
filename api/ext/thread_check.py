from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_THREAD_CHECK = b"clap.thread-check"

class host_thread_check(Structure):
    _fields_ = [
        ('is_main_thread', ABI(c_bool, POINTER(api.host))),
        ('is_audio_thread', ABI(c_bool, POINTER(api.host))),
    ]

