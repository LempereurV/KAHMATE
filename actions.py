from rugbymen import *
from board import Color


def ask_if_action_finished():
    while True:
        finished_move = input("Type 'no' if you haven't finished the action of this rugbyman, type 'yes' if you have finished")
        if finished_move is "yes":
            return True
        if finished_move is "no":
            return False

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

def input_move_rugbyman(available_positions):
    while True:
        cancel = input("If you don't want to move, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = input("Choisis la nouvelle abcisse de ton joueur parmi celles proposées: par exemple tape 3")
        input_y = input("Choisis la nouvelle ordonnée de ton joueur parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_positions:
            return [input_x, input_y]

def move_rugbyman(rugbyman, game, moves_executed): #prendre en compte le moves_executed choisi (3e coordonnée)
    "Moves rugbyman to an available position chosen by player"
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    scope = rugbyman.move_points() - moves_executed
    rugbymen_positions_list = game.positions()
    #Ne pas oublier de prendre en compte la 3e coordonnée
    available_positions = available_move_positions(current_x, current_y, scope - moves_executed, rugbymen_positions_list) + [current_x, current_y] #Current position should be available
    input_x, input_y = input_move_rugbyman(available_positions)
    moves_executed += abs(current_x - input_x) + abs(current_y - input_y)
    rugbyman.new_posx(input_x)
    rugbyman.new_posy(input_y)
    if game.ball.is_carried_by_rugbyman(rugbyman):
        game.ball.moves([input_x, input_y])
    if moves_executed < rugbyman.moove_points:
        return ask_if_action_finished()
    else:
        return True

def available_pass_positions(color, current_x, current_y, max_x, max_y, pass_scope, game):
    available = []
    if color is Color.RED:
        for x in range(current_x - pass_scope, current_x):
            for y in range(current_y - pass_scope, current_y + pass_scope + 1):
                if game.is_position_correct([x, y]):
                    available.append([x, y])
    if color is Color.BLUE:
        for x in range(current_x + 1, min(current_x + pass_scope, max_x) + 1):
            for y in range(max(current_y - pass_scope, 0), min(current_y + pass_scope, max_y)):
                available.append([x, y])
    return available

def input_pass_ball(available_positions):
    while True:
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = input("Choisis la nouvelle abcisse de la balle parmi celles proposées: par exemple tape 3")
        input_y = input("Choisis la nouvelle ordonnée de la balle parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_positions:
            return [input_x, input_y]
        
def pass_ball(rugbyman, game, pass_scope):
    """
    Ball possessor passes the ball to another position
    """
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    max_x = game.max_x()
    max_y = game.max_y()
    available_pass_positions = available_pass_positions(rugbyman.color(), current_x, current_y, max_x, max_y, pass_scope, game)
    input_x, input_y = input_pass_ball(available_pass_positions)
    if [input_x, input_y] in available_pass_positions:
        game.ball.new_carrier(None)
        game.ball.moved([input_x, input_y])
        for rugbyman_ball_potential_owner in game.players():
            if rugbyman_ball_potential_owner.posx() == input_x and rugbyman_ball_potential_owner.posy() == input_y:
                game.ball.new_carrier(rugbyman_ball_potential_owner)
    return True
def available_tackle_positions(color, current_x, current_y, scope, game):
    """ 
    Returns the list of admissible new positions for a rugbyman in position (current_x, current_y).
    Used in move_rugbyman(rugbyman, game).
    """    
    available = [current_x, current_y]
    moves_executed = 0
    while moves_executed < scope:
        for intermediate_position in available:
            for delta in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                new_position = [intermediate_position[0] + delta[0], intermediate_position[1] + delta[1], moves_executed]
                if not ((new_position in available) 
                        and game.is_position_correct(new_position)
                        and game.is_position_occupied_by_team(color, new_position, game)):
                     available.append(intermediate_position)
        moves_executed +=1
    return available

def pick_card(player):
    cards = player.pick_card()

def input_tackle(available_move_positions):
    while True:
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = input("Choisis la nouvelle abcisse de la balle parmi celles proposées: par exemple tape 3")
        input_y = input("Choisis la nouvelle ordonnée de la balle parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_move_positions:
            return [input_x, input_y]

def tackle(rugbyman, game):
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    color = rugbyman.color()
    scope = rugbyman.moove_points()
    available_move_positions = available_tackle_positions(color, current_x,current_y, scope, game)
    input_x, input_y = input_tackle(available_move_positions)
    if [input_x, input_y] in available_tackle_positions:
        game.ball.new_carrier(None)
        game.ball.moved([input_x, input_y])
        for rugbyman_ball_potential_owner in game.players():
            if rugbyman_ball_potential_owner.posx() == input_x and rugbyman_ball_potential_owner.posy() == input_y:
                game.ball.new_carrier(rugbyman_ball_potential_owner)

def available_forward_pass(color, current_x, current_y, forward_pass_scope, game):
    available = []
    if color is Color.RED:
        for x in range(current_x + 1, current_x + forward_pass_scope + 1):
            for y in range(current_y - forward_pass_scope, current_y + forward_pass_scope + 1):
                intermediate_position = [x, y]
                if game.is_position_valid(intermediate_position) and game.is_position_unoccupied(intermediate_position):
                    available.append(intermediate_position)
        return available
    if color is Color.BLUE:
        for x in range(current_x - forward_pass_scope, current_x):
            for y in range(current_y - forward_pass_scope, current_y + forward_pass_scope + 1):
                intermediate_position = [x, y]
                if game.is_position_valid(intermediate_position) and game.is_position_unoccupied(intermediate_position):
                    available.append(intermediate_position)
        return available

def input_forward_pass(available_forward_pass):
    while True:
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is 'cancel':
            return False
        input_x = input("Choisis la nouvelle abcisse de la balle parmi celles proposées: par exemple tape 3")
        input_y = input("Choisis la nouvelle ordonnée de la balle parmi celles proposées: par exemple tape 5")
        if [input_x, input_y] in available_forward_pass:
            return [input_x, input_y]

def forward_pass(rugbyman, game):
    color = rugbyman.color()
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    forward_pass_scope = game.forward_pass_scope()
    available_forward_pass = available_forward_pass(color, current_x, current_y, forward_pass_scope, game)
    input_x, input_y = input_forward_pass(available_forward_pass) 
    if [input_x, input_y] in available_forward_pass:
        game.ball.moved([input_x, input_y])
        game.ball.left()

def available_score(color, current_x, game):
    available = []
    if color is Color.RED:
        if current_x == game.max_x():
            available.append([89, 89])
    if color is Color.BLUE:
        if current_x == 0:
            available.append([88, 88])
    return available

def score(rugbyman, game):
    color = rugbyman.color()
    current_x = rugbyman.posx()
    if available_score(color, current_x, game) != []:
        return True

class Actions: 

    def moove_up(self):
            print("")
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
