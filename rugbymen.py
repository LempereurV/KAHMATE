# Classe de base Player
class Rugbyman:
    def __init__(self, color):
        self.color = color
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.moove_points = 3
        self.posx = 0
        self.posy = 0
        self.possesion = False  # True if the player has the ball
        self.active = True  # False if the player is KO


class StrongRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 2
        self.defense_bonus = 1
        self.moove_points = 2


class HardRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 1


class SmartRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.defense_bonus = 1


class FastRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = -1
        self.defense_bonus = -1
        self.moove_points = 4
