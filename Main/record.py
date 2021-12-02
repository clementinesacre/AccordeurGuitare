import sounddevice as sd
from numpy.fft import rfft
import soundfile
from numpy import argmax
import wavio as wv
import statistics
import find_note


Fs = 44100
record_time = 2


# Start recording

def getFrequencies(tune):
    print('Recording')
    recording = sd.rec(int(record_time * Fs), samplerate=Fs, channels=1)
    sd.wait()
    print('Stop recording')

    # writing in .wav file
    wv.write("../test2.wav", recording, Fs, sampwidth=3)

    # reading file .wav and retrieving its information
    audio_samples, sample_rate = soundfile.read("../test2.wav", dtype="int16")
    """
    # Compute Fourier transform of windowed signal
    windowed = audio_samples * len(audio_samples)
    f = rfft(windowed)
    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f))  # Just use this for less-accurate, naive version
    # true_i = parabolic(log(abs(f)), i)[0]
    """

    frequency = argmax(abs(rfft(audio_samples - statistics.mean(audio_samples)))) / record_time
    # print("result v1 : ", Fs * i / len(windowed))  # same value as previous "i"
    print("result v2 : ", frequency)

    dict_freq = find_note.get_target_note(frequency, tune)
    dict_freq["freqActu"] = frequency
    print("your note is : ", dict_freq)
    return dict_freq
