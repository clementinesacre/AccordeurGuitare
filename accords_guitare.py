guitar_tunings = {
    "standard_indexes": [82.41, 110.00, 146.83, 196.00, 246.94, 329.63],
    "standard": [('E', 0), ('A', 0), ('D', 0), ('G', 0), ('B', 0), ('E', 0)],
    "un_ton_plus_bas": [('D', -2), ('G', -2), ('C', -2), ('F', -2), ('A', -2), ('D', -2)],
    "open_mi": [('E', 0), ('B', 2), ('E', 2), ('E', 0), ('B', 0), ('E', 0)],
    "open_do": [('C', -2), ('G', -1), ('C', -1), ('C', -4), ('G', -2), ('C', -2)],
    "drop_d": [('D', -2), ('A', 0), ('D', 0), ('G', 0), ('B', 0), ('E', 0)]
}

tunings_types = {
    "standard": ['E', 'A', 'D', 'G', 'B', 'E'],
    "un_ton_plus_bas": ['D', 'G', 'C', 'F', 'A', 'D'],
    "open_mi": ['E', 'B', 'E', 'E', 'B', 'E'],
    "open_do": ['C', 'G', 'C', 'C', 'G', 'C'],
    "drop_d": ['D', 'A', 'D', 'G', 'B', 'E']
}

if __name__ == "__main__":
    print(guitar_tunings)
