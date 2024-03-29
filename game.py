import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import world


class MainView(tk.Frame):
    """
    main_view
    dev: Joseph et Adrien
    date: 2021-12-16 09:54:25

    Description:
    Cree la fenetre principale du jeu space invader, avec ses propriétées

    Parametres:
        tk.Frame [tkinter] : crée une frame tkinter dans la fenetre principale
    """

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pack(side="top", fill="both", expand=True)

        # frame pour afficher les info du jeu : nbr de vie, score, boutons...
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # canvas qui aura toutes les entitées du jeu.
        self.cv = tk.Canvas(self)
        self.cv.focus_set()
        self.cv.grid(row=1, column=0, sticky="nsew")

        # creation des boutons
        bouton_quitter = tk.Button(
            self.info_frame, text="Quitter", fg="black", command=self.master.destroy
        )
        bouton_quitter.grid(row=0, column=6, sticky="ensw")
        bouton_new_game = tk.Button(
            self.info_frame, text="New Game", fg="black", command=self.new_game
        )
        bouton_new_game.grid(row=0, column=5, sticky="ensw")

        # ajout d'un boutton menu pour choisir le background
        background_menu = tk.Menubutton(
            self.info_frame, text="Background", fg="black")
        background_menu.menu = tk.Menu(background_menu)
        background_menu["menu"] = background_menu.menu
        background_menu.menu.add_command(
            label="Terre",
            command=lambda: [
                self.new_background("images/background_space_1.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Terre 2",
            command=lambda: [
                self.new_background("images/background_space_2.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Galaxy",
            command=lambda: [
                self.new_background("images/background_space_3.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.menu.add_command(
            label="Voie Lactée",
            command=lambda: [
                self.new_background("images/background_space_4.png"),
                self.cv.tag_lower("background"),
            ],
        )
        background_menu.grid(row=0, column=4, sticky="esw")

        # creation du background
        self.cv.update_idletasks()
        self.new_background("images/background_space_3.png")
        self.world = world.World(self.cv)

        # bind des touches de commandes
        self.cv.bind(
            "r",
            lambda e: [
                self.new_background(self.background_image),
                self.cv.tag_lower("background"),
            ],
        )
        self.cv.bind("<Key>", self.world.player.deplacement_player)
        self.cv.bind("<space>", self.world.player.shoot)

        self.label_info()
        self.centrage()
        self.multi_fct()

    def label_info(self):
        '''
        label_info
        dev: Joseph
        date: 2022-01-20 18:28:09

        Description:
        On cree les labels qui permettent d'afficher le score, les vies du joueur, et le level atteint.
        '''
        self.label_score = tk.Label(
            self.info_frame, text="score: " +
            str(self.world.player.score) + "  "
        )
        self.label_lives = tk.Label(
            self.info_frame, text="vie: " + str(self.world.player.lives) + "  "
        )
        self.label_lvl = tk.Label(
            self.info_frame, text="level: " + str(self.world.lvl) + "  "
        )
        self.label_lives.grid(row=0, column=1, sticky="nsew")
        self.label_lvl.grid(row=0, column=2, sticky="nsew")
        self.label_score.grid(row=0, column=3, sticky="nsew")

    def centrage(self):
        """
        centrage
        dev: Joseph
        date: 2021-11-27 20:54:14

        Description:
        centre la fenetre tkinter sur l'ecran de l'utilisateur

        Parametres:
            self [Frame] : une frame tkinter
        """
        self.sizeX = self.master.winfo_screenwidth() * 0.9
        self.sizeY = self.master.winfo_screenheight() * 0.9
        positionX = self.master.winfo_screenwidth() / 2 - (self.sizeX) / 2
        positionY = self.master.winfo_screenheight() / 2 - (self.sizeY) / 2
        self.master.geometry(
            "{}x{}+{}+{}".format(
                int(self.sizeX), int(self.sizeY), int(
                    positionX), int(positionY)
            )
        )

    def new_background(self, img):
        '''
        new_background
        dev: Joseph et Adrien
        date: 2022-01-20 19:22:48

        Description:
        permet de changer le background du canvas

        Parametres:
            img [chemin d'accès] : chemin d'accès à l'image
        '''
        self.background_image = img
        self.space_image = Image.open(img)
        self.space_image = self.space_image.resize(
            (self.cv.winfo_width(), self.cv.winfo_height()), Image.ANTIALIAS
        )
        self.background_resize = ImageTk.PhotoImage(self.space_image)
        self.background = self.cv.create_image(
            0, 0, image=self.background_resize, anchor="nw", tag="background"
        )

    def new_game(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def multi_fct(self):
        '''
        multi_fct
        dev: Joseph
        date: 2022-01-20 18:29:45

        Description:
        on lance les fonctions qui cree les monstres, verifient les collisions, et met a jour les labels.
        '''
        self.world.creation_lvl()
        self.world.fct_monster()
        self.world.fct_player()
        self.world.dead()
        self.label_info()

        self.cv.after(17, self.multi_fct)
