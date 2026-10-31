class ManicMinelayers:
    def __init__(self, m=5, n=10):
        self.m = m
        self.n = n

        self.plateau = []
        for i in range(self.m):
            ligne = []
            for j in range(self.n):
                ligne.append(0)
            self.plateau.append(ligne)

        self.positions = {1: None, 2: None}

    def adversaire(self, joueur):
        if joueur == 1:
            return 2
        return 1

    def est_vide(self, ligne, colonne):
        if ligne < 0 or ligne >= self.m or colonne < 0 or colonne >= self.n:
            return False
        if self.plateau[ligne][colonne] == 0:
            return True
        return False

    def coups_possibles(self, joueur):
        coups = []
        position = self.positions[joueur]

        if position is None:
            if joueur == 1:
                colonne = 0
            else:
                colonne = self.n - 1

            for ligne in range(self.m):
                if self.est_vide(ligne, colonne):
                    coups.append((ligne, colonne))
            return coups

        sauts = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for saut in sauts:
            ligne = position[0] + saut[0]
            colonne = position[1] + saut[1]
            if self.est_vide(ligne, colonne):
                coups.append((ligne, colonne))
        return coups

    def jouer_coup(self, coup, joueur):
        if coup not in self.coups_possibles(joueur):
            raise ValueError("Coup invalide")

        ancienne_position = self.positions[joueur]
        if ancienne_position is not None:
            self.plateau[ancienne_position[0]][ancienne_position[1]] = 3

        self.plateau[coup[0]][coup[1]] = joueur
        self.positions[joueur] = coup

    def est_bloque(self, joueur):
        if self.positions[joueur] is None:
            return False
        if len(self.coups_possibles(joueur)) == 0:
            return True
        return False

    def gagnant(self):
        bloque_1 = self.est_bloque(1)
        bloque_2 = self.est_bloque(2)

        if bloque_2 and not bloque_1:
            return 1
        if bloque_1 and not bloque_2:
            return 2
        return 0

    def est_nul(self):
        if self.est_bloque(1) and self.est_bloque(2):
            return True
        return False
