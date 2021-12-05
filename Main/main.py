import tkinter as tk
from tkinter import *
from PIL import ImageTk
import accords_guitare
import find_note
from variables import *
import time
from threading import *
import numpy as np
from numpy.fft import rfft
from numpy import argmax
import sounddevice as sd

"""
Record automatically
"""

"""
def startRecord(tune):
    global limit

    dictNote = record.getFrequencies(tune)
    targetFreq = dictNote["target_frequency"]
    actualFrequency = dictNote["freqActu"]
    higher_note = dictNote["higher_note"]
    lower_note = dictNote["lower_note"]
    print("Start : Frequency to reach automatically : ", targetFreq)
    print("Start : Actual Frequency : ", actualFrequency)
    print('-----------------------------')
    scale.changeScale(dictNote["target_note_string"], lower_note, higher_note)
    limit = widthCanvas / (targetFreq * 2)
    pointer.changeTargetF(actualFrequency)
    root.after_idle(move)
"""


def startFunctionAutomatic():
    """
    Manage multithreading, by running the function that reaches a note automatically,
    and then the function that moves the cursor.
    """
    t1 = Thread(target=automaticRecord)
    t2 = Thread(target=moveFrq)
    t1.start()
    t2.start()


def callbackAutomatic(indata, frames, time, status):
    """Callback function of the function that records by automatically finding the note to reach."""
    global limit

    if status:
        print(status)
    if any(indata[:, 0]):
        frequence = argmax(abs(rfft(indata[:, 0] - np.mean(indata[:, 0]))))
        dico = find_note.get_target_note(frequence)
        targetFreq = dico["target_frequency"]

        values.change(frequence, targetFreq)
        scale.changeScale(targetFreq)
        limit = widthCanvas / (targetFreq * 2)
        pointer.changeTargetF(frequence)

        print("frequence a atteindre automatiquement : ", targetFreq)
        print("frequence actuelle : ", frequence)
        print('-----------------------------')
    else:
        print('No input')


def automaticRecord():
    """Record by automatically finding the note to reach."""
    with sd.InputStream(channels=1, callback=callbackAutomatic, blocksize=int(size_sample), samplerate=fs):
        flag = True
        while flag:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                exit()


def startFunctionManual(freq):
    """
    Manage multithreading, running the function that reaches a manually chosen note, and then the function
    that moves the cursor.
    """
    global freqRef
    freqRef = freq

    t1 = Thread(target=manualRecord)
    t2 = Thread(target=moveFrq)
    t1.start()
    t2.start()


def callbackManual(indata, frames, time, status):
    """Callback function of the function that records by finding manually the note to reach."""
    global limit

    if status:
        print(status)
    if any(indata[:, 0]):
        frequence = argmax(abs(rfft(indata[:, 0] - np.mean(indata[:, 0]))))
        targetFreq = freqRef

        values.change(frequence, targetFreq)
        scale.changeScale(targetFreq)
        limit = widthCanvas / (targetFreq * 2)
        pointer.changeTargetF(frequence)

        print("frequence a atteindre automatiquement : ", targetFreq)
        print("frequence actuelle : ", frequence)
        print('-----------------------------')
    else:
        print('No input')


def manualRecord():
    """Record by manually choosing the note to reach."""
    with sd.InputStream(channels=1, callback=callbackManual, blocksize=int(size_sample), samplerate=fs):
        while True:
            time.sleep(0.01)


"""
Move the cursor
"""


def moveFrq():
    """Move the pointer."""
    while True:
        pointer.move()
        time.sleep(0.01)


"""
Set all the dict for later usage
"""


def setTunings():
    for t in accords_guitare.tunings_types:
        if t != "un_ton_plus_bas":
            name_tuning.append(t)
            setting_tuning.append(accords_guitare.tunings_types[t])
        else:
            pass


"""
Class for the scale (with frequencies and tone chosen)
"""


class Scale:
    def __init__(self, container):
        self.canvas = container
        self.lower = ""
        self.higher = ""
        self.center = ""
        self.maxCanvas = canvas.create_text(widthCanvas - 35, 20, text=self.lower, fill="#26ff34", font='Helvetica 15')
        self.minCanvas = canvas.create_text(35, 20, text=self.higher, fill="#26ff34", font='Helvetica 15')
        self.centerCanvas = canvas.create_text(widthCanvas / 2, 20, text=self.center, fill="#26ff34",
                                               font='Helvetica 15')

    def changeScale(self, center, lower="lower", higher="higher"):
        self.center = center
        self.lower = lower
        self.higher = higher
        self.canvas.itemconfig(self.centerCanvas, text=center)
        self.canvas.itemconfig(self.minCanvas, text=lower)
        self.canvas.itemconfig(self.maxCanvas, text=higher)


"""
Class of the cursor moving to the right frequency
"""


