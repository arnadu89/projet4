import mvc_chess.views.player_view as player_view
from mvc_chess.views.base_view import BaseView


class TournamentView:
    @classmethod
    def tournament_list_view(cls, tournaments, message=None):
        BaseView.base_view()
        if message:
            print(message)

        print("-- Tournaments list :")
        if not tournaments:
            print("No tournament in the base")
        else:
            print("ID\tName\t\t\tLocation\t\t\tDate\t\t\tPlayers\t\t\tState")
            for tournament in tournaments:
                print(
                    f"{tournament.id}\t{tournament.name}"
                    f"\t\t{tournament.location}\t\t\t{tournament.date}"
                    f"\t\t{len(tournament.players)}/{tournament.number_players}"
                    f"\t\t\t{tournament.state()}")

        print("\n1. Create a new tournament")
        if tournaments:
            print("2. View tournament detail")
            print("3. Manage a tournament")
        print("M. Main menu")
        print("Q. Quit")
        return input("Choice : ")

    @classmethod
    def tournament_create_view(cls):
        BaseView.base_view()
        print("-- Create a new tournament :")
        return {
            "name": input("Name : "),
            "location": input("Location : "),
            "date": input("Date : "),
            "time_control": input("Time control [Bullet | Blitz | Rapid]: "),
            "description": input("Description : "),
        }

    @classmethod
    def tournament_read_view(cls, tournament,
                             show_players=True,
                             show_turns=True,
                             show_matchs=True):
        BaseView.base_view()

        print("-- Tournament detail :")
        print(f"Name : {tournament.name} - Location : {tournament.location} - Date : {tournament.date}")
        print(f"State : {tournament.state()}")
        print(f"Description : {tournament.description}")
        if show_players:
            print(f"Players : {len(tournament.players)}/{tournament.number_players}")
            for player_tournament_number in range(tournament.number_players):
                try:
                    current_player = tournament.players[player_tournament_number]
                    print(f"-> {current_player} "
                          f"- Score : {tournament.get_player_score(current_player)}")
                except IndexError:
                    current_player = "Player not assigned"
                    print(f"-> {current_player}")

        if show_turns:
            if tournament.get_turns():
                print("\nRounds :")
                for turn in tournament.get_turns():
                    print(f"{turn.name} -", end=" ")
                    print(f"Start at : {turn.start_date_time} "
                          f"- End at : {turn.end_date_time if turn.end_date_time else 'Turn not ended yet'}")
                    if show_matchs:
                        for match in turn.matchs:
                            print(f"\t{match}")
            else:
                print("\nRounds : No rounds launched")

        print("\n1. List tournaments")
        print("2. View this tournament with players sorted in alphabetical order")
        print("3. View this tournament with players sorted by rank")
        print("4. View this tournament without matchs (only turns)")
        print("5. Manage this tournament")
        return input("Choice : ")

    @classmethod
    def _tournament_display(cls, tournament):
        print(f"Tournament : {tournament.name} - {tournament.location} - {tournament.date}")
        print(f"State : {tournament.state()}")
        print(f"Players : {len(tournament.players)}/{tournament.number_players}")
        for player_tournament_number in range(tournament.number_players):
            try:
                current_player = tournament.players[player_tournament_number]
                print(f"Player {player_tournament_number} : {current_player} "
                      f"- Score : {tournament.get_player_score(current_player)}")
            except IndexError:
                current_player = "Player not assigned"
                print(f"Player {player_tournament_number} : {current_player}")

        if tournament.get_turns():
            print("\nRounds :")
            for turn in tournament.get_turns():
                print(turn)

    @classmethod
    def _tournament_display_short(cls, tournament):
        print(f"Tournament : {tournament.name} - {tournament.location} - {tournament.date}")

    @classmethod
    def tournament_manage_base_view(cls, tournament, message=None):
        BaseView.base_view()
        if message:
            print(message, "\n")

        TournamentView._tournament_display(tournament)

    @classmethod
    def tournament_manage_with_not_all_players_view(cls, tournament):
        print("\nYou must add player to start tournament")
        print("\n")
        print("1. List tournaments")
        print("2. Add player")
        return input("Choice : ")

    @classmethod
    def tournament_manage_not_started_view(cls, tournament):
        print("\nYou can now start tournament")
        print("\n")
        print("1. List tournaments")
        print("2. Start tournament")
        return input("Choice : ")

    @classmethod
    def tournament_manage_started_waiting_next_turn(cls, tournament):
        print("\n")
        print("1. List tournaments")
        print("2. Begin next turn")
        return input("Choice : ")

    @classmethod
    def tournament_manage_started_turn_in_progress_view(cls, tournament):
        print("\n")
        print("1. List tournaments")
        for match_index, match in enumerate(tournament.get_current_turn().matchs):
            if not match.is_finish():
                print(f"{match_index + 2}. Set result for the match {match_index + 1}")
        if tournament.get_current_turn().is_all_matchs_finish():
            print("6. Mark current turn as finish")
        return input("Choice : ")

    @classmethod
    def tournament_manage_finished(cls, tournament):
        print("\n")
        print("1. List tournaments")
        return input("Choice : ")

    @classmethod
    def tournament_assign_player_view(cls, tournament, players):
        BaseView.base_view()
        TournamentView._tournament_display_short(tournament)

        if not players:
            print("No available player in the base.")

        print("Players list :")
        for player in players:
            player_view.PlayerView.player_display(player)

        print("\n")
        return input("Add a player with ID : ")

    @classmethod
    def tournament_valid_match(cls, tournament, match):
        BaseView.base_view()
        TournamentView._tournament_display_short(tournament)

        print(match)

        print(f"1. The winner is : {match.get_first_player()}")
        print(f"2. The winner is : {match.get_second_player()}")
        print("3. The match result is a draw")
        return input("Set match result : ")
