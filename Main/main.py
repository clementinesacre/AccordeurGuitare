import tkinter as tk
from tkinter import *
from AccordeurGuitare.Main import record
from PIL import ImageTk
from AccordeurGuitare.Main import accords_guitare
from AccordeurGuitare.Main.variables import *

"""
Record automatically
"""


def startRecord():
    global limit

    dictNote = record.getFrequencies()
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
Move the cursor
"""


def move():
    pointer.move()
    root.after(10, move)


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
        self.bg = ImageTk.PhotoImage(file="../Resources/GuitarHead.jpg")


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
        print(self.text)


class ButtonRecord:
    def __init__(self, master, text, pos_x, pos_y, width):
        self.color = buttonColor
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.button = tk.Button(master, text=text, bg=self.color, command=startRecord, width=width)
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
        global limit
        self.dict = record.getFrequencies()
        self.targetFreq = self.note
        actualFrequency = self.dict["freqActu"]
        print("frequency to reach manually : ", self.targetFreq)
        print("actual frequency : ", actualFrequency)
        print('-----------------------------')
        scale.changeScale(self.dict["target_note_string"])
        limit = widthCanvas / (self.targetFreq * 2)
        pointer.changeTargetF(actualFrequency)
        root.after_idle(move)

    def changeSettings(self):
        pass


setTunings()
root = Window()
canvas = Canvas(master=root, bg="#000000", width=widthCanvas, height=heightCanvas)
scale = Scale(canvas)
pointer = Pointer(canvas)

# attributing each object with its class

buttonSave = ButtonRecord(root, "record", 20, 30, "6")

for e in range(len(name_tuning) + 1):
    buttons.append("button" + str(e + 1))
    buttons_note.append("button_note" + str(e + 1))

for e in range(len(buttons) - 1):
    buttons[e] = ButtonTunings(root, name_tuning[e], 20, pos_x_button, "7")
    pos_x_button += 30

for b in range(6):
    buttons_note[e] = ButtonNotes(root, setting_tuning[0][b], 20, pos_button_note,
                                  accords_guitare.guitar_tunings["standard_indexes"][b], "7")
    pos_button_note += 30

# main loop

root.mainloop()
