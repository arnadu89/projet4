class TournamentView:
    @classmethod
    def tournament_list_view(cls, tournaments):
        print("-- MVC Chess --\n")

        print("-- Tournaments list :")
        if not tournaments:
            print("Aucun tournoi dans la base")
        else:
            print("ID\tName\t\t\tLocation\t\t\tDate\t\t\tPlayers\t\t\tState")
            for tournament in tournaments:
                print(
                    f"{tournament.id}\t{tournament.name}"
                    f"\t\t{tournament.location}\t\t\t{tournament.date}"
                    f"\t\t{len(tournament.players)}/{tournament.number_players}"
                    f"\t\t\t{tournament.state()}")

        print("\n")
        print("1. Create a new tournament")
        print("2. Manage a tournament")
        print("M. Main menu")
        print("Q. Quit")
        return input("Choice : ")

    @classmethod
    def _tournament_display(cls, tournament):
        print(f"Tournament : {tournament.name} - {tournament.location} - {tournament.date}")
        print(f"State : {tournament.state()}")
        print(f"Players : {len(tournament.players)}/{tournament.number_players}")
        for player_tournament_number in range(tournament.number_players):
            try:
                current_player = tournament.players[player_tournament_number]
            except IndexError:
                current_player = "Player not assigned"
            print(f"Player {player_tournament_number} : {current_player}")

    @classmethod
    def tournament_manage_view(cls, tournament):
        print("-- MVC Chess --\n")
        TournamentView._tournament_display(tournament)

        print("\n")
        print("1. List tournaments")
        print("M. Main menu")
        print("Q. Quit")
        return input("Choice : ")