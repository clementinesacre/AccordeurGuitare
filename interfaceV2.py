import tkinter as tk
from tkinter import ttk
from tkinter import *
from random import *
import main
import find_note
import sounddevice as sd
import numpy as np
from numpy.fft import rfft
from numpy import argmax
from threading import *
import time


widthCanvas = 1200
heightCanvas = 100
freqRef = 0
limit = 3 #1200/3 = 400hz --> 400Hz represents the maximum frequency that can be displayed on the canva.
fs = 2000
size_sample = 2000


def startFunctionAutomatic() :
    """
    Manage multithreading, by running the function that reaches a note automatically,
    and then the function that moves the cursor.
    """
    t1=Thread(target=automaticRecord)
    t2=Thread(target=moveFrq)
    t1.start()
    t2.start()

def callbackAutomatic(indata, frames, time, status):
    """Callback function of the function that records by automatically finding the note to reach."""
    if status:
        print(status)
    if any(indata[:,0]):
        frequence = argmax(abs(rfft(indata[:,0] - np.mean(indata[:,0]))))
        dico = find_note.get_target_note(frequence)
        targetFreq = dico["target_frequency"]
        
        values.change(frequence, targetFreq)
        scale.changeScale(targetFreq)
        limit = widthCanvas/(targetFreq*2)
        pointer.changeTargetF(frequence)
        
        print("frequence a atteindre automatiquement : ", targetFreq)
        print("frequence actuelle : ", frequence)
        print('-----------------------------')
    else:
        print('No input')

def automaticRecord() :
    """Record by automatically finding the note to reach."""
    with sd.InputStream(channels=1, callback=callbackAutomatic,blocksize=int(size_sample),samplerate=fs):
        while True:
            time.sleep(0.03)


def startFunctionManual(freq) :
    """
    Manage multithreading, running the function that reaches a manually chosen note, and then the function
    that moves the cursor.
    """
    global freqRef
    freqRef = freq
    
    t1=Thread(target=manualRecord)
    t2=Thread(target=moveFrq)
    t1.start()
    t2.start()
    
def callbackManual(indata, frames, time, status):
    """Callback function of the function that records by finding manually the note to reach."""
    if status:
        print(status)
    if any(indata[:,0]):
        frequence = argmax(abs(rfft(indata[:,0] - np.mean(indata[:,0]))))
        targetFreq = freqRef
        
        values.change(frequence, targetFreq)
        scale.changeScale(targetFreq)
        limit = widthCanvas/(targetFreq*2)
        pointer.changeTargetF(frequence)
        
        print("frequence a atteindre automatiquement : ", targetFreq)
        print("frequence actuelle : ", frequence)
        print('-----------------------------')
    else:
        print('No input')

def manualRecord() :
    """Record by manually choosing the note to reach."""
    with sd.InputStream(channels=1, callback=callbackManual,blocksize=int(size_sample),samplerate=fs):
        while True:
            time.sleep(0.01)


def moveFrq():
    """Move the pointer."""
    while True :
        pointer.move()
        time.sleep(0.01)


