import matplotlib.pyplot as plt

from bufferedmicrophone import BufferedMicrophone
import numpy as np


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