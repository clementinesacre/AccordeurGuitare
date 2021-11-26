import tkinter as tk
from tkinter import ttk
from tkinter import *


def callback():
    print("cc")

def recuperation_port():
    print("saluuut")
    aiguille.move()
        
    root.after(10, recuperation_port)
    
    

class Aiguille():
    def __init__(self, master = None):
        self.master = master
        self.canvas= Canvas(master, width=1200, height=100)
        self.pos_x1 = 50
        self.pos_y1 = 50
        self.pos_x2 = 100
        self.pos_y2 = 100
        self.rectangle = self.canvas.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x2, self.pos_y2, fill="red", outline = 'blue') 
        self.canvas.pack()
        self.move()
        
    def move(self) :
        self.canvas.move(self.rectangle, 1, 0)

root = tk.Tk()
root.title('Tkinter Window Demo')
root.geometry('1200x800+50+50')

   
    
buttonEnregistrer = ttk.Button(root, text="enregistrer", command=lambda: callback())
buttonEnregistrer.pack(ipadx=5,ipady=5,expand=True)

buttonNote1 = ttk.Button(root, text="E", command=lambda: callback())
buttonNote1.pack(ipadx=5,ipady=5,expand=True)

buttonNote2 = ttk.Button(root, text="a", command=lambda: callback())
buttonNote2.pack(ipadx=5,ipady=5,expand=True)

buttonNote3 = ttk.Button(root, text="d", command=lambda: callback())
buttonNote3.pack(ipadx=5,ipady=5,expand=True)

buttonNote4 = ttk.Button(root, text="g", command=lambda: callback())
buttonNote4.pack(ipadx=5,ipady=5,expand=True)

buttonNote5 = ttk.Button(root, text="b", command=lambda: callback())
buttonNote5.pack(ipadx=5,ipady=5,expand=True)

buttonNote6 = ttk.Button(root, text="e", command=lambda: callback())
buttonNote6.pack(ipadx=5,ipady=5,expand=True)




aiguille = Aiguille()
aiguille.move()




root.after_idle(recuperation_port) #after_idle est appelé quand il n'y a plus d'événements à traiter dans la boucle principale. Appelé qu'une fois 


root.mainloop()

# imports every file form tkinter and tkinter.ttk
'''from tkinter import *
from tkinter.ttk import *

class GFG:
	def __init__(self, master = None):
		self.master = master
		
		# to take care movement in x direction
		self.x = 1
		# to take care movement in y direction
		self.y = 0

		# canvas object to create shape
		self.canvas = Canvas(master)
		# creating rectangle
		self.rectangle = self.canvas.create_rectangle(
						5, 5, 25, 25, fill = "black")
		self.canvas.pack()

		# calling class's movement method to
		# move the rectangle
		self.movement()
	
	def movement(self):

		# This is where the move() method is called
		# This moves the rectangle to x, y coordinates
		self.canvas.move(self.rectangle, self.x, self.y)

		self.canvas.after(100, self.movement)
	
	# for motion in negative x direction
	def left(self, event):
		print(event.keysym)
		self.x = -5
		self.y = 0
	
	# for motion in positive x direction
	def right(self, event):
		print(event.keysym)
		self.x = 5
		self.y = 0
	
	# for motion in positive y direction
	def up(self, event):
		print(event.keysym)
		self.x = 0
		self.y = -5
	
	# for motion in negative y direction
	def down(self, event):
		print(event.keysym)
		self.x = 0
		self.y = 5

if __name__ == "__main__":

	# object of class Tk, responsible for creating
	# a tkinter toplevel window
	master = Tk()
	gfg = GFG(master)

	# This will bind arrow keys to the tkinter
	# toplevel which will navigate the image or drawing
	master.bind("<KeyPress-Left>", lambda e: gfg.left(e))
	master.bind("<KeyPress-Right>", lambda e: gfg.right(e))
	master.bind("<KeyPress-Up>", lambda e: gfg.up(e))
	master.bind("<KeyPress-Down>", lambda e: gfg.down(e))
	
	# Infinite loop breaks only by interrupt
	mainloop()'''


