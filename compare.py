import matplotlib.pyplot as plt

from bufferedmicrophone import BufferedMicrophone
import numpy as np
from constants import SPEED_OF_SOUND
from vector3 import Vector3
from scipy.optimize import root, least_squares
def compare_mic_audio(mics: list[BufferedMicrophone]):
    for mic in mics:
        t = np.linspace(0, len(mic.all_data) / mic.sample_rate, len(mic.all_data))
        #plt.plot(t, mic.all_data)
        plt.plot(mic.all_data)

    plt.xlabel("Time (s)")
    plt.show()


def plot_sample(data, sample_rate):
    t = np.linspace(0, len(data) / sample_rate, len(data))
    plt.plot(t, data)


def get_source_pos(ref_pos: Vector3, others_info: list[(Vector3, float)]):
    others_info.append((ref_pos, 0))
    init_guess = [0, 0, 0, 0]
    def to_optimize(vars):
        x, y, z, t = vars
        m_list = [
            (x - pos.x)**2 + (y - pos.y)**2 + (z - pos.z)**2 - (SPEED_OF_SOUND * (deltatime + t))**2
            for (pos, deltatime) in others_info
        ]
        return m_list
    
    result = root(to_optimize, init_guess)

    if result.success:
        print(f"Source position: {Vector3(*result.x[:3])}")
    else:
        print(f"Failed to find source position: {result.message}")
    
    
def get_source_pos_ls(ref_pos: Vector3, others_info: list[(Vector3, float)], real_sound_source: Vector3):
    others_info.append((ref_pos, 0))
    init_guess = [0, 0, 0, 0]
    def to_optimize(vars):
        x, y, z, t = vars
        m_list = [
            (x - pos.x)**2 + (y - pos.y)**2 + (z - pos.z)**2 - (SPEED_OF_SOUND * (deltatime + t))**2
            for (pos, deltatime) in others_info
        ]
        return m_list
    
    result = least_squares(to_optimize, init_guess, max_nfev=100000, method="trf")

    if result.success:
        print(f"Source position: {Vector3(*result.x[:3])}")
        print(f"Distance to real source: {Vector3(*result.x[:3]).dist(real_sound_source)}")
    else:
        print(f"Failed to find source position: {result.message}")
    
