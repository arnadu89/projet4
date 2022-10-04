import mvc_chess.models.tour as tour

class Tournoi:
    controles_temps = [
        "Bullet",
        "Blitz",
        "Coup rapide"
    ]
    nombre_joueurs = 8

    def __init__(self,
                 nom, lieu, date,
                 controle_temps, description,
                 nombre_tours=4
                 ):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.tournees = []
        self.joueurs = []
        self.scores = []
        self._controle_temps = controle_temps
        self.description = description
        self.nombre_tours = nombre_tours
        self.paires_already_played = []

    @property
    def controle_temps(self):
        return self.controle_temps

    @controle_temps.setter
    def controle_temps(self, value):
        if value in Tournoi.controles_temps:
            self.controle_temps = value

    def ajouter_joueur(self, joueur):
        self.joueurs.append(joueur)

    def generer_paires_old(self):
        # Premier tour
        if len(self.tournees) == 1:
            sorted_joueurs = sorted(self.joueurs, key=lambda j: j.classement, reverse=True)
            paires = zip(
                sorted_joueurs[:int(Tournoi.nombre_joueurs / 2)],
                sorted_joueurs[int(Tournoi.nombre_joueurs / 2):]
            )
            paires = list(paires)
            self.paires_already_played.extend(paires)
        else: # Tours suivants
            # On tri les joueurs selon leur score/classement
            mixed_joueurs = []
            for joueur in self.joueurs:
                score_joueur = next(score[1] for score in self.scores if score[0] is joueur)
                print(f"score de {joueur} est {score_joueur}")
                mixed_joueurs.append((joueur, score_joueur, joueur.classement))
            sorted_joueurs_score = sorted(mixed_joueurs, key=lambda j: (j[1], j[2]), reverse=True)
            sorted_joueurs = [elm[0] for elm in sorted_joueurs_score]
            # On aparie les joueurs séquentiellement sauf s'ils ont déjà joué avec leur paire,
            # dans ce cas on décale
            paires = []
            while sorted_joueurs:
                current_joueur = sorted_joueurs.pop(0)
                for joueur in sorted_joueurs:
                    paire = [current_joueur, joueur]
                    if paire not in self.paires_already_played and\
                     paire[::-1] not in self.paires_already_played:
                        paires.append(paire)
                        self.paires_already_played.append(paire)
                        sorted_joueurs.remove(joueur)
                        break

            self.paires_already_played.append(paire)

        return paires

    def generer_paires(self):
        # Premier tour
        if len(self.tournees) == 1:
            sorted_joueurs = sorted(self.joueurs, key=lambda j: j.classement, reverse=True)
            paires = zip(
                sorted_joueurs[:int(Tournoi.nombre_joueurs / 2)],
                sorted_joueurs[int(Tournoi.nombre_joueurs / 2):]
            )
            paires = list(paires)
            self.paires_already_played.extend(paires)
        else:  # Tours suivants
            # On tri les joueurs selon leur score/classement
            mixed_joueurs = []
            for joueur in self.joueurs:
                score_joueur = next(score[1] for score in self.scores if score[0] is joueur)
                print(f"score de {joueur} est {score_joueur}")
                mixed_joueurs.append((joueur, score_joueur, joueur.classement))
            sorted_joueurs_score = sorted(mixed_joueurs, key=lambda j: (j[1], j[2]), reverse=True)
            sorted_joueurs = [elm[0] for elm in sorted_joueurs_score]

            # On aparie les joueurs séquentiellement sauf s'ils ont déjà joué avec leur paire,
            # dans ce cas on échange avec le suivant et on continue
            for i in range(0,5,2):
                paire = [sorted_joueurs[i], sorted_joueurs[i+1]]
                if paire in self.paires_already_played or\
                        paire[::-1] in self.paires_already_played:
                    sorted_joueurs[i+1], sorted_joueurs[i+2] = sorted_joueurs[i+2], sorted_joueurs[i+1]

            paires = list(zip(sorted_joueurs[::2], sorted_joueurs[1::2]))

            self.paires_already_played.append(paire)

        return paires

    def lancer_tour_suivant(self):
        nouveau_tour = tour.Tour(f"Round {len(self.tournees)+1}")
        self.tournees.append(nouveau_tour)

        paires = self.generer_paires()
        nouveau_tour.create_matches(paires)

    def finir_tour_courant(self):
        self.update_scores()
        self.tournees[-1].marquer_comme_terminer()

    def update_scores(self):
        self.scores = []
        all_scores = [joueur_and_score
                      for tournee in self.tournees
                      for match in tournee.matchs
                      for joueur_and_score in match]
        for joueur in self.joueurs:
            joueur_score = 0
            for score in all_scores:
                if joueur is score[0]:
                    joueur_score += score[1]
            self.scores.append((joueur, joueur_score))

    def statut(self):
        if not self.tournees:
            statut = "Non démarré"
        elif len(self.tournees) == self.nombre_tours:
            statut = "Terminé"
        else:
            statut = "En cours"
        return statut

    def __repr__(self):
        repr = f"{self.nom} - {self.lieu} - {self.date} - Statut : {self.statut()} \n"
        repr += f"Joueurs : {len(self.joueurs)}/{Tournoi.nombre_joueurs}\n"
        for joueur in self.joueurs:
            repr += f"\t{joueur}\n"

        repr += "\n"
        for tour in self.tournees:
            repr += f"{tour} \n"

        return repr
