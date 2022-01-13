import random
import tkinter as tk
import time
from PIL import Image, ImageTk
import os, sys


class MainView(tk.Frame):
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
        self.configure(highlightbackground="yellow", highlightthickness=2)
        self.pack(side="top", fill="both", expand=True)
        # frame pour afficher les info du jeu : nbr de vie, score, boutons...
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=0, column=0, sticky="nsew")
        self.info_frame.configure(highlightbackground="red", highlightthickness=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # canvas qui aura toutes les entitées du jeu.
        self.cv = tk.Canvas(self)
        self.cv.configure(highlightbackground="blue", highlightthickness=2)
        self.cv.grid(row=1, column=0, sticky="nsew")

        bouton_quitter = tk.Button(
            self.info_frame, text="Quitter", fg="black", command=self.master.destroy
        )
        bouton_quitter.grid(row=0, column=4, sticky="ensw")
        bouton_new_game = tk.Button(
            self.info_frame, text="New Game", fg="black", command=self.new_game
        )
        bouton_new_game.grid(row=0, column=3, sticky="ensw")


        # ajout d'un boutton menu pour choisir le background
        background_menu = tk.Menubutton(self.info_frame, text="Background", fg="black")
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

    def new_game(self):
        os.execl(sys.executable, sys.executable, *sys.argv)


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
    def __init__(self, canvas,main_view):
        self.canvas = canvas
        self.main_view = main_view
        self.player = Player(
            "player",
            lives=3,
            img="images/vaisseau_player.png",
            position=[self.canvas.winfo_width() / 2, self.canvas.winfo_height() * 0.75],
            canvas=self.canvas,
        )
        self.player.create(tag="player")
        self.canvas.focus_set()


        self.score = 0
        self.create_obstacle()
        self.score_printed = tk.StringVar()
        label_score = tk.Label(
            self.main_view.info_frame, textvariable=self.score_printed, fg="black"
        )
        label_score.grid(row=0, column=5, sticky="ensw")
        self.score_printed.set("Score : "+str(self.score))

        self.lives_printed = tk.StringVar()
        label_lives = tk.Label(
            self.main_view.info_frame, textvariable=self.lives_printed, fg="black"
        )
        label_lives.grid(row=0, column=6, sticky="ensw")
        self.lives_printed.set("     Lives : "+str(self.player.lives))




    def level_monster(self, lvl):
        self.lvl = lvl
        x = self.canvas.winfo_width() / lvl
        self.list_monster = []
        for i in range(lvl):
            self.monster = Monster(
                "monster",
                1,
                self.canvas,
                lvl * 3,
                position=[x, 70],
                img="images/vaisseau_enemy_3.png",
            )
            self.monster.direction = "r"
            self.monster.create(tag="monster")
            self.list_monster.append(self.monster)
            x += 150
        self.fct_monsters()
        self.shoot_monster()
        self.fct_player()
       # self.boss_stage()

    def fct_monsters(self):
        for monster in self.list_monster:
            monster.deplacement_monstre()
            monster.deplacement_bullet()
            monster.suppr_bullet()
        self.canvas.after(17, self.fct_monsters)

    def fct_player(self):
        self.player.deplacement_bullet()
        self.player.suppr_bullet()
        self.canvas.after(17, self.fct_player)

    def shoot_monster(self):
        if len(self.list_monster) - 1 != 0:
            rand = random.randint(0, len(self.list_monster) - 1)
            shoot_monster = self.list_monster[rand]
            shoot_monster.shoot(None)
            self.canvas.after(self.lvl * 100, self.shoot_monster)

    # def boss_stage(self):
    #     if self.list_monster == [] and self.monster.name == "monster":
    #         x = self.canvas.winfo_width()
    #         self.monster = Monster(
    #             "Boss",
    #             10,
    #             self.canvas,
    #             speed= 20,
    #             position = [x, 40 ],
    #             img="images/vaisseau_enemy_boss_1.png"
    #         )
    #     if self.monster.name == "Boss":
    #         self.dead()
    #     self.monster.direction = "r"
    #     self.monster.create(tag="monster")
    #     self.list_monster.append(self.monster)
    #     self.canvas.after(20,self.boss_stage)

    def create_obstacle(self):
        i = random.randint(1,3)
        print(i)
        x =  50   # self.canvas.winfo_width() / 3
        y =  400   # self.canvas.winfo_height() / 2
        self.photo_obstacle = tk.PhotoImage(file="images/obstacle_transparent.png")
        for nb in range(i):
            
            self.canvas.create_image(
                x, y, image=self.photo_obstacle
            )
            print('yes')
            x +=300


    def dead(self):
        for monster in self.list_monster:
            if monster.lives <= 0:
                if self.monster.name=="monster":
                    self.score += 15
                elif self.monster.name=="Boss":
                    self.score += 150
                self.score_printed.set("Score : "+str(self.score))
                
                self.canvas.delete(monster.form)
                self.list_monster.remove(monster)
                
                for b in monster.bullets:
                    self.canvas.delete(b)
                del monster
        if self.player.lives <= 0:
            self.canvas.delete(self.player.form)
            del self.player
            restart = tk.messagebox.askquestion("Rejouer ?", "Voulez vous rejouer? ")
            if restart.upper() == "YES":
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif restart.upper() == "NO":
                sys.exit()

        self.lives_minus()
        self.canvas.after(10, self.dead)

    def lives_minus(self):
        bullet_suppr = []
        for monster in self.list_monster:
            # print(monster.lives)
            for b in self.player.bullets.keys():
                if (
                    (monster.position[0] - 47.0)
                    <= self.player.bullets[b][0]
                    <= (monster.position[0] + 47.0)
                ) and (
                    (monster.position[1] - 47.0)
                    <= self.player.bullets[b][1]
                    <= (monster.position[1] + 47.0)
                ):
                    bullet_suppr.append(b)
                    monster.lives -= 1
            if bullet_suppr != []:
                for b in bullet_suppr:
                    self.canvas.delete(b)
                    self.player.bullets.pop(b)

            bullet_suppr = []
            for b in monster.bullets.keys():
                if (
                    (self.player.position[0] - 47.0)
                    <= monster.bullets[b][0]
                    <= (self.player.position[0] + 47.0)
                ) and (
                    (self.player.position[1] - 47.0)
                    <= monster.bullets[b][1]
                    <= (self.player.position[1] + 47.0)
                ):
                    bullet_suppr.append(b)
                    self.player.lives -= 1
                    self.lives_printed.set("     Lives : "+str(self.player.lives))
            if bullet_suppr != []:
                for b in bullet_suppr:
                    self.canvas.delete(b)
                    monster.bullets.pop(b)
                    bullet_suppr.remove(b)


class Entity(World):
    """
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu, regroupe toutes les données essentielles sur une entité du jeu.
    """

    def __init__(self, name, lives, canvas, speed=40, position=[0, 0], img=""):
        # nombre de vies (3 pour le joueur et a definir pour les enemies)
        self.name = name
        self.lives = lives
        self.position = position  # position sur la map
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
                self.bullets[bullet][1] -= 20
            else:
                self.bullets[bullet][1] += 5
            self.canvas.coords(
                bullet,
                self.bullets[bullet][0] - 5,
                self.bullets[bullet][1] - 5,
                self.bullets[bullet][0] + 5,
                self.bullets[bullet][1] + 5,
            )
        # self.canvas.after(20, self.deplacement_bullet)

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
        # self.canvas.after(20, self.suppr_bullet)

    # def lives_minus(self, ennemi):
    #     list_suppr = []
    #     for b in self.bullets.keys():
    #         # print(ennemi.position)
    #         if (
    #             (ennemi.position[0] - 47.0)
    #             <= self.bullets[b][0]
    #             <= (ennemi.position[0] + 47.0)
    #         ) and (
    #             (ennemi.position[1] - 47.0)
    #             <= self.bullets[b][1]
    #             <= (ennemi.position[1] + 47.0)
    #         ):
    #             list_suppr.append(ennemi)
    #             ennemi.lives -= 1  # on a la balle en 0 et l'ennemi en 1

    #     """
    #     Faut il mieux return la list_suppr???
    #     et tt suppr dans la class world?
    #     """
    #     return list_suppr
    #     # if list_suppr != []:
    #     #     try:
    #     #         for element in list_suppr:
    #     #             self.canvas.delete(element)
    #     #         ennemi.__del__()
    #     #         print(list_suppr[1])

    #     #     except IndexError:
    #     #         pass
    #     # try:
    #     #     self.canvas.after(10, lambda: self.lives_minus(ennemi))
    #     # except Exception:
    #     #     return


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

    # def __del__(self):
    #     del self
    #     print("you lose")

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
        if self.position[0] < self.canvas.winfo_width() - 50 and self.direction == "r":
            self.position[0] += self.speed
        elif (
            self.position[0] >= self.canvas.winfo_width() - 50 and self.direction == "r"
        ):
            self.direction = "l"
        elif self.position[0] > 0 + 50 and self.direction == "l":
            self.position[0] -= self.speed
        elif self.position[0] <= 0 + 50 and self.direction == "l":
            self.direction = "r"
        self.canvas.coords(self.form, self.position[0], self.position[1])
        # self.canvas.after(100, lambda: self.deplacement_monstre(direction))

    # def __del__(self):
    #     del self
    #     print("a monster has been deleted")

    # def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
    #     if nb == 0:
    #         self.direction_tir = "up"
    #     elif nb == 1:
    #         self.direction_tir = "down"
