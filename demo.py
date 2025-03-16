from ctypes import CDLL, cast, POINTER, byref, c_void_p, pointer, sizeof
import api
import entry
import factory.plugin
import host
import ext.thread_check
import ext.log
import ext.gui
import ext.timer_support
import ext.audio_ports
import threading
import time
import Xlib.display
from Xlib import X, Xutil

display = Xlib.display.Display()

# Application window (only one)
class Window(object):
    def __init__(self, system, display, width, height):
        self.system = system
        self.d = display
        self.objects = []

        # Find which screen to open the window on
        self.screen = self.d.screen()

        self.window = self.screen.root.create_window(
            50, 50, width, height, 2,
            self.screen.root_depth,
            X.InputOutput,
            X.CopyFromParent,
            event_mask = (X.ExposureMask |
                          X.StructureNotifyMask |
                          X.ButtonPressMask |
                          X.ButtonReleaseMask |
                          X.Button1MotionMask),
            colormap = X.CopyFromParent,
            )

        self.gc = self.window.create_gc(
            foreground = self.screen.black_pixel,
            background = self.screen.white_pixel,
            )

        # Set some WM info

        self.WM_DELETE_WINDOW = self.d.intern_atom('WM_DELETE_WINDOW')
        self.WM_PROTOCOLS = self.d.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name('Xlib example: draw.py')
        self.window.set_wm_icon_name('draw.py')
        self.window.set_wm_class('draw', 'XlibExample')

        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])
        self.window.set_wm_hints(flags = Xutil.StateHint,
                                 initial_state = Xutil.NormalState)

        self.window.set_wm_normal_hints(flags = (Xutil.PPosition | Xutil.PSize
                                                 | Xutil.PMinSize),
                                        min_width = 20,
                                        min_height = 20)

        # Map the window, making it visible
        self.window.map()

    def loop(self):
        while self.system.running:
            # plugin[0].on_main_thread(plugin)
            now = time.time()
            for timer_id in self.system.timers:
                freqms, last, plugin = self.system.timers[timer_id]
                if (now - last) * 1000 >= freqms:
                    plugin.timer_support.on_timer(timer_id)
                    self.system.timers[timer_id] = freqms, now, plugin

            if self.d.pending_events():
                e = self.d.next_event()
                
                # Window has been destroyed, quit
                if e.type == X.DestroyNotify:
                    self.system.running = False
                    return
                
                # Button released, add or subtract
                elif e.type == X.ButtonRelease:
                    pass
                
                # Somebody wants to tell us something
                elif e.type == X.ClientMessage:
                    if e.client_type == self.WM_PROTOCOLS:
                        fmt, data = e.data
                        if fmt == 32 and data[0] == self.WM_DELETE_WINDOW:
                            self.system.running = False
                            return
            else:
                time.sleep(0.010)


main_thread_id = threading.get_ident()

class System:
    def __init__(self):
        self.running = False
        self.timers = {}
        self.next_timer_id = 1

class MyHost(host.Host):
    name = b"clappy"
    vendor = b"cheery"
    url = None
    version = b"0.0.0"
    def __init__(self, plugin, system):
        super().__init__(plugin)
        self.system = system

    def request_restart(self):
        print("restart requested")

    def request_process(self):
        print("process requested")

    def request_callback(self):
        print("callback requested")

    @host.hook(ext.thread_check, 'is_main_thread')
    def is_main_thread(self):
        return threading.get_ident() == main_thread_id

    @host.hook(ext.thread_check, 'is_audio_thread')
    def is_audio_thread(self):
        return True

    @host.hook(ext.log, 'log')
    def log(self, severity, message):
        print(f"{severity}: {message}")

    @host.hook(ext.gui, 'resize_hints_changed')
    def resize_hints_changed(self):
        pass

    @host.hook(ext.gui, 'request_resize')
    def request_resize(self, width, height):
        return False

    @host.hook(ext.gui, 'request_show')
    def request_show(self):
        return False

    @host.hook(ext.gui, 'request_hide')
    def request_hide(self):
        return False

    @host.hook(ext.gui, 'closed')
    def closed(self, was_destroyed):
        pass

    @host.hook(ext.timer_support, 'register_timer')
    def register_timer(self, freqms, c_timer_id):
        c_timer_id[0] = tid = self.system.next_timer_id
        self.system.timers[tid] = freqms, time.time(), self.plugin
        self.system.next_timer_id += 1
        return True

    @host.hook(ext.timer_support, 'unregister_timer')
    def unregister_timer(self, timer_id):
        if timer_id in self.system.timers:
            self.system.timers.pop(timer_id)
            return True
        return False

    @host.hook(ext.audio_ports, 'is_rescan_flag_supported')
    def is_rescan_flag_supported(self, flags):
        return False

    @host.hook(ext.audio_ports, 'rescan')
    def rescan(self, flags):
        pass

