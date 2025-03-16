import platform
import ctypes
from ctypes import c_void_p, Structure, POINTER, CFUNCTYPE
from ctypes import c_bool, c_char_p, c_void_p
from ctypes import c_uint8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64
from ctypes import c_float, c_double

NAME_SIZE = 256
PATH_SIZE = 1024

id = c_uint32

INVALID_ID = 0xFFFFFFFF

BEATTIME_FACTOR = 1 << 31
SECTIME_FACTOR = 1 << 31

beattime = c_int64
sectime = c_int64

match platform.system():
    case 'Linux':
        search_paths = [
            "~/.clap",
            "/usr/lib/clap",
        ]
    case 'Windows':
        search_paths = [
            "%COMMONPROGRAMFILES%\\CLAP",
            "%LOCALAPPDATA%\\Programs\\Common\\CLAP"
        ]
    case 'Mac':
        search_paths = [
            "/Library/Audio/Plug-Ins/CLAP",
			"~/Library/Audio/Plug-Ins/CLAP",
        ]

ABI = CFUNCTYPE

class version(Structure):
    _fields_ = [
        ('major', c_uint32),
        ('minor', c_uint32),
        ('revision', c_uint32),
    ]

VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_REVISION = 6

class plugin_entry(Structure):
    _fields_ = [
        ('clap_version', version),
        ('init', ABI(c_bool, c_char_p)),
        ('deinit', ABI(None)),
        ('get_factory', ABI(c_void_p, c_char_p)),
    ]

PLUGIN_FACTORY_ID = b"clap.plugin-factory"

class plugin(Structure):
    pass

class plugin_descriptor(Structure):
    pass

class plugin_factory(Structure):
    pass

class host(Structure):
    pass

plugin_factory._fields_ = [
        ('get_plugin_count', ABI(c_uint32, POINTER(plugin_factory))),
        ('get_plugin_descriptor', ABI(POINTER(plugin_descriptor),
                                      POINTER(plugin_factory),
                                      c_uint32)),
        ('create_plugin', ABI(POINTER(plugin),
                              POINTER(plugin_factory),
                              POINTER(host),
                              c_char_p)),              # plugin_id
    ]

timestamp = c_uint64
TIMESTAMP_UNKNOWN = 0

class universal_plugin_id(Structure):
    _fields_ = [
        ('abi', c_char_p),
        ('id', c_char_p),
    ]

PRESET_DISCOVERY_FACTORY_ID = b"clap.preset-discovery-factory/2"

PRESET_DISCOVERY_LOCATION_FILE = 0
PRESET_DISCOVERY_LOCATION_PLUGIN = 1

PRESET_DISCOVERY_IS_FACTORY_CONTENT = 1 << 0
PRESET_DISCOVERY_IS_USER_CONTENT = 1 << 1
PRESET_DISCOVERY_IS_DEMO_CONTENT = 1 << 2
PRESET_DISCOVERY_IS_FAVORITE = 1 << 3

class preset_discovery_metadata_receiver(Structure):
    pass

preset_discovery_metadata_receiver._fields_ = [
        ('receiver_data', c_void_p),
        ('on_error', ABI(None,
                         POINTER(preset_discovery_metadata_receiver),
                         c_int32,
                         c_char_p)),
        ('begin_preset', ABI(c_bool,
                             POINTER(preset_discovery_metadata_receiver),
                             c_char_p,
                             c_char_p)),
        ('add_plugin_id', ABI(None,
                              POINTER(preset_discovery_metadata_receiver),
                              POINTER(universal_plugin_id))),
        ('set_soundpack_id', ABI(None,
                                 POINTER(preset_discovery_metadata_receiver),
                                 c_char_p)),
        ('set_flags', ABI(None,
                          POINTER(preset_discovery_metadata_receiver),
                          c_uint32)),
        ('add_creator', ABI(None,
                            POINTER(preset_discovery_metadata_receiver),
                            c_char_p)),
        ('set_description', ABI(None,
                                POINTER(preset_discovery_metadata_receiver),
                                c_char_p)),
        ('set_timestamps', ABI(None,
                               POINTER(preset_discovery_metadata_receiver),
                               timestamp,
                               timestamp)),
        ('add_feature', ABI(None,
                            POINTER(preset_discovery_metadata_receiver),
                            c_char_p)),
        ('add_extra_info', ABI(c_bool,
                               POINTER(preset_discovery_metadata_receiver),
                               c_char_p,
                               c_char_p)),
    ]

