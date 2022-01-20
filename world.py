import player
import monster
import entity
import random
from tkinter import messagebox
import os
import sys

class World:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lvl = 0
        self.list_monster = []
        self.list_asteroide = []
        # self.main_view = main_view
        self.player = player.Player(
            "player",
            lives=3,
            img="images/vaisseau_player.png",
            position=[self.canvas.winfo_width(
            ) / 2, self.canvas.winfo_height() * 0.75],
            canvas=self.canvas,
        )
        self.player.create(tag="player")
        self.canvas.focus_set()

    def level_monster(self, lvl):
        self.lvl = lvl
        x = self.canvas.winfo_width() / lvl
        self.list_monster = []
        self.shoot_monster()

    def creation_lvl(self):
        if self.list_monster == [] and self.lvl == 4:
            self.boss_stage()
            self.lvl += 1

        if self.list_monster == []:
            self.level_monster(self.lvl, 70)
            self.lvl += 1

        if self.list_monster == [] and self.lvl > 5:
            # on affiche les monstres par rangée de 5
            for i in range(self.lvl // 5):
                if i == 0:
                    self.level_monster(self.lvl // 5, 70)
                else:
                    self.level_monster(5, (i + 1) * 140 + 70)
            self.lvl += 1

    def level_monster(self, lvl, posy):
        x = self.canvas.winfo_width() / (lvl + 1)
        for i in range(lvl):
            self.monster = monster.Monster(
                "monster",
                int(lvl / 2 + 1),
                self.canvas,
                lvl * 5,
                position=[x, posy],
                img="images/vaisseau_enemy_3.png",
            )
            self.monster.direction = "r"
            self.monster.create(tag="monster")
            self.list_monster.append(self.monster)
            self.list_asteroide.clear()
            self.create_obstacle()
            x += 150
        self.fct_monster()
        self.shoot_monster()
        self.fct_player()

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
        self.canvas.after(int((self.lvl * 100)), self.shoot_monster)

    def boss_stage(self):
        if self.list_monster == [] and self.lvl == 4 and self.monster.name == "monster":
            x = self.canvas.winfo_width()
            self.monster = monster.Monster(
                "Boss",
                10,
                self.canvas,
                speed=20,
                position=[x, 40],
                img="images/vaisseau_enemy_boss_1.png",
            )
        if self.monster.name == "Boss":
            self.dead()
        self.monster.direction = "r"
        self.monster.create(tag="monster")
        self.list_monster.append(self.monster)

    def create_obstacle(self):
        i = random.randint(1, 3)
        x = 50  # self.canvas.winfo_width() / 3
        y = 400  # self.canvas.winfo_height() / 2)
        for nb in range(i):
            self.asteroide = entity.Entity(
                "asteroide",
                1000,
                self.canvas,
                speed=0,
                position=[x, y],
                img="images/obstacle_transparent_v3.png",
            )
            self.asteroide.create(tag="asteroide")
            self.list_asteroide.append(self.asteroide)
            x += 500

    def dead(self):
        for monster in self.list_monster:
            if monster.lives <= 0:

                self.canvas.delete(monster.form)
                self.list_monster.remove(monster)

                for b in monster.bullets:
                    self.canvas.delete(b)
                self.player.score += 10
        if self.player.lives <= 0:
            self.canvas.delete(self.player.form)
            restart = messagebox.askquestion(
                "Perdu",
                "Votre score est de : "
                + str(self.player.score)
                + " points. Voulez vous rejouer? ",
            )
            if restart.upper() == "YES":
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif restart.upper() == "NO":
                sys.exit()
        # on lance la fct qui enleve des vies aux entité
        self.lives_minus()

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

            for asteroide in self.list_asteroide:
                self.bullet_suppr = self.collision(
                    self.player.bullets, asteroide)

                if self.bullet_suppr != []:
                    for b in self.bullet_suppr:
                        self.canvas.delete(b)
                        self.player.bullets.pop(b)
                self.bullet_suppr = self.collision(monster.bullets, asteroide)

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