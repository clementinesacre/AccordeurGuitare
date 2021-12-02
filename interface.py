import tkinter as tk
from tkinter import *
import main
from PIL import ImageTk
from AccordeurGuitare import accords_guitare

buttonColor = "#9d9d9d"
widthInterface = 1200
heightInterface = 800
widthCanvas = 1200
heightCanvas = 100
freqRef = 0
limit = 3  # 1200/3 = 400hz ==> max
pos_button = 150

name_tuning = []
setting_tuning = []
buttons = list()

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


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Guitar Tuner")
        container = tk.Frame(self, height=800, width=1200)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.bg = ImageTk.PhotoImage(file="GuitarHead.jpg")


class Button:
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






def setTunings():
    for e in accords_guitare.tunings_types:
        if e != "un_ton_plus_bas":
            name_tuning.append(e)
            setting_tuning.append(accords_guitare.tunings_types[e])
        else : pass


setTunings()
for e in range(len(name_tuning) + 1):
    buttons.append("button" + str((e)+ 1))
for i in range(len(buttons)):
    print(buttons[i])



# canvas.create_image(320, 0, image=bg, anchor='nw')
root = Window()

canvas = Canvas(master=root, bg="#000000", width=widthCanvas, height=heightCanvas)
scale = Scale(canvas)
pointer = Pointer(canvas)

"""buttonSave = Button(root, "record", startRecord, 20, 30, "6")

buttonTunings = Button(root, "Tunings", setTunings, 20, 100, "6")
"""

for e in range(len(buttons)-1):
    buttons[e] = Button(root, name_tuning[e], 20, pos_button, "7")
    pos_button += 30


"""
buttonNote1 = tk.Button(root, bg=buttonColor, width="6", text="E", command=lambda: chooseNote(82.41))
buttonNote1.pack(ipadx=5, ipady=5, expand=True)
buttonNote1.place(x=355, y=470)

buttonNote2 = tk.Button(root, bg=buttonColor, width="6", text="A", command=lambda: chooseNote(110.00))
buttonNote2.pack(ipadx=5, ipady=5, expand=True)
buttonNote2.place(x=375, y=400)

buttonNote3 = tk.Button(root, bg=buttonColor, width="6", text="D", command=lambda: chooseNote(146.83))
buttonNote3.pack(ipadx=5, ipady=5, expand=True)
buttonNote3.place(x=395, y=325)

buttonNote4 = tk.Button(root, bg=buttonColor, width="6", text="G", command=lambda: chooseNote(196.00))
buttonNote4.pack(ipadx=5, ipady=5, expand=True)
buttonNote4.place(x=415, y=250)

buttonNote5 = tk.Button(root, bg=buttonColor, width="6", text="B", command=lambda: chooseNote(246.93))
buttonNote5.pack(ipadx=5, ipady=5, expand=True)
buttonNote5.place(x=440, y=175)

buttonNote6 = tk.Button(root, bg=buttonColor, width="6", text="E", command=lambda: chooseNote(329.63))
buttonNote6.pack(ipadx=5, ipady=5, expand=True)
buttonNote6.place(x=460, y=100)
"""

# root.after_idle(generateRand) # after_idle est appelé quand il n'y a plus d'événements à traiter dans la boucle
# principale ; # Appelé qu'une fois

root.mainloop()
