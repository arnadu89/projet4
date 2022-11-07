import subprocess
from mvc_chess.models import models_manager
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
        self.route_params = {}
        self.exit = False

    def run(self):
        models_manager_instance = models_manager.ModelsManager()

        keep = input("Keep data ? : ")
        models_manager_instance.demo_db(int(keep))

        while not self.exit:
            subprocess.call("clear", shell=True)
            print(f"route is : {self.route}")
            print(f"route_params is : {self.route_params}")

            controller_method = self.routes[self.route]

            next_route, next_params = controller_method(
                models_manager_instance,
                self.route_params
            )

            self.route = next_route
            self.route_params = next_params

            if next_route == "quit":
                self.exit = True
