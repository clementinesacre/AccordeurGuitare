clear all;
close all;
clc;

% instrument_pitch = 888;

function [closest_note, closest_pitch] = get_closest_note(instrument_pitch)
  A4_pitch = 440;
  string_notes = [
    "A"; "A#"; "B "; "C "; "C#"; "D "; "D#"; "E "; "F "; "F#"; "G "; "G#"
   ];
  pitch_index = round(log2(instrument_pitch / A4_pitch) * 12);
   
  octave_number = int2str(4 + fix((i + 9) / 12));

  simple_note = string_notes(mod(pitch_index, 12) + 1);

  closest_note = strcat(simple_note, octave_number);
  closest_pitch = A4_pitch * power(2, (pitch_index / 12)); 
  closest_note;
  closest_pitch;
endfunction

[closest_note, closest_pitch] = get_closest_note(888);
closest_note