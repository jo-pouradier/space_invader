import tkinter as tk


class Entity:
    """
    Entity
    dev: Adrien et Joseph
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
