import math


def get_closest_note(instrument_pitch):
    A4_pitch = 440
    string_notes = [
    "A", "A#", "B ", "C ", "C#", "D ", "D#", "E ", "F ", "F#", "G ", "G#"
    ]

    pitch_index = int(
        round(
            math.log(instrument_pitch / A4_pitch, 2) * 12
        )
    )

    octave_number = 4 + (pitch_index + 9) // 12

    simple_note = string_notes[pitch_index % 12]

    closest_note = simple_note + str(octave_number)

    closest_pitch = round(A4_pitch * 2 ** (pitch_index / 12), 1)

    return closest_pitch, closest_note, octave_number


if __name__ == "__main__":
    print(get_closest_note(880))
