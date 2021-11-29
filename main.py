import sounddevice as sd
from numpy.fft import rfft
import soundfile
from numpy import argmax
import wavio as wv
import statistics
import find_note

Fs = 44100
dureeEnregistrement = 2


# Lancement de l'enregistrement

def getFrenquencies():
    print('Démarrage enregistrement')
    recording = sd.rec(int(dureeEnregistrement * Fs), samplerate=Fs, channels=1)
    sd.wait()
    print('Fin enregistrement')

    # Ecriture du son dans un fichier wav
    wv.write("test2.wav", recording, Fs, sampwidth=3)

    # Lecture du fichier wav et récupération de ses informations
    audio_samples, sample_rate = soundfile.read("test2.wav", dtype="int16")

    # Compute Fourier transform of windowed signal
    windowed = audio_samples * len(audio_samples)
    f = rfft(windowed)
    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f))  # Just use this for less-accurate, naive version
    # true_i = parabolic(log(abs(f)), i)[0]

    frequency = argmax(abs(rfft(audio_samples - statistics.mean(audio_samples)))) / dureeEnregistrement
    #print("reponse v1 : ", Fs * i / len(windowed))  # même valeur que le i au dessus
    print("reponse v2 : ", frequency)

    print("Votre note est : ", find_note.get_target_note(frequency))
    dico = find_note.get_target_note(frequency)
    dico["freqActu"] = frequency
    return dico
