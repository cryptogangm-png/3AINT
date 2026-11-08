class Human:
    def __init__(self, jeu):
        self.__jeu = jeu

    def get_nom(self):
        return "Humain"

    def choisir_coup(self, case):
        if case in self.__jeu.coups_possibles():
            return case
        return None