system = System()

dexed = False

if dexed:
    e = entry.load('/home/cheery/.clap/Dexed.clap')
    plugin_id = b'com.digital-suburban.dexed'
else:
    e = entry.load('/home/cheery/.clap/Surge XT.clap')
    plugin_id = b'org.surge-synth-team.surge-xt'
e.pf = e.get_factory(factory.plugin)
for desc in e.pf:
    print(desc)
plugin = e.pf.create(MyHost, plugin_id, system)
plugin.gui = plugin.get_extension(ext.gui)
plugin.timer_support = plugin.get_extension(ext.timer_support)
plugin.audio_ports = plugin.get_extension(ext.audio_ports)

frames_count = 1024

class AudioBuffer:
    def __init__(self, channel_count, frames_count):
        self.channels = []
        for i in range(channel_count):
            self.channels.append((api.c_float*frames_count)())
        self.c_array = (POINTER(api.c_float)*2)(*self.channels)
        self.c = api.audio_buffer(self.c_array, None, channel_count, 0, 0)

input_buffers = []
output_buffers = []
for port in plugin.audio_ports.inputs:
    print(port)
    input_buffers.append(
        AudioBuffer(port['channel_count'], frames_count))

for port in plugin.audio_ports.outputs:
    print(port)
    output_buffers.append(
        AudioBuffer(port['channel_count'], frames_count))

# TODO: convert into list/queue/array handler.
evt1 = api.event_note(
    api.event_header(
        sizeof(api.event_note),
        0,
        0,
        api.EVENT_NOTE_ON,
        api.EVENT_IS_LIVE
    ),
    -1, -1, -1, 69, 1.0)

@api.hook(api.input_events, 'size')
def size_hook(_):
    return 1

@api.hook(api.input_events, 'get')
def get_hook(_, index):
    if index == 0:
        return cast(pointer(evt1), c_void_p).value
    return None

blank_events = api.input_events(None, size_hook, get_hook)

## TODO: Make an event pusher
@api.hook(api.output_events, 'try_push')
def try_push_hook(_, event):
    #print('pssh', event[0].type)
    return True

push_push_events = api.output_events(None, try_push_hook)

plugin.activate(44100.0, frames_count, frames_count)

class Process:
    def __init__(self, c):
        self.c = c

def audio_loop():
    plugin.start_processing()

    c_inputs = (api.audio_buffer*len(input_buffers))(
        *(b.c for b in input_buffers))
    c_outputs = (api.audio_buffer*len(output_buffers))(
        *(b.c for b in output_buffers))
    process = api.process(
        steady_time = -1,
        frames_count = frames_count,
        transport = None,
        audio_inputs = c_inputs,
        audio_inputs_count = len(input_buffers),
        audio_outputs = c_outputs,
        audio_outputs_count = len(output_buffers),
        in_events = pointer(blank_events),
        out_events = pointer(push_push_events),
    )
    process = Process(process)
    while system.running:
        resp = plugin.process(process)
        if resp != api.PROCESS_CONTINUE:
            system.running = False
            print('bad response:', resp)
        else:
            time.sleep(0.010)
    plugin.stop_processing()

system.running = True
audio = threading.Thread(target=audio_loop)
audio.start()

assert plugin.gui.is_api_supported(b'x11', False)
plugin.gui.create(b'x11', False)
plugin.gui.set_scale(1.1)
gui_width, gui_height = plugin.gui.get_size()
window = Window(system, display, gui_width, gui_height)

plugin.gui.set_parent((b'x11', window.window.id))

window.loop()

plugin.gui.destroy()

print(plugin.host.requested_extensions - set(plugin.host.available_extensions))
audio.join()

plugin.deactivate()
plugin.destroy()
e.deinit()