class preset_discovery_filetype(Structure):
    _fields_ = [
        ('name', c_char_p),
        ('description', c_char_p),
        ('file_extension', c_char_p),
    ]

class preset_discovery_location(Structure):
    _fields_ = [
        ('flags', c_uint32),
        ('name', c_char_p),
        ('kind', c_uint32),
        ('location', c_char_p),
    ]

class preset_discovery_soundpack(Structure):
    _fields_ = [
        ('flags', c_uint32),
        ('id', c_char_p),
        ('name', c_char_p),
        ('description', c_char_p),
        ('homepage_url', c_char_p),
        ('vendor', c_char_p),
        ('image_path', c_char_p),
        ('release_timestamp', timestamp),
    ]

class preset_discovery_provider_descriptor(Structure):
    _fields_ = [
        ('clap_version', version),
        ('id', c_char_p),
        ('name', c_char_p),
        ('vendor', c_char_p),
    ]

class preset_discovery_provider(Structure):
    pass

preset_discovery_provider._fields_ = [
    ('desc', POINTER(preset_discovery_provider_descriptor)),
    ('provider_data', c_void_p),
    ('init', ABI(c_bool, POINTER(preset_discovery_provider))),
    ('destroy', ABI(None, POINTER(preset_discovery_provider))),
    ('get_metadata', ABI(c_bool,
                         POINTER(preset_discovery_provider),
                         c_uint32,
                         c_char_p,
                         POINTER(preset_discovery_metadata_receiver))),
    ('get_extension', ABI(c_void_p,
                          POINTER(preset_discovery_provider),
                          c_char_p)),
]

class preset_discovery_indexer(Structure):
    pass

preset_discovery_indexer._fields_ = [
    ('clap_version', version),
    ('name', c_char_p),
    ('vendor', c_char_p),
    ('url', c_char_p),
    ('version', c_char_p),
    ('indexer_data', c_void_p),
    ('declare_filetype', ABI(c_bool,
                             POINTER(preset_discovery_indexer),
                             POINTER(preset_discovery_filetype))),
    ('declare_location', ABI(c_bool,
                             POINTER(preset_discovery_indexer),
                             POINTER(preset_discovery_location))),
    ('declare_soundpack', ABI(c_bool,
                             POINTER(preset_discovery_soundpack),
                             POINTER(preset_discovery_location))),
    ('get_extension', ABI(c_void_p,
                          POINTER(preset_discovery_indexer),
                          c_char_p)),
]

class preset_discovery_factory(Structure):
    pass

preset_discovery_factory._fields_ = [
    ('count', ABI(c_uint32, POINTER(preset_discovery_factory))),
    ('get_descriptor', ABI(POINTER(preset_discovery_provider_descriptor),
                           POINTER(preset_discovery_factory),
                           c_uint32)),
    ('create', ABI(POINTER(preset_discovery_provider),
                           POINTER(preset_discovery_factory),
                           POINTER(preset_discovery_indexer),
                           c_char_p)),
]


class event_header(Structure):
    _fields_ = [
        ('size', c_uint32),
        ('time', c_uint32),
        ('space_id', c_uint32),
        ('type', c_uint32),
        ('flags', c_uint32),
    ]

CORE_EVENT_SPACE_ID = 0
EVENT_IS_LIVE = 1 << 0
EVENT_DONT_RECORD = 1 << 1

