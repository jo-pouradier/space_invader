from random import *
import tkinter as tk
import time

# pas sur qu'elle soit utile


class Space_invaders():
    '''
    Space_invaders
    dev: Adrien
    date: 2021-12-16 09:55:42

    Description:
    Classe qui regroupe toutes les entitées du jeu.
    '''

    def __init__(self, canvas, player, x_max, y_max):
        self.canvas = canvas
        self.enemy = []
        self.player = player
        self.x_fenetre_max = x_max
        self.y_fentre_max = y_max


# utile??
Sp_Inv = Space_invaders("myWindow", "player", 300, 300)  # initialisation test


class Entity():
    '''
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu
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
        key = event.keysym
        if key == 'space':
            self.bullets[(self.canvas.create_oval(
                self.position[0]-5, self.position[1]-5, self.position[0]+5, self.position[1]+5, fill='green'))] = [self.position[0], self.position[1]]

        else:
            self.bullets.append(self.canvas.create_oval(
                self.position[0]-5, self.position[1]-5, self.position[0]+5, self.position[1]+5, fill='red'))

    def deplacement_bullet(self):
        for bullet in self.bullets.keys():
            if self.name == 'player':
                self.bullets[bullet][1] -= 5
            else:
                self.bullets[bullet][1] += 5
            self.canvas.coords(
                bullet, self.bullets[bullet][0]-5, self.bullets[bullet][1]-5, self.bullets[bullet][0]+5, self.bullets[bullet][1]+5)
        self.canvas.after(20, self.deplacement_bullet)

    def suppr_bullet(self):
        list_suppr = []
        # A FAIRE
        # il faut faire la difference pour player et monster
        for bullet in self.bullets.keys():
            if self.bullets[bullet][1] < 200:
                list_suppr.append(bullet)
        for b in list_suppr:
            self.canvas.delete(b)
            self.bullets.pop(b)
        self.canvas.after(20, self.suppr_bullet)


class Player(Entity):

    def deplacement_player(self, event):  # side = gauche ou droite
        side = event.keysym
        print(side)
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
        print(self.__dict__)
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

    # def deplacement_player(self):

    def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
        if nb == 0:
            self.direction_tir = "up"
        elif nb == 1:
            self.direction_tir = "down"


if __name__ == '__main__':
    player = Player(3, "vaisseau_player.jpg")
    monster = Monster(lives=3, speed=10, position=[300, Sp_Inv.y_fentre_max])
    monster.deplacement_monstre()
