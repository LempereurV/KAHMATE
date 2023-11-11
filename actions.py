from rugbymen import *

def available_positions(current_x,current_y, max_x, max_y, scope, rugbymen_positions_list):
    """ 
    Returns the list of admissible new positions for a rugbyman in position (current_x, current_y).
    Used in move_rugbyman(rugbyman, game).
    """
    available = []
    for x in range(max(current_x - scope, 0), min(current_x + scope, max_x) + 1):
        for y in range(max(current_y - scope, 0), min(current_y + scope, max_y) + 1):
            if abs(x - current_x) + abs(y - current_y) <=scope:
                if not [x, y] in rugbymen_positions_list:
                    available.append([x, y])
    return available
    

def move_rugbyman(rugbyman, game, moves_executed):
    "Moves rugbyman to an available position chosen by player"
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    max_x = game.x_limit()
    max_y = game.y_limit()
    scope = rugbyman.moove_points() - moves_executed
    rugbymen_positions_list = game.positions()
    available_positions = available_positions(current_x, current_y, max_x, max_y, scope - moves_executed, rugbymen_positions_list) + [current_x, current_y] #Current position should be available
    while True:
        print(available_positions)
        cancel = input("If you don't want to move, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = ("Choisis la nouvelle abcisse de ton joueur parmi celles proposées: par exemple tape 3")
        input_y = ("Choisis la nouvelle ordonnée de ton joueur parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_positions:
            moves_executed += abs(current_x - input_x) + abs(current_y - input_y)
            rugbyman.new_posx(input_x)
            rugbyman.new_posy(input_y)
            if game.ball.is_carried_by_rugbyman(rugbyman):
                game.ball.moves([input_x, input_y])
            break
    if moves_executed < rugbyman.moove_points:
        while True:
            finished_move = input("Type 'no' if you haven't finished moving this rugbyman, type 'yes' if you have finished")
            if finished_move is "yes":
                return True
            if finished_move is "no":
                return False 
    else: 
        return True

def available_pass_positions(color, current_x, current_y, max_x, max_y, pass_scope):
    available = []
    if color is "red":
        for x in range(max(current_x - pass_scope, 0), current_x):
            for y in range(max(current_y - pass_scope, 0), min(current_y + pass_scope, max_y)):
                available.append([x, y])
    if color is "blue":
        for x in range(current_x + 1, min(current_x + pass_scope, max_x) + 1):
            for y in range(max(current_y - pass_scope, 0), min(current_y + pass_scope, max_y)):
                available.append([x, y])
    return available

def pass_ball(rugbyman, game, pass_scope):
    """
    Ball possessor passes the ball to another position
    """
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    max_x = game.x_limit()
    max_y = game.y_limit()
    available_pass_positions = available_pass_positions(rugbyman.color, current_x, current_y, max_x, max_y)
    print(available_pass_positions)
    while True:
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is 'cancel':
            return
        input_x = ("Choisis la nouvelle abcisse de la balle parmi celles proposées: par exemple tape 3")
        input_y = ("Choisis la nouvelle ordonnée de la balle parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_pass_positions:
            game.ball.new_carrier(None)
            game.ball.moved([input_x, input_y])
            for rugbyman_ball_potential_owner in game.players():
                if rugbyman_ball_potential_owner.posx() == input_x and rugbyman_ball_potential_owner.posy() == input_y:
                    game.ball.new_carrier(rugbyman_ball_potential_owner)
    
def tackle(attacker, defender, game):
    pass

def forward_pass(rugbyman, game):
    pass

def score(rugbyman, game):
    pass
class Actions: 

    def moove_up(self):
            self.posy += 1

        def moove_down(self):
            self.posy -= 1

        def moove_left(self):
            self.posx -= 1

        def moove_right(self):
            self.posx += 1

        def tackle(self, card_self, other, card_other):
            if (
                self.active == True
                and self.possesion == False
                and self.posx == other.posx
                and self.posy == other.posy
            ):
                if (self.attack_bonus + card_self.point) > (
                    other.defense_bonus + card_other.point
                ):
                    other.active = False
                    return True
            return False

        def push_through(self, card_self, other, card_other):
            if (
                self.active == True
                and self.possesion == True
                and self.posx == other.posx
                and self.posy == other.posy
            ):
                if (self.attack_bonus + card_self.point) > (
                    other.defense_bonus + card_other.point
                ):
                    other.active = False
                    return True
            return False

        def grubber_kick(self, throw):
            if self.possesion == True:
                return True
            else:
                return False

        def place_rugbyman(self, x, y):
            self.posx = x
            sel#Fonction qui traduit coordonnées en numéro de hitbox
def coord_to_hitbox(coord):
    return coord[0]+11*coord[1]

def hitbox_to_coord(n_hit):
    return (n_hit%11, n_hit//11)
