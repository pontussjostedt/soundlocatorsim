import numpy as np
from constants import SPEED_OF_SOUND
from vector3 import Vector3
from scipy.io import wavfile
def from_wav_file(path: str, pos: Vector3) -> 'SoundFromWav':
    sample_rate, audio_data = wavfile.read(path)
    return SoundFromWav(sample_rate, audio_data, pos)
        

class SoundFromWav:
    def __init__(self, sampling_frequency: int, data: np.ndarray, pos: Vector3, travel_speed: float = SPEED_OF_SOUND) -> None:
        self.sampling_frequency = sampling_frequency
        self.data = data
        self.pos = pos
        self.travel_speed = travel_speed

    def get_sound(self, time: float, pos: Vector3) -> float:
        time_of_output: float = time + (self.pos.dist(pos) / self.travel_speed)
        index: int = int(time_of_output * self.sampling_frequency)
        return self.data[index] if index in range(len(self.data)) else 0
    





