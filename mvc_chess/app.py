import subprocess
from models import models_manager
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
        "tournament_create": TournamentController.tournament_create,
        "tournament_read": TournamentController.tournament_read,
        "tournament_manage": TournamentController.tournament_manage,
        "tournament_assign_player": TournamentController.tournament_assign_player,
        "tournament_valid_match": TournamentController.tournament_valid_match,
    }

    def __init__(self):
        self.route = "main_menu"
        self.route_params = None
        self.exit = False

    def run(self):
        # loading ModelsManager
        mm = models_manager.ModelsManager()
        # mm.demo()

        keep = input("Keep data ? : ")
        mm.demo_db(int(keep))

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
