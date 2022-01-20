import entity


class Player(entity.Entity):
    """
    Player
    dev: Adrien et Joseph
    date: 2021-12-17 23:40:06

    Description:
    Classe qui donne les methodes qui s'appliqueront a Player en tant qu'entité du jeu.

    Parametres:
        Entity [class] : voir description de la class
    """

    def __init__(self, name, lives, canvas, speed=40, position=[0, 0], img=""):
        super().__init__(name, lives, canvas, speed=speed, position=position, img=img)
        self.score = 0

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
        if side == "Left":
            if self.position[0] - self.speed > 0+50:
                self.position[0] -= self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Right":
            if self.position[0] + self.speed < self.canvas.winfo_width()-50:
                self.position[0] += self.speed
            else:
                self.position[0] = self.position[0]

        if side == "Up":
            if self.position[1] - self.speed > 0 + 50:
                self.position[1] -= self.speed
            else:
                self.position[1] = self.position[1]

        if side == "Down":
            if self.position[1] + self.speed < self.canvas.winfo_height()-50:
                self.position[1] += self.speed
            else:
                self.position[1] = self.position[1]
        self.canvas.coords(self.form, self.position[0], self.position[1])
