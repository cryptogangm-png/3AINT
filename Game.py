from ManicMinelayers import ManicMinelayers
from Human import Human


class Game:
    def __init__(self, m=5, n=10):
        self.jeu = ManicMinelayers(m, n)
        self.joueurs = {1: Human(self.jeu, 1), 2: Human(self.jeu, 2)}
        self.joueur_actuel = 1

    def afficher(self):
        print()
        print("  ", end=' ')
        for j in range(self.jeu.n):
            print(j, end=' ')
        print()

        for i in range(self.jeu.m):
            print(i, " ", end='')
            for j in range(self.jeu.n):
                valeur = self.jeu.plateau[i][j]
                if valeur == 0:
                    print('.', end=' ')
                elif valeur == 1:
                    print('A', end=' ')
                elif valeur == 2:
                    print('B', end=' ')
                else:
                    print('x', end=' ')
            print()
        print()

    def lancer(self):
        while True:
            self.afficher()
            print("Coups possibles :", self.jeu.coups_possibles(self.joueur_actuel))

            coup = self.joueurs[self.joueur_actuel].choisir_coup()
            self.jeu.jouer_coup(coup, self.joueur_actuel)
            print("Joueur", self.joueur_actuel, "joue en", coup)

            gagnant = self.jeu.gagnant()
            if gagnant != 0:
                self.afficher()
                print("Victoire du joueur", gagnant)
                return gagnant

            if self.jeu.est_nul():
                self.afficher()
                print("Match nul")
                return 0

            self.joueur_actuel = self.jeu.adversaire(self.joueur_actuel)


if __name__ == "__main__":
    game = Game()
    game.lancer()
