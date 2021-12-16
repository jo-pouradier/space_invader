from random import *
from tkinter import *
import time

class Space_invaders():

    def __init__(self,fenetre,player,x_max,y_max):
        self.fenetre = fenetre
        self.enemy = []
        self.player = player
        self.x_fenetre_max = x_max
        self.y_fentre_max = y_max


Sp_Inv = Space_invaders("myWindow","player",300,300)  # initialisation test 
class Entity():

    def __init__(self,lives,speed = 1, position = [0,0]):
        self.forme = []        # les petits carrés à afficher
        self.lives = lives     # nombre de vies (3 pour le joueur et a definir pour les enemies)
        self.position = position  # position sur la map
        self.damage = 1
        self.border = 0  # désigne la ligne que le joueur ou le monstre ne peux pas dépasser
        self.speed = speed

    def

    def placement(self,position):  # positionne l'entité dur la map
        if len(position) == 2 and position[0]>=0 and position[1]>=0:
            self.position.append(position)
        else:
            self.position.append([0,0])


    def shoot(self,nb):  # nb=0 pour le player et nb=1 pour les monstres
        if nb==0:
            self.direction_tir = "up"
        elif nb==1:
            self.direction_tir = "down"



class Player(Entity):
    def deplacement_player(self,side): # side = gauche ou droite
        if side == "left":
            if self.position[0]-self.speed>0:
                self.position[0] -= self.speed
            else:
                self.position[0] = 0
        
        if side == "right":
            if self.position[0]+self.speed<Sp_Inv.x_fenetre_max:
                self.position[0] += self.speed
            else:
                self.position[0] = Sp_Inv.x_fenetre_max

        if side == "down":
            if self.position[1]-self.speed>0:
                self.position[1] -= self.speed
            else:
                self.position[1] = 0
        
        if side == "up":
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

        elif self.position[0] == Sp_Inv.x_fenetre_max:
            while self.position[0] != 0:
                if self.position[0]-self.speed>0:
                    self.position[0] -= self.speed
                else: 
                    self.position[0] = 0
                print(self.position)
                time.sleep(1)





player = Player(3)
monster = Monster(3,10,[300,Sp_Inv.y_fentre_max])
monster.deplacement_monstre()








