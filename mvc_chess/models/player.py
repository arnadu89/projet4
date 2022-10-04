class Player:
    genres = [
        "Autre",
        "Femme",
        "Homme"
    ]

    def __init__(self, nom, prenom, date_naissance, genre, classement):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self._genre = genre
        self._classement = classement

    @property
    def genre(self):
        return self.genre

    @genre.setter
    def genre(self, value):
        if value in Player.genres:
            self.genre = value

    @property
    def classement(self):
        return self._classement

    @classement.setter
    def classement(self, value):
        if value >= 0:
            self._classement = value

    def __repr__(self):
        return f"{self.nom} {self.prenom} {self.date_naissance} {self.classement}"
    