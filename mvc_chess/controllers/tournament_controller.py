from mvc_chess.views.tournament_view import TournamentView


class TournamentController:
    @classmethod
    def tournament_list(cls, models_manager, route_params=None):
        tournaments = models_manager.tournaments
        choice = TournamentView.tournament_list_view(tournaments)

        match choice:
            case "2":
                try:
                    tournament_id = int(input("Tournament id : "))
                    next_route = "tournament_manage"
                    next_params = {"id": tournament_id}
                except ValueError:
                    print(f"Error : tournament if must be an integer")
                    next_route = "tournament_list"
                    next_params = None
            case "m":
                next_route = "main_menu"
                next_params = None
            case _:
                next_route = "tournament_list"
                next_params = None

        return next_route, next_params

    @classmethod
    def tournament_manage(cls, models_manager, route_params=None):
        try:
            id = route_params["id"]
            tournament = models_manager.tournaments[id]
        except IndexError:
            print(f"Error : tournament with id {id} does not exist")
            next_route = "tournament_list"
            return next_route, None

        choice = TournamentView.tournament_manage_view(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = None
            case "m":
                next_route = "main_menu"
                next_params = None
            case _:
                next_route = "tournament_list"
                next_params = None

        return next_route, next_params