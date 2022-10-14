import random
from mvc_chess.models.player import Player
from mvc_chess.models.tournament import Tournament


class ModelsManager:
    players = []
    tournaments = []

    @classmethod
    def demo(cls):
        # Players
        players = [
            Player("echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
            Player("echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
        ]

        for player_id, player_instance in enumerate(players):
            player_instance.set_id(player_id)

        ModelsManager.players.extend(players)

        # Tournois
        # Tournoi - non démarré
        tournament_datas = {
            'name': 'Tournoi Régional 1',
            'location': 'Paris',
            'date': '24/03/2021',
            'time_control': 'Bullet',
            'description': 'Tournoi régional de paris junior',
        }
        tournament_instance = Tournament(**tournament_datas)
        ModelsManager.tournaments.append(tournament_instance)
        tournament_instance.set_id(0)

        # Tournoi - démarré 7/8 joueurs
        tournament_datas = {
            'name': 'Tournoi National 1',
            'location': 'Paris',
            'date': '14/06/2021',
            'time_control': 'Bullet',
            'description': 'Tournoi national de paris senior',
        }
        tournament_instance = Tournament(**tournament_datas)
        ModelsManager.tournaments.append(tournament_instance)
        tournament_instance.set_id(1)

        for player in players[:7]:
            tournament_instance.add_player(player)

        # Tournoi - démarré 8/8 joueurs Tour 1 juste démarré
        tournament_datas = {
            'name': 'Tournoi National 2',
            'location': 'Paris',
            'date': '14/06/2022',
            'time_control': 'Bullet',
            'description': 'Tournoi national de paris senior',
        }
        tournament_instance = Tournament(**tournament_datas)
        ModelsManager.tournaments.append(tournament_instance)
        tournament_instance.set_id(2)

        for player in players[:8]:
            tournament_instance.add_player(player)

        tournament_instance.begin_next_turn()

        # Tournoi - démarré 8/8 joueurs Tour 1 complet / Tour 2 juste démarré
        tournament_datas = {
            'name': 'Tournoi National 2',
            'location': 'Paris',
            'date': '14/06/2022',
            'time_control': 'Bullet',
            'description': 'Tournoi national de paris senior',
        }
        tournament_instance = Tournament(**tournament_datas)
        ModelsManager.tournaments.append(tournament_instance)
        tournament_instance.set_id(3)

        for player in players[:8]:
            tournament_instance.add_player(player)

        tournament_instance.begin_next_turn()

        for match in tournament_instance.get_matchs():
            match.set_score("first")

        tournament_instance.end_current_turn()

        # Tournoi - démarré 8/8 joueurs Dernier tour à finir
        tournament_datas = {
            'name': 'Tournoi National 2',
            'location': 'Paris',
            'date': '14/06/2022',
            'time_control': 'Bullet',
            'description': 'Tournoi national de paris senior',
        }
        tournament_instance = Tournament(**tournament_datas)
        ModelsManager.tournaments.append(tournament_instance)
        tournament_instance.set_id(4)

        for player in players[:8]:
            tournament_instance.add_player(player)

        for i in range(tournament_instance.number_tours-1):
            tournament_instance.begin_next_turn()
            for match in tournament_instance.get_current_turn().matchs:
                match.set_score("first")

            tournament_instance.end_current_turn()
