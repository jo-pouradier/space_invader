import entity


class Monster(entity.Entity):
    def deplacement_monstre(self):
        '''
        deplacement_monstre
        dev: Adrien et Joseph
        date: 2022-01-20 18:31:36

        Description:
        Le monstre se déplace de 50px jusqu'a atteindre le bord de droite, puis change de direction, ainsi de suite.
        '''
        if self.position[0] < self.canvas.winfo_width() - 50 and self.direction == "r":
            self.position[0] += self.speed
        elif (
            self.position[0] >= self.canvas.winfo_width() -
            50 and self.direction == "r"
        ):
            self.direction = "l"
        elif self.position[0] > 0 + 50 and self.direction == "l":
            self.position[0] -= self.speed
        elif self.position[0] <= 0 + 50 and self.direction == "l":
            self.direction = "r"
        self.canvas.coords(self.form, self.position[0], self.position[1])
