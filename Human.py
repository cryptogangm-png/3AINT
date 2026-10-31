class Human:
    def __init__(self, jeu, joueur):
        self.jeu = jeu
        self.joueur = joueur

    def demander_entier(self, texte):
        while True:
            entree = input(texte)
            try:
                return int(entree)
            except ValueError:
                print("Veuillez saisir un entier")

    def choisir_coup(self):
        while True:
            ligne = self.demander_entier("Joueur " + str(self.joueur) + ", ligne : ")
            colonne = self.demander_entier("Joueur " + str(self.joueur) + ", colonne : ")
            coup = (ligne, colonne)

            if coup in self.jeu.coups_possibles(self.joueur):
                return coup

            print("Coup invalide")
