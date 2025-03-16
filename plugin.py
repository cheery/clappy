from ctypes import CDLL, cast, POINTER, byref, c_void_p, pointer
import api
import host

class Plugin:
    def destroy(self):
        self.c[0].destroy(self.c)
        self.host.release()

    def activate(self, sample_rate, min_frames_count, max_frames_count):
        if not self.c[0].activate(self.c, sample_rate, min_frames_count, max_frames_count):
            raise Exception(f"could not activate plugin")

    def deactivate(self):
        self.c[0].deactivate(self.c)

    def start_processing(self):
        if not self.c[0].start_processing(self.c):
            raise Exception(f"could not start processing with plugin")

    def stop_processing(self):
        self.c[0].stop_processing(self.c)

    def reset(self):
        self.c[0].reset(self.c)

    def process(self, process):
        return self.c[0].process(self.c, byref(process.c))

    def get_extension(self, ext_module):
        ext = self.c[0].get_extension(self.c, ext_module.ID)
        ext = cast(ext, POINTER(ext_module.plugin_structure))
        if not ext:
            raise Exception(f"could not get extension {repr(ext_module.ID.decode('utf-8'))}")
        return ext_module.PluginExtension(self.c, ext)

    def on_main_thread(self):
        self.c[0].on_main_thread(self.c)
