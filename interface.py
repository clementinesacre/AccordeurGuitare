import tkinter as tk
from tkinter import ttk
from tkinter import *
from AccordeurGuitare import main

widthCanvas = 1200
heightCanvas = 100
freqRef = 0
limit = 3  # 1200/3 = 400hz ==> max

"""
Record manually
"""


def chooseNote(freq):
    global limit

    dict = main.getFrenquencies()
    targetFreq = freq
    actualFrequency = dict["freqActu"]
    print("frequency to reach manually : ", targetFreq)
    print("actual frequency : ", actualFrequency)
    print('-----------------------------')
    scale.changeScale(dict["target_note_string"])
    limit = widthCanvas / (targetFreq * 2)
    pointer.changeTargetF(actualFrequency)
    root.after_idle(move)


"""
Record automatically
"""


def startRecord():
    global limit

    dict = main.getFrenquencies()
    targetFreq = dict["target_frequency"]
    actualFrequency = dict["freqActu"]
    higher_note = dict["higher_note"]
    lower_note = dict["lower_note"]
    print("Start : Frequency to reach automatically : ", targetFreq)
    print("Start : Actual Frequency : ", actualFrequency)
    print('-----------------------------')
    scale.changeScale(dict["target_note_string"], lower_note, higher_note)
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
Class for the scale (with frequencies and tone chosen)
"""


class Scale:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lower = ""
        self.higher = ""
        self.center = ""
        self.maxCanvas = canvas.create_text(widthCanvas - 35, 20, text=self.lower, fill="blue", font='Helvetica 15')
        self.minCanvas = canvas.create_text(35, 20, text=self.higher, fill="blue", font='Helvetica 15')
        self.centerCanvas = canvas.create_text(widthCanvas / 2, 20, text=self.center, fill="blue",
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
    def __init__(self, canvas):
        self.canvas = canvas
        self.pos_x1 = (widthCanvas / 2)
        self.pos_y1 = 50
        self.size = 50
        self.target_freq = 0
        self.step = 5
        self.rectangle = self.canvas.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1 + 2,
                                                      self.pos_y1 + self.size, fill="red", outline='blue')
        self.canvas.pack()

    def move(self):
        listE = []
        for i in range(-self.step + 1, self.step):
            listE.append(self.pos_x1 + i)

        if self.pos_x1 >= widthCanvas - self.size or self.pos_x1 <= 0:
            pass
        elif self.target_freq in listE:
            # print("equal")
            pass
        elif self.target_freq > self.pos_x1:
            # print("greater")
            self.canvas.move(self.rectangle, self.step, 0)
            self.pos_x1 += self.step
        elif self.target_freq < self.pos_x1:
            # print("smaller")
            self.canvas.move(self.rectangle, -self.step, 0)
            self.pos_x1 -= self.step

    def changeTargetF(self, newF):
        self.target_freq = int(newF * limit)


root = tk.Tk()
root.title('Guitar Tuner')
root.geometry('1200x800+50+50')

buttonSave = ttk.Button(root, text="Record", command=lambda: startRecord())
buttonSave.pack(ipadx=5, ipady=5, expand=True)

buttonNote1 = ttk.Button(root, text="E", command=lambda: chooseNote(82.41))
buttonNote1.pack(ipadx=5, ipady=5, expand=True)
buttonNote2 = ttk.Button(root, text="A", command=lambda: chooseNote(110.00))
buttonNote2.pack(ipadx=5, ipady=5, expand=True)
buttonNote3 = ttk.Button(root, text="D", command=lambda: chooseNote(146.83))
buttonNote3.pack(ipadx=5, ipady=5, expand=True)
buttonNote4 = ttk.Button(root, text="G", command=lambda: chooseNote(196.00))
buttonNote4.pack(ipadx=5, ipady=5, expand=True)
buttonNote5 = ttk.Button(root, text="B", command=lambda: chooseNote(246.93))
buttonNote5.pack(ipadx=5, ipady=5, expand=True)
buttonNote6 = ttk.Button(root, text="E", command=lambda: chooseNote(329.63))
buttonNote6.pack(ipadx=5, ipady=5, expand=True)

canvas = Canvas(master=root, bg="black", width=widthCanvas, height=heightCanvas)

scale = Scale(canvas)
pointer = Pointer(canvas)

# root.after_idle(generateRand) # after_idle est appelé quand il n'y a plus d'événements à traiter dans la boucle
# principale ; # Appelé qu'une fois

root.mainloop()
