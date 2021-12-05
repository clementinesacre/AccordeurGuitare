import tkinter as tk
from tkinter import *
from PIL import ImageTk
# from AccordeurGuitare.Main import accords_guitare
# from AccordeurGuitare.Main import find_note
# from AccordeurGuitare.Main.variables import *
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
    global flag
    global flag2

    # toggle the automatic flag
    flag = not flag

    # stop the manual thread
    flag2 = False

    # if the automatic recorder thread is going to start
    if flag:
        # change the start button to a stop button
        buttonSave.changeParam("Stop", "red")

        # make sure all the other buttons are not highlighted
        for button in buttons_note:
            button.setColor(buttonColor)
            button.selected = False

    else:
        # change stop button to start button
        buttonSave.changeParam("Start", "green")

    # start all needed threads
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
        dico = find_note.get_target_note(frequence, selectedTune)
        targetFreq = dico["target_frequency"]

        values.change(frequence, targetFreq)
        scale.changeScale(
            dico["target_note_string"], 
            dico["lower_note"], 
            dico["higher_note"]
        )
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
        while flag:
            time.sleep(0.01)


def startFunctionManual(freq, noteText):
    """
    Manage multithreading, running the function that reaches a manually chosen note, and then the function
    that moves the cursor.
    """
    global freqRef
    global centeredNote
    global flag
    global flag2

    # stop the automatic thread
    flag = False

    # toggle the manual thread state
    flag2 = not flag2
    freqRef = freq

    # set the target note var to the text of the clicked button
    centeredNote = noteText

    # start all needed threads
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
        scale.changeScale(centeredNote)
        limit = widthCanvas / (targetFreq * 2)
        pointer.changeTargetF(frequence)

        print("frequence a atteindre manuellement : ", targetFreq)
        print("frequence actuelle : ", frequence)
        print('-----------------------------')
    else:
        print('No input')


def manualRecord():
    """Record by manually choosing the note to reach."""
    with sd.InputStream(channels=1, callback=callbackManual, blocksize=int(size_sample), samplerate=fs):
        while flag2:
            time.sleep(0.01)


def moveFrq():
    """Move the pointer."""
    while True:
        pointer.move()
        time.sleep(0.01)


def setTunings():
    """
    Set all the dict for later usage
    """
    for t in accords_guitare.tunings_types:
        if t != "un_ton_plus_bas":
            name_tuning.append(t)
            setting_tuning.append(accords_guitare.tunings_types[t])
        else:
            pass


class Scale:
    """
    Class for the scale (with frequencies and tone chosen)
    """
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


class Pointer:
    """
    Class of the cursor moving to the right frequency
    """
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

        # if the pointer is at one end and il wants to go further to that same end...
        if (
            (
                (self.pos_x1 >= widthCanvas - self.size) and 
                self.target_freq > self.pos_x1
            ) or (
                self.pos_x1 <= 0 and 
                self.target_freq < self.pos_x1
            )
        ):
            # ...do nothing
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
        global selectedTune

        # set the selected tune to a new value
        selectedTune = self.text

        # reset all the tune buttons color
        for e in buttons:
            e.setColor(buttonColor)

        # highlight the clicked button
        self.setColor('blue')

        buttonSave.tune = self.text
        tuning_pitches = find_note.guitar_tune_frequencies(self.text)

        # change the text inside the note selector buttons
        for string in range(6):
            buttons_note[string].setButton(
                tuning_pitches[string][0],
                tuning_pitches[string][1]
            )

    def setColor(self, newColor):
        self.color = newColor
        self.button['bg'] = self.color


class ButtonRecord:
    def __init__(self, master, text, pos_x, pos_y, width):
        self.color = "green"
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.tune = "standard"
        self.button = tk.Button(master, text=text, bg=self.color, command=lambda: startFunctionAutomatic(), width=width)
        self.button.pack(ipadx=5, ipady=5, expand=True)
        self.button.place(x=pos_x, y=pos_y)

    def changeParam(self, newText, newColor):
        self.button['text'] = newText
        self.button['bg'] = newColor


class ButtonNotes:
    def __init__(self, master, text, pos_x, pos_y, note, width):
        self.color = buttonColor
        self.selected = False
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
        global flag2
        buttonSave.changeParam("Start", "green")

        # if the button is selected (meaning the user wants to unselect it)...
        if self.selected:
            self.selected = False

            # stop the record
            flag2 = False

            # ...reset its color
            self.setColor(buttonColor)
        else:
            flag2 = False

            for button in buttons_note:
                button.setColor(buttonColor)
                button.selected = False

            # otherwise, highlight that button
            self.setColor('blue')
            startFunctionManual(self.note, self.text)
            self.selected = True



    def setButton(self, newText, newNote):
        global flag2
        self.note = newNote
        self.text = newText
        self.button['text'] = newText
        print(self.selected)

        if self.selected:
            flag2 = False
            startFunctionManual(self.note, self.text)

    def setColor(self, newColor):
        self.color = newColor
        self.button['bg'] = self.color



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

for e in range(len(name_tuning)):
    buttons.append(ButtonTunings(root, name_tuning[e], 20, pos_x_button, "7"))
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

# highlight the standard tune button
buttons[0].showValue()


if __name__ == "__main__":
    root.mainloop()
