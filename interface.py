import tkinter as tk
from tkinter import ttk
from tkinter import *
from random import *
from AccordeurGuitare import main

widthCanvas = 1200
heightCanvas = 100
freqRef = 0
limit = 3 #1200/3 = 400hz ==> max

def chooseNote(freq):
    targetFreq = freq
    global limit
    dict = main.getFrenquencies()
    actualFrequency = dict["freqActu"]
    scale.changeScale(targetFreq)
    limit = widthCanvas/(targetFreq*2)
    aiguille.changeTargetF(actualFrequency)
    root.after_idle(Move)  # after_idle est appelé quand il n'y a plus d'événements à traiter dans la boucle principale.
    #aiguille.move()


def startRecord():
    global limit
    dict = main.getFrenquencies()
    targetFreq = dict["target_frequency"]
    actualFrequency = dict["freqActu"]
    scale.changeScale(targetFreq)
    limit = widthCanvas/(targetFreq*2)
    aiguille.changeTargetF(actualFrequency)
    root.after_idle(Move)  # after_idle est appelé quand il n'y a plus d'événements à traiter dans la boucle principale.
    #aiguille.move()


def callback():
    pass


def Move():
    aiguille.move()
    root.after(10, Move)

"""def generateRand():
    aiguille.random()
    # aiguille.move()
    root.after(2000, generateRand)"""


class Scale:
    def __init__(self, canvas):
        self.canvas = canvas
        self.min = "A#"
        self.max = "e"
        self.center = 'G#'

        self.minCanvas = canvas.create_text(widthCanvas - 20, 20, text=self.min, fill="blue", font='Helvetica 15 bold')
        self.maxCanvas = canvas.create_text(10, 20, text=self.max, fill="blue", font='Helvetica 15 bold')
        self.centerCanvas = canvas.create_text(widthCanvas / 2, 20, text=self.center, fill="blue",
                                               font='Helvetica 15 bold')

    def changeScale(self, center):
        self.center = center
        self.canvas.itemconfig(self.centerCanvas, text=center)


class Aiguille:
    def __init__(self, canvas):
        # self.master = master
        # self.canvas = Canvas(master, bg="black", width=1200, height=100)
        self.canvas = canvas
        self.pos_x1 = widthCanvas/2
        self.pos_y1 = 50
        self.taille = 50
        self.target_freq = 0
        self.step = 5
        self.rectangle = self.canvas.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1 + self.taille,
                                                      self.pos_y1 + self.taille, fill="red",
                                                      outline='blue')
        self.canvas.pack()

    def move(self):
        # self.movement = self.pos_x1 - self.target_freq
        #print(" POS : " ,self.pos_x1, "  Limite : ",self.target_freq)
        if self.pos_x1 >= widthCanvas - self.taille or self.pos_x1 <= 0:
           pass
        elif self.target_freq > self.pos_x1 or self.target_freq > self.pos_x1 + 4 or self.target_freq > self.pos_x1 - 4:
            self.canvas.move(self.rectangle, self.step, 0)
            self.pos_x1 += self.step
        elif self.target_freq < self.pos_x1 or self.target_freq < self.pos_x1 + 4 or self.target_freq < self.pos_x1 - 4:
            self.canvas.move(self.rectangle, -self.step, 0)
            self.pos_x1 -= self.step
        elif self.target_freq == self.pos_x1:
            pass

        """elif self.target_freq * limit == self.pos_x1 or self.target_freq * limit <= self.pos_x1 - self.step or self.target_freq * limit >= self.pos_x1 + self.step:
                    print("condition")"""


        # self.pos_x1 = self.movement

    def changeTargetF(self, newF):
        self.target_freq = int(newF * limit)

    """def random(self):
        self.target_freq = randint(1, 1200)
        print(self.target_freq)"""


root = tk.Tk()
root.title('Tkinter Window Demo')
root.geometry('1200x800+50+50')

buttonEnregistrer = ttk.Button(root, text="enregistrer", command=lambda: startRecord())
buttonEnregistrer.pack(ipadx=5, ipady=5, expand=True)

buttonNote1 = ttk.Button(root, text="E", command=lambda: chooseNote(82.41))
buttonNote1.pack(ipadx=5, ipady=5, expand=True)

buttonNote2 = ttk.Button(root, text="a", command=lambda: chooseNote(110.00))
buttonNote2.pack(ipadx=5, ipady=5, expand=True)

buttonNote3 = ttk.Button(root, text="d", command=lambda: chooseNote(146.83))
buttonNote3.pack(ipadx=5, ipady=5, expand=True)

buttonNote4 = ttk.Button(root, text="g", command=lambda: chooseNote(196.00))
buttonNote4.pack(ipadx=5, ipady=5, expand=True)

buttonNote5 = ttk.Button(root, text="b", command=lambda: chooseNote(246.93))
buttonNote5.pack(ipadx=5, ipady=5, expand=True)

buttonNote6 = ttk.Button(root, text="e", command=lambda: chooseNote(329.63))
buttonNote6.pack(ipadx=5, ipady=5, expand=True)

canvas = Canvas(master=root, bg="black", width=widthCanvas, height=heightCanvas)
scale = Scale(canvas)

aiguille = Aiguille(canvas)
#aiguille.move()


# Appelé qu'une fois
# root.after_idle(generateRand)

root.mainloop()

# imports every file form tkinter and tkinter.ttk
