import datetime
from mvc_chess.models.match import Match


class Turn:
    def __init__(self, name):
        self.name = name
        self.matchs = []

        self.start_date_time = datetime.datetime.now()
        self.end_date_time = None

    def mark_as_complete(self):
        self.end_date_time = datetime.datetime.now()

    def is_finish(self):
        return self.end_date_time is not None

    def is_all_matchs_finish(self):
        for match in self.matchs:
            if not match.is_finish():
                return False
        return True

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
        repr = f"{self.name} " \
               f"- Debut : {self.start_date_time.strftime('%Y-%m-%d %H:%M')}"
        if self.end_date_time:
            repr += f" - Fin : {self.end_date_time.strftime('%Y-%m-%d %H:%M')})"
        repr += "\n"
        for match in self.matchs:
            repr += f"{match}"
            repr += "\n"

        return repr
