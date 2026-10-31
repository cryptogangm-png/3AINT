# Manic Minelayers 

## Dépendances : 
- Pygame 2.6.1 : https://pypi.org/project/pygame/
- Python 3.13.2 : https://www.python.org/downloads/latest/python3.13/

Ecrire `python .\Game.py` dans un terminal à la racine du projet pour lancer le jeu

## ManicMinelayers.py : 

Contient toute la logique du jeu d'un point de vu jouabilité et déplacements. Le constructeur contient 2 arguments optionnels : 
- m (le nombre de lignes), par défaut 5
- n (le nombre de colonnes), par défaut 10

Le jeu est écrit de sorte à être joué en 1 contre 1. La fonction adversaire détermine l'autre joueur à partir du joueur rentré en argument.

La fonction "est_vide" détermine si une position à déjà été jouée ou non (dans la logique du jeu, une même position ne peut être jouée qu'une seule fois, après une mine apparaît à son emplacement, caractérisée par un remplissage de couleur gris dans notre cas). Elle prend deux arguments en compte : un numéro de ligne et de colonne.

La fonction "coups_possibles" renvoit à partir de la position actuelle d'un joueur. Sachant que le jeu se joue en format déplacement de 2 cases dans une direction puis 1 case dans une autre (à la manière d'un cavalier dans un jeu d'échec), on regarde toutes les cases au tour du joueur qui sont valides (dans le plateau) et vides (cf. fonction "est_vide"). Elle prend en argument un joueur.

La fonction "jouer_coup" est la fonction qui est appelée lorsqu'un joueur se déplace. Elle prend en argument un coup de type objet avec 2 éléments : un numéro de ligne et un numéro de colonne ainsi que le joueur.

La fonction "est_bloque" détermine si un joueur peut encore jouer un coup ou non (appel de la fonction "coups_possibles" pour le déterminer)

La fonction "gagnant" détermine si l'un des deux joueur à gagner, c'est à dire qu'il est bloqué (cf. "est_bloque")

La fonction "est_nul" détermine si, pour une position de plateau les deux joueurs sont bloqués.

## Human.py

Classe de joueur humain qui choisi un coup via la fonction "choisir_coup" avec en argument une case (objet contenant un numéro de ligne et un numéro de colonne)

## Game.py

[Dépendance Pygame]

Logique de plateau visuel du jeu. Utilisation de la library pygame. Plateau intéractif permettant a un joueur Humain de sélectionner directement sa case sur l'interface graphique. Dessin de m lignes et n colonnes, avec par défaut m=5 et n=10.

Code couleur : 
- Remplissage en blanc des cases vides
- Remplissage en gris des cases jouées
- Cercle Rouge et Bleu correspondant aux joueurs 1 et 2
- Cercle Vert visibles sur les cases disponibles pour le déplacement pour un joueur.

Constructeur : 
- M et N (lignes et colonnes)
- Taille case (par défaut 60)
A noter aussi qu'on ajoute un espace de 40 pixels en dessous du plateau afin de pouvoir afficher une zone de texte (cf. "self.message")
