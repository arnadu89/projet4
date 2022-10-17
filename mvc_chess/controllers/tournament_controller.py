from mvc_chess.views.tournament_view import TournamentView


class TournamentController:
    @classmethod
    def tournament_list(cls, models_manager, route_params=None):
        tournaments = models_manager.tournaments
        choice = TournamentView.tournament_list_view(tournaments)

        match choice:
            case "2" | "3":
                try:
                    tournament_id = int(input("Tournament id : "))
                except ValueError:
                    print("Error : tournament if must be an integer")
                    next_route = "tournament_list"
                    next_params = None
                    return next_route, next_params

                next_params = {"id": tournament_id}
                if choice == "3":
                    next_route = "tournament_manage"
                else:
                    next_route = "tournament_read"

            case "m":
                next_route = "main_menu"
                next_params = None
            case "q":
                next_route = "quit"
                next_params = None
            case _:
                next_route = "tournament_list"
                next_params = None

        return next_route, next_params

    @classmethod
    def tournament_read(cls, models_manager, route_params=None):
        try:
            tournament_id = route_params["id"]
            tournament = models_manager.tournaments[tournament_id]
        except KeyError:
            print("Error : missing ID in route parameters to read tournament")
            next_route = "tournament_list"
            return next_route, None
        except IndexError:
            print(f"Error : tournament with id {tournament_id} does not exist")
            next_route = "tournament_list"
            return next_route, None

        try:
            if "players_order" in route_params.keys():
                if route_params["players_order"] == "alphabetical":
                    tournament.players.sort(key=lambda p: [p.lastname, p.firstname])
                elif route_params["players_order"] == "rank":
                    tournament.players.sort(key=lambda p: [p.rank], reverse=True)
        except AttributeError:
            print("Error : missing ID in route parameters to read tournament")
            next_route = "tournament_list"
            return next_route, None

        show_matchs = True
        if "show_matchs" in route_params.keys() and route_params["show_matchs"] is False:
            show_matchs = False

        choice = TournamentView.tournament_read_view(tournament, show_matchs=show_matchs)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = None
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
            case "m":
                next_route = "main_menu"
                next_params = None
            case _:
                next_route = "tournament_read"
                next_params = {"id": tournament_id}

        return next_route, next_params

    @classmethod
    def tournament_manage(cls, models_manager, route_params=None):
        try:
            tournament_id = route_params["id"]
            tournament = models_manager.tournaments[tournament_id]
        except KeyError:
            print("Error : missing ID in route parameters to managing tournament")
            next_route = "tournament_list"
            return next_route, None
        except IndexError:
            print(f"Error : tournament with id {tournament_id} does not exist")
            next_route = "tournament_list"
            return next_route, None

        # Manage tournament
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

        return next_route, next_params

    @classmethod
    def _manage_tournament_with_not_all_players(cls, models_manager, tournament):
        choice = TournamentView.tournament_manage_with_not_all_players_view(tournament)

        match choice:
            case "1":
                next_route = "tournament_list"
                next_params = None
            case "2":
                next_route = "tournament_assign_player"
                next_params = {"id": tournament.id}
            case "m":
                next_route = "main_menu"
                next_params = None
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
                next_params = None
            case "2":
                tournament.begin_next_turn()
                models_manager.save()
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
            case "m":
                next_route = "main_menu"
                next_params = None
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
                next_params = None
            case "2" | "3" | "4" | "5":
                match_id = int(choice)-2
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
            case "m":
                next_route = "main_menu"
                next_params = None
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
                next_params = None
            case "2":
                tournament.begin_next_turn()
                models_manager.save()
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}
            case "m":
                next_route = "main_menu"
                next_params = None
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
                next_params = None
            case "m":
                next_route = "main_menu"
                next_params = None
            case _:
                next_route = "tournament_manage"
                next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def tournament_assign_player(cls, models_manager, route_params=None):
        """Assign player to tournament"""
        try:
            id = route_params["id"]
            tournament = models_manager.tournaments[id]
        except KeyError:
            print("Error : missing ID in route parameters to assign player to tournament")
            next_route = "tournament_list"
            return next_route, None
        except IndexError:
            print(f"Error : tournament with id {id} does not exist")
            next_route = "tournament_list"
            return next_route, None

        # Get players that are not already assign to this tournament
        assignable_players = [player
                              for player in models_manager.players
                              if player.id not in [p.id for p in tournament.players]]
        player_id = TournamentView.tournament_assign_player_view(tournament, assignable_players)

        try:
            player = next(player for player in assignable_players if int(player_id) == player.id)
            tournament.add_player(player)
            models_manager.save()
        except ValueError:
            print("Error : the player ID is not an integer")
            next_route = "tournament_manage"
            next_params = {"id": tournament.id}
            return next_route, next_params
        except StopIteration:
            print("Error : player with id {player_id} does not exist")
            next_route = "tournament_manage"
            next_params = {"id": tournament.id}
            return next_route, next_params

        next_route = "tournament_manage"
        next_params = {"id": tournament.id}

        return next_route, next_params

    @classmethod
    def tournament_valid_match(cls, models_manager, route_params=None):
        """Set score to tournament match"""
        try:
            tournament_id = route_params["tournament_id"]
            tournament = models_manager.tournaments[tournament_id]
        except KeyError:
            print("Error : missing tournament_ID in route parameters to set tournament match result")
            next_route = "tournament_list"
            return next_route, None
        except IndexError:
            print(f"Error : tournament with id {tournament_id} does not exist")
            next_route = "tournament_list"
            return next_route, None

        try:
            match_id = route_params["match_id"]
            match = tournament.get_current_turn().matchs[match_id]
        except KeyError:
            print("Error : missing match_ID in route parameters to set tournament match result")
            next_route = "tournament_list"
            return next_route, None
        except IndexError:
            print(f"Error : match id {match_id} does not exist in {tournament.name}")
            next_route = "tournament_list"
            return next_route, None

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
        models_manager.save()

        return next_route, next_params
