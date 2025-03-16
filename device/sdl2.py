import ctypes
import numpy
import sdl2

class SDL2AudioDevice:
    def __init__(self, system, audio_buffer, sample_rate):
        self.system = system
        self.audio_buffer = audio_buffer
        self.c_callback = sdl2.SDL_AudioCallback(self._callback)
        wanted = sdl2.SDL_AudioSpec(sample_rate, sdl2.AUDIO_F32, len(audio_buffer.channels), audio_buffer.frames_count)
        wanted.callback = self.c_callback
        wanted.userdata = None
        self.channels = [numpy.ctypeslib.as_array(channel)
                         for channel in audio_buffer.channels]
        self.audio = sdl2.SDL_OpenAudio(ctypes.byref(wanted), None)
        sdl2.SDL_PauseAudio(0)

    def lock(self):
        sdl2.SDL_LockAudio()

    def unlock(self):
        sdl2.SDL_UnlockAudio()

    def _callback(self, _, stream, length):
        self.system.audio_callback()
        data = numpy.dstack(self.channels).flatten()
        ctypes.memmove(stream, data.ctypes.data, min(len(data)*4, length))

    def close(self):
        sdl2.SDL_PauseAudio(1)

Device = SDL2AudioDevice
