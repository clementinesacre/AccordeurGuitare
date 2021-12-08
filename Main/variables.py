buttonColor = "#b5b5b5"
widthInterface = 1200
heightInterface = 800
widthCanvas = 1200
heightCanvas = 100
freqRef = 0
centeredNote = "X"  # note that is centered on the scale
limit = 3  # 1200/3 = 400hz ==> max
pos_button_tune_x = 150
pos_button_tune_y = 250
pos_button_note_x = 400
pos_button_note_y = 305
name_tuning = []
setting_tuning = []
buttons = list()
buttons_note = list()
fs = 2000
size_sample = 1000 #so data are send very half second (time = size-sample * 1/fs)
flag = False    # flag that controls the automatic recorder
flag2 = False   # flag that controls the manual recorder
selectedTune = "standard"
