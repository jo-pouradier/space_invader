import tkinter as tk
import classes as cl
from PIL import Image, ImageTk


if __name__ == "__main__":
    ######WINDOW######
    # creation de la page window tkinter
    root = tk.Tk()
    window = cl.main_view(root)
    window.configure(highlightbackground='yellow', highlightthickness=2)
    window.pack(side="top", fill="both", expand=True)
    # creation du background
    window.update_idletasks()
    window.new_background('images/background_space_3.png')
    root.bind("<Motion>", lambda e: [window.new_background(
        window.background_image), window.cv.tag_lower('background')])  # changer le bind de cet event !!!!

    #####JOUEUR######
    # creation du joueur
    player = cl.Player(lives=3, img='images/vaisseau_player.png',
                       position=[window.sizeX/2, window.sizeY*0.75], canvas=window.cv)
    player.create(tag='player')

    # mouvement du joueur
    player.speed = 50  # la ca va vite en vrai pour un debut de jeu
    window.cv.focus_set()  # mise en place du focus pour prendre en compte les events
    window.cv.bind('<Key>', player.deplacement_player)
    # creation du shoot de balles
    window.cv.bind('<space>', player.shoot)
    # on lui donne un nom pour différencier des monstres plus tard
    player.name = 'player'
    player.deplacement_bullet()
    player.suppr_bullet()

    #####MONSTER#####
    # creation d'ennemis
    monster = cl.Monster(1, window.cv, position=[
                         window.cv.winfo_width()/2, 70], img='images/vaisseau_enemy_3.png')
    monster.create(tag='monster')
    window.cv.tag_raise('monster')
    # deplacement des monstres
    monster.speed = 4  # a voir une vitesse adequate
    print(monster.form)
    monster.deplacement_monstre()

    root.mainloop()
