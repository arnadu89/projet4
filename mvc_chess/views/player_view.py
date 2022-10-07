class PlayerView:
    @classmethod
    def player_list_view(cls, players, message=None):
        print(f"-- MVC Chess --\n")
        if message:
            print(message)

        print(f"-- Players list :")
        if not players:
            print(f"Aucun joueur dans la base")
        else:
            print(f"Nom\t\t\tPrénom\t\t\tDate de naissance\t\t\tClassement")
            for player in players:
                print(f"{player.lastname}\t\t\t{player.firstname}\t\t\t{player.birthdate}\t\t\t{player.rank}")

        print(f"\n")
        print(f"1. Create a new player")
        print(f"2. Update a player")
        print(f"3. List player in alphabetical order")
        print(f"4. List player in rank order")
        print(f"M. Main menu")
        print(f"Q. Quit")
        return input("Choice : ")

    @classmethod
    def player_create_view(cls):
        print(f"-- MVC Chess --\n")
        print(f"-- Create à new player :")
        return {
            "lastname": input("Nom : "),
            "firstname": input("Prénom : "),
            "birthdate": input("Date de naissance : "),
            "gender": input("Genre : "),
            "rank": input("Classement : "),
        }

    @classmethod
    def player_update_view(cls):
        pass