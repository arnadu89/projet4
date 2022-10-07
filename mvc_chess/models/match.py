class Match(tuple):
    def __new__(cls, players_pair):
        tuple_args = (
            [players_pair[0], None],
            [players_pair[1], None]
        )
        return super(Match, cls).__new__(cls, tuple(tuple_args))

    def get_first_player(self):
        return self[0][0]

    def get_second_player(self):
        return self[1][0]

    def get_players(self):
        return self[0][0], self[1][0]

    def get_score_first_player(self):
        return self[0][0]

    def get_score_second_player(self):
        return self[1][0]

    def get_scores(self):
        return self[0][1], self[1][1]

    def set_score(self, score):
        match score:
            case "first":
                self[0][1] = 1
                self[1][1] = -1
            case "second":
                self[0][1] = -1
                self[1][1] = 1
            case "draw":
                self[0][1] = 1/2
                self[1][1] = 1/2
            case _:
                raise Exception(f"Error : Score in match must be first, second or draw "
                                f": {score} given")
