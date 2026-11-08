"""Tactique gloutonne : évalue seulement les positions obtenues après notre prochain coup."""

from random import Random


class Glouton:
    def __init__(self, jeu, graine=None):
        self.__jeu = jeu
        self.__hasard = Random(graine)
        self.__moi = None

    def get_nom(self):
        return "Glouton"

    def __evaluer(self, jeu):
        """Note la position après notre coup, du point de vue de self.__moi."""
        adversaire = jeu.adversaire(self.__moi)
        gagnant = jeu.get_gagnant()
        if gagnant == self.__moi:
            return float("inf")
        if gagnant == adversaire:
            return -float("inf")
        if jeu.est_nul():
            return 0
        return (len(jeu.coups_possibles_de(self.__moi))
                - len(jeu.coups_possibles_de(adversaire)))

    def choisir_coup(self):
        if self.__jeu.est_fini():
            return None
        self.__moi = self.__jeu.get_joueur_courant()

        evaluations = []
        for coup in self.__jeu.coups_possibles():
            copie = self.__jeu.copie()
            copie.jouer(coup)
            evaluations.append((coup, self.__evaluer(copie)))
        if not evaluations:
            return None

        meilleur = max(score for _, score in evaluations)
        return self.__hasard.choice([coup for coup, score in evaluations if score == meilleur])