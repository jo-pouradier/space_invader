from random import *
import tkinter as tk
import time
from PIL import Image, ImageTk
import os, sys


class main_view(tk.Frame):
    """
    main_view
    dev: Joseph
    date: 2021-12-16 09:54:25

    Description:
    Cree la fenetre principale du jeu space invader, avec ses proporiété

    Parametres:
        tk [tk] : cree une frame tkinter dans la page principale
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # frame pour afficher les info du jeu : nbr de vie, score, boutons...
        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, sticky="nsew")
        info_frame.configure(highlightbackground="red", highlightthickness=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # canvas qui aura toutes les entitées du jeu.
        self.cv = tk.Canvas(self)
        self.cv.configure(highlightbackground="blue", highlightthickness=2)
        self.cv.grid(row=1, column=0, sticky="nsew")

        bouton_quitter = tk.Button(
            info_frame, text="Quitter", fg="black", command=self.master.destroy
        )
        bouton_quitter.grid(row=0, column=4, sticky="ensw")
        bouton_new_game = tk.Button(
            info_frame, text="New Game", fg="black", command=None
        )
        bouton_new_game.grid(row=0, column=3, sticky="ensw")

        # ajout d'un boutton menu pour choisir le background
        background_menu = tk.Menubutton(info_frame, text="Background", fg="black")
        background_menu.menu = tk.Menu(background_menu)
        background_menu["menu"] = background_menu.menu
        background_menu.menu.add_command(
            label="Terre",
            command=lambda: [
                self.new_background("images/background_space_1.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Terre 2",
            command=lambda: [
                self.new_background("images/background_space_2.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Galaxy",
            command=lambda: [
                self.new_background("images/background_space_3.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Voie Lactée",
            command=lambda: [
                self.new_background("images/background_space_4.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.grid(row=0, column=2, sticky="esw")

        self.centrage()

    def centrage(self):
        """
        centrage
        dev: Joseph
        date: 2021-11-27 20:54:14

        Description:
        centre la fenetre tkinter sur l'ecran de l'utilisateur

        Parametres:
            self [Frame] : une frame tkinter
        """
        self.sizeX = self.master.winfo_screenwidth() * 0.9
        self.sizeY = self.master.winfo_screenheight() * 0.9
        positionX = self.master.winfo_screenwidth() / 2 - (self.sizeX) / 2
        positionY = self.master.winfo_screenheight() / 2 - (self.sizeY) / 2
        self.master.geometry(
            "{}x{}+{}+{}".format(
                int(self.sizeX), int(self.sizeY), int(positionX), int(positionY)
            )
        )

    def new_background(self, img):
        self.background_image = img
        self.space_image = Image.open(img)
        self.space_image = self.space_image.resize(
            (self.cv.winfo_width(), self.cv.winfo_height()), Image.ANTIALIAS
        )
        self.background_resize = ImageTk.PhotoImage(self.space_image)
        self.background = self.cv.create_image(
            0, 0, image=self.background_resize, anchor="nw", tag="background"
        )


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


class World:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player = Player(
            "player",
            lives=3,
            img="images/vaisseau_player.png",
            position=[self.canvas.winfo_width() / 2, self.canvas.winfo_height() * 0.75],
            canvas=self.canvas,
        )
        self.player.create(tag="player")

        # self.monster = Monster(
        #     "monster",
        #     1,
        #     self.canvas,
        #     position=[self.canvas.winfo_width() / 4, 70],
        #     img="images/vaisseau_enemy_3.png",
        # )
        # self.monster.create(tag="monster")
        # self.canvas.tag_raise("monster")
        # self.monster.deplacement_monstre()

        # self.player.lives_minus(self.monster)
        # self.monster.lives_minus(self.player)
        self.canvas.focus_set()

    def level_monster(self, lvl):
        self.lvl = lvl
        x = self.canvas.winfo_width() / lvl
        self.list_monster = []
        for i in range(lvl):
            monster = Monster(
                "monster",
                1,
                self.canvas,
                position=[x, 70],
                img="images/vaisseau_enemy_3.png",
            )
            monster.create(tag="monster")
            self.list_monster.append(monster)
            x += 150
        
    def moove_monsters(self):
        #verifier celui de droite et celui de gauche pour choisir la direction
        

    def dead(self):
        if self.player.lives == 0:
            self.canvas.delete(self.player.form)
            self.player.__del__()
            restart = tk.messagebox.askquestion("Rejouer ?", "Voulez vous rejouer? ")
            if restart.upper() == "YES":
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif restart.upper() == "NO":
                sys.exit()
        self.canvas.after(50, self.dead)

    def player_shoot(self):
        self.player.deplacement_bullet()
        self.player.suppr_bullet()

    def monster_shoot(self):
        self.monster.shoot(None)
        self.monster.deplacement_bullet()
        self.monster.suppr_bullet()


class Entity(World):
    """
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu, regroupe toutes les données essentielles sur une entité du jeu.
    """

    def __init__(self, name, lives, canvas, speed=1, position=[0, 0], img=""):
        # nombre de vies (3 pour le joueur et a definir pour les enemies)
        self.name = name
        self.lives = lives
        self.position = position  # position sur la map
        self.damage = 1
        self.border = (
            0  # désigne la ligne que le joueur ou le monstre ne peux pas dépasser
        )
        self.speed = speed
        self.img = img
        self.canvas = canvas
        self.bullets = {}

    def create(self, tag):
        self.photo = tk.PhotoImage(file=self.img)
        self.form = self.canvas.create_image(
            self.position[0], self.position[1], image=self.photo, tag=tag
        )

    # je crois pas quelle soit utile...
    # def placement(self, position):  # positionne l'entité dur la map
    #     if len(position) == 2 and position[0] >= 0 and position[1] >= 0:
    #         self.position[0] = position[0]
    #         self.position[1] = position[1]
    #     else:
    #         self.position.append([0, 0])

    # def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
    #     if nb == 0:
    #         self.direction_tir = 'up'
    #     elif nb == 1:
    #         self.direction_tir = "down"

    def shoot(self, event):
        """
        shoot
        dev: Joseph
        date: 2021-12-17 23:31:43

        Description:
        Creation des bullets en fonction de l'event <space>, pour le player, et par rien pour les monstres.
        On met dans un dictionnaire l'objet tkinter (oval) et sa position ( par rapport en l'envoyeur).

        Parametres:
            event [event] : <space> pour le payer ou rien pour un monstre.
        """
        try:
            key = event.keysym
        except AttributeError:
            key = None
        # on passe par l'event (<space>) pour le player et par rien pour les monstres.
        if key == "space":
            self.bullets[
                (
                    self.canvas.create_oval(
                        self.position[0] - 5,
                        self.position[1] - 5,
                        self.position[0] + 5,
                        self.position[1] + 5,
                        fill="green",
                        tag="bullet",
                    )
                )
            ] = [self.position[0], self.position[1]]

        else:
            self.bullets[
                (
                    self.canvas.create_oval(
                        self.position[0] - 5,
                        self.position[1] - 5,
                        self.position[0] + 5,
                        self.position[1] + 5,
                        fill="red",
                    )
                )
            ] = [self.position[0], self.position[1]]

    def deplacement_bullet(self):
        """
        deplacement_bullet
        dev: Joseph
        date: 2021-12-17 23:34:09

        Description:
        En fonction de self (player ou monstre), la balles se deplace vers le haut ou vers le bas.
        """

        for bullet in self.bullets.keys():
            if self.name == "player":
                self.bullets[bullet][1] -= 5
            else:
                self.bullets[bullet][1] += 5
            self.canvas.coords(
                bullet,
                self.bullets[bullet][0] - 5,
                self.bullets[bullet][1] - 5,
                self.bullets[bullet][0] + 5,
                self.bullets[bullet][1] + 5,
            )
        self.canvas.after(20, self.deplacement_bullet)

    def suppr_bullet(self):
        """
        suppr_bullet
        dev: Joseph
        date: 2021-12-17 23:35:25

        Description:
        On parcours la liste des bullets, on enregistres celles qui sortent dee la fenetre,
        puis on les suprimes du canvas et du dictionnaire.
        """

        list_suppr = []
        for bullet in self.bullets.keys():
            if (
                self.bullets[bullet][1] < 0
                or self.bullets[bullet][1] > self.canvas.winfo_height()
            ):
                list_suppr.append(bullet)
        for b in list_suppr:
            self.canvas.delete(b)
            self.bullets.pop(b)
        self.canvas.after(20, self.suppr_bullet)

    def lives_minus(self, ennemi):
        list_suppr = []
        for b in self.bullets.keys():
            # print(ennemi.position)
            if (
                (ennemi.position[0] - 47.0)
                <= self.bullets[b][0]
                <= (ennemi.position[0] + 47.0)
            ) and (
                (ennemi.position[1] - 47.0)
                <= self.bullets[b][1]
                <= (ennemi.position[1] + 47.0)
            ):
                list_suppr.append(b)
                list_suppr.append(ennemi)
                ennemi.lives -= 1  # on a la balle en 0 et l'ennemi en 1
        if list_suppr != []:
            try:
                self.canvas.delete(list_suppr[0])
                self.bullets.pop(list_suppr[0])
            except IndexError:
                pass
        try:
            self.canvas.after(10, lambda: self.lives_minus(ennemi))
        except Exception:
            return


class Player(Entity):
    """
    Player
    dev: Adrien
    date: 2021-12-17 23:40:06

    Description:
    Classe qui donne les methodes qui s'appliqueront a player en tant qu'entité du jeu.

    Parametres:
        Entity [class] : voir description de la class
    """

    def __del__(self):
        print("you lose")

    def deplacement_player(self, event):
        """
        deplacement_player
        dev: Adrien et Joseph
        date: 2021-12-17 23:41:49

        Description:
        Deplace le joueur (l'image du vaisseau), en fonction des touches, sans sortir des limites du canvas.

        Parametres:
            event [event] : les fleches du clavier (up, right,...)
        """
        side = event.keysym
        # print(side)
        if side == "Left":
            if self.position[0] - self.speed > 0:
                self.position[0] -= self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Right":
            if self.position[0] + self.speed < self.canvas.winfo_width():
                self.position[0] += self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Up":
            if self.position[1] - self.speed > 0 + 45:
                self.position[1] -= self.speed
            else:
                self.position[1] = self.position[1]

        if side == "Down":
            if self.position[1] + self.speed < self.canvas.winfo_height():
                self.position[1] += self.speed
            else:
                self.position[1] = self.position[1]
        # print(self.__dict__)
        self.canvas.coords(self.form, self.position[0], self.position[1])


class Monster(Entity):
    def deplacement_monstre(self, direction="r"):  # speed est un nombre de pixels
        # if self.position[0] != 0:  # on est a x=0 (gauche)
        #     while self.position[0] != self.canvas.winfo_width():
        #         if self.position[0]+self.speed < self.canvas.winfo_width():
        #             self.position[0] += self.speed
        #         else:
        #             self.position[0] = self.canvas.winfo_width()
        #         # print(self.position)
        #         time.sleep(1)

        # if self.position[0] != self.canvas.winfo_width():
        #     while self.position[0] != 0:
        #         if self.position[0]-self.speed > 0:
        #             self.position[0] -= self.speed
        #         else:
        #             self.position[0] = 0
        #         print(self.position)
        #         time.sleep(1)
        # self.canvas.coords(self.form, self.position[0], self.position[1])
        # self.canvas.after(20, self.deplacement_monstre)

        if self.position[0] < self.canvas.winfo_width() - 50 and direction == "r":
            self.position[0] += self.speed
        elif self.position[0] >= self.canvas.winfo_width() - 50 and direction == "r":
            direction = "l"
        elif self.position[0] > 0 + 50 and direction == "l":
            self.position[0] -= self.speed
        elif self.position[0] <= 0 + 50 and direction == "l":
            direction = "r"
        self.canvas.coords(self.form, self.position[0], self.position[1])
        self.canvas.after(10, lambda: self.deplacement_monstre(direction))

    def __del__(self):
        print("a monster has been deleted")

    # def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
    #     if nb == 0:
    #         self.direction_tir = "up"
    #     elif nb == 1:
    #         self.direction_tir = "down"
