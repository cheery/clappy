from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p, c_int
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_POSIX_FD_SUPPORT = b"clap.posix-fd-support"

posix_fd_flags = c_int32

POSIX_FD_READ = 1 << 0
POSIX_FD_WRITE = 1 << 1
POSIX_FD_ERROR = 1 << 2

class plugin_posix_fd_support(Structure):
    _fields_ = [
        ('on_fd', ABI(None, POINTER(api.plugin), c_int, posix_fd_flags)),
    ]

class host_posix_fd_support(Structure):
    _fields_ = [
        ('register_fd', ABI(c_bool, POINTER(api.host), c_int, posix_fd_flags)),
        ('modify_fd', ABI(c_bool, POINTER(api.host), c_int, posix_fd_flags)),
        ('unregister_fd', ABI(c_bool, POINTER(api.host), c_int)),
    ]

