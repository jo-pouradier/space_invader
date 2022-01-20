import entity


class Monster(entity.Entity):
    def deplacement_monstre(self):
        '''
        deplacement_monstre
        dev: Joseph
        date: [description]

        Description:
        boizdvnozdfnvozkfdnv

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
