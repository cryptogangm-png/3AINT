class Human:
    def __init__(self, jeu, joueur):
        self.__jeu = jeu
        self.__joueur = joueur

    def choisir_coup(self, case):
        if case in self.__jeu.coups_possibles_de(self.__joueur):
            return case
        return None