EVENT_NOTE_ON = 0
EVENT_NOTE_OFF = 1
EVENT_NOTE_CHOKE = 2
EVENT_NOTE_END = 3

EVENT_NOTE_EXPRESSION = 4

EVENT_PARAM_VALUE = 5
EVENT_PARAM_MOD = 6

EVENT_PARAM_GESTURE_BEGIN = 7
EVENT_PARAM_GESTURE_END = 8

EVENT_TRANSPORT = 9

EVENT_MIDI = 10
EVENT_MIDI_SYSEX = 11
EVENT_MIDI2 = 12

class event_note(Structure):
    _fields_ = [
        ('header', event_header),
        ('note_id', c_int32),
        ('port_index', c_int16),
        ('channel', c_int16),
        ('key', c_int16),
        ('velocity', c_double),
    ]

NOTE_EXPRESSION_VOLUME = 0
NOTE_EXPRESSION_PAN = 1
NOTE_EXPRESSION_TUNING = 2
NOTE_EXPRESSION_VIBRATO = 3
NOTE_EXPRESSION_EXPRESSION = 4
NOTE_EXPRESSION_BRIGHTNESS = 5
NOTE_EXPRESSION_PRESSURE = 6

note_expression = c_int32

class event_note_expression(Structure):
    _fields_ = [
        ('header', event_header),
        ('expression_id', note_expression),
        ('note_id', c_int32),
        ('port_index', c_int16),
        ('channel', c_int16),
        ('key', c_int16),
        ('value', c_double),
    ]

class event_param_value(Structure):
    _fields_ = [
        ('header', event_header),
        ('cookie', c_void_p),
        ('note_id', c_int32),
        ('port_index', c_int16),
        ('channel', c_int16),
        ('key', c_int16),
        ('value', c_double),
    ]

class event_param_mod(Structure):
    _fields_ = [
        ('header', event_header),
        ('param_id', id),
        ('cookie', c_void_p),
        ('note_id', c_int32),
        ('port_index', c_int16),
        ('channel', c_int16),
        ('key', c_int16),
        ('amount', c_double),
    ]

class event_param_gesture(Structure):
    _fields_ = [
        ('header', event_header),
        ('param_id', id),
    ]

transport_flags = c_uint32

TRANSPORT_HAS_TEMPO = 1 << 0
TRANSPORT_HAS_BEATS_TIMELINE = 1 << 1
TRANSPORT_HAS_SECONDS_TIMELINE = 1 << 2
TRANSPORT_HAS_TIME_SIGNATURE = 1 << 3
TRANSPORT_IS_PLAYING = 1 << 4
TRANSPORT_IS_RECORDING = 1 << 5
TRANSPORT_IS_LOOP_ACTIVE = 1 << 6
TRANSPORT_IS_WITHIN_PRE_ROLL = 1 << 7

class event_transport(Structure):
    _fields_ = [
        ('header', event_header),
        ('flags', transport_flags),
        ('song_pos_beats', beattime),
        ('song_pos_seconds', sectime),
        ('tempo', c_double),
        ('tempo_inc', c_double),
        ('loop_start_beats', beattime),
        ('loop_end_beats', beattime),
        ('loop_start_seconds', sectime),
        ('loop_end_seconds', sectime),
        ('bar_start', beattime),
        ('bar_number', c_int32),
        ('tsig_num', c_uint16),
        ('tsig_denom', c_uint16),
    ]

class event_midi(Structure):
    _fields_ = [
        ('header', event_header),
        ('port_index', c_uint16),
        ('data', c_uint8*3),
    ]

class event_midi_sysex(Structure):
    _fields_ = [
        ('header', event_header),
        ('buffer', POINTER(c_uint8)),
        ('size', c_uint32),
    ]

class event_midi2(Structure):
    _fields_ = [
        ('header', event_header),
        ('port_index', c_uint16),
        ('data', c_uint8*4),
    ]

