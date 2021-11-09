Fs = 44100 ;
dureeEnregistrement = 3;

%Création d'un objet enregistrement
sonEnregistre = audiorecorder(Fs,24,1,1);

%Démarrage de l'enregistrement
fprintf('Démarrage enregistrement');
recordblocking(sonEnregistre, dureeEnregistrement)
fprintf('Fin enregistrement');

%Lecture des données captées
sonDonnees = getaudiodata(sonEnregistre);
[valeurMax,indexMax] = max(abs(fft(sonDonnees-mean(sonDonnees))));

%Calcul de la fréquence
sonFrequence = (indexMax * Fs) / length(0:1/Fs:dureeEnregistrement);
fprintf('frequence : %f\n', sonFrequence)

%Affichage du signal sur un graphe
plot(sonDonnees);
