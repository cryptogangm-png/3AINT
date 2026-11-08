import time
from itertools import combinations

from ManicMinelayers import ManicMinelayers
from MinMax import MinMax
from StupidBot import StupidBot
from Glouton import Glouton
from MCTS import MCTS


class Concours:

    def __init__(self, jeu, joueur_a, joueur_b):
        self.__jeu = jeu
        self.__joueur_a = joueur_a
        self.__joueur_b = joueur_b

    def __jouer_une_partie(self, premier, second):
        """Joue une partie complète et renvoie 1, 2 (correspondant au joueur gagnant) ou 0 en cas de match nul"""
        self.__jeu.reinitialiser()
        while not self.__jeu.est_fini():
            if self.__jeu.get_joueur_courant() == 1:
                coup = premier.choisir_coup()
            else:
                coup = second.choisir_coup()
            self.__jeu.jouer(coup)
        return self.__jeu.get_gagnant()

    def __jouer_serie(self, premier, second, nb_parties):
        """Renvoie les scores dans l'ordre : victoires du joueur 1, victoires du joueur 2, matchs nuls."""
        victoires_premier = 0
        victoires_second = 0
        nuls = 0
        for _ in range(nb_parties):
            resultat = self.__jouer_une_partie(premier, second)
            if resultat == 1:
                victoires_premier += 1
            elif resultat == 2:
                victoires_second += 1
            else:
                nuls += 1
        return victoires_premier, victoires_second, nuls

    def lancer(self, nb_parties=100):
        """Moitié des parties avec A qui commence, moitié avec B qui commence."""
        moitie = nb_parties // 2
        a_commence = self.__jouer_serie(self.__joueur_a, self.__joueur_b, moitie)
        b_commence = self.__jouer_serie(self.__joueur_b, self.__joueur_a, moitie)
        return {
            "a": self.__joueur_a.get_nom(),
            "b": self.__joueur_b.get_nom(),
            "a_commence": a_commence,  # (victoires A, victoires B, nuls)
            "b_commence": b_commence,  # (victoires B, victoires A, nuls)
        }


def afficher_resultats(resultats, nb_parties):
    moitie = nb_parties // 2
    print()
    print(f"{'Affrontement':<28} | {'A commence':^17} | {'B commence':^17} | {'Total':^17}")
    print(f"{'(A contre B)':<28} | {'A   B   nul':^17} | {'A   B   nul':^17} | {'A   B   nul':^17}")
    print("-" * 88)

    victoires_premier = 0
    victoires_second = 0
    nuls_total = 0

    for r in resultats:
        va1, vb1, n1 = r["a_commence"]
        vb2, va2, n2 = r["b_commence"]
        nom = r["a"] + " vs " + r["b"]
        print(f"{nom:<28} | {va1:>3} {vb1:>3} {n1:>3}       | {va2:>3} {vb2:>3} {n2:>3}       | "
              f"{va1 + va2:>3} {vb1 + vb2:>3} {n1 + n2:>3}")
        victoires_premier += va1 + vb2
        victoires_second += vb1 + va2
        nuls_total += n1 + n2

    total = victoires_premier + victoires_second + nuls_total
    print("-" * 88)
    print(f"Influence du premier joueur sur {total} parties ({moitie} par sens et par couple) :")
    print(f"  le joueur qui commence gagne {victoires_premier} fois ({100 * victoires_premier / total:.1f} %)")
    print(f"  le second joueur gagne {victoires_second} fois ({100 * victoires_second / total:.1f} %)")
    print(f"  matchs nuls : {nuls_total} ({100 * nuls_total / total:.1f} %)")


if __name__ == "__main__":
    nombre_de_parties = 100
    jeu = ManicMinelayers(5, 10)

    joueurs = [
        MinMax(jeu, profondeur=5, heuristique=1),
        MinMax(jeu, profondeur=5, heuristique=2),
        StupidBot(jeu),
        Glouton(jeu),
        MCTS(jeu, iterations=300),
    ]

    resultats = []
    for joueur_a, joueur_b in combinations(joueurs, 2):
        debut = time.perf_counter()
        print(f"{joueur_a.get_nom()} contre {joueur_b.get_nom()}...", end=" ", flush=True)
        resultats.append(Concours(jeu, joueur_a, joueur_b).lancer(nombre_de_parties))
        print(f"{time.perf_counter() - debut:.1f} s")

    afficher_resultats(resultats, nombre_de_parties)