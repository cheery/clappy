from api import ABI
import api
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double
from ctypes import c_ulong

EXT_AUDIO_PORTS = b"clap.audio-ports"

AUDIO_PORT_IS_MAIN = 1 << 0
AUDIO_PORT_SUPPORTS_64BITS = 1 << 1
AUDIO_PORT_PREFERS_64BITS = 1 << 2
AUDIO_PORT_REQUIRES_COMMON_SAMPLE_SIZE = 1 << 3

class audio_port_info(Structure):
    _fields_ = [
        ('id', api.id),
        ('name', c_char*api.NAME_SIZE),
        ('flags', c_uint32),
        ('channel_count', c_uint32),
        ('port_type', c_char_p),
        ('in_place_pair', api.id),
    ]

class plugin_audio_ports(Structure):
    _fields_ = [
        ('count', ABI(c_uint32, POINTER(api.plugin), c_bool)),
        ('get', ABI(c_bool,
                    POINTER(api.plugin),
                    c_uint32,
                    c_bool,
                    POINTER(audio_port_info))),
    ]

AUDIO_PORTS_RESCAN_NAMES = 1 << 0
AUDIO_PORTS_RESCAN_FLAGS = 1 << 1
AUDIO_PORTS_RESCAN_CHANNEL_COUNT = 1 << 2
AUDIO_PORTS_RESCAN_PORT_TYPE = 1 << 3
AUDIO_PORTS_RESCAN_IN_PLACE_PAIR = 1 << 4
AUDIO_PORTS_RESCAN_LIST = 1 << 5

class host_audio_ports(Structure):
    _fields_ = [
        ('is_rescan_flag_supported', ABI(c_bool, POINTER(api.host), c_uint32)),
        ('rescan', ABI(None, POINTER(api.host), c_uint32)),
    ]

