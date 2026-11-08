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
    __HAUTEUR_TEXTE = 70

    def __init__(self, jeu, joueur_a, joueur_b, nb_parties=1, taille_case=60, delai_ia=600, pause_fin=1500):
        pygame.init()
        self.__jeu = jeu
        self.__m = jeu.get_m()
        self.__n = jeu.get_n()
        self.__participants = (joueur_a, joueur_b)
        self.__nb_parties = nb_parties
        self.__taille_case = taille_case
        self.__delai_ia = delai_ia
        self.__pause_fin = pause_fin

        largeur = self.__n * self.__taille_case
        hauteur = self.__m * self.__taille_case + self.__HAUTEUR_TEXTE
        self.__ecran = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Manic Minelayers")
        self.__police = pygame.font.SysFont("arial", 18)

        self.__recommencer_serie()

    def __recommencer_serie(self):
        self.__partie = 1
        self.__victoires = [0, 0]  # victoires de joueur_a, de joueur_b
        self.__nuls = 0
        self.__premier = 0         # 0 : joueur_a commence (rouge), 1 : joueur_b commence
        self.__nouvelle_partie()

    def __nouvelle_partie(self):
        self.__jeu.reinitialiser()
        self.__fin = False
        self.__instant = pygame.time.get_ticks()  # dernier coup ou fin de partie

    def __partie_suivante(self):
        self.__partie += 1
        self.__premier = 1 - self.__premier  # on alterne qui commence
        self.__nouvelle_partie()

    def __serie_terminee(self):
        return self.__fin and self.__partie >= self.__nb_parties

    def __index(self, numero):
        """Indice (0 ou 1) du participant qui joue le pion numero (1 = rouge, 2 = bleu)."""
        if numero == 1:
            return self.__premier
        return 1 - self.__premier

    def __nom(self, index):
        nom = self.__participants[index].get_nom()

        if self.__participants[0].get_nom() == self.__participants[1].get_nom():
            if index == 0:
                nom = nom + " (A)"
            else:
                nom = nom + " (B)"
        return nom

    def __jouer(self, coup):
        self.__jeu.jouer(coup)
        self.__instant = pygame.time.get_ticks()
        if self.__jeu.est_fini():
            self.__fin = True
            gagnant = self.__jeu.get_gagnant()
            if gagnant == 0:
                self.__nuls += 1
            else:
                self.__victoires[self.__index(gagnant)] += 1

    def __texte_statut(self):
        if not self.__fin:
            courant = self.__jeu.get_joueur_courant()
            return f"Au tour de {self.__nom(self.__index(courant))} ({self.__NOMS_COULEURS[courant]})"
        gagnant = self.__jeu.get_gagnant()
        if gagnant == 0:
            texte = "Match nul"
        else:
            texte = f"Victoire de {self.__nom(self.__index(gagnant))} ({self.__NOMS_COULEURS[gagnant]})"
        if self.__serie_terminee():
            texte += " - Série terminée, R pour recommencer"
        return texte

    def __texte_score(self):
        return (f"Partie {self.__partie}/{self.__nb_parties} | "
                f"{self.__nom(0)} : {self.__victoires[0]} | "
                f"{self.__nom(1)} : {self.__victoires[1]} | Nuls : {self.__nuls}")

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

        y = self.__m * self.__taille_case
        statut = self.__police.render(self.__texte_statut(), True, self.__COULEURS["Noir"])
        score = self.__police.render(self.__texte_score(), True, self.__COULEURS["Noir"])
        self.__ecran.blit(statut, (10, y + 10))
        self.__ecran.blit(score, (10, y + 38))
        pygame.display.flip()

    def lancer(self):
        en_cours = True

        while en_cours:
            maintenant = pygame.time.get_ticks()
            joueur = self.__participants[self.__index(self.__jeu.get_joueur_courant())]
            tour_humain = isinstance(joueur, Human)

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    en_cours = False

                elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                    self.__recommencer_serie()

                elif (evenement.type == pygame.MOUSEBUTTONDOWN
                      and tour_humain and not self.__fin):
                    x, y = evenement.pos
                    case = (y // self.__taille_case, x // self.__taille_case)
                    coup = joueur.choisir_coup(case)
                    if coup is not None:
                        self.__jouer(coup)

            if self.__fin:
                # On laisse voir la fin de partie, puis on enchaîne si la série continue.
                if not self.__serie_terminee() and maintenant - self.__instant >= self.__pause_fin:
                    self.__partie_suivante()
            elif not tour_humain and maintenant - self.__instant >= self.__delai_ia:
                self.__jouer(joueur.choisir_coup())

            self.__afficher()
            pygame.time.wait(10)

        pygame.quit()


def choisir_joueur(jeu, titre):
    print()
    print(titre)
    print("1. Humain")
    print("2. Stupid Bot")
    print("3. MinMax heuristique 1")
    print("4. MinMax heuristique 2")
    print("5. Glouton")
    print("6. MCTS")
    while True:
        choix = input("Choix : ")
        if choix == "1":
            return Human(jeu)
        if choix == "2":
            return StupidBot(jeu)
        if choix == "3":
            return MinMax(jeu, profondeur=5, heuristique=1)
        if choix == "4":
            return MinMax(jeu, profondeur=5, heuristique=2)
        if choix == "5":
            return Glouton(jeu)
        if choix == "6":
            return MCTS(jeu, iterations=1000)
        print("Choix invalide, recommence.")


if __name__ == "__main__":
    jeu = ManicMinelayers(5, 10)
    joueur_a = choisir_joueur(jeu, "Joueur 1 (rouge) :")
    joueur_b = choisir_joueur(jeu, "Joueur 2 (bleu) :")
    Game(jeu, joueur_a, joueur_b).lancer()