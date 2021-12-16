from random import *
import tkinter as tk
import time


class Space_invaders():
    '''
    Space_invaders
    dev: Adrien
    date: 2021-12-16 09:55:42

    Description:
    Classe qui regroupe toutes les entitées du jeu.
    '''

    def __init__(self, fenetre, player, x_max, y_max):
        self.fenetre = fenetre
        self.enemy = []
        self.player = player
        self.x_fenetre_max = x_max
        self.y_fentre_max = y_max


Sp_Inv = Space_invaders("myWindow", "player", 300, 300)  # initialisation test


class Entity():
    '''
    Entity
    dev: Adrien
    date: 2021-12-16 09:56:36

    Description:
    Classe de position des entitées du jeu
    '''
    def __init__(self,lives,speed = 1, position = [0,0],img = ""):
        self.lives = lives     # nombre de vies (3 pour le joueur et a definir pour les enemies)
        self.position = position  # position sur la map
        self.damage = 1
        self.border = 0  # désigne la ligne que le joueur ou le monstre ne peux pas dépasser
        self.speed = speed
        self.img = img

    def create(self):
        self.photo = tk.PhotoImage(file=self.img)
        self.canvas = tk.Canvas.create_image(self.position[0], self.position[1], image = self.photo)

    def placement(self, position):  # positionne l'entité dur la map
        if len(position) == 2 and position[0] >= 0 and position[1] >= 0:

            self.position.append(position)
        else:
            self.position.append([0, 0])

    def shoot(self, nb):  # nb=0 pour le player et nb=1 pour les monstres
        if nb == 0:
            self.direction_tir = "up"
        elif nb == 1:
            self.direction_tir = "down"


class Player(Entity):
    def deplacement_player(self,event): # side = gauche ou droite
        side = event.keysym

        if side == "<Left>":
            if self.position[0]-self.speed>0:
                self.position[0] -= self.speed
            else:
                self.position[0] = 0
        
        if side == "<Right>":
            if self.position[0]+self.speed<Sp_Inv.x_fenetre_max:
                self.position[0] += self.speed
            else:
                self.position[0] = Sp_Inv.x_fenetre_max

        if side == "<Up>":
            if self.position[1]-self.speed>0:
                self.position[1] -= self.speed
            else:
                self.position[1] = 0
        
        if side == "<Down>":
            if self.position[1]+self.speed<Sp_Inv.y_fenetre_max:
                self.position[1] += self.speed
            else:
                self.position[1] = Sp_Inv.y_fenetre_max
        print(self.position)


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


if __name__=='__main__':
    player = Player(3,"vaisseau_player.jpg")
    monster = Monster(3,10,[300,Sp_Inv.y_fentre_max])
    monster.deplacement_monstre()








