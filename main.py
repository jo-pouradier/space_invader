import tkinter as tk
import classes as cl


class main_view(tk.Frame):
    '''
    main_view
    dev: Joseph
    date: 2021-12-16 09:54:25

    Description:
    Cree la fenetre principale du jeu space invader, avec ses proporiété

    Parametres:
        tk [tk] : cree une frame tkinter dans la page principale
    '''

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, sticky='nsew')
        info_frame.configure(highlightbackground='red', highlightthickness=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.cv = tk.Canvas(self)
        self.cv.configure(highlightbackground='blue',
                          highlightthickness=2)
        self.cv.grid(row=1, column=0, sticky='nsew')

        bouton_quitter = tk.Button(
            info_frame, text='Quitter', fg='black', command=self.master.destroy)
        bouton_quitter.grid(row=0, column=4, sticky='e')
        bouton_new_game = tk.Button(
            info_frame, text='New Game', fg='black', command=None)
        bouton_new_game.grid(row=0, column=3, sticky='e')
        main_view.centrage(self)

    def centrage(self):
        '''
        centrage
        dev: Joseph
        date: 2021-11-27 20:54:14

        Description:
        centre la fenetre tkinter sur l'ecran de l'utilisateur

        Parametres:
            self [Frame] : c'est une frame tkinter
        '''
        self.sizeX = self.master.winfo_screenwidth()*0.9
        self.sizeY = self.master.winfo_screenheight()*0.9
        positionX = self.master.winfo_screenwidth()/2-(self.sizeX)/2
        positionY = self.master.winfo_screenheight()/2-(self.sizeY)/2
        self.master.geometry(
            "{}x{}+{}+{}".format(int(self.sizeX), int(self.sizeY), int(positionX), int(positionY)))


if __name__ == "__main__":
    root = tk.Tk()
    window = main_view(root)
    window.configure(highlightbackground='yellow', highlightthickness=2)
    window.pack(side="top", fill="both", expand=True)
    # creation du joueur
    player = cl.Player(lives=3, img='images/vaisseau_player.png',
                       position=[window.sizeX/2, window.sizeY/2], canvas=window.cv)
    player.placement([window.sizeX/2, window.sizeY/2])
    player.create(window.cv)

    # mouvement du joueur
    player.speed = 50
    window.cv.focus_set()
    window.cv.bind('<Key>', player.deplacement_player)
    window.cv.bind('<space>', player.shoot)
    player.name = 'player'
    player.deplacement_bullet()
    player.suppr_bullet()

    root.mainloop()
