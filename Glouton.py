"""Évaluation des seules positions obtenues après notre prochain coup."""

from copy import deepcopy
from random import Random


class Glouton:
    def __init__(self, jeu, joueur, graine=None):
        if joueur not in (1, 2):
            raise ValueError("Le joueur doit être 1 ou 2")
        self.__jeu = jeu
        self.__joueur = joueur
        self.__hasard = Random(graine)

    def __evaluer(self, jeu):
        adversaire = jeu.adversaire(self.__joueur)
        gagnant = jeu.gagnant()
        if gagnant == self.__joueur:
            return float("inf")
        if gagnant == adversaire:
            return -float("inf")
        if jeu.est_nul():
            return 0
        return (len(jeu.coups_possibles(self.__joueur))
                - len(jeu.coups_possibles(adversaire)))

    def choisir_coup(self):
        if self.__jeu.gagnant() != 0 or self.__jeu.est_nul():
            return None
        evaluations = []
        for coup in self.__jeu.coups_possibles(self.__joueur):
            copie = deepcopy(self.__jeu)
            copie.jouer_coup(coup, self.__joueur)
            evaluations.append((coup, self.__evaluer(copie)))
        if not evaluations:
            return None
        meilleur = max(score for _, score in evaluations)
        return self.__hasard.choice([coup for coup, score in evaluations if score == meilleur])
