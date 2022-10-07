from mvc_chess.views.player_view import PlayerView


class PlayerController:
    @classmethod
    def player_list(cls, models_manager, route_params=None):
        players = models_manager.players
        choice = PlayerView.player_list_view(players)
        choice = choice.lower()
        next_params = None

        match choice:
            case "m":
                next_route = "main_menu"
            case "q":
                next_route = "quit"
            case _:
                print("Error : Invalid parameter")
                next_route = "player_list"

        return next_route, next_params
