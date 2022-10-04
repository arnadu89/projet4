import datetime


class Tour:
    def __init__(self, nom):
        self.nom = nom
        self.matchs = []

        self.date_heure_debut = datetime.datetime.now()
        self.date_heure_fin = None

    def marquer_comme_terminer(self):
        self.date_heure_fin = datetime.datetime.now()

    def create_match(self, paire_joueurs):
        match = (
            [paire_joueurs[0], None],
            [paire_joueurs[1], None]
        )
        self.matchs.append(match)

    def create_matches(self, paires_joueurs):
        for paire in paires_joueurs:
            self.create_match(paire)

    def set_match_score(self, match_index, score):
        match = self.matchs[match_index]
        if score == 1:
            match[0][1] = 1
            match[1][1] = -1
        elif score == 0:
            match[0][1] = -1
            match[1][1] = 1
        else:
            match[0][1] = 0.5
            match[1][1] = 0.5


    def __repr__(self):
        repr = f"{self.nom} " \
               f"- Debut : {self.date_heure_debut.strftime('%Y-%m-%d %H:%M')}"
        if self.date_heure_fin:
            repr += f" - Fin : {self.date_heure_fin.strftime('%Y-%m-%d %H:%M')})"
        repr += "\n"
        for match in self.matchs:
            player_1, score_player_1 = match[0]
            player_2, score_player_2 = match[1]
            repr += f"{player_1} VS {player_2}"
            if score_player_1 is not None:
                if score_player_1 == 1:
                    repr += f" -> {player_1} wins"
                elif 0 < score_player_1 < 1 :
                    repr += f" -> draw"
                else:
                    repr += f" -> {player_2} wins"
            else:
                repr += f" -> waiting match result"
            repr += "\n"

        return repr
