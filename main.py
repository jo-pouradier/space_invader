import tkinter as tk
import classes as cl


if __name__ == "__main__":
    # ----WINDOW----
    root = tk.Tk()
    window = cl.main_view(root)
    # creation du background
    window.update_idletasks()
    window.new_background("images/background_space_3.png")

    # ---- CREATION DU MONDE ----
    world = cl.World(window.cv)
    world.level_monster(5)
    world.dead()

    # ----CREATION DES BIND----
    root.bind(
        "r",
        lambda e: [
            window.new_background(window.background_image),
            window.cv.tag_lower("background"),
        ],
    )
    window.cv.bind("<Key>", world.player.deplacement_player)
    window.cv.bind("<space>", world.player.shoot)

    root.mainloop()
