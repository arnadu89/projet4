from models import player, tournoi


class Application:
    @classmethod
    def demo(cls):
        import random
        # Créer un nouveau tournoi
        tournoi_datas = {
            'nom' : 'Tournoi Régional 1',
            'lieu': 'Paris',
            'date': '24/03/2021',
            'controle_temps': 'Bullet',
            'description': 'Tournoi régional de paris junior',
        }
        tournoi_instance = tournoi.Tournoi(**tournoi_datas)

        # Créer des joueurs
        joueurs = [
            player.Player("echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
        ]
        # [print(p) for p in joueurs]

        # Ajout 8 joueurs au tournoi
        [tournoi_instance.ajouter_joueur(p) for p in joueurs]

        print(tournoi_instance)
        # Jouer les tours
        for i in range(tournoi_instance.nombre_tours):
            tournoi_instance.lancer_tour_suivant()
            # print(tournoi_instance)

            # valider les matchs du tour
            last_turn = tournoi_instance.tournees[-1]
            for match_index in range(4):
                last_turn.set_match_score(match_index, random.randrange(-1, 2))

            tournoi_instance.finir_tour_courant()
            print(tournoi_instance)

    @classmethod
    def run(cls):
        Application.demo()