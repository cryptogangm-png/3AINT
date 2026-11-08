from ManicMinelayers import ManicMinelayers
from MinMax import MinMax
from StupidBot import StupidBot


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

        print("  " + premier.get_nom() + " commence :",
              premier.get_nom(), "gagne", victoires_premier, "|",
              second.get_nom(), "gagne", victoires_second, "|",
              "nuls", nuls)

    def lancer(self, nb_parties=100):
        print("\n===", self.__joueur_a.get_nom(), "contre", self.__joueur_b.get_nom(), "===")
        self.__jouer_serie(self.__joueur_a, self.__joueur_b, nb_parties // 2)
        self.__jouer_serie(self.__joueur_b, self.__joueur_a, nb_parties // 2)


if __name__ == "__main__":
    jeu = ManicMinelayers(5, 10)

    minmax_h1 = MinMax(jeu, profondeur=5, heuristique=1)
    minmax_h2 = MinMax(jeu, profondeur=5, heuristique=2)
    stupid_bot = StupidBot(jeu)

    Concours(jeu, minmax_h1, stupid_bot).lancer(20)
    Concours(jeu, minmax_h2, stupid_bot).lancer(20)
    Concours(jeu, minmax_h1, minmax_h2).lancer(20)
