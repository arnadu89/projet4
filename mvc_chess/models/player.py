class Player:
    genders = [
        "Autre",
        "Femme",
        "Homme"
    ]

    def __init__(self, lastname, firstname, birthdate, gender, rank):
        self.id = None
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self._gender = gender
        self._rank = None
        self.rank = rank

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value in Player.genders:
            self._gender = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if value >= 0:
            self._rank = value

    def set_id(self, new_id):
        try:
            self.id = int(new_id)
        except ValueError as error:
            raise ValueError(error)

    def is_valid(self,):
        pass

    def __repr__(self):
        return f"{self.lastname} {self.firstname} {self.birthdate} {self.rank}"
