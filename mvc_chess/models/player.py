class Player:
    genders = [
        "Autre",
        "Femme",
        "Homme"
    ]

    def __init__(self, id, lastname, firstname, birthdate, gender, rank):
        self.id = id
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

    @classmethod
    def is_valid(cls, lastname, firstname, birthdate, gender, rank):
        if not lastname or not firstname or not birthdate:
            return False
        try:
            if gender not in Player.genders:
                raise ValueError
        except ValueError:
            return False

        try:
            int(rank)
            if int(rank) < 0:
                raise ValueError
        except ValueError:
            return False

        return True

    def serialize(self):
        serialized_player = {
            "id": self.id,
            "lastname": self.lastname,
            "firstname": self.firstname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "rank": self.rank,
        }

        return serialized_player

    @classmethod
    def deserialize(cls, serialized_player):
        player = Player(**serialized_player)
        return player

    def __repr__(self):
        return f"{self.lastname} {self.firstname} {self.birthdate} {self.rank}"
