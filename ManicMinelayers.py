from copy import deepcopy

class ManicMinelayers:
    valeur_case_vide = 0
    valeur_case_mine = 3
    __sauts_possibles = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    def __init__(self, m=5, n=10):
        self.__m = m
        self.__n = n
        self.reinitialiser()

    def get_m(self):
        return self.__m

    def get_n(self):
        return self.__n

    def get_case(self, ligne, colonne):
        return self.__plateau[ligne][colonne]

    def get_joueur_courant(self):
        return self.__joueur_courant

    def reinitialiser(self):
        self.__plateau = [[self.valeur_case_vide] * self.__n for _ in range(self.__m)]
        self.__positions = {1: None, 2: None}
        self.__joueur_courant = 1

    def copie(self):
        return deepcopy(self)

    def adversaire(self, joueur):
        return 2 if joueur == 1 else 1

    def est_vide(self, ligne, colonne):
        if not (0 <= ligne < self.__m and 0 <= colonne < self.__n):
            return False
        return self.__plateau[ligne][colonne] == self.valeur_case_vide

    def sauts_cavalier(self, ligne, colonne):
        """Cases vides atteignables en un saut depuis (ligne, colonne)."""
        cases = []
        for dl, dc in self.__sauts_possibles:
            if self.est_vide(ligne + dl, colonne + dc):
                cases.append((ligne + dl, colonne + dc))
        return cases

    def coups_possibles_de(self, joueur):
        position = self.__positions[joueur]
        if position is None:
            colonne = 0 if joueur == 1 else self.__n - 1
            return [(l, colonne) for l in range(self.__m) if self.est_vide(l, colonne)]
        return self.sauts_cavalier(position[0], position[1])

    def coups_possibles(self):
        return self.coups_possibles_de(self.__joueur_courant)

    def jouer(self, coup):
        joueur = self.__joueur_courant
        if coup not in self.coups_possibles_de(joueur):
            raise ValueError("Coup invalide")
        ancienne = self.__positions[joueur]
        if ancienne is not None:
            self.__plateau[ancienne[0]][ancienne[1]] = self.valeur_case_mine
        self.__plateau[coup[0]][coup[1]] = joueur
        self.__positions[joueur] = coup
        self.__joueur_courant = self.adversaire(joueur)

    def est_bloque(self, joueur):
        if self.__positions[joueur] is None:
            return False
        return len(self.coups_possibles_de(joueur)) == 0

    def est_fini(self):
        return self.est_bloque(self.__joueur_courant)

    def get_gagnant(self):
        if not self.est_fini():
            return 0
        precedent = self.adversaire(self.__joueur_courant)
        if self.est_bloque(precedent):
            return 0
        return precedent

    def est_nul(self):
        return self.est_fini() and self.get_gagnant() == 0