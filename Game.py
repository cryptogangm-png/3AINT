import pygame

from ManicMinelayers import ManicMinelayers
from Human import Human


class Game:
    __COULEURS = {
        "Blanc": (255, 255, 255),
        "Noir": (0, 0, 0),
        "Gris": (100, 100, 100),
        "Vert": (150, 220, 150),
        "Rouge": (220, 50, 50),
        "Bleu": (50, 80, 220)
    }

    def __init__(self, m=5, n=10, taille_case=60):
        pygame.init()
        self.__m = m
        self.__n = n
        self.__jeu = ManicMinelayers(m, n)
        self.__joueurs = {1: Human(self.__jeu, 1), 2: Human(self.__jeu, 2)}
        self.__fin = False
        self.__message = "Au tour du joueur 1 (rouge)"
        self.__taille_case = taille_case

        largeur = n * self.__taille_case
        hauteur = m * self.__taille_case + 40
        self.__ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Manic Minelayers")
        self.__police = pygame.font.SysFont("arial", 22)

    def __afficher(self):
        self.__ecran.fill(self.__COULEURS["Blanc"])

        coups = []
        if not self.__fin:
            coups = self.__jeu.coups_possibles()

        for i in range(self.__m):
            for j in range(self.__n):
                rectangle = pygame.Rect(j * self.__taille_case, i * self.__taille_case,
                                        self.__taille_case, self.__taille_case)
                valeur = self.__jeu.get_case(i, j)

                if valeur == ManicMinelayers.MINE:
                    pygame.draw.rect(self.__ecran, self.__COULEURS["Gris"], rectangle)
                elif (i, j) in coups:
                    pygame.draw.rect(self.__ecran, self.__COULEURS["Vert"], rectangle)

                pygame.draw.rect(self.__ecran, self.__COULEURS["Noir"], rectangle, 1)

                if valeur == 1:
                    pygame.draw.circle(self.__ecran, self.__COULEURS["Rouge"],
                                       rectangle.center, self.__taille_case // 3)
                elif valeur == 2:
                    pygame.draw.circle(self.__ecran, self.__COULEURS["Bleu"],
                                       rectangle.center, self.__taille_case // 3)

        texte = self.__police.render(self.__message, True, self.__COULEURS["Noir"])
        self.__ecran.blit(texte, (10, self.__m * self.__taille_case + 10))
        pygame.display.flip()

    def __jouer(self, coup):
        self.__jeu.jouer(coup)

        gagnant = self.__jeu.get_gagnant()
        if gagnant != 0:
            self.__fin = True
            self.__message = "Victoire du joueur " + str(gagnant)
        elif self.__jeu.est_nul():
            self.__fin = True
            self.__message = "Match nul"
        elif self.__jeu.get_joueur_courant() == 1:
            self.__message = "Au tour du joueur 1 (rouge)"
        else:
            self.__message = "Au tour du joueur 2 (bleu)"

    def lancer(self):
        en_cours = True

        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    en_cours = False

                elif evenement.type == pygame.MOUSEBUTTONDOWN and not self.__fin:
                    x, y = evenement.pos
                    case = (y // self.__taille_case, x // self.__taille_case)
                    joueur = self.__joueurs[self.__jeu.get_joueur_courant()]
                    coup = joueur.choisir_coup(case)
                    if coup is not None:
                        self.__jouer(coup)

            self.__afficher()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.lancer()