class input_events(Structure):
    pass

input_events._fields_ = [
    ('ctx', c_void_p),
    ('size', ABI(c_uint32, POINTER(input_events))),
    ('get', ABI(c_void_p, POINTER(input_events), c_uint32)),
] 

class output_events(Structure):
    pass

output_events._fields_ = [
    ('ctx', c_void_p),
    ('try_push', ABI(c_bool, POINTER(output_events), POINTER(event_header))),
] 

# Sample code for reading a stereo buffer:
#
# bool isLeftConstant = (buffer->constant_mask & (1 << 0)) != 0;
# bool isRightConstant = (buffer->constant_mask & (1 << 1)) != 0;
#
# for (int i = 0; i < N; ++i) {
#    float l = data32[0][isLeftConstant ? 0 : i];
#    float r = data32[1][isRightConstant ? 0 : i];
# }

class audio_buffer(Structure):
    _fields_ = [
        ('data32', POINTER(POINTER(c_float))),
        ('data64', POINTER(POINTER(c_double))),
        ('channel_count', c_uint32),
        ('latency', c_uint32),
        ('constant_mask', c_uint64),
    ]

process_status = c_int32

PROCESS_ERROR = 0
PROCESS_CONTINUE = 1
PROCESS_CONTINUE_IF_NOT_QUIET = 2
PROCESS_TAIL = 3
PROCESS_SLEEP = 4

class process(Structure):
    _fields_ = [
        ('steady_time', c_int64),
        ('frames_count', c_uint32),
        ('transport', POINTER(event_transport)),
        ('audio_inputs', POINTER(audio_buffer)),
        ('audio_outputs', POINTER(audio_buffer)),
        ('audio_inputs_count', c_uint32),
        ('audio_outputs_count', c_uint32),
        ('in_events', POINTER(input_events)),
        ('out_events', POINTER(output_events)),
    ]

plugin_descriptor._fields_ = [
    ('clap_version', version),
    ('id', c_char_p),
    ('name', c_char_p),
    ('vendor', c_char_p),
    ('url', c_char_p),
    ('manual_url', c_char_p),
    ('support_url', c_char_p),
    ('version', c_char_p),
    ('description', c_char_p),
    ('features', POINTER(c_char_p)),
]

plugin._fields_ = [
    ('desc', POINTER(plugin_descriptor)),
    ('plugin_data', c_void_p),
    ('init', ABI(c_bool, POINTER(plugin))),
    ('destroy', ABI(None, POINTER(plugin))),
    ('activate', ABI(c_bool,
                     POINTER(plugin),
                     c_double,        # sample rate
                     c_uint32,        # min_frames_count
                     c_uint32)),      # max_frames_count
    ('deactivate', ABI(None, POINTER(plugin))),
    ('start_processing', ABI(c_bool, POINTER(plugin))),
    ('stop_processing', ABI(c_bool, POINTER(plugin))),
    ('reset', ABI(c_bool, POINTER(plugin))),
    ('process', ABI(process_status, POINTER(plugin), POINTER(process))),
    ('get_extension', ABI(c_void_p, POINTER(plugin), c_char_p)),
    ('on_main_thread', ABI(None, POINTER(plugin))),
]

host._fields_ = [
    ('clap_version', version),
    ('host_data', c_void_p),
    ('name', c_char_p),
    ('vendor', c_char_p),
    ('url', c_char_p),
    ('version', c_char_p),
    ('get_extension', ABI(c_void_p, POINTER(host), c_char_p)),
    ('request_restart', ABI(None, POINTER(host))),
    ('request_process', ABI(None, POINTER(host))),
    ('request_callback', ABI(None, POINTER(host))),
]

def hook(structure, method):
    for name, ty in structure._fields_:
        if name == method:
            return ty
    raise AttributeError

def nt_iter(items):
    i = 0
    while items[i]:
        yield items[i]
        i += 1

def nt_list(items):
    return list(nt_iter(items))
