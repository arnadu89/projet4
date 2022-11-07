import random

from mvc_chess.models.player import Player
from mvc_chess.models.tournament import Tournament


def append_players(mm):
    # Players
    players = [
        Player(0, "echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(1, "echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(2, "echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(3, "echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(4, "echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(5, "echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(6, "echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
        Player(7, "echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
    ]

    for player_id, player_instance in enumerate(players):
        player_instance.set_id(player_id)

    mm.players = players


# Tournois
def append_tournament_1(mm):
    # Tournoi - non démarré
    tournament_datas = {
        "id": 0,
        "name": "Tournoi Régional 1",
        "location": "Paris",
        "date": "24/03/2021",
        "time_control": "Bullet",
        "description": "Tournoi régional de paris junior",
    }
    tournament_instance = Tournament(**tournament_datas)
    mm.tournaments.append(tournament_instance)


def append_tournament_2(mm):
    # Tournoi - démarré 7/8 joueurs
    tournament_datas = {
        "id": 1,
        "name": "Tournoi National 1",
        "location": "Paris",
        "date": "14/06/2021",
        "time_control": "Bullet",
        "description": "Tournoi national de paris senior",
    }
    tournament_instance = Tournament(**tournament_datas)
    mm.tournaments.append(tournament_instance)

    for player in mm.players[:7]:
        tournament_instance.add_player(player)


def append_tournament_3(mm):
    # Tournoi - démarré 8/8 joueurs Tour 1 juste démarré
    tournament_datas = {
        "id": 2,
        "name": "Tournoi National 2",
        "location": "Paris",
        "date": "14/06/2022",
        "time_control": "Bullet",
        "description": "Tournoi national de paris senior",
    }
    tournament_instance = Tournament(**tournament_datas)
    mm.tournaments.append(tournament_instance)

    for player in mm.players[:8]:
        tournament_instance.add_player(player)

    tournament_instance.begin_next_turn()


def append_tournament_4(mm):
    # Tournoi - démarré 8/8 joueurs Tour 1 complet / Tour 2 juste démarré
    tournament_datas = {
        "id": 3,
        "name": "Tournoi National 2",
        "location": "Paris",
        "date": "14/06/2022",
        "time_control": "Bullet",
        "description": "Tournoi national de paris senior",
    }
    tournament_instance = Tournament(**tournament_datas)
    mm.tournaments.append(tournament_instance)

    for player in mm.players[:8]:
        tournament_instance.add_player(player)

    tournament_instance.begin_next_turn()

    for match in tournament_instance.get_matchs():
        match.set_score("first")

    tournament_instance.end_current_turn()


def append_tournament_5(mm):
    # Tournoi - démarré 8/8 joueurs Dernier tour à finir
    tournament_datas = {
        "id": 4,
        "name": "Tournoi National 2",
        "location": "Paris",
        "date": "14/06/2022",
        "time_control": "Bullet",
        "description": "Tournoi national de paris senior",
    }
    tournament_instance = Tournament(**tournament_datas)
    mm.tournaments.append(tournament_instance)

    for player in mm.players[:8]:
        tournament_instance.add_player(player)

    for i in range(tournament_instance.number_turns - 1):
        tournament_instance.begin_next_turn()
        for match in tournament_instance.get_current_turn().matchs:
            match.set_score("first")

        tournament_instance.end_current_turn()
