import random
import tkinter as tk
import os, sys
from PIL import Image, ImageTk
from tkinter import messagebox


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
        self.configure(highlightbackground="yellow", highlightthickness=2)
        self.pack(side="top", fill="both", expand=True)
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
            info_frame, text="New Game", fg="black", command=self.new_game
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

    def new_game(self):
        os.execl(sys.executable, sys.executable, *sys.argv)


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
        self.lvl = 1
        self.list_monster = []
        self.canvas.focus_set()
        self.creation_lvl()
        self.shoot_monster()

    def creation_lvl(self):
        if self.list_monster == [] and self.lvl < 5:
            self.level_monster(self.lvl, 70)
            self.lvl += 1
        if self.list_monster == []:
            for i in range(int(self.lvl / 5)):
                self.level_monster(self.lvl - (i + 1) * 5, i * 140 + 70)
            self.lvl += 1
        # on lance les fonctions liers a player et a monster
        self.fct_monster()
        self.fct_player()
        self.dead()
        self.canvas.after(17, self.creation_lvl)

    def level_monster(self, lvl, posy):
        x = self.canvas.winfo_width() / (lvl + 1)
        for i in range(lvl):
            self.monster = Monster(
                "monster",
                int(lvl / 2 + 1),
                self.canvas,
                lvl * 3,
                position=[x, posy],
                img="images/vaisseau_enemy_3.png",
            )
            self.monster.direction = "r"
            self.monster.create(tag="monster")
            self.list_monster.append(self.monster)
            x += 150

    def fct_monster(self):
        for monster in self.list_monster:
            monster.deplacement_monstre()
            monster.deplacement_bullet()
            monster.suppr_bullet()

    def fct_player(self):
        self.player.deplacement_bullet()
        self.player.suppr_bullet()

    def shoot_monster(self):
        if len(self.list_monster) - 1 != 0:
            try:
                rand = random.randint(0, len(self.list_monster) - 1)
                shoot_monster = self.list_monster[rand]
                shoot_monster.shoot(None)
            except ValueError:
                pass
        self.canvas.after(int((self.lvl / 2 * 100)), self.shoot_monster)

    def dead(self):
        for monster in self.list_monster:
            if monster.lives <= 0:
                self.canvas.delete(monster.form)
                self.list_monster.remove(monster)
                for b in monster.bullets:
                    self.canvas.delete(b)
        if self.player.lives <= 0:
            self.canvas.delete(self.player.form)
            restart = messagebox.askquestion("Rejouer ?", "Voulez vous rejouer? ")
            if restart.upper() == "YES":
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif restart.upper() == "NO":
                sys.exit()
        # on lance la fct qui enleve des vies aux entité
        self.lives_minus()
        # self.canvas.after(10, self.dead)

    def lives_minus(self):  # faut changer le nom de cette fct
        for monster in self.list_monster:
            self.bullet_suppr = self.collision(self.player.bullets, monster)
            if self.bullet_suppr != []:
                for b in self.bullet_suppr:
                    self.canvas.delete(b)
                    self.player.bullets.pop(b)
            self.bullet_suppr = self.collision(monster.bullets, self.player)
            if self.bullet_suppr != []:
                for b in self.bullet_suppr:
                    self.canvas.delete(b)
                    monster.bullets.pop(b)

    def collision(self, bullets, entity):
        bullet_suppr = []
        for b in bullets.keys():
            if (
                (entity.position[0] - 50.0)
                <= bullets[b][0]
                <= (entity.position[0] + 50.0)
            ) and (
                (entity.position[1] - 50.0)
                <= bullets[b][1]
                <= (entity.position[1] + 50.0)
            ):
                bullet_suppr.append(b)
                entity.lives -= 1
        return bullet_suppr


class Entity(World):
    """
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu, regroupe toutes les données essentielles sur une entité du jeu.
    """

    def __init__(self, name, lives, canvas, speed=40, position=[0, 0], img=""):
        self.name = name
        self.lives = lives
        self.position = position
        self.speed = speed
        self.img = img
        self.canvas = canvas
        self.bullets = {}

    def create(self, tag):
        self.photo = tk.PhotoImage(file=self.img)
        self.form = self.canvas.create_image(
            self.position[0], self.position[1], image=self.photo, tag=tag
        )

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

    def suppr_bullet(self):
        """
        suppr_bullet
        dev: Joseph
        date: 2021-12-17 23:35:25

        Description:
        On parcours la liste des bullets, on enregistres celles qui sortent dee la fenetre,
        puis on les suprimes du canvas et du dictionnaire (on ne peut pas supprimer dans un dict pendant une iteration)
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
        self.canvas.coords(self.form, self.position[0], self.position[1])


class Monster(Entity):
    def deplacement_monstre(self):
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
