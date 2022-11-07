import datetime
from mvc_chess.models.match import Match


class Turn:
    def __init__(self, name):
        self.name = name
        self.matchs = []

        self.start_date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.end_date_time = None

    def mark_as_complete(self):
        self.end_date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def is_finish(self):
        return self.end_date_time is not None

    def is_all_matchs_finish(self):
        for match in self.matchs:
            if not match.is_finish():
                return False
        return True

    def create_match(self, player_1, player_2):
        match = Match(player_1, player_2)
        self.matchs.append(match)

    def create_matches(self, players_pairs):
        for players_pair in players_pairs:
            self.create_match(*players_pair)

    def set_match_score(self, match_index, score):
        match = self.matchs[match_index]
        match.set_score(score)

    def get_match_by_index(self, match_index):
        try:
            match = self.matchs[match_index]
        except IndexError:
            return None
        except TypeError:
            return None

        return match

    def serialize(self):
        serialized_turn = {
            "name": self.name,
            "matchs": [
                match.serialize() for match in self.matchs
            ],
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
        }
        return serialized_turn

    @classmethod
    def deserialize(cls, serialized_turn, players):
        turn = Turn(serialized_turn["name"])
        turn.matchs = [
            Match.deserialize(serialized_match, players)
            for serialized_match in serialized_turn["matchs"]
        ]
        turn.start_date_time = serialized_turn["start_date_time"]
        turn.end_date_time = serialized_turn["end_date_time"]
        return turn

    def __repr__(self):
        repr = f"{self.name} " \
               f"- Debut : {self.start_date_time}"
        if self.end_date_time:
            repr += f" - Fin : {self.end_date_time})"
        repr += "\n"
        for match in self.matchs:
            repr += f"{match}"
            repr += "\n"

        return repr
