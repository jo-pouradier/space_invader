# space_invader

il faut instaler la library pillow de python.
https://pillow.readthedocs.io/en/stable/installation.html
utilisation des commandes suivantes dans le terminal (macos et windows) pour installer pillow:
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade Pillow

POUR JOUER:
    lancer le fichier main.
    on se déplace grace aux flèches directionnelles, on tire avec la barre espace.

OPTIONS:
    posibilité de changer le fond d'écran grace au menu déroulant ( "Background" ).
    Si on change la taille de la fenêtre (plus grande ou plus petite), il faut redimensionner le background grâce à la touch "r" (resize).

IMPLEMENTATION:
    De nombreuses listes sont utilisées : pour stocker les balles à supprimer  notament dans le fichier world.py ou encore pour stocker les entités monster ou asteroides dans le fichier world.py.
    Une pile : permet de stocker les coordonnées des positions potentielles des asteroides dans le fchier world.py.

FONCTIONNALITES:
    Une création pseudo-aléatoire d'astéroides sur la carte.
    Une difficulé qui augmente avec le nombre de vagues.
    Un boss qui apparaît à certaines vagues.
    



