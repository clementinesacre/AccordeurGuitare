import math
from AccordeurGuitare import accords_guitare


# prend une fréquence en paramètre et renvoie la note correcte la plus proche de cette fréquence
def get_closest_note(instrument_pitch):
    # fréquence de référence
    A4_pitch = 440

    # noms des différentes notes
    string_notes = [
        "A", "A#", "B ", "C ", "C#", "D ", "D#", "E ", "F ", "F#", "G ", "G#"
    ]

    # index de la note la plus proche de la fréquence d'entrée pour le tableau de noms
    pitch_index = int(
        round(
            math.log(instrument_pitch / A4_pitch, 2) * 12
        )
    )

    # numéro de l'octave dans laquelle se trouve la note la plus proche
    octave_number = 4 + (pitch_index + 9) // 12
    simple_note = string_notes[pitch_index % 12]

    # création de la note en texte
    closest_note = simple_note + str(octave_number)

    # 
    closest_pitch = round(A4_pitch * 2 ** (pitch_index / 12), 1)

    return pitch_index


# trouve la note dont laquelle il faut se rapprocher
def get_target_note(instrument_pitch, tune="standard"):
    # fréquence de référence
    A4_pitch = 440

    # ce tableau va contenir les fréquences de l'accordage choisi
    guitar_tuning_pitches = []

    # noms des différentes notes
    string_notes = [
        "A", "A#", "B ", "C ", "C#", "D ", "D#", "E ", "F ", "F#", "G ", "G#"
    ]

    # index de la note la plus proche de la fréquence d'entrée pour le tableau de noms
    pitch_index = int(
        round(
            math.log(instrument_pitch / A4_pitch, 2) * 12
        )
    )

    # on calcule les fréquences des cordes de l'accordage sélectionné
    # à partir des fréquences de l'accordage standard et de la différence en tons
    for i in range(6):
        guitar_tuning_pitches.append(
            accords_guitare.guitar_tunings["standard_indexes"][i] - (
                    accords_guitare.guitar_tunings["standard_indexes"][i] -
                    round(
                        accords_guitare.guitar_tunings["standard_indexes"][i] * 2 ** (
                                accords_guitare.guitar_tunings[tune][i][1] / 12), 2
                    )
            )
        )

    # fonction de comparaison
    absolute_difference_function = lambda list_value: abs(list_value - instrument_pitch)

    # recherche de la fréquence la plus proche de la fréquence d'entrée
    # on compare donc la fréquence d'entrée aux fréquences de l'accord sélectionné
    target_frequency = min(guitar_tuning_pitches, key=absolute_difference_function)

    # numéro de l'octave dans laquelle se trouve la note la plus proche
    target_pitch_index = int(
        round(
            math.log(target_frequency / A4_pitch, 2) * 12
        )
    )

    target_note = string_notes[target_pitch_index % 12]
    target_octave = 4 + (target_pitch_index + 9) // 12
    string_target_note = target_note + str(target_octave)

    return {
        "target_note_string": string_target_note,
        "target_octave": target_octave,
        "target_frequency": target_frequency
    }


if __name__ == "__main__":
    print(get_target_note(200, "un_ton_plus_bas"))
