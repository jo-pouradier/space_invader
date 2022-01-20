import player
import monster
import entity
import random
from tkinter import messagebox
import os
import sys


class World:
    '''
    World
    dev: Adrien et Joseph
    date: 2022-01-20 18:38:29

    Description:
    Classe qui represente tout les objets du canvas.
    '''

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
        '''
        creation_lvl
        dev: Joseph et Adrien
        date: 2022-01-20 18:40:28

        Description:
        Fonction qui cree les monstres (de la classe Monster en fonction du level de la partie.
        '''
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
        '''
        level_monster
        dev: Joseph et Adrien
        date: 2022-01-20 18:41:39

        Description:
        Cree les monstres avec des attributs different selon le lvl de la partie

        Parametres:
            lvl [int] : level de la partie en cours
            posy [int] : position des monstres selon l'axe y.
        '''
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
        '''
        fct_monster
        dev: Joseph
        date: 2022-01-20 18:44:16

        Description:
        on parcours la liste de monstre et on leur applique les fonctions importantes (déplacment et fct des missiles).
        '''
        for monster in self.list_monster:
            monster.deplacement_monstre()
            monster.deplacement_bullet()
            monster.suppr_bullet()

    def fct_player(self):
        '''
        fct_player
        dev: Joseph
        date: 2022-01-20 18:46:18

        Description:
        on déplace les missiles de Payer et on les supprimes.
        '''
        self.player.deplacement_bullet()
        self.player.suppr_bullet()

    def shoot_monster(self):
        '''
        shoot_monster
        dev: Joseph
        date: 2022-01-20 18:47:41

        Description:
        On choisie un monstre aleatoire et on le fait tirer un missile.
        '''
        if len(self.list_monster) - 1 != 0:
            try:
                rand = random.randint(0, len(self.list_monster) - 1)
                shoot_monster = self.list_monster[rand]
                shoot_monster.shoot(None)
            except ValueError:
                pass
        self.canvas.after(int((self.lvl * 100)), self.shoot_monster)

    def boss_stage(self):
        '''
        boss_stage
        dev: Adrien
        date: 2022-01-20 18:48:13

        Description:
        Une fois le level 5 atteint on fait apparaitre un boss.
        '''
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
        '''
        create_obstacle
        dev: Adrien
        date: 2022-01-20 18:49:14

        Description:
        On fais apparaitre des obstacles (quantité aleatoire entre 1 et 3 a chaque level).
        '''
        i = random.randint(1, 3)
        pile_coord = [100,600,1100]
        random.shuffle(pile_coord)
        y = 400  # self.canvas.winfo_height() / 2)
        for nb in range(i):
            self.asteroide = entity.Entity(
                "asteroide",
                1000,
                self.canvas,
                speed=0,
                position=[pile_coord[-1], y],
                img="images/obstacle_transparent_v3.png",
            )
            self.asteroide.create(tag="asteroide")
            self.list_asteroide.append(self.asteroide)
            self.depiler(pile_coord)

    def pile_vide(self,pile):
        '''
        pile_vide
        dev: Adrien
        date: 2022-01-20 19:08:20

        Description:
            vérifie si la pile est vide

        Parametres:
            pile [[list]] : [pile des coordonnées des obstacles à créer]
        Returns:
            [[bouleen]] : [True or False]
        '''
        if pile == []:
            return True
        else : 
            return False

    def depiler(self,pile):
        '''
        depiler
        dev: Adrien
        date: 2022-01-20 19:10:08

        Description:
        supprime le dernier élément de la pile

        Parametres:
            pile [[list]] : [pile des coordonnées des obstacles à créer]
        '''
        if self.pile_vide(pile)==False:
            pile.pop()


    def dead(self):
        '''
        dead
        dev: Joseph
        date: 2022-01-20 18:50:11

        Description:
        On vérifie les attributs de Monster et le Player pour savoir si ils sont mort, puis on les supprime si nécessaire.
        '''
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
        '''
        lives_minus
        dev: Joseph et Adrien
        date: 2022-01-20 18:52:30

        Description:
        permet de vérifier les collisions entre chaque type d'entité à chaque instant
        '''
        """collisions des balles du joueur avec les monstres et des balles des monstres avec le player"""
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

            """collisions des balles des monstres et du player avec les asteroides"""
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
        '''
        collision
        dev: Adrien et Joseph
        date: 2022-01-20 19:15:06

        Description:
        calcule si il y a collision entre une balle et une autre entité (peut import la provenance de la balle)

        Parametres:
            bullets [dictionnaire] : dico contenant les balles et leurs coordonnées
            entity [class : entity] : le player ou un monstre ou un asteroide
        Returns:
            [list] : la liste des balles à supprimer
        '''
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