class Pointer:
    def __init__(self, newCanvas):
        self.canvas = newCanvas
        self.pos_x1 = (widthCanvas / 2)
        self.pos_y1 = 50
        self.size = 50
        self.target_freq = 0
        self.step = 5
        self.rectangle = self.canvas.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1 + 2,
                                                      self.pos_y1 + self.size, fill="red", outline='red')
        self.canvas.pack()

    def move(self):
        listE = []
        for j in range(-self.step + 1, self.step):
            listE.append(self.pos_x1 + j)

        if self.pos_x1 >= widthCanvas - self.size or self.pos_x1 <= 0:
            pass
        elif self.target_freq in listE:
            pass
        elif self.target_freq > self.pos_x1:
            self.canvas.move(self.rectangle, self.step, 0)
            self.pos_x1 += self.step
        elif self.target_freq < self.pos_x1:
            self.canvas.move(self.rectangle, -self.step, 0)
            self.pos_x1 -= self.step

    def changeTargetF(self, newF):
        self.target_freq = int(newF * limit)


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Guitar Tuner")
        container = tk.Frame(self, height=800, width=1200)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # self.bg = ImageTk.PhotoImage(file="../Resources/GuitarHead.jpg")


class ButtonTunings:
    def __init__(self, master, text, pos_x, pos_y, width):
        self.color = buttonColor
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.button = tk.Button(master, text=text, bg=self.color, command=self.showValue, width=width)
        self.button.pack(ipadx=5, ipady=5, expand=True)
        self.button.place(x=pos_x, y=pos_y)

    def showValue(self):
        buttonSave.tune = self.text
        tuning_pitches = find_note.guitar_tune_frequencies(self.text)

        for string in range(6):
            buttons_note[string].setButton(
                tuning_pitches[string][0],
                tuning_pitches[string][1]
            )


class ButtonRecord:
    def __init__(self, master, text, pos_x, pos_y, width):
        self.color = buttonColor
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.tune = "standard"
        self.button = tk.Button(master, text=text, bg=self.color, command=lambda: startFunctionAutomatic(), width=width)
        self.button.pack(ipadx=5, ipady=5, expand=True)
        self.button.place(x=pos_x, y=pos_y)


class ButtonNotes:
    def __init__(self, master, text, pos_x, pos_y, note, width):
        self.color = buttonColor
        self.dict = ()
        self.targetFreq = 0
        self.note = note
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.button = tk.Button(master, text=text, bg=self.color, command=self.chooseNote, width=width)
        self.button.pack(ipadx=5, ipady=5, expand=True)
        self.button.place(x=pos_x, y=pos_y)

    def chooseNote(self):
        startFunctionManual(self.note)

    def setButton(self, newText, newNote):
        self.note = newNote
        self.text = newText
        self.button['text'] = newText


class Values:
    """Text boxes displaying the current frequency and the frequency to be reached."""

    def __init__(self, canvas2):
        self.canvas = canvas2
        self.canvas.pack()

        self.actualText = 0
        self.targetText = 0

        self.actualCanvas = Canvas(self.canvas, width=100, height=30, bg="yellow")
        self.actualCanvas.pack()
        self.actualFrequency = self.actualCanvas.create_text(50, 20, text=self.actualText, fill="red",
                                                             font='Helvetica 15 bold')

        self.targetCanvas = Canvas(self.canvas, width=100, height=30, bg="blue")
        self.targetCanvas.pack()
        self.targetFrequency = self.targetCanvas.create_text(50, 20, text=self.targetText, fill="red",
                                                             font='Helvetica 15 bold')

    def change(self, actual, target):
        """Change the values of the displayed frequencies."""
        self.actualText = actual
        self.targetText = target
        self.actualCanvas.itemconfig(self.actualFrequency, text=self.actualText)
        self.targetCanvas.itemconfig(self.targetFrequency, text=self.targetText)


setTunings()
root = Window()
canvas = Canvas(master=root, bg="#000000", width=widthCanvas, height=heightCanvas)
canvasValue = Canvas(master=root, bg="purple", width=widthCanvas, height=heightCanvas)
scale = Scale(canvas)
values = Values(canvasValue)
pointer = Pointer(canvas)

# attributing each object with its class

buttonSave = ButtonRecord(root, "record", 20, 30, "6")
for e in range(len(name_tuning) + 1):
    buttons.append("button" + str(e + 1))
    # buttons_note.append("button_note" + str(e + 1))

for e in range(len(buttons) - 1):
    buttons[e] = ButtonTunings(root, name_tuning[e], 20, pos_x_button, "7")
    pos_x_button += 30

for b in range(6):
    buttons_note.append(ButtonNotes(
        root,
        setting_tuning[0][b],
        20,
        pos_button_note,
        accords_guitare.guitar_tunings["standard_indexes"][b],
        "7"
    ))

    pos_button_note += 30

buttons[0].showValue()
# main loop


if __name__ == "__main__":
    root.mainloop()
