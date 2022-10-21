import mvc_chess.models.turn as turn
from mvc_chess.models.player import Player
from mvc_chess.models.turn import Turn


class Tournament:
    states = {
        "NOT_STARTED": "Non démarré",
        "IN_PROGRESS": "En cours",
        "FINISHED": "Terminé"
    }
    time_controls = [
        "Bullet",
        "Blitz",
        "Coup rapide"
    ]
    number_players = 8

    def __init__(self, id,
                 name, location, date,
                 time_control, description,
                 number_turns=4
                 ):
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.players = []
        self.turns = []
        self.scores = [] # todo : transform to id dict
        self._time_control = time_control
        self.description = description
        self.number_turns = number_turns
        self.pairs_already_played = []

    @property
    def time_control(self):
        return self._time_control

    @time_control.setter
    def time_control(self, value):
        if value in Tournament.time_controls:
            self.time_control = value

    def add_player(self, new_player):
        self.players.append(new_player)

    def has_pairs_already_played(self, two_players):
        if two_players in self.pairs_already_played or\
                two_players[::-1] in self.pairs_already_played:
            return True
        return False

    def refresh_pairs_already_played(self):
        all_matchs = [match
                      for turn in self.turns
                      for match in turn.matchs]
        for match in all_matchs:
            pair = match.get_players()
            if pair not in self.pairs_already_played:
                self.pairs_already_played.append(pair)

    def generate_pairs(self):
        # Premier tour
        if len(self.turns) == 1:
            sorted_players = sorted(self.players, key=lambda j: j.rank, reverse=True)
            pairs = zip(
                sorted_players[:int(Tournament.number_players / 2)],
                sorted_players[int(Tournament.number_players / 2):]
            )
            pairs = list(pairs)
        else:  # Tours suivants
            # On tri les players selon leur score/rank
            mixed_players = []
            for player in self.players:
                mixed_players.append((player, self.get_player_score(player), player.rank))

            sorted_players_score = sorted(mixed_players, key=lambda elm: (elm[1], elm[2]), reverse=True)
            sorted_players = [elm[0] for elm in sorted_players_score]

            # On aparie les joueurs dans l'ordre des scores/rank en décalant si le match a déjà eu lieu
            pairs = []
            while sorted_players:
                current_player = sorted_players.pop(0)
                for potential_player in sorted_players:
                    potential_pair = [current_player, potential_player]
                    if not self.has_pairs_already_played(potential_pair):
                        pair = potential_pair
                        sorted_players.remove(potential_player)
                        break
                else:
                    pair = [current_player, sorted_players[0]]
                    sorted_players.pop(0)

                pairs.append(pair)

        self.pairs_already_played.extend(pairs)
        return pairs

    def begin_next_turn(self):
        new_turn = turn.Turn(f"Round {len(self.turns) + 1}")
        self.turns.append(new_turn)

        pairs = self.generate_pairs()
        new_turn.create_matches(pairs)

    def end_current_turn(self):
        self.update_scores()
        self.turns[-1].mark_as_complete()

    def get_current_turn(self):
        return self.get_turns()[-1] if self.get_turns() else None

    def update_scores(self):
        self.scores = []
        all_matchs = [match
                      for turn in self.turns
                      for match in turn.matchs]

        for player in self.players:
            player_score = 0
            for match in all_matchs:
                if player is match.get_first_player():
                    player_score += match.get_score_first_player()
                elif player is match.get_second_player():
                    player_score += match.get_score_second_player()
            self.scores.append((player, player_score))

    def get_player_score(self, player):
        player_score = [score for score in self.scores if score[0] is player]
        return player_score[0][1] if player_score else 0

    def get_players_by_name(self):
        return sorted(self.players, key=lambda p: p.nom)

    def get_players_by_rank(self):
        return sorted(self.players, key=lambda p: p.rank)

    def get_turns(self):
        return self.turns

    def get_matchs(self):
        return [match
                for turn in self.turns
                for match in turn.matchs
                ]

    def state(self):
        if not self.turns:
            state = Tournament.states["NOT_STARTED"]
        elif len(self.turns) == self.number_turns and\
                self.turns[-1].is_finish():
            state = Tournament.states["FINISHED"]
        else:
            state = Tournament.states["IN_PROGRESS"]

        return state

    def set_id(self, new_id):
        try:
            self.id = int(new_id)
        except ValueError as error:
            raise ValueError(error)

    def serialize(self):
        serialized_tournament = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": [
                player.id for player in self.players
            ],
            "turns": [
                turn.serialize() for turn in self.turns
            ],
            "time_control": self.time_control,
            "description": self.description,
            "number_turns": self.number_turns,
        }

        return serialized_tournament

    @classmethod
    def deserialize(cls, serialized_tournament, players):
        tournament = Tournament(
            serialized_tournament["id"],
            serialized_tournament["name"],
            serialized_tournament["location"],
            serialized_tournament["date"],
            serialized_tournament["time_control"],
            serialized_tournament["description"],
            serialized_tournament["number_turns"]
        )

        for player_id in serialized_tournament["players"]:
            player = next(player for player in players if player.id == player_id)
            tournament.add_player(player)

        for serialized_turn in serialized_tournament["turns"]:
            deserialized_turn = Turn.deserialize(serialized_turn)
            tournament.turns.append(deserialized_turn)

        tournament.update_scores()
        tournament.refresh_pairs_already_played()
        return tournament

    @classmethod
    def is_valid(cls, name, location, date,
                 time_control, description):
        if not name or not location or not date:
            return False
        if time_control not in Tournament.time_controls:
            return False
        return True

    def __repr__(self):
        repr = f"{self.name} - {self.location} - {self.date} - state : {self.state()} \n"
        repr += f"players : {len(self.players)}/{Tournament.number_players}\n"
        sorted_players = sorted(self.players, key=lambda p: [self.get_player_score(p), p.rank], reverse=True)
        for player in sorted_players:
            repr += f"\t{player.lastname}\t{player.firstname}\t{player.rank}\t{self.get_player_score(player)}\n"

        repr += "\n"
        for tournament_turn in self.turns:
            repr += f"{tournament_turn} \n"

        return repr
