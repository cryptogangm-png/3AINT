import pygame

from ManicMinelayers import ManicMinelayers
from Human import Human

Couleurs = {
    "Blanc": (255, 255, 255),
    "Noir": (0, 0, 0),
    "Gris": (100, 100, 100),
    "Vert": (150, 220, 150),
    "Rouge": (220, 50, 50),
    "Bleu": (50, 80, 220)
}

class Game:
    def __init__(self, m=5, n=10, taille_case=60):
        pygame.init()
        self.jeu = ManicMinelayers(m, n)
        self.joueurs = {1: Human(self.jeu, 1), 2: Human(self.jeu, 2)}
        self.joueur_actuel = 1
        self.fin = False
        self.message = "Au tour du joueur 1 (rouge)"
        self.taille_case = taille_case

        largeur = n * self.taille_case
        hauteur = m * self.taille_case + 40
        self.ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Manic Minelayers")
        self.police = pygame.font.SysFont("arial", 22)

    def afficher(self):
        self.ecran.fill(Couleurs["Blanc"])

        coups = []
        if not self.fin:
            coups = self.jeu.coups_possibles(self.joueur_actuel)

        for i in range(self.jeu.m):
            for j in range(self.jeu.n):
                rectangle = pygame.Rect(j * self.taille_case, i * self.taille_case, self.taille_case, self.taille_case)
                valeur = self.jeu.plateau[i][j]

                if valeur == 3:
                    pygame.draw.rect(self.ecran, Couleurs["Gris"], rectangle)
                elif (i, j) in coups:
                    pygame.draw.rect(self.ecran, Couleurs["Vert"], rectangle)

                pygame.draw.rect(self.ecran, Couleurs["Noir"], rectangle, 1)

                if valeur == 1:
                    pygame.draw.circle(self.ecran, Couleurs["Rouge"], rectangle.center, self.taille_case // 3)
                elif valeur == 2:
                    pygame.draw.circle(self.ecran, Couleurs["Bleu"], rectangle.center, self.taille_case // 3)

        texte = self.police.render(self.message, True, Couleurs["Noir"])
        self.ecran.blit(texte, (10, self.jeu.m * self.taille_case + 10))
        pygame.display.flip()

    def jouer(self, coup):
        self.jeu.jouer_coup(coup, self.joueur_actuel)

        gagnant = self.jeu.gagnant()
        if gagnant != 0:
            self.fin = True
            self.message = "Victoire du joueur " + str(gagnant)
        elif self.jeu.est_nul():
            self.fin = True
            self.message = "Match nul"
        else:
            self.joueur_actuel = self.jeu.adversaire(self.joueur_actuel)
            if self.joueur_actuel == 1:
                self.message = "Au tour du joueur 1 (rouge)"
            else:
                self.message = "Au tour du joueur 2 (bleu)"

    def lancer(self):
        en_cours = True

        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    en_cours = False

                elif evenement.type == pygame.MOUSEBUTTONDOWN and not self.fin:
                    x, y = evenement.pos
                    case = (y // self.taille_case, x // self.taille_case)
                    coup = self.joueurs[self.joueur_actuel].choisir_coup(case)
                    if coup is not None:
                        self.jouer(coup)

            self.afficher()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.lancer()
