from mvc_chess.views.player_view import PlayerView
from mvc_chess.models.player import Player


class PlayerController:
    @classmethod
    def player_list(cls, models_manager, route_params={}):
        players = models_manager.players
        message = route_params.get("message")

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
        next_params = {}

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
                next_route = "player_list"
                next_params = {"message": "Invalid choice"}

        return next_route, next_params

    @classmethod
    def player_create(cls, models_manager, route_params={}):
        datas = PlayerView.player_create_view()

        if Player.is_valid(**datas):
            all_players = models_manager.players
            datas["id"] = len(all_players)
            datas["rank"] = int(datas["rank"])
            new_player = Player(**datas)

            all_players.append(new_player)
            models_manager.save()

            next_route = "player_list"
            next_params = {}
        else:
            next_route = "player_list"
            next_params = {"message": "Error during player creation"}

        return next_route, next_params

    @classmethod
    def player_update(cls, models_manager, route_params={}):
        player_id = route_params.get("id")
        player = PlayerController._get_player_by_id(models_manager, player_id)
        if player is None:
            next_route = "player_list"
            next_params = {"message": f"Error during updating player with id {player_id}"}
        else:
            datas = PlayerView.player_update_view(player)

            # Fill with original player data if updated data is empty
            updated_datas = {}
            for key, value in datas.items():
                if value == "":
                    updated_datas[key] = getattr(player, key)
                else:
                    updated_datas[key] = value

            if Player.is_valid(**updated_datas):
                player.lastname = updated_datas["lastname"]
                player.firstname = updated_datas["firstname"]
                player.birthdate = updated_datas["birthdate"]
                player.gender = updated_datas["gender"]
                player.rank = int(updated_datas["rank"])

                models_manager.save()

                next_route = "player_list"
                next_params = {}
            else:
                next_route = "player_list"
                next_params = {"message": f"Error during updating player with id {player.id}"}

        return next_route, next_params

    @classmethod
    def _get_player_by_id(cls, models_manager, player_id):
        try:
            player = models_manager.players[player_id]
        except IndexError:
            return None

        return player
