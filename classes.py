from random import *
import tkinter as tk
import time
from PIL import Image, ImageTk


class main_view(tk.Frame):
    '''
    main_view
    dev: Joseph
    date: 2021-12-16 09:54:25

    Description:
    Cree la fenetre principale du jeu space invader, avec ses proporiété

    Parametres:
        tk [tk] : cree une frame tkinter dans la page principale
    '''

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # frame pour afficher les info du jeu : nbr de vie, score, boutons...
        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, sticky='nsew')
        info_frame.configure(highlightbackground='red', highlightthickness=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # canvas qui aura toutes les entitées du jeu.
        self.cv = tk.Canvas(self)
        self.cv.configure(highlightbackground='blue',
                          highlightthickness=2)
        self.cv.grid(row=1, column=0, sticky='nsew')

        bouton_quitter = tk.Button(
            info_frame, text='Quitter', fg='black', command=self.master.destroy)
        bouton_quitter.grid(row=0, column=4, sticky='e')
        bouton_new_game = tk.Button(
            info_frame, text='New Game', fg='black', command=None)
        bouton_new_game.grid(row=0, column=3, sticky='e')

        self.centrage()

    def centrage(self):
        '''
        centrage
        dev: Joseph
        date: 2021-11-27 20:54:14

        Description:
        centre la fenetre tkinter sur l'ecran de l'utilisateur

        Parametres:
            self [Frame] : une frame tkinter
        '''
        self.sizeX = self.master.winfo_screenwidth()*0.9
        self.sizeY = self.master.winfo_screenheight()*0.9
        positionX = self.master.winfo_screenwidth()/2-(self.sizeX)/2
        positionY = self.master.winfo_screenheight()/2-(self.sizeY)/2
        self.master.geometry(
            "{}x{}+{}+{}".format(int(self.sizeX), int(self.sizeY), int(positionX), int(positionY)))

# pas sur qu'elle soit utile

# class Space_invaders():
#     '''
#     Space_invaders
#     dev: Adrien
#     date: 2021-12-16 09:55:42

#     Description:
#     Classe qui regroupe toutes les entitées du jeu.
#     '''

#     def __init__(self, canvas, player, x_max, y_max):
#         self.canvas = canvas
#         self.enemy = []
#         self.player = player
#         self.x_fenetre_max = x_max
#         self.y_fentre_max = y_max


# utile??
# Sp_Inv = Space_invaders("myWindow", "player", 300, 300)  # initialisation test


class Entity():
    '''
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu, regroupe toutes les données essentielles sur une entité du jeu.
    '''

    def __init__(self, lives, canvas, speed=1, position=[0, 0], img=""):
        # nombre de vies (3 pour le joueur et a definir pour les enemies)
        self.lives = lives
        self.position = position  # position sur la map
        self.damage = 1
        self.border = 0  # désigne la ligne que le joueur ou le monstre ne peux pas dépasser
        self.speed = speed
        self.img = img
        self.canvas = canvas
        self.bullets = {}

    def create(self, canvas):
        self.photo = tk.PhotoImage(file=self.img)
        self.form = canvas.create_image(
            self.position[0], self.position[1], image=self.photo)

    # je crois pas quelle soit utile...
    def placement(self, position):  # positionne l'entité dur la map
        if len(position) == 2 and position[0] >= 0 and position[1] >= 0:
            self.position[0] = position[0]
            self.position[1] = position[1]
        else:
            self.position.append([0, 0])

    # def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
    #     if nb == 0:
    #         self.direction_tir = 'up'
    #     elif nb == 1:
    #         self.direction_tir = "down"

    def shoot(self, event):
        '''
        shoot
        dev: Joseph
        date: 2021-12-17 23:31:43

        Description:
        Creation des bullets en fonction de l'event <space>, pour le player, et par rien pour les monstres.
        On met dans un dictionnaire l'objet tkinter (oval) et sa position ( par rapport en l'envoyeur).

        Parametres:
            event [event] : <space> pour le payer ou rien pour un monstre.
        '''

        key = event.keysym
        # on passe par l'event (<space>) pour le player et par rien pour les monstres.
        if key == 'space':
            self.bullets[(self.canvas.create_oval(
                self.position[0]-5, self.position[1]-5, self.position[0]+5, self.position[1]+5, fill='green'))] = [self.position[0], self.position[1]]

        else:
            self.bullets[(self.canvas.create_oval(
                self.position[0]-5, self.position[1]-5, self.position[0]+5, self.position[1]+5, fill='red'))] = [self.position[0], self.position[1]]

    def deplacement_bullet(self):
        '''
        deplacement_bullet
        dev: Joseph
        date: 2021-12-17 23:34:09

        Description:
        En fonction de self (player ou monstre), la balles se deplace vers le haut ou vers le bas.
        '''

        for bullet in self.bullets.keys():
            if self.name == 'player':
                self.bullets[bullet][1] -= 5
            else:
                self.bullets[bullet][1] += 5
            self.canvas.coords(
                bullet, self.bullets[bullet][0]-5, self.bullets[bullet][1]-5, self.bullets[bullet][0]+5, self.bullets[bullet][1]+5)
        self.canvas.after(20, self.deplacement_bullet)

    def suppr_bullet(self):
        '''
        suppr_bullet
        dev: Joseph
        date: 2021-12-17 23:35:25

        Description:
        On parcours la liste des bullets, on enregistres celles qui sortent dee la fenetre,
        puis on les suprimes du canvas et du dictionnaire.
        '''

        list_suppr = []
        for bullet in self.bullets.keys():
            if self.bullets[bullet][1] < 0 or self.bullets[bullet][1] > self.canvas.winfo_height():
                list_suppr.append(bullet)
        for b in list_suppr:
            self.canvas.delete(b)
            self.bullets.pop(b)
        self.canvas.after(20, self.suppr_bullet)


class Player(Entity):
    '''
    Player
    dev: Adrien
    date: 2021-12-17 23:40:06

    Description:
    Classe qui donne les methodes qui s'appliqueront a player en tant qu'entité du jeu.

    Parametres:
        Entity [class] : voir description de la class
    '''

    def deplacement_player(self, event):
        '''
        deplacement_player
        dev: Adrien et Joseph
        date: 2021-12-17 23:41:49

        Description:
        Deplace le joueur (l'image du vaisseau), en fonction des touches, sans sortir des limites du canvas.

        Parametres:
            event [event] : les fleches du clavier (up, right,...)
        '''
        side = event.keysym
        # print(side)
        if side == "Left":
            if self.position[0]-self.speed > 0:
                self.position[0] -= self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Right":
            if self.position[0]+self.speed < self.canvas.winfo_width():
                self.position[0] += self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Up":
            if self.position[1]-self.speed > 0+50:
                self.position[1] -= self.speed
            else:
                self.position[1] = self.position[1]

        if side == "Down":
            if self.position[1]+self.speed < self.canvas.winfo_height()-50:
                self.position[1] += self.speed
            else:
                self.position[1] = self.position[1]
        # print(self.__dict__)
        self.canvas.coords(self.form, self.position[0], self.position[1])


class Monster(Entity):

    def deplacement_monstre(self):   # speed est un nombre de pixels
        if self.position[0] == 0:
            while self.position[0] != Sp_Inv.x_fenetre_max:
                if self.position[0]+self.speed < Sp_Inv.x_fenetre_max:
                    self.position[0] += self.speed
                else:
                    self.position[0] = Sp_Inv.x_fenetre_max
                print(self.position)
                time.sleep(1)

        if self.position[0] == Sp_Inv.x_fenetre_max:
            while self.position[0] != 0:
                if self.position[0]-self.speed > 0:
                    self.position[0] -= self.speed
                else:
                    self.position[0] = 0
                print(self.position)
                time.sleep(1)

    # def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
    #     if nb == 0:
    #         self.direction_tir = "up"
    #     elif nb == 1:
    #         self.direction_tir = "down"


if __name__ == '__main__':
    player = Player(3, "vaisseau_player.jpg")
    monster = Monster(lives=3, speed=10, position=[300, Sp_Inv.y_fentre_max])
    monster.deplacement_monstre()
