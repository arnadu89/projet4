import random
from tinydb import TinyDB
from mvc_chess.models.player import Player
from mvc_chess.models.tournament import Tournament
import mvc_chess.models.demo_funcs as demo


class ModelsManager:
    _db_player = TinyDB("db_player.json")
    _db_tournament = TinyDB("db_tournament.json")

    def __init__(self):
        self.players = []
        self.tournaments = []
        self.load()

    def save(self):
        serialized_players = []
        for player in self.players:
            serialized_player = player.serialize()
            serialized_players.append(serialized_player)
        ModelsManager._db_player.truncate()
        ModelsManager._db_player.insert_multiple(serialized_players)

        serialized_tournaments = []
        for tournament in self.tournaments:
            serialized_tournament = tournament.serialize()
            serialized_tournaments.append(serialized_tournament)
        ModelsManager._db_tournament.truncate()
        ModelsManager._db_tournament.insert_multiple(serialized_tournaments)

    def load(self):
        self.players = []
        serialized_players = ModelsManager._db_player.all()
        for player_id, serialized_player in enumerate(serialized_players):
            player = Player.deserialize(serialized_player)
            player.set_id(player_id)
            self.players.append(player)

        self.tournaments = []
        serialized_tournaments = ModelsManager._db_tournament.all()
        for tournament_id, serialized_tournament in enumerate(serialized_tournaments):
            tournament = Tournament.deserialize(serialized_tournament)
            tournament.set_id(tournament_id)
            self.tournaments.append(tournament)

    def demo_db(self, keep):
        if not keep:
            self.players = []
            self.tournaments = []
            demo.append_players(self)
            demo.append_tournament_1(self)
            demo.append_tournament_2(self)

            self.save()

        self.load()
