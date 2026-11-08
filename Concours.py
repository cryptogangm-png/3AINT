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
        self.__jeu.reinitialiser()
        while not self.__jeu.est_fini():
            if self.__jeu.get_joueur_courant() == 1:
                coup = premier.choisir_coup()
            else:
                coup = second.choisir_coup()
            self.__jeu.jouer(coup)
        return self.__jeu.get_gagnant()

    def __jouer_serie(self, premier, second, nb_parties):
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
        nom_a = self.__joueur_a.get_nom()
        nom_b = self.__joueur_b.get_nom()
        moitie = nb_parties // 2

        a_1, b_1, nuls_1 = self.__jouer_serie(self.__joueur_a, self.__joueur_b, moitie)
        b_2, a_2, nuls_2 = self.__jouer_serie(self.__joueur_b, self.__joueur_a, moitie)

        print()
        print(nom_a, "contre", nom_b)
        print("  " + nom_a, "commence :", nom_a, a_1, "|", nom_b, b_1, "| nuls", nuls_1)
        print("  " + nom_b, "commence :", nom_a, a_2, "|", nom_b, b_2, "| nuls", nuls_2)
        print("  Total :", nom_a, a_1 + a_2, "|", nom_b, b_1 + b_2, "| nuls", nuls_1 + nuls_2)

        return a_1 + b_2, b_1 + a_2, nuls_1 + nuls_2


def demander_entier(question):
    reponse = input(question)
    while not reponse.isdigit() or int(reponse) < 2:
        reponse = input("Il faut un nombre entier d'au moins 2 : ")
    return int(reponse)


def choisir_ia(jeu, titre):
    print()
    print(titre)
    print("1. Stupid Bot")
    print("2. MinMax heuristique 1")
    print("3. MinMax heuristique 2")
    print("4. Glouton")
    print("5. MCTS")
    while True:
        choix = input("Choix : ")
        if choix == "1":
            return StupidBot(jeu)
        if choix == "2":
            return MinMax(jeu, profondeur=5, heuristique=1)
        if choix == "3":
            return MinMax(jeu, profondeur=5, heuristique=2)
        if choix == "4":
            return Glouton(jeu)
        if choix == "5":
            return MCTS(jeu, iterations=300)
        print("Choix invalide, recommence.")


if __name__ == "__main__":
    jeu = ManicMinelayers(5, 10)
    nb_parties = demander_entier("Nombre de parties par affrontement : ")

    print()
    print("1. Statistiques sur tous les couples d'IA (sans affichage)")
    print("2. Regarder un affrontement entre deux IA dans la GUI")
    mode = input("Choix : ")
    while mode != "1" and mode != "2":
        mode = input("Choix invalide, recommence : ")

    if mode == "1":
        joueurs = [
            MinMax(jeu, profondeur=5, heuristique=1),
            MinMax(jeu, profondeur=5, heuristique=2),
            StupidBot(jeu),
            Glouton(jeu),
            MCTS(jeu, iterations=300),
        ]

        victoires_premier = 0
        victoires_second = 0
        nuls = 0
        # combinations donne tous les couples possibles de joueurs (10 affrontements)
        for joueur_a, joueur_b in combinations(joueurs, 2):
            premier, second, nul = Concours(jeu, joueur_a, joueur_b).lancer(nb_parties)
            victoires_premier += premier
            victoires_second += second
            nuls += nul

        print()
        print("Influence du joueur qui commence, sur toutes les parties :")
        print("  Le joueur qui commence gagne", victoires_premier, "fois")
        print("  Le second joueur gagne", victoires_second, "fois")
        print("  Matchs nuls :", nuls)

    else:
        from Game import Game
        joueur_a = choisir_ia(jeu, "IA A (commence la première partie) :")
        joueur_b = choisir_ia(jeu, "IA B :")
        Game(jeu, joueur_a, joueur_b, nb_parties, delai_ia=300, pause_fin=1000).lancer()