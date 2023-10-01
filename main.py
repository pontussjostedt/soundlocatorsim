from simpy import *
from scipy.io import wavfile
from soundfromwav import *
from bufferedmicrophone import *
from constants import *
from compare import *
from utils import *

ready = True

def plot_in_time(env: Environment, time: float, trigger_mic: BufferedMicrophone, sample_delay: int):
    yield env.timeout(time)
    ref_dist_to_source = trigger_mic.pos.dist(env.sound_source_pos)
    ref_mic = trigger_mic
    ref_mic_buffer = ref_mic.get_buffer()
    trigger_index = sample_delay
    for mic in env.mics:
        if mic != ref_mic:
            corr_result = np.correlate(mic.get_buffer(), ref_mic_buffer, "full")
            max_x, max_y = max(enumerate(corr_result), key=lambda x: x[1])
            index_offset = (max_x - len(ref_mic_buffer) + 1)
            time_offset = index_offset / STANDARD_MICROPHONE_SAMPLE_RATE
            print(f"Microphone: {mic.name} got offset: {time_offset} seconds; should be: {(mic.pos.dist(env.sound_source_pos) - ref_dist_to_source) / SPEED_OF_SOUND} seconds")
            #plt.scatter([max_x], [max_y], color="red")
            #plt.plot(corr_result)
            plt.plot(shift_padd(mic.get_buffer(), -index_offset))
    plt.plot(ref_mic_buffer, label="ref mic")
    plt.title("Buffer sound shifted to ref mic")
    plt.legend()
    print(index_offset)
    plt.show()


    plt.scatter([trigger_index], [ref_mic_buffer[trigger_index]], color="red")
    for mic in env.mics:
        plt.plot(mic.get_buffer())
    plt.show()

class MicTrigger:
    def __init__(self, trig_threshold: float, trigger_sample_delay: int) -> None:
        self.ready = True
        self.trig_threshold = trig_threshold
        self.trigger_sample_delay = trigger_sample_delay

    def __call__(self, mic: BufferedMicrophone):
        if self.ready and mic._buffer.last() > self.trig_threshold:
            mic.env.process(plot_in_time(mic.env, self.trigger_sample_delay/STANDARD_MICROPHONE_SAMPLE_RATE, mic, self.trigger_sample_delay))
            self.ready = False

if __name__ == "__main__":
    env: Environment = Environment()
    #Fs, data = wavfile.read("testsounds/abruptsound.wav")
    #play_audio(Fs, data)

    sound_source = from_wav_file("testsounds/clap.wav", Vector3(50, 0, 0))
    env.sound_source_pos = sound_source.pos

    microphones= [
        BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(0, 0, 0), CyclicBuffer(BUFFER_SIZE), [sound_source], env, name="Origin Trigger mic", extra_info=MicTrigger(29000, BUFFER_SIZE//2)),
        BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(0, 10, 0), CyclicBuffer(BUFFER_SIZE), [sound_source], env, name="Vector3(0, 10, 0) Microphone"),
        BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(0, 0, 10), CyclicBuffer(BUFFER_SIZE), [sound_source], env, name="Vector3(0, 0, 10) Microphone"),
        BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(10, 0, 0), CyclicBuffer(BUFFER_SIZE), [sound_source], env, name="Vector3(10, 0, 0) Microphone"),
    ]
    #microphone3 = BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(0, 0, 1), CyclicBuffer(2**12), [sound_source], env)
    #microphone4 = BufferedMicrophone(STANDARD_MICROPHONE_SAMPLE_RATE, Vector3(0, 0, 0), CyclicBuffer(2**12), [sound_source], env)
    env.mics =microphones

    env.run(until=6)
    compare_mic_audio(microphones)

    new_audio = normalize(sum(map(lambda mic: np.array(mic.all_data), microphones)), -2**15, 2**15)
    wavfile.write("outsounds/echo.wav", STANDARD_MICROPHONE_SAMPLE_RATE, new_audio)
