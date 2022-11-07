from mvc_chess.views.main_menu_view import MainMenuView


class MainMenuController:
    @classmethod
    def main_menu(cls, models_manager, route_params=None):
        choice = MainMenuView.main_menu_view()

        match choice:
            case "1":
                next_route = "player_list"
            case "2":
                next_route = "tournament_list"
            case "q":
                next_route = "quit"
            case _:
                print("Error : Invalid parameter")
                next_route = "main_menu"

        return next_route, {}
