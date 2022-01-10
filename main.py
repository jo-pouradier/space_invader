import tkinter as tk
import classes as cl
from PIL import Image, ImageTk
from tkinter import messagebox


if __name__ == "__main__":
    ### WINDOW ###
    # creation de la page window tkinter
    root = tk.Tk()
    window = cl.main_view(root)
    window.configure(highlightbackground="yellow", highlightthickness=2)
    window.pack(side="top", fill="both", expand=True)
    # creation du background
    window.update_idletasks()
    window.new_background("images/background_space_3.png")
    root.bind(
        "r",
        lambda e: [
            window.new_background(window.background_image),
            window.cv.tag_lower("background"),
        ],
    )  # changer le bind de cet event !!!!

    ### CREATION DU MONDE ###
    world = cl.World(window.cv)
    world.level_monster(5)
    world.shoot_monster()
    window.cv.bind("<Key>", world.player.deplacement_player)
    window.cv.bind("<space>", world.player.shoot)
    world.fct_player()
    

    world.player.speed = 50  # la ca va vite en vrai pour un debut de jeu
    # world.monster.speed = 4  # change la vitesse d'un seul

    ### MORT ###
    world.dead()

    root.mainloop()
