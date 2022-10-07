import mvc_chess.models.tour as tour

class Tournoi:
    controles_temps = [
        "Bullet",
        "Blitz",
        "Coup rapide"
    ]
    number_players = 8

    def __init__(self,
                 nom, lieu, date,
                 controle_temps, description,
                 number_tours=4
                 ):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.tournees = []
        self.players = []
        self.scores = []
        self._controle_temps = controle_temps
        self.description = description
        self.number_tours = number_tours
        self.pairs_already_played = []

    @property
    def controle_temps(self):
        return self.controle_temps

    @controle_temps.setter
    def controle_temps(self, value):
        if value in Tournoi.controles_temps:
            self.controle_temps = value

    def add_player(self, player):
        self.players.append(player)

    def generer_pairs_old(self):
        # Premier tour
        if len(self.tournees) == 1:
            sorted_players = sorted(self.players, key=lambda j: j.rank, reverse=True)
            pairs = zip(
                sorted_players[:int(Tournoi.number_players / 2)],
                sorted_players[int(Tournoi.number_players / 2):]
            )
            pairs = list(pairs)
            self.pairs_already_played.extend(pairs)
        else: # Tours suivants
            # On tri les players selon leur score/rank
            mixed_players = []
            for player in self.players:
                score_player = next(score[1] for score in self.scores if score[0] is player)
                print(f"score de {player} est {score_player}")
                mixed_players.append((player, score_player, player.rank))
            sorted_players_score = sorted(mixed_players, key=lambda j: (j[1], j[2]), reverse=True)
            sorted_players = [elm[0] for elm in sorted_players_score]
            # On aparie les players séquentiellement sauf s'ils ont déjà joué avec leur paire,
            # dans ce cas on décale
            pairs = []
            while sorted_players:
                current_player = sorted_players.pop(0)
                for player in sorted_players:
                    paire = [current_player, player]
                    if paire not in self.pairs_already_played and\
                     paire[::-1] not in self.pairs_already_played:
                        pairs.append(paire)
                        self.pairs_already_played.append(paire)
                        sorted_players.remove(player)
                        break

            self.pairs_already_played.append(paire)

        return pairs

    def generer_pairs(self):
        # Premier tour
        if len(self.tournees) == 1:
            sorted_players = sorted(self.players, key=lambda j: j.rank, reverse=True)
            pairs = zip(
                sorted_players[:int(Tournoi.number_players / 2)],
                sorted_players[int(Tournoi.number_players / 2):]
            )
            pairs = list(pairs)
            self.pairs_already_played.extend(pairs)
        else:  # Tours suivants
            # On tri les players selon leur score/rank
            mixed_players = []
            for player in self.players:
                score_player = next(score[1] for score in self.scores if score[0] is player)
                print(f"score de {player} est {score_player}")
                mixed_players.append((player, score_player, player.rank))
            sorted_players_score = sorted(mixed_players, key=lambda j: (j[1], j[2]), reverse=True)
            sorted_players = [elm[0] for elm in sorted_players_score]

            # On aparie les players séquentiellement sauf s'ils ont déjà joué avec leur paire,
            # dans ce cas on échange avec le suivant et on continue
            for i in range(0,5,2):
                paire = [sorted_players[i], sorted_players[i+1]]
                if paire in self.pairs_already_played or\
                        paire[::-1] in self.pairs_already_played:
                    sorted_players[i+1], sorted_players[i+2] = sorted_players[i+2], sorted_players[i+1]

            pairs = list(zip(sorted_players[::2], sorted_players[1::2]))

            self.pairs_already_played.append(paire)

        return pairs

    def lancer_tour_suivant(self):
        nouveau_tour = tour.Tour(f"Round {len(self.tournees)+1}")
        self.tournees.append(nouveau_tour)

        pairs = self.generer_pairs()
        nouveau_tour.create_matches(pairs)

    def finir_tour_courant(self):
        self.update_scores()
        self.tournees[-1].marquer_comme_terminer()

    def update_scores(self):
        self.scores = []
        all_scores = [player_and_score
                      for tournee in self.tournees
                      for match in tournee.matchs
                      for player_and_score in match]
        for player in self.players:
            player_score = 0
            for score in all_scores:
                if player is score[0]:
                    player_score += score[1]
            self.scores.append((player, player_score))

    def get_players_by_name(self):
        return sorted(self.players, key=lambda p: p.nom)

    def get_players_by_rank(self):
        return sorted(self.players, key=lambda p: p.rank)

    def get_turns(self):
        return self.tournees

    def get_matchs(self):
        return [match
                      for tournee in self.tournees
                      for match in tournee.matchs]

    def statut(self):
        if not self.tournees:
            statut = "Non démarré"
        elif len(self.tournees) == self.number_tours:
            statut = "Terminé"
        else:
            statut = "En cours"

        return statut

    def __repr__(self):
        repr = f"{self.nom} - {self.lieu} - {self.date} - Statut : {self.statut()} \n"
        repr += f"players : {len(self.players)}/{Tournoi.number_players}\n"
        for player in self.players:
            repr += f"\t{player}\n"

        repr += "\n"
        for tour in self.tournees:
            repr += f"{tour} \n"

        return repr
