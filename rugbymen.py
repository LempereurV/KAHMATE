# Classe de base Player
import enum

class Spec(enum.Enum):
    STRONG = "strong"
    SMART = "smart"
    FAST = "fast"
    HARD = "hard"
    NORMAL = "normal"

class Rugbyman:
    def __init__(self, color):
        self.color = color
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.moove_points = 3
        self.posx = 0
        self.posy = 0
        self.spec = Spec.NORMAL
        self.possesion = False  # True if the player has the ball
        self.active = True  # False if the player is KO

    def color(self):
        return self.color
    
    def moove_points(self):
        return self.moove_points

    def posx(self):
        return self.posx
    
    def posy(self):
        return self.posy

    def new_posx(self, new_posx): #utiliser une propriété
        self.posx = new_posx
        return
    
    def new_posy(self, new_posy): #utiliser une propriété
        self.posy = new_posy
        return
        
class StrongRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 2
        self.defense_bonus = 1
        self.moove_points = 2
        self.spec = Spec.STRONG


class HardRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = 1
        self.spec = Spec.HARD

class SmartRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.defense_bonus = 1
        self.spec = Spec.SMART


class FastRugbyman(Rugbyman):
    def __init__(self, attack_bonus, defense_bonus, moove_points):
        super().__init__(attack_bonus, defense_bonus, moove_points)
        self.attack_bonus = -1
        self.defense_bonus = -1
        self.moove_points = 4
        self.spec = Spec.FAST