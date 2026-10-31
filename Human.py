class Human:
    def __init__(self, jeu, joueur):
        self.jeu = jeu
        self.joueur = joueur

    def choisir_coup(self, case):
        if case in self.jeu.coups_possibles(self.joueur):
            return case
        return None
