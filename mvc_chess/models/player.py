class Player:
    genres = [
        "Autre",
        "Femme",
        "Homme"
    ]

    def __init__(self, nom, prenom, date_naissance, genre, rank):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self._genre = genre
        self._rank = rank

    @property
    def genre(self):
        return self.genre

    @genre.setter
    def genre(self, value):
        if value in Player.genres:
            self.genre = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if value >= 0:
            self._rank = value

    def __repr__(self):
        return f"{self.nom} {self.prenom} {self.date_naissance} {self.rank}"
    