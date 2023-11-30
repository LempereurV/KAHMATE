from rugbymen import *
from game import *

def available_move_positions(current_x, current_y, game, scope):
    """ 
    Returns the list of admissible new positions for a rugbyman in position (current_x, current_y).
    Used in move_rugbyman(rugbyman, game).
    """ 
    current_x = int(current_x)
    current_y = int(current_y)
    scope = int(scope)
    available = []
    for x in range(current_x-scope, current_x+scope+1):
        for y in range(current_y-scope, current_y+scope+1):
            if game.is_position_valid([x, y]) and (abs(current_x-x)+abs(current_y-y))<=scope: # and game.is_position_unoccupied([x, y])
                available.append([x, y])
    return available

def move_rugbyman(rugbyman, game, moves_executed): #prendre en compte le moves_executed choisi (3e coordonnée)
    "Moves rugbyman to an available position chosen by player"
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    scope = rugbyman.move_points() - moves_executed
    rugbymen_positions_list = game.positions()
    available_positions = available_move_positions(current_x, current_y, scope - moves_executed, rugbymen_positions_list) + [current_x, current_y] #Current position should be available
    while True:
        print(available_positions)
        cancel = input("If you don't want to move, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = ("Choisis la nouvelle abscisse de ton joueur parmi celles proposées: par exemple tape 3")
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

def available_pass_positions(color, current_x, current_y, max_x, max_y, pass_scope, game):
    available = []
    if color is "red":
        for x in range(current_x - pass_scope, current_x):
            for y in range(current_y - pass_scope, current_y + pass_scope + 1):
                if game.is_position_correct([x, y]):
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
    max_x = game.max_x()
    max_y = game.max_y()
    available_pass_positions = available_pass_positions(rugbyman.color(), current_x, current_y, max_x, max_y, pass_scope, game)
    while True:
        print(available_pass_positions)
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

def available_forward_pass(color, current_x, current_y, forward_pass_scope, game):
    available = []
    if color is "red":
        for x in range(current_x + 1, current_x + forward_pass_scope + 1):
            for y in range(current_y - forward_pass_scope, current_y + forward_pass_scope + 1):
                intermediate_position = [x, y]
                if game.is_position_valid(intermediate_position) and game.is_position_unoccupied(intermediate_position):
                    available.append(intermediate_position)
        return available
    if color is "blue":
        for x in range(current_x - forward_pass_scope, current_x):
            for y in range(current_y - forward_pass_scope, current_y + forward_pass_scope + 1):
                intermediate_position = [x, y]
                if game.is_position_valid(intermediate_position) and game.is_position_unoccupied(intermediate_position):
                    available.append(intermediate_position)
        return available

def forward_pass(rugbyman, game):
    color = rugbyman.color()
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    forward_pass_scope = game.forward_pass_scope()
    available_forward_pass = available_forward_pass(color, current_x, current_y, forward_pass_scope, game)
    while True:
        print(available_forward_pass)
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is 'cancel':
            return
        input_x = input("Choisis la nouvelle abcisse parmi celles proposées: par exemple tape 3")
        input_y = input("Choisis la nouvelle abcisse parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_forward_pass:
            game.ball.moved([input_x, input_y])
            game.ball.left()

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
        #Fonction qui traduit coordonnées en numéro de hitbox
def coord_to_hitbox(coord):
    return coord[0]+11*coord[1]

def hitbox_to_coord(n_hit):
    return [n_hit%11, n_hit//11]
