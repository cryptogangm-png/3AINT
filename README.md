# Manic Minelayers 

## Dépendances : 
- Pygame 2.6.1 : https://pypi.org/project/pygame/
- Python 3.13.2 : https://www.python.org/downloads/latest/python3.13/

Ecrire `python .\Game.py` dans un terminal à la racine du projet pour lancer le jeu

## ManicMinelayers.py : 

Contient toute la logique du jeu d'un point de vu jouabilité et déplacements. Le constructeur contient 2 arguments optionnels : 
- m (le nombre de lignes), par défaut 5
- n (le nombre de colonnes), par défaut 10

Le jeu est écrit de sorte à être joué en 1 contre 1. La méthode adversaire détermine l'autre joueur à partir du joueur rentré en argument.

La méthode "est_vide" détermine si une position à déjà été jouée ou non (dans la logique du jeu, une même position ne peut être jouée qu'une seule fois, après une mine apparaît à son emplacement, caractérisée par un remplissage de couleur gris dans notre cas). Elle prend deux arguments en compte : un numéro de ligne et de colonne.

La méthode "coups_possibles" renvoit à partir de la position actuelle d'un joueur. Sachant que le jeu se joue en format déplacement de 2 cases dans une direction puis 1 case dans une autre (à la manière d'un cavalier dans un jeu d'échec), on regarde toutes les cases au tour du joueur qui sont valides (dans le plateau) et vides (cf. méthode "est_vide"). Elle prend en argument un joueur.

La méthode "jouer_coup" est la méthode qui est appelée lorsqu'un joueur se déplace. Elle prend en argument un coup de type objet avec 2 éléments : un numéro de ligne et un numéro de colonne ainsi que le joueur.

La méthode "est_bloque" détermine si un joueur peut encore jouer un coup ou non (appel de la méthode "coups_possibles" pour le déterminer)

La méthode "gagnant" détermine si l'un des deux joueur à gagner, c'est à dire qu'il est bloqué (cf. "est_bloque")

La méthode "est_nul" détermine si, pour une position de plateau les deux joueurs sont bloqués.

## Human.py

Classe de joueur humain qui choisi un coup via la méthode "choisir_coup" avec en argument une case (objet contenant un numéro de ligne et un numéro de colonne)

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


## MinMax.py

La classe MinMax est, comme son nom l'indique, l'algorithme MinMax. C'est le "cerveau" qui choisit le meilleur coup à chaque tour. Sans lui, le bot jouerait au hasard, au même titre que StupidBot.
- Le but de MinMax est de simuler plusieurs coups a l'avance. Il se demande, s'il joue un coup, ce que l'adversaire jouera derriere et fait une simulation de tous les coups possibles en fonction de la profondeur choisie. Si on choisit profondeur 1, il n'ira voir que ses prochains coups, si on choisit profondeur 2, il regardera ces prochains coups plus ceux de l'adversaire, si on met 3, ses prochains coups, ceux de l'adversaire et ses coups d'après, etc. Evidemment, plus la profondeur est grande, plus l'IA est efficace, au détriment des performances.
- Il est très compliqué de mettre beaucoup de profondeur à cause de problèmes de performance. Nous avons donc une "heuristique", qui est une note pour savoir si le coup est bon ou pas avec un score. Dans mon code, deux heuristiques sont possibles : une vient calculer le nombre de coups qu'il me reste apres la simulation par rapport à celui de l'adversaire. Si l'adversaire a 2 coups restant et moi 4, le MinMax vient mettre un score de +2, ensuite il comparera lequel des coups a le plus gros score pour l'effectuer. La deuxième est plus efficace mais consomme plus de ressources, elle mesure le nombre de cases que l'IA peut atteindre en autant de sauts de cavalier nécessaire, moins celui de l'adversaire. Elle mesure donc plus l'espace de jeu.

**Le constructeur** reçoit en paramètres le jeu, la profondeur que l'on peut choisir (qui affectera l'efficacité et les performances) et l'heuristique que l'on souhaite utiliser. L'attribut `__moi` identifie le joueur incarné par l'IA, qui sera défini plus tard au moment de jouer via `choisir_coup`.

La méthode **`get_nom`** renvoie juste "MinMax h" avec le numero de l'heuristique choisie (par exemple "MinMax h1").

La méthode **`choisir_coup`** est la méthode principale de la classe, c'est elle qu'on appelle quand c'est a l'IA de jouer. C'est elle qui renvoie le coup à jouer.
Dans celle-ci, on va définir qui on est, savoir si l'IA est joueur 1 ou 2.
Par la suite, on définira la valeur -l'infini, qui est la plus basse, pour le `meilleur_score`. On part du pire score possible donc n'importe quel prochain coup sera mieux. On a aussi une liste qui du coup enregistrera les meilleurs coups.
On testera ensuite chaque coup possible avec une boucle en faisant une copie du plateau de jeu pour y executer `__minmax`. Par la suite, on regardera si notre score trouvé dans cette tentative est meilleur que le meilleur score actuel. Si c'est le cas, le score devient le meilleur, et on écrase la liste `meilleurs_coups` en y mettant le coup actuel qui deviendra pour l'instant le meilleur. Si le score est égal au `meilleur_score`, on ajoutera juste le coup à la liste `meilleurs_coups` pour, à la fin, choisir un coup au hasard dans cette liste `meilleurs_coups` pour le jouer.

