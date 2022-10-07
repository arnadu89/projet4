from mvc_chess.views.player_view import PlayerView
from mvc_chess.models.player import Player


class PlayerController:
    @classmethod
    def player_list(cls, models_manager, route_params=None):
        players = models_manager.players
        message = None
        match route_params:
            case "alphabetical":
                message = "Players list in alphabetical order"
                players = sorted(players, key=lambda p: (p.lastname, p.firstname))
            case "rank":
                message = "Players list order by rank"
                players = sorted(players, key=lambda p: p.rank, reverse=True)

        choice = PlayerView.player_list_view(players, message)
        choice = choice.lower()
        next_params = None

        match choice:
            case "1":
                next_route = "player_create"
            case "3":
                next_route = "player_list"
                next_params = "alphabetical"
            case "4":
                next_route = "player_list"
                next_params = "rank"
            case "m":
                next_route = "main_menu"
            case "q":
                next_route = "quit"
            case _:
                print("Error : Invalid parameter")
                next_route = "player_list"

        return next_route, next_params

    @classmethod
    def player_create(cls, models_manager, route_params=None):
        datas = PlayerView.player_create_view()

        datas["rank"] = int(datas["rank"])
        new_player = Player(**datas)

        models_manager.players.append(new_player)

        next_route = "player_list"
        next_params = None
        # next_route = "player_read"
        # next_params = len(models_manager.players)

        return next_route, next_params
