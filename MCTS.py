import math
import random
import time

from Sommet import Sommet


class MCTS:
    def __init__(self, jeu, joueur, iterations=1000,
                 temperature=math.sqrt(2), temps_max=None, graine=None):

        if joueur not in (1, 2):
            raise ValueError("Le joueur doit être 1 ou 2")

        if iterations is not None:
            if not isinstance(iterations, int) or iterations <= 0:
                raise ValueError("Le nombre d'itérations doit être positif")

        if temperature < 0:
            raise ValueError("La température doit être positive ou nulle")

        if temps_max is not None:
            if temps_max <= 0:
                raise ValueError("Le temps maximal doit être positif")

        if iterations is None and temps_max is None:
            raise ValueError("Il faut au moins une limite de recherche")

        self.__jeu = jeu
        self.__joueur = joueur
        self.__iterations = iterations
        self.__temperature = temperature
        self.__temps_max = temps_max

        # Une graine permet de reproduire les mêmes tirages.
        self.__hasard = random.Random(graine)
        self.__iterations_effectuees = 0

    @property
    def iterations_effectuees(self):
        return self.__iterations_effectuees

    def __simuler(self, sommet):
        # On joue sur une copie pour ne pas modifier la vraie partie.
        jeu = sommet.copier_jeu()
        joueur = sommet.joueur

        while jeu.gagnant() == 0 and not jeu.est_nul():
            coups = jeu.coups_possibles(joueur)

            if not coups:
                raise RuntimeError("Le joueur ne peut pas jouer")

            coup = self.__hasard.choice(coups)
            jeu.jouer_coup(coup, joueur)

            joueur = jeu.adversaire(joueur)

        # 1 ou 2 pour une victoire, 0 pour un match nul.
        return jeu.gagnant()

    def choisir_coup(self):
        self.__iterations_effectuees = 0
        racine = Sommet(self.__jeu, self.__joueur)

        if racine.est_terminal():
            return None

        coups = self.__jeu.coups_possibles(self.__joueur)

        if not coups:
            return None

        debut = time.perf_counter()

        while True:
            # Vérifier le nombre d'itérations.
            if self.__iterations is not None:
                if self.__iterations_effectuees >= self.__iterations:
                    break

            # Vérifier le temps écoulé.
            if self.__temps_max is not None:
                temps_ecoule = time.perf_counter() - debut

                if temps_ecoule >= self.__temps_max:
                    break

            # 1. Sélection : descendre dans l'arbre avec UCT.
            sommet = racine

            while not sommet.est_terminal() and sommet.est_complet():
                sommet = sommet.meilleur_enfant(
                    self.__temperature,
                    self.__hasard
                )

            # 2. Expansion : ajouter un enfant.
            if not sommet.est_terminal():
                sommet = sommet.developper(self.__hasard)

            # 3. Simulation : terminer une partie au hasard.
            gagnant = self.__simuler(sommet)

            # 4. Rétropropagation : mettre à jour les statistiques.
            sommet.retropropager(gagnant)

            self.__iterations_effectuees += 1

        # Si le temps était trop court pour explorer l'arbre.
        if not racine.enfants:
            return self.__hasard.choice(coups)

        # Chercher les enfants qui ont le plus de visites.
        visites_max = -1
        meilleurs_enfants = []

        for enfant in racine.enfants:
            if enfant.visites > visites_max:
                visites_max = enfant.visites
                meilleurs_enfants = [enfant]

            elif enfant.visites == visites_max:
                meilleurs_enfants.append(enfant)

        enfant_choisi = self.__hasard.choice(meilleurs_enfants)

        return enfant_choisi.coup