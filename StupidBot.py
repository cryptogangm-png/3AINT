import random


class StupidBot:

    def __init__(self, jeu):
        self.__jeu = jeu

    def get_nom(self):
        return "Stupid Bot"

    def choisir_coup(self):
        return random.choice(self.__jeu.coups_possibles())
