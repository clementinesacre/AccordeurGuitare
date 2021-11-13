clear all;
close all;
clc;

test_note = 888

% fontion se base sur la fréquence donné en paramètre pour trouver la note la 
% plus proche et la fréquence correcte la plus proche
function [closest_note, closest_pitch] = get_closest_note(instrument_pitch)
  % note de référence (la de la 4e octave)
  A4_pitch = 440;
  
  % noms de toutes les notes
  string_notes = [
    "A"; "A#"; "B "; "C "; "C#"; "D "; "D#"; "E "; "F "; "F#"; "G "; "G#"
   ];
   
  % index de la fréquence par rapport à toutes les notes de toutes les gammes
  pitch_index = round(log2(instrument_pitch / A4_pitch) * 12);
   
  % n° de gamme
  octave_number = int2str(4 + fix((i + 9) / 12));

  % récupération du nom de la note à partir de l'index
  simple_note = string_notes(mod(pitch_index, 12) + 1);

  % liasont de la note et du n° de gamme
  closest_note = strcat(simple_note, octave_number);
  
  % récupération de la fréquence la plus proche de la fréquence d'entrée
  closest_pitch = A4_pitch * power(2, (pitch_index / 12)); 
endfunction

[closest_note, closest_pitch] = get_closest_note(test_note);
