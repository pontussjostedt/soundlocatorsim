from simpy import *
from soundfromwav import SoundFromWav
from vector3 import Vector3
from cyclicbuffer import CyclicBuffer
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
class BufferedMicrophone:
    def __init__(self, sample_rate: int, pos: Vector3, buffer: CyclicBuffer, sound_sources: list[SoundFromWav], env: Environment, name: str = "Unamed Microphone", extra_info = None) -> None:
        self.sound_sources = sound_sources
        self.pos = pos
        self.env = env
        self._buffer = buffer
        self.env.process(self.run())
        self.sample_rate = sample_rate
        self.name = name
        self.extra_info = extra_info
        self.all_data = []

    def run(self):
        while True:
            new_value = sum([sound_source.get_sound(self.env.now, self.pos) for sound_source in self.sound_sources])
            self._buffer.offer(new_value)
            self.all_data.append(new_value)
            if self.extra_info:
                self.extra_info(self)
            yield self.env.timeout(1 / self.sample_rate)

    def get_buffer(self) -> list[int]:
        return [x for x in self._buffer]
    

    def to_wav(self, path: str):
        wavfile.write(path, self.sample_rate, np.array(self.all_data, dtype=np.int16))