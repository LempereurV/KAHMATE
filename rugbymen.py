# Classe de base Player
class Rugbyman:
    def __init__(self, color):
        self.color = color
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.moove_points = 3


class Strong_rugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 2
        self.defense_bonus = 1
        self.moove_points = 2


class Hard_rugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 1


class Smart_rugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.defense_bonus = 1


class Fast_rugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = -1
        self.defense_bonus = -1
        self.moove_points = 4
