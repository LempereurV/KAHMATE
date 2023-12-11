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
<<<<<<< HEAD
        self.moves = 3 # Nombre de cases que le rugbyman peut parcourir à chaque tour
        self.moves_left = self.moves # Nombre de cases que le rugbyman peut encore parcourir pendant le tour
        self.posx = 0
=======
        self.move_points = 3
        self.moves_left = self.move_points
        self.pos_x = 0
>>>>>>> branche_de_felix2
        self.posy = 0
        self.spec = Spec.NORMAL
        self.possesion = False  # True if the player has the ball
        self.KO = 0  # 0 if the player is active

    def __str__(self):  # Possibilité de la changer
        return f"{self.color} Rugbyman ({self.spec})"

    def spec(self):
        return self.spec

    def get_move_points(self):
        return self.moves_left

    def get_color(self):
        return self.color
<<<<<<< HEAD

    def has_partners_in_front(self, game):
        """
        Renvoie la présence ou non de joueurs alliés devant le joueur.
        Utilisé pour la passe en-avant
        """
        if self.color == board.Color.BLUE:
            for rugbyman in game.blue_player():
                if rugbyman.posx() < self.posx():
                    return True
        if self.color is board.Color.RED:
            for rugbyman in game.red_player():
                if rugbyman.posx() > self.posx():
                    return True
        return False

    def moves(self):
        return self.moves

    def moves_left(self):
=======
    
    def set_KO(self):
        self.KO = 2
    
    def get_KO(self):
        return self.KO
    
    def move_points(self):
        return self.move_points

    def get_attack_bonus(self):
        return self.attack_bonus
    
    def get_defense_bonus(self):
        return self.defense_bonus
    
    def move_left(self):
>>>>>>> branche_de_felix2
        return self.moves_left

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.posy

    def get_pos(self):
        return [self.pos_x, self.posy]

    def set_pos_x(self, new_pos_x):  # utiliser une propriété
        self.pos_x = new_pos_x

    def set_pos_y(self, new_posy):  # utiliser une propriété
        self.posy = new_posy
    def set_pos(self, pos):
        self.pos_x = pos[0]
        self.posy = pos[1]

    def set_possesion(self, boolean):
        self.possesion = boolean
    
    def get_possesion(self):
        return self.possesion


    def refresh_stats(self):
        self.moves_left = self.move_points
        if self.get_KO() > 0:
            self.KO -= 1

    def get_moves_left(self):
        return self.moves_left
    
    def actualize_move_left(self, move_points):
        self.moves_left -= move_points
    def set_move_left(self, move_points):
        self.moves_left = move_points
    def has_ball(self):
        return self.possesion


class StrongRugbyman(Rugbyman):
    def __init__(self, color):
        Rugbyman.__init__(self, color)
        self.attack_bonus = 2
        self.defense_bonus = 1
<<<<<<< HEAD
        self.moves = 2
=======
        self.move_points = 2
        self.moves_left = self.move_points
>>>>>>> branche_de_felix2
        self.spec = Spec.STRONG


class HardRugbyman(Rugbyman):
    def __init__(self, color):
        Rugbyman.__init__(self, color)
        self.attack_bonus = 1
        self.spec = Spec.HARD


class SmartRugbyman(Rugbyman):
    def __init__(self, color):
        Rugbyman.__init__(self, color)
        self.defense_bonus = 1
        self.spec = Spec.SMART


class FastRugbyman(Rugbyman):
    def __init__(self, color):
        Rugbyman.__init__(self, color)
        # Achanger
        self.attack_bonus = -1
        #
        self.defense_bonus = -1
<<<<<<< HEAD
        self.moves = 4
=======
        self.move_points = 4
        self.moves_left = self.move_points
>>>>>>> branche_de_felix2
        self.spec = Spec.FAST
