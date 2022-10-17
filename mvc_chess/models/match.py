from mvc_chess.models.player import Player


class Match:
    score_names = [
        "first",
        "second",
        "draw"
    ]

    def __init__(self, players_pair):
        self.players = players_pair
        self.scores = [0, 0]

    def get_first_player(self):
        return self.players[0]

    def get_second_player(self):
        return self.players[1]

    def get_players(self):
        return self.players

    def get_score_first_player(self):
        return self.scores[0]

    def get_score_second_player(self):
        return self.scores[1]

    def get_scores(self):
        return self.scores

    def set_score(self, score):
        match score:
            case "first":
                self.scores[0] = 1
                self.scores[1] = -1
            case "second":
                self.scores[0] = -1
                self.scores[1] = 1
            case "draw":
                self.scores[0] = 1/2
                self.scores[1] = 1/2
            case _:
                scores_names = ''.join([score_name for score_name in Match.score_names])
                raise Exception(f"Error : Score in match must be {scores_names}"
                                f": {score} given")

    def is_finish(self):
        return self.scores[0] != 0

    def serialize(self):
        serialized_match = {
            "players": [
                player.serialize() for player in self.players
            ],
            "scores": self.scores,
        }
        return serialized_match

    @classmethod
    def deserialize(cls, serialized_match):
        deserialized_players = [
            Player.deserialize(serialized_player)
            for serialized_player in serialized_match["players"]
        ]
        match = Match(deserialized_players)
        match.scores = serialized_match["scores"]
        return match

    def __repr__(self):
        player_1, player_2 = self.get_players()
        score_player_1, score_player_2 = self.get_scores()
        repr = f"{player_1} VS {player_2}"
        if self.is_finish():
            if score_player_1 == 1:
                repr += f" -> {player_1} wins"
            elif 0 < score_player_1 < 1:
                repr += " -> draw"
            else:
                repr += f" -> {player_2} wins"
        else:
            repr += " -> waiting match result"
        return repr
