"""-------------------------------------------SPACE-INVADERS--------------------------------------------------------"""
from tkinter import *


myWindow = Tk()
labelTitre = Label(myWindow, text="SPACE_INVADRES", fg="black")
labelTitre.pack()

boutonQuitter = Button(myWindow, text="Quitter", fg='black', command= myWindow.destroy)
boutonQuitter.pack(side='top')


























myWindow.mainloop()





