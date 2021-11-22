import sounddevice as sd
import wavio as wv
from numpy.fft import fft, ifft
import numpy
import soundfile
from matplotlib import pylab

'''Fs = 44100
dureeEnregistrement = 3

# Création d'un objet enregistrement
# Démarrage de l'enregistrement
print('Démarrage enregistrement')
recording = sd.rec(int(dureeEnregistrement * Fs), samplerate=Fs, channels=1)
sd.wait()
print('Fin enregistrement')

# Lecture des données captées
# print(recording)
sd.default.samplerate = 44100
# sd.play(recording) #entendre l'enregistrement
wv.write("test.wav", recording, Fs, sampwidth=3)

audio_samples, sample_rate = soundfile.read("test.wav", dtype="int16")
number_samples = len(audio_samples)
duration = round(number_samples / sample_rate, 2)
freq_bins = numpy.arange(number_samples // 2) * sample_rate / number_samples

fft_data = fft(audio_samples)
print(fft_data)

pylab.plot(freq_bins, fft_data, colo="blue")'''

Fs = 44100 ;
dureeEnregistrement = 3;

# Création d'un objet enregistrement


# Démarrage de l'enregistrement
print('Démarrage enregistrement');
recording = sd.rec(int(dureeEnregistrement * Fs), samplerate=Fs, channels=1)
sd.wait()
print('Fin enregistrement');

# Lecture des données captées
# sonDonnees = getaudiodata(sonEnregistre);
# [valeurMax,indexMax] = max(abs(fft(sonDonnees-mean(sonDonnees))));
wv.write("test.wav", recording, Fs, sampwidth=3)

audio_samples, sample_rate = soundfile.read("test.wav", dtype="int16")

# Calcul de la fréquence
#sonFrequence = (indexMax * Fs) / len([i for i in range(0, dureeEnregistrement, 1/Fs)]);
# print('frequence : %f\n', sonFrequence)

# Affichage du signal sur un graphe
# plot(sonDonnees);
print("Audio sample : ")
print(audio_samples)
print("Sample rate : ", sample_rate)