La méthode privé **`__minmax`** est donc l'algorithme MinMax et la méthode récursive qui explore l'arbre des coups.
Elle reçoit 4 paramètres : le jeu, qui est la copie du jeu, soit la position à simuler, la profondeur, alpha, qui est le meilleur score garanti pour l'IA, et beta, le meilleur score déjà garanti pour l'adversaire, qui est le plus bas pour nous.
La méthode verifie d'abord si le jeu est fini, si c'est le cas elle renvoie directement +1000 si l'IA gagne, -1000 si elle perd ou 0 pour un match nul.
Ensuite, on vérifie si la profondeur est atteinte ; si elle l'est, on note la position avec l'heuristique choisie en appelant la méthode `__evaluer`.
Si c'est au tour de l'IA, on affecte -l'infini a `meilleur`.
La méthode se rappellera elle-même en réduisant de 1 à chaque fois la profondeur pour descendre d'un étage.
On met alpha à jour.
On fait ensuite de l'élagage : si alpha >= beta, on break, c'est que sur la branche actuelle, l'adversaire a déjà une meilleure solution ailleurs, donc ça ne sert à rien de continuer à descendre.
Et si beta est au dessus, on ne rentre pas dans la condition, on continue de tester les coups suivants et une fois la boucle finie, on return le meilleur.
Le else qui suit fait la même chose mais pour le pire : on suppose que l'adversaire joue le pire coup pour l'IA, on met beta à jour dans ce sens.

La méthode privé **`__evaluer`**
Evaluer permet d'utiliser l'heuristique choisie, elle renvoie le score de l'IA moins celui de l'adversaire.

La méthode **`__compter_cases_atteignables`** est privé, elle permet, comme son nom l'indique, de compter combien de cases un joueur peut atteindre depuis son emplacement actuel. Plus il en a, moins il a de risque d'être bloqué.
On obtient donc la liste des cases où le joueur peut sauter.
On parcours ensuite ces cases une par une.
On regarde où on peut aller depuis chacune d'elles en un saut de plus.
Si elle n'est pas dans la liste `cases`, on l'ajoute.
Et ensuite, on renvoie la longueur de la liste, qui est notre nombre de cases.


## Concours.py

La classe Concours permet de faire s'affronter des joueurs sans interface graphique.
Dans notre cas, pour faire s'affronter deux MinMax avec des heuristiques différentes ou contre le StupidBot par exemple. Elle nous permet d'avoir des statistiques pour savoir ce qui est le plus efficace.

Le **constructeur** reçoit comme paramètres le jeu, le joueur a et le joueur b. On peut donc mettre un MinMax ou un StupidBot.

La méthode **`__jouer_une_partie`** permet de jouer une partie sans interface graphique.
La méthode commence par remettre le plateau à zéro avant que chaque partie commence.
Ensuite, tant que personne n'est bloqué, elle continue de jouer.
Elle regarde ensuite a qui est le tour et en fonction fait jouer le joueur un ou le joueur deux.
Pour finir, elle renvoie le gagnant.

La méthode privée **`__jouer_serie`** a comme paramètres premier, second, qui sont les joueurs, et le nombre de parties que l'on veut lancer. Elle permettra de jouer autant de parties que l'on veut d'affilée pour obtenir des statistiques.
Elle va donc initialiser trois variables : victoires_premier, victoires_second et nuls.
Elle fait donc une boucle qui se répète autant que l'on souhaite en fonction du nombre de parties que l'on a mis.
Elle va ensuite, en fonction du gagnant, ajouter +1 à victoires_premier, victoires_second ou nuls après avoir executer **`__jouer_une_partie`**.
Elle finira par print les resultats.

La méthode **`lancer`** est la seule méthode publique de la classe, c'est elle que l'on va appeler dans le programme principal pour lancer les tests. Elle affiche le nom des deux joueurs puis appelle deux fois la fonction privée `__jouer_serie`, qui elle appellera `__jouer_une_partie` : la moitié des parties avec le joueur a qui commence, puis l'autre moitié avec le joueur b qui commence, pour que ce soit équitable.

## StupidBot.py

StupidBot est une classe tres simple de deux petites méthodes. Au final, c'est un bot qui joue de manière aléatoire.

Le **`constructeur`** a juste comme paramètre le jeu et donc un seul attribut qui est jeu.

La méthode **`get_nom`** return juste le nom "Stupid Bot".

Et pour finir, une deuxième méthode **`choisir_coup`** qui va juste faire un coup aleatoire dans les coups possibles.