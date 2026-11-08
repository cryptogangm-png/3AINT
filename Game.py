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

    def __init__(self, jeu, joueur_a, joueur_b, nb_parties=1,
                 taille_case=60, delai_ia=600, pause_fin=1500):
        """joueur_a / joueur_b : Human ou une IA. Ils alternent pour commencer.
        delai_ia : temps minimal (ms) entre deux coups d'IA, pour pouvoir les suivre.
        pause_fin : temps (ms) pendant lequel on montre la fin d'une partie."""
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

    # --- Gestion de la série de parties ---
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
        nom_a = self.__participants[0].get_nom()
        nom_b = self.__participants[1].get_nom()
        nom = self.__participants[index].get_nom()
        if nom_a == nom_b:  # deux fois la même IA : on les distingue
            nom += " (A)" if index == 0 else " (B)"
        return nom

    # --- Déroulé d'une partie ---
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

    # --- Affichage ---
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
        return (f"Partie {self.__partie}/{self.__nb_parties}   |   "
                f"{self.__nom(0)} : {self.__victoires[0]}   "
                f"{self.__nom(1)} : {self.__victoires[1]}   Nuls : {self.__nuls}")

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
        for ligne, texte in enumerate((self.__texte_statut(), self.__texte_score())):
            surface = self.__police.render(texte, True, self.__COULEURS["Noir"])
            self.__ecran.blit(surface, (10, y + 10 + ligne * 28))
        pygame.display.flip()

    # --- Boucle principale ---
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
    """Affiche la liste des joueurs dans le terminal et crée celui qui est choisi."""
    options = {
        "1": ("Humain", lambda: Human(jeu)),
        "2": ("Stupid Bot", lambda: StupidBot(jeu)),
        "3": ("MinMax heuristique 1", lambda: MinMax(jeu, profondeur=5, heuristique=1)),
        "4": ("MinMax heuristique 2", lambda: MinMax(jeu, profondeur=5, heuristique=2)),
        "5": ("Glouton", lambda: Glouton(jeu)),
        "6": ("MCTS", lambda: MCTS(jeu, iterations=1000)),
    }
    print(f"\n{titre} :")
    for cle, (nom, _) in options.items():
        print(f"  {cle}. {nom}")
    choix = input("Choix : ").strip()
    while choix not in options:
        choix = input("Choix invalide, recommence : ").strip()
    return options[choix][1]()


if __name__ == "__main__":
    jeu = ManicMinelayers(5, 10)
    joueur_a = choisir_joueur(jeu, "Joueur 1 (rouge)")
    joueur_b = choisir_joueur(jeu, "Joueur 2 (bleu)")
    Game(jeu, joueur_a, joueur_b).lancer()