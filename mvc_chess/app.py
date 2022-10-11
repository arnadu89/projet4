import subprocess
from models import player, tournament, models_manager
from mvc_chess.controllers.main_menu_controller import MainMenuController
from mvc_chess.controllers.player_controller import PlayerController
from mvc_chess.controllers.tournament_controller import TournamentController


class Application:
    routes = {
        "main_menu": MainMenuController.main_menu,
        "player_list": PlayerController.player_list,
        "player_create": PlayerController.player_create,
        "player_update": PlayerController.player_update,
        "tournament_list": TournamentController.tournament_list,
        "tournament_manage": TournamentController.tournament_manage,
    }

    def __init__(self):
        self.route = "main_menu"
        self.route_params = None
        self.exit = False

    @classmethod
    def demo(cls):
        import random
        # Créer un nouveau tournoi
        tournament_datas = {
            'name': 'Tournoi Régional 1',
            'location': 'Paris',
            'date': '24/03/2021',
            'time_control': 'Bullet',
            'description': 'Tournoi régional de paris junior',
        }
        tournament_instance = tournament.Tournament(**tournament_datas)

        # Créer des joueurs
        joueurs = [
            player.Player("echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
        ]
        # [print(p) for p in joueurs]

        # Ajout 8 joueurs au tournoi
        [tournament_instance.add_player(p) for p in joueurs]

        # print(tournament_instance)
        # Jouer les tours
        scores_name = [
            "first",
            "second",
            "draw"
        ]
        for i in range(tournament_instance.number_tours):
            tournament_instance.begin_next_turn()
            # print(tournament_instance)

            # valider les matchs du tour
            last_turn = tournament_instance.turns[-1]
            for match_index in range(4):
                last_turn.set_match_score(match_index, random.choice(scores_name))

            tournament_instance.end_current_turn()
            print(tournament_instance)

            # print(f"matchs : {tournament_instance.get_matchs()}")

    def run(self):
        # Application.demo()

        # loading ModelsManager
        mm = models_manager.ModelsManager()
        models_manager.ModelsManager.demo()

        while not self.exit:
            subprocess.call("clear", shell=True)

            controller_method = self.routes[self.route]

            next_route, next_params = controller_method(
                mm,
                self.route_params
            )

            self.route = next_route
            self.route_params = next_params

            if next_route == "quit":
                self.exit = True
