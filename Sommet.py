"""Un état indépendant et ses statistiques dans l'arbre MCTS."""

from math import log, sqrt


class Sommet:
    def __init__(self, jeu, parent=None, coup=None):
        self.__jeu = jeu.copie()
        self.__joueur = self.__jeu.get_joueur_courant()
        self.__parent = parent
        self.__coup = coup
        self.__enfants = []
        self.__coups_restants = list(self.__jeu.coups_possibles())
        self.__visites = 0
        self.__gains = 0.0

    @property
    def joueur(self):
        return self.__joueur

    @property
    def parent(self):
        return self.__parent

    @property
    def coup(self):
        return self.__coup

    @property
    def enfants(self):
        return tuple(self.__enfants)

    @property
    def visites(self):
        return self.__visites

    @property
    def gains(self):
        return self.__gains
    def copier_jeu(self):
        return self.__jeu.copie()

    def est_terminal(self):
        return self.__jeu.est_fini()

    def est_complet(self):
        return not self.__coups_restants

    def developper(self, hasard):
        """Ajoute exactement un enfant correspondant à un coup non exploré."""
        if self.est_terminal() or self.est_complet():
            raise ValueError("Ce sommet ne peut pas être développé")
        coup = hasard.choice(self.__coups_restants)
        self.__coups_restants.remove(coup)
        jeu = self.copier_jeu()
        jeu.jouer(coup)
        enfant = Sommet(jeu, self, coup)
        self.__enfants.append(enfant)
        return enfant

    def meilleur_enfant(self, temperature, hasard):
        """UCT : gains vus par le joueur ayant effectué le coup vers l'enfant."""
        if not self.__enfants:
            raise ValueError("Ce sommet n'a pas d'enfant")

        def uct(enfant):
            if enfant.visites == 0:
                return float("inf")
            exploitation = enfant.gains / enfant.visites
            exploration = temperature * sqrt(log(max(1, self.__visites)) / enfant.visites)
            return exploitation + exploration

        scores = [(enfant, uct(enfant)) for enfant in self.__enfants]
        meilleur = max(score for _, score in scores)
        return hasard.choice([enfant for enfant, score in scores if score == meilleur])

    def retropropager(self, gagnant):
        """0 désigne un nul ; chaque sommet stocke le gain du joueur précédent."""
        sommet = self
        while sommet is not None:
            sommet.__visites += 1
            joueur_precedent = sommet.__jeu.adversaire(sommet.__joueur)
            if gagnant == 0:
                sommet.__gains += 0.5
            elif gagnant == joueur_precedent:
                sommet.__gains += 1.0
            sommet = sommet.__parent