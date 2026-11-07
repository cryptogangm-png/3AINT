import math
import random


class MinMax:

    def __init__(self, jeu, profondeur=3, heuristique=1):
        self.__jeu = jeu
        self.__profondeur = profondeur
        self.__heuristique = heuristique
        self.__moi = None

    def get_nom(self):
        return "MinMax h" + str(self.__heuristique)

    def choisir_coup(self):
        self.__moi = self.__jeu.get_joueur_courant()

        meilleur_score = -math.inf
        meilleurs_coups = []

        for coup in self.__jeu.coups_possibles():
            copie = self.__jeu.copie()
            copie.jouer(coup)
            score = self.__minmax(copie, self.__profondeur - 1, -math.inf, math.inf)

            if score > meilleur_score:
                meilleur_score = score
                meilleurs_coups = [coup]
            elif score == meilleur_score:
                meilleurs_coups.append(coup)

        return random.choice(meilleurs_coups)

    def __minmax(self, jeu, profondeur, alpha, beta):
        if jeu.est_fini():
            if jeu.get_gagnant() == self.__moi:
                return 1000
            elif jeu.get_gagnant() == 0:
                return 0
            else:
                return -1000

        if profondeur == 0:
            return self.__evaluer(jeu)

        if jeu.get_joueur_courant() == self.__moi:
            meilleur = -math.inf
            for coup in jeu.coups_possibles():
                copie = jeu.copie()
                copie.jouer(coup)
                score = self.__minmax(copie, profondeur - 1, alpha, beta)
                meilleur = max(meilleur, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return meilleur

        else:
            pire = math.inf
            for coup in jeu.coups_possibles():
                copie = jeu.copie()
                copie.jouer(coup)
                score = self.__minmax(copie, profondeur - 1, alpha, beta)
                pire = min(pire, score)
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return pire

    def __evaluer(self, jeu):
        adversaire = jeu.adversaire(self.__moi)

        if self.__heuristique == 1:
            return len(jeu.coups_possibles_de(self.__moi)) - len(jeu.coups_possibles_de(adversaire))
        else:
            return self.__compter_cases_atteignables(jeu, self.__moi) - self.__compter_cases_atteignables(jeu, adversaire)

    def __compter_cases_atteignables(self, jeu, joueur):
        cases = jeu.coups_possibles_de(joueur)
        for case in cases:
            for voisine in jeu.sauts_cavalier(case[0], case[1]):
                if voisine not in cases:
                    cases.append(voisine)
        return len(cases)
