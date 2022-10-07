import datetime
from mvc_chess.models.match import Match


class Tour:
    def __init__(self, nom):
        self.nom = nom
        self.matchs = []

        self.date_heure_debut = datetime.datetime.now()
        self.date_heure_fin = None

    def marquer_comme_terminer(self):
        self.date_heure_fin = datetime.datetime.now()

    def create_match(self, players_pair):
        match = Match(players_pair)
        self.matchs.append(match)

    def create_matches(self, players_pairs):
        for players_pair in players_pairs:
            self.create_match(players_pair)

    def set_match_score(self, match_index, score):
        match = self.matchs[match_index]
        match.set_score(score)

    def __repr__(self):
        repr = f"{self.nom} " \
               f"- Debut : {self.date_heure_debut.strftime('%Y-%m-%d %H:%M')}"
        if self.date_heure_fin:
            repr += f" - Fin : {self.date_heure_fin.strftime('%Y-%m-%d %H:%M')})"
        repr += "\n"
        for match in self.matchs:
            player_1, player_2 = match.get_players()
            score_player_1, score_player_2 = match.get_scores()
            repr += f"{player_1} VS {player_2}"
            if score_player_1 is not None:
                if score_player_1 == 1:
                    repr += f" -> {player_1} wins"
                elif 0 < score_player_1 < 1:
                    repr += f" -> draw"
                else:
                    repr += f" -> {player_2} wins"
            else:
                repr += f" -> waiting match result"
            repr += "\n"

        return repr
