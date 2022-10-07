import random
import mvc_chess.models.player as player
import mvc_chess.models.tournoi as tournoi


class ModelsManager:
    players = []
    tournois = []

    @classmethod
    def demo(cls):
        # Players
        players = [
            player.Player("echecs", "joueur 1", "01/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 2", "02/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 3", "03/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 4", "04/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 5", "05/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 6", "06/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 7", "07/02/1999", "Autre", random.randint(10, 80) * 10),
            player.Player("echecs", "joueur 8", "08/02/1999", "Autre", random.randint(10, 80) * 10),
        ]

        ModelsManager.players.extend(players)

        # Tournoi
        tournoi_datas = {
            'nom': 'Tournoi Régional 1',
            'lieu': 'Paris',
            'date': '24/03/2021',
            'controle_temps': 'Bullet',
            'description': 'Tournoi régional de paris junior',
        }
        ModelsManager.tournois.append(tournoi.Tournoi(**tournoi_datas))