class Scale:
    """Frequency scale (with tones displayed according to what needs to be reached)."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.min = "A#"
        self.max = "e"
        self.center = 'G#'
        self.minCanvas = canvas.create_text(widthCanvas - 20, 20, text=self.min, fill="blue", font='Helvetica 15 bold')
        self.maxCanvas = canvas.create_text(10, 20, text=self.max, fill="blue", font='Helvetica 15 bold')
        self.centerCanvas = canvas.create_text(widthCanvas / 2, 20, text=self.center, fill="blue", font='Helvetica 15 bold')

    def changeScale(self, center):
        """Change the legend representing tones to be achieved."""
        self.center = center

class Pointer:
    """Pointer that moves to display the correct frequency."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.pos_x1 = widthCanvas/2
        self.pos_y1 = 50
        self.taille = 50
        self.target_freq = 0
        self.step = 4
        self.rectangle = self.canvas.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1 + self.taille,self.pos_y1 + self.taille, fill="red", outline='blue')
        self.canvas.pack()

    def move(self):
        """Move the pointer according to the coordinate on which it needs to go."""
        liste = []
        for i in range(-self.step+1, self.step) :
            liste.append(self.pos_x1 + i)

        if (self.pos_x1 >= widthCanvas - self.taille and self.target_freq > 670) or (self.pos_x1 <= 0 and self.target_freq < 2 ):
            pass
        elif self.target_freq in liste :
            pass
        elif self.target_freq > self.pos_x1 :
            self.canvas.move(self.rectangle, self.step, 0)
            self.pos_x1 += self.step
        elif self.target_freq < self.pos_x1 :
            self.canvas.move(self.rectangle, -self.step, 0)
            self.pos_x1 -= self.step

    def changeTargetF(self, newF):
        """Change the coordinate on which the pointer needs to go."""
        self.target_freq = int(newF * limit)

class Values() :
    """Text boxes displaying the current frequency and the frequency to be reached."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.pack()
        
        self.actualText = 0
        self.targetText = 0
        
        self.actualCanvas = Canvas(self.canvas, width=100, height=30, bg="yellow")
        self.actualCanvas.pack()
        self.actualFrequency = self.actualCanvas.create_text(50, 20, text=self.actualText, fill="red", font='Helvetica 15 bold')
        
        self.targetCanvas = Canvas(self.canvas, width=100, height=30, bg="blue")
        self.targetCanvas.pack()
        self.targetFrequency = self.targetCanvas.create_text(50, 20, text=self.targetText, fill="red", font='Helvetica 15 bold')
        
    def change(self, actual, target) :
        """Change the values of the displayed frequencies."""
        self.actualText = actual
        self.targetText = target
        self.actualCanvas.itemconfig(self.actualFrequency, text=self.actualText)
        self.targetCanvas.itemconfig(self.targetFrequency, text=self.targetText)
        
        
#Window initialization.
root = tk.Tk()
root.title('Accordeur guitare')
root.geometry('1200x800+50+50')

#Button that starts the recording to automatically reach the note.
buttonSave = ttk.Button(root, text="Enregistrer", command=lambda: startFunctionAutomatic())
buttonSave.pack(ipadx=5, ipady=5, expand=True)

#Buttons that start the recording by manually specifying the note to be reached.
buttonNote1 = ttk.Button(root, text="E", command=lambda: startFunctionManual(82.41))
buttonNote1.pack(ipadx=5, ipady=5, expand=True)
buttonNote2 = ttk.Button(root, text="A", command=lambda: startFunctionManual(110.00))
buttonNote2.pack(ipadx=5, ipady=5, expand=True)
buttonNote3 = ttk.Button(root, text="D", command=lambda: startFunctionManual(146.83))
buttonNote3.pack(ipadx=5, ipady=5, expand=True)
buttonNote4 = ttk.Button(root, text="G", command=lambda: startFunctionManual(196.00))
buttonNote4.pack(ipadx=5, ipady=5, expand=True)
buttonNote5 = ttk.Button(root, text="B", command=lambda: startFunctionManual(246.93))
buttonNote5.pack(ipadx=5, ipady=5, expand=True)
buttonNote6 = ttk.Button(root, text="E", command=lambda: startFunctionManual(329.63))
buttonNote6.pack(ipadx=5, ipady=5, expand=True)

#Area containing the needle and the scale of grades to be reached.
canvas = Canvas(master=root, bg="black", width=widthCanvas, height=heightCanvas)
#Area containing the current frequency and the frequency to be reached, in Hz.
canvaValue = Canvas(master=root, bg="purple", width=widthCanvas, height=heightCanvas)

#Initialization of the needle, the scale of the notes to reach, and the frequencies in Hz.
values = Values(canvaValue)
scale = Scale(canvas)
pointer = Pointer(canvas)

root.mainloop()
