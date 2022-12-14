from mvc_chess.views.base_view import BaseView


class PlayerView:
    @classmethod
    def player_list_view(cls, players, message=None):
        BaseView.base_view()
        if message:
            print(message)

        print("-- Players list :")
        if not players:
            print("No player in the base")
        else:
            print("ID\tLastname\t\t\tFirstname\t\t\tBirthdate\t\t\tRank")
            for player in players:
                print(f"{player.id}\t{player.lastname}\t\t\t{player.firstname}\t\t\t"
                      f"{player.birthdate}\t\t\t{player.rank}")

        print("\n")
        print("1. Create a new player")
        print("2. Update a player")
        print("3. List player in alphabetical order")
        print("4. List player in rank order")
        print("M. Main menu")
        print("Q. Quit")
        return input("Choice : ")

    @classmethod
    def player_display(cls, player):
        print(f"{player.id}\t{player.lastname}\t\t\t{player.firstname}\t\t\t"
              f"{player.birthdate}\t\t\t{player.rank}")

    @classmethod
    def player_create_view(cls):
        BaseView.base_view()
        print("-- Create a new player :")
        return {
            "lastname": input("Lastname : "),
            "firstname": input("Firstname : "),
            "birthdate": input("Birthdate : "),
            "gender": input("Gender [Autre | Femme | Homme]: "),
            "rank": input("Rank [must be an integer]: "),
        }

    @classmethod
    def player_update_view(cls, player):
        BaseView.base_view()
        print("-- Update a player :")
        print(f"Player ID is : {player.id}")
        return {
            "lastname": input(f"Lastname is {player.lastname} left blank to keep or update for : "),
            "firstname": input(f"Firstname is {player.firstname} left blank to keep or update for : "),
            "birthdate": input(f"Birthdate is {player.birthdate} left blank to keep or update for : "),
            "gender": input(f"Gender is {player.gender} left blank to keep or update for : "),
            "rank": input(f"Rank is {player.rank} left blank to keep or update for : "),
        }
