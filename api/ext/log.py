from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_LOG = b"clap.log"

LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARNING = 2
LOG_ERROR = 3
LOG_FATAL = 4

LOG_HOST_MISBEHAVING = 5
LOG_PLUGIN_MISBEHAVING = 6

log_severity = c_int32

class host_log(Structure):
    _fields_ = [
        ('log', ABI(None, POINTER(api.host), log_severity, c_char_p)),
    ]

