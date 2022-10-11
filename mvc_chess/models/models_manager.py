import random
import mvc_chess.models.player as player
import mvc_chess.models.tournament as tournament


class ModelsManager:
    players = []
    tournaments = []

    @classmethod
    def demo(cls):
        # Players
        players = [
            player.Player("echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
        ]

        for player_id, player_instance in enumerate(players):
            player_instance.set_id(player_id)

        ModelsManager.players.extend(players)

        # Tournoi
        tournament_datas = {
            'name': 'Tournoi Régional 1',
            'location': 'Paris',
            'date': '24/03/2021',
            'time_control': 'Bullet',
            'description': 'Tournoi régional de paris junior',
        }
        ModelsManager.tournaments.append(tournament.Tournament(**tournament_datas))
        ModelsManager.tournaments[-1].set_id(0)