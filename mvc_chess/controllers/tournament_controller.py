from mvc_chess.views.tournament_view import TournamentView
from mvc_chess.models.tournament import Tournament


class TournamentController:
    @classmethod
    def tournament_list(cls, models_manager, route_params={}):
        tournaments = models_manager.tournaments
        message = route_params.get("message")
        choice = TournamentView.tournament_list_view(tournaments, message)
        next_params = {}

        match choice:
            case "1":
                next_route = "tournament_create"
            case "2" | "3":
                try:
                    tournament_id = int(input("Tournament id : "))
                except ValueError:
                    print("Error : tournament if must be an integer")
                    next_route = "tournament_list"
                    return next_route, next_params

                next_params = {"id": tournament_id}
                if choice == "3":
                    next_route = "tournament_manage"
                else:
                    next_route = "tournament_read"

            case "m":
                next_route = "main_menu"
            case "q":
                next_route = "quit"
            case _:
                next_route = "tournament_list"

        return next_route, next_params

    @classmethod
    def tournament_create(cls, models_manager, route_params={}):
        datas = TournamentView.tournament_create_view()
        next_params = {}

        if Tournament.is_valid(**datas):
            all_tournaments = models_manager.tournaments
            datas["id"] = len(all_tournaments)
            new_tournament = Tournament(**datas)
            all_tournaments.append(new_tournament)
            models_manager.save()

            next_route = "tournament_read"
            next_params = {
                "id": new_tournament.id,
                "message": "Error : Error during tournament creation"
            }
        else:
            next_route = "tournament_list"

        return next_route, next_params

    @classmethod
    def tournament_read(cls, models_manager, route_params={}):
        tournament_id = route_params.get("id")
        tournament = TournamentController.__get_tournament_by_id(models_manager, tournament_id)
        if tournament is None:
            next_route = "tournament_list"
            next_params = {"message": "Error : incorrect ID in route parameters to read tournament"}
        else:
            # Players sorting
            if route_params.get("players_order") == "alphabetical":
                tournament.players.sort(key=lambda p: [p.lastname, p.firstname])
            elif route_params.get("players_order") == "rank":
                tournament.players.sort(key=lambda p: [p.rank], reverse=True)

            # Matchs visibility
            show_matchs = False if route_params.get("show_matchs") is False else True

            choice = TournamentView.tournament_read_view(tournament, show_matchs=show_matchs)

            match choice:
                case "1":
                    next_route = "tournament_list"
                    next_params = {}
                case "2":
                    next_route = "tournament_read"
                    next_params = {
                        "id": tournament_id,
                        "players_order": "alphabetical"
                    }
                case "3":
                    next_route = "tournament_read"
                    next_params = {
                        "id": tournament_id,
                        "players_order": "rank"
                    }
                case "4":
                    next_route = "tournament_read"
                    next_params = {
                        "id": tournament_id,
                        "show_matchs": False
                    }
                case "5":
                    next_route = "tournament_manage"
                    next_params = {"id": tournament_id}
                case _:
                    next_route = "tournament_read"
                    next_params = {"id": tournament_id}

        return next_route, next_params

    @classmethod
    def tournament_manage(cls, models_manager, route_params={}):
        tournament_id = route_params.get("id")
        tournament = TournamentController.__get_tournament_by_id(models_manager, tournament_id)
        if tournament is None:
            next_route = "tournament_list"
            next_params = {"message": "Error : incorrect ID in route parameters to manage tournament"}
        else:
            message = route_params.get("message")
            TournamentView.tournament_manage_base_view(tournament, message=message)
            if len(tournament.players) < tournament.number_players:
                # Manage not started tournament - not all players assigned
                next_route, next_params = TournamentController._manage_tournament_with_not_all_players(
                    models_manager,
                    tournament
                )
            elif tournament.state() == tournament.states["NOT_STARTED"]:
                # Manage not started tournament - all player - ready to start
                next_route, next_params = TournamentController._manage_tournament_not_started(
                    models_manager,
                    tournament
                )
            elif tournament.state() == tournament.states["FINISHED"]:
                # Manage finish tournament - all turns are finished
                next_route, next_params = TournamentController._manage_tournament_finished(
                    models_manager,
                    tournament
                )
            elif tournament.state() == tournament.states["IN_PROGRESS"] and not tournament.get_current_turn().is_finish():
                # Manage started tournament - current turn not finish
                next_route, next_params = TournamentController._manage_tournament_started_turn_in_progress(
                    models_manager,
                    tournament
                )
            elif tournament.state() == tournament.states["IN_PROGRESS"] and tournament.get_current_turn().is_finish():
                # Manage started tournament - current turn finish waiting for next turn to br started
                next_route, next_params = TournamentController._manage_tournament_started_waiting_next_turn(
                    models_manager,
                    tournament
                )
            else:
                next_route = "tournament_list"
                next_params = {f"message": f"Error : Tournament with id {tournament.id} is not suitable for management"}

        return next_route, next_params

    @classmethod
    def _manage_tournament_with_not_all_players(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_with_not_all_players_view(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = {}
            case "2":
                next_route = "tournament_assign_player"
                next_params = {"id": tournament.id}
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def _manage_tournament_not_started(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_not_started_view(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = {}
            case "2":
                tournament.begin_next_turn()
                models_manager.save()
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def _manage_tournament_started_turn_in_progress(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_started_turn_in_progress_view(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = {}
            case "2" | "3" | "4" | "5":
                match_id = int(choice) - 2
                next_route = "tournament_valid_match"
                next_params = {
                    "tournament_id": tournament.id,
                    "match_id": match_id
                }
            case "6":
                current_turn = tournament.get_current_turn()
                if current_turn.is_all_matchs_finish():
                    tournament.end_current_turn()
                    models_manager.save()
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def _manage_tournament_started_waiting_next_turn(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_started_waiting_next_turn(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = {}
            case "2":
                tournament.begin_next_turn()
                models_manager.save()
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def _manage_tournament_finished(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_finished(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = {}
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def tournament_assign_player(cls, models_manager, route_params={}):
        """Assign player to tournament"""
        tournament_id = route_params.get("id")
        tournament = TournamentController.__get_tournament_by_id(models_manager, tournament_id)
        if tournament is None:
            next_route = "tournament_list"
            next_params = {"message": "Error : incorrect ID in route parameters to assign players tournament"}
        else:
            # Get players that are not already assign to this tournament
            assignable_players = [player
                                  for player in models_manager.players
                                  if player.id not in [p.id for p in tournament.players]]
            player_id = TournamentView.tournament_assign_player_view(tournament, assignable_players)

            try:
                player = next(player for player in assignable_players if int(player_id) == player.id)
                tournament.add_player(player)
                print("tournament add player")
            except ValueError:
                next_route = "tournament_manage"
                next_params = {
                    "id": tournament.id,
                    "message": "Error : the player ID is not an integer",
                }
                return next_route, next_params
            except StopIteration:
                next_route = "tournament_manage"
                next_params = {
                    "id": tournament.id,
                    "message": f"Error : player with id {player_id} does not exist",
                }
                return next_route, next_params

            models_manager.save()
            next_route = "tournament_manage"
            next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def tournament_valid_match(cls, models_manager, route_params={}):
        """Set score to tournament match"""
        tournament_id = route_params.get("tournament_id")
        tournament = TournamentController.__get_tournament_by_id(models_manager, tournament_id)
        if tournament is None:
            next_route = "tournament_list"
            next_params = {"message": "Error : incorrect ID in route parameters to valid match tournament"}
        else:
            match_id = route_params.get("match_id")
            match = tournament.get_current_turn().get_match_by_index(match_id)
            if match is None:
                next_route = "tournament_manage"
                next_params = {
                    "message": f"Error : Can't find match with id {match_id} for tournament with id {tournament.id}"
                }
            else:
                if match.is_finish():
                    next_route = "tournament_manage"
                    next_params = {"id": tournament.id}
                    return next_route, next_params

                match_result = TournamentView.tournament_valid_match(tournament, match)

                match match_result:
                    case "1":
                        match.set_score("first")
                    case "2":
                        match.set_score("second")
                    case "3":
                        match.set_score("draw")
                    case _:
                        next_route = "tournament_manage"
                        next_params = {"id": tournament.id}
                        return next_route, next_params

                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
                tournament.update_score()
                models_manager.save()

        return next_route, next_params

    @classmethod
    def __get_tournament_by_id(cls, models_manager, tournament_id):
        try:
            tournament = models_manager.tournaments[tournament_id]
        except IndexError:
            return None
        except TypeError:
            return None

        return tournament
