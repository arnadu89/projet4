class PlayerView:
    @classmethod
    def player_list_view(cls, players):
        print(f"-- MVC Chess --\n")
        print(f"-- Players list :")
        if not players:
            print(f"Aucun joueur dans la base")
        else:
            print(f"Nom\t\tPrénom\t\tDate de naissance\tClassement")
            for player in players:
                print(f"{player.nom}\t\t{player.prenom}\t\t{player.date_naissance}\t{player.rank}")

        print(f"M. Main menu")
        print(f"Q. Quit")
        return input("Choice : ")
