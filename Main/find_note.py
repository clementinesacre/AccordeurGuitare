import math
import accords_guitare

# reference pitch
A4_pitch = 440
# names of the different notes
string_notes = [
    "A", "A#", "B ", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"
]


# return the closest correct note for a given frequency (given as an argument)
def get_closest_note(instrument_pitch):
    # get the octave number
    octave_number = get_octave_number(instrument_pitch)
    # get the pitch index of the closest correct note
    pitch_index = get_pitch_index(instrument_pitch)
    simple_note = string_notes[pitch_index % 12]

    # create the closest not in string format
    closest_note = simple_note + octave_number

    # calculate the closest note frequency from the pitch_index
    closest_pitch = round(A4_pitch * 2 ** (pitch_index / 12), 2)

    return closest_note, closest_pitch


def get_target_note(instrument_pitch, tune="standard"):
    """
    Function searches the closest matching frequency from a given guitar tune and a 
    given input frequency.
    It then returns that frequency and the given guitar tune's frequency and string 
    representations of notes.
    """
    # comparison function
    absolute_difference_function = lambda list_value: abs(list_value - instrument_pitch)

    # searching the closest matching value to the input frequency
    target_frequency = min(find_tuning_frequencies(tune), key=absolute_difference_function)

    # index of the target note relative the reference pitch (A4)
    target_pitch_index = get_pitch_index(target_frequency)

    target_note = string_notes[target_pitch_index % 12]
    target_octave = 4 + (target_pitch_index + 9) // 12
    string_target_note = target_note + str(target_octave)
    tune_frequencies = guitar_tune_frequencies(tune)
    higher_lower = get_higher_lower(target_frequency, tune, tune_frequencies)

    return {
        "lower_note": higher_lower[0],
        "higher_note": higher_lower[1],
        "target_note_string": string_target_note,
        "target_octave": target_octave,
        "target_frequency": target_frequency,
        "guitar_tune_frequencies": tune_frequencies
    }


def find_tuning_frequencies(tune="standard"):
    """
    Function finds the frequencies of all the notes of a same tuning set.
    It does so with help from the tone difference relative to the standard tuning.
    """
    guitar_tuning_pitches = []

    # For each note of the tuning set, calculate (from the tone difference relative to
    # the standard tuning set) the frequency difference with the standard tunings set's 
    # frequencies.
    # Then subtract that difference from the standard tune's frequency in order
    # to obtain the frequency of the searched tuning set's note
    for i in range(6):
        guitar_tuning_pitches.append(
            round(
                accords_guitare.guitar_tunings["standard_indexes"][i] * 2 ** (
                        accords_guitare.guitar_tunings[tune][i][1] / 12), 2
            )
        )

    return guitar_tuning_pitches


def guitar_tune_frequencies(tune="standard"):
    """
    Function returns a list with a given tuning set's string notes and frequencies
    """
    # get a copy of the searched tuning set
    tune_frequencies = accords_guitare.guitar_tunings[tune][:]
    # get the frequencies of that tuning set
    guitar_tuning_pitches = find_tuning_frequencies(tune)

    # replace the tone difference with the actual frequency
    for i in range(6):
        tune_frequencies[i] = (
            tune_frequencies[i][0] + get_octave_number(guitar_tuning_pitches[i]),
            guitar_tuning_pitches[i]
        )

    return tune_frequencies


# returns the octave number of a given frequency
def get_octave_number(frequency):
    # returns the octave number of the pitch index relative to the reference pitch (A4)
    return str(4 + (get_pitch_index(frequency) + 9) // 12)


def get_pitch_index(frequency):
    """
    Function returns the pitch index relative to the reference pitch (A4)
    of the note that is closest to matching the given frequency.
    """
    return int(
        round(
            math.log(frequency / A4_pitch, 2) * 12
        )
    )


def get_higher_lower(frequency, tune, guitar_tune_frequencies):
    """
    Function returns the higher and lower text note of a frequency it got as
    argument
    """
    guitar_tuning_pitches = find_tuning_frequencies(tune)

    if guitar_tuning_pitches.index(frequency) == 0:
        return (
            "lowest",
            guitar_tune_frequencies[guitar_tuning_pitches.index(frequency) + 1][0]
        )
    elif guitar_tuning_pitches.index(frequency) == 5:
        return (
            guitar_tune_frequencies[guitar_tuning_pitches.index(frequency) - 1][0],
            "highest"
        )
    else:
        return (
            guitar_tune_frequencies[guitar_tuning_pitches.index(frequency) - 1][0],
            guitar_tune_frequencies[guitar_tuning_pitches.index(frequency) + 1][0]
        )


if __name__ == "__main__":
    print(get_target_note(196.0))
