from mvc_chess.views.player_view import PlayerView
from mvc_chess.models.player import Player


class PlayerController:
    @classmethod
    def player_list(cls, models_manager, route_params=None):
        players = models_manager.players
        message = None

        if route_params and "player_sort" in route_params:
            player_sort = route_params["player_sort"]
            match player_sort:
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
            case "2":
                try:
                    input_id = int(input("ID of the player to update : "))
                except ValueError:
                    print("Error : ID must be an integer")
                    next_route = "player_list"
                else:
                    next_route = "player_update"
                    next_params = {"id": input_id}
            case "3":
                next_route = "player_list"
                next_params = {"player_sort": "alphabetical"}

            case "4":
                next_route = "player_list"
                next_params = {"player_sort": "rank"}

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
        # todo : validating datas of new player with is_valid method on player model object

        all_players = models_manager.players
        new_player.set_id(len(all_players))

        all_players.append(new_player)

        next_route = "player_list"
        next_params = None

        return next_route, next_params

    @classmethod
    def player_update(cls, models_manager, route_params=None):
        player = models_manager.players[route_params["id"]]
        input_player_update_datas = PlayerView.player_update_view(player)
        # todo : validating datas of updated player with is_valid method on player model object

        # updated_datas = dict(player.__dict__)
        # print(f"Updated datas = {updated_datas}")
        #
        # updated_datas.update(input_player_update_datas)
        # updated_player = Player(**updated_datas)
        # print(updated_player)

        next_route = "player_list"
        next_params = None
        return next_route, next_params
