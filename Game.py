import pygame

from ManicMinelayers import ManicMinelayers
from Human import Human
from StupidBot import StupidBot
from MinMax import MinMax
from Glouton import Glouton
from MCTS import MCTS


class Game:
    __COULEURS = {
        "Blanc": (255, 255, 255),
        "Noir": (0, 0, 0),
        "Gris": (100, 100, 100),
        "Vert": (150, 220, 150),
        "Rouge": (220, 50, 50),
        "Bleu": (50, 80, 220)
    }
    __NOMS_COULEURS = {1: "rouge", 2: "bleu"}

    def __init__(self, jeu, joueur1, joueur2, taille_case=60, delai_ia=600):
        """jeu : la partie (ManicMinelayers). joueur1 / joueur2 : Human ou une IA.
        delai_ia : temps minimal (en ms) entre deux coups d'IA, pour pouvoir les suivre."""
        pygame.init()
        self.__jeu = jeu
        self.__m = jeu.get_m()
        self.__n = jeu.get_n()
        self.__joueurs = {1: joueur1, 2: joueur2}
        self.__taille_case = taille_case
        self.__delai_ia = delai_ia
        self.__fin = False
        self.__dernier_coup = 0
        self.__message = ""
        self.__mettre_a_jour_message()

        largeur = self.__n * self.__taille_case
        hauteur = self.__m * self.__taille_case + 40
        self.__ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Manic Minelayers")
        self.__police = pygame.font.SysFont("arial", 20)

    def __nom(self, numero):
        joueur = self.__joueurs[numero]
        if isinstance(joueur, Human):
            return "Humain"
        return joueur.get_nom()

    def __mettre_a_jour_message(self):
        gagnant = self.__jeu.get_gagnant()
        if gagnant != 0:
            self.__fin = True
            self.__message = (f"Victoire de {self.__nom(gagnant)} "
                              f"({self.__NOMS_COULEURS[gagnant]}) - R pour rejouer")
        elif self.__jeu.est_nul():
            self.__fin = True
            self.__message = "Match nul - R pour rejouer"
        else:
            courant = self.__jeu.get_joueur_courant()
            self.__message = f"Au tour de {self.__nom(courant)} ({self.__NOMS_COULEURS[courant]})"

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

                if valeur == ManicMinelayers.valeur_case_mine:
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
        self.__dernier_coup = pygame.time.get_ticks()
        self.__mettre_a_jour_message()

    def __recommencer(self):
        self.__jeu.reinitialiser()
        self.__fin = False
        self.__dernier_coup = pygame.time.get_ticks()
        self.__mettre_a_jour_message()

    def lancer(self):
        en_cours = True

        while en_cours:
            joueur = self.__joueurs[self.__jeu.get_joueur_courant()]
            tour_humain = isinstance(joueur, Human)

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    en_cours = False

                elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                    self.__recommencer()

                elif (evenement.type == pygame.MOUSEBUTTONDOWN
                      and tour_humain and not self.__fin):
                    x, y = evenement.pos
                    case = (y // self.__taille_case, x // self.__taille_case)
                    coup = joueur.choisir_coup(case)
                    if coup is not None:
                        self.__jouer(coup)

            # Tour d'une IA : on attend le délai pour que l'on puisse suivre le coup.
            if (en_cours and not self.__fin and not tour_humain
                    and pygame.time.get_ticks() - self.__dernier_coup >= self.__delai_ia):
                self.__jouer(joueur.choisir_coup())

            self.__afficher()
            pygame.time.wait(10)

        pygame.quit()


def choisir_joueur(jeu, numero):
    """Petit menu console pour choisir qui joue."""
    options = {
        "1": ("Humain", lambda: Human(jeu, numero)),
        "2": ("Stupid Bot", lambda: StupidBot(jeu)),
        "3": ("MinMax heuristique 1", lambda: MinMax(jeu, profondeur=5, heuristique=1)),
        "4": ("MinMax heuristique 2", lambda: MinMax(jeu, profondeur=5, heuristique=2)),
        "5": ("Glouton", lambda: Glouton(jeu)),
        "6": ("MCTS", lambda: MCTS(jeu, iterations=1000)),
    }
    print(f"\nJoueur {numero} ({'rouge' if numero == 1 else 'bleu'}) :")
    for cle, (nom, _) in options.items():
        print(f"  {cle}. {nom}")
    choix = input("Choix : ").strip()
    while choix not in options:
        choix = input("Choix invalide, recommence : ").strip()
    return options[choix][1]()


if __name__ == "__main__":
    jeu = ManicMinelayers(5, 10)
    joueur1 = choisir_joueur(jeu, 1)
    joueur2 = choisir_joueur(jeu, 2)
    Game(jeu, joueur1, joueur2).lancer()