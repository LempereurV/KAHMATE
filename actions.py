import rugbymen
import front
import random
from color import Color
import players
import game
import ball

def placement_orders(color):
    R = {
        "First Normal Rugbyman": rugbymen.Rugbyman(color),
        "Second Normal Rugbyman": rugbymen.Rugbyman(color),
        "Strong Rugbyman": rugbymen.StrongRugbyman(color),
        "Hard Rugbyman": rugbymen.HardRugbyman(color),
        "Smart Rugbyman": rugbymen.SmartRugbyman(color),
        "Fast Rugbyman": rugbymen.FastRugbyman(color),
    }
    return R


def positions_rugbymen_player(color, n_column, placement_order, Graphique):

    i = 0
    n_rugbymen = len(placement_order)
    R = [None] * n_rugbymen 
    Noms = list(placement_order.keys())  

    
    ### A enlever ####
    for i in range(n_rugbymen):
        placement_order[Noms[i]].set_posx(i+2)
        if color == Color.RED:
            placement_order[Noms[i]].set_posy(4)
        else:
            placement_order[Noms[i]].set_posy(random.randint(6, 10))

        R[i]=placement_order[Noms[i]]
        front.Graphique.affiche_joueur(Graphique,11 * rugbymen.Rugbyman.get_posx(R[i]) + rugbymen.Rugbyman.get_posy(R[i]),front.path_convertor(placement_order[Noms[i]]))
    #print(R)
    return R
    ####    FIn a enlever
    

    while i < n_rugbymen:
        print(
            str(color).split(".")[-1] + " Player, Choose the position of the " + Noms[i]
        )  # Changer Color.split(".")[-1] for the color to display as intended
        pos = front.Graphique.get_hitbox_for_back(
            Graphique
        )  # Fonction de la classe graphique qui renvoie une liste de la forme [i,j] avec i et j les colonnes et lignes de la case cliquée
        if pos in R:
            cond_pos_already_taken = True
            while cond_pos_already_taken:
                print("The position chosen is already taken, re choose the position")
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if not pos in R:
                    cond_pos_already_taken = False
        if (
            color == Color.RED and pos[1] >= n_column // 2
        ):  # Red characters should be placed on the left
            cond_RED = True
            while cond_RED:
                print(
                    "The position isn't correct, the red team is suppose to be on the left, re choose the position"
                )
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if pos[1] < n_column // 2:
                    cond_RED = False

        if color == Color.BLUE and pos[1] <= n_column // 2:
            cond_Blue = True
            while cond_Blue:
                print(
                    "The position isn't correct, the blue team is suppose to be on the right, re choose the position"
                )
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if pos[1] > n_column // 2:
                    cond_Blue = False
        front.Graphique.affiche_joueur(
            Graphique,
            pos[0] * n_column + pos[1],
            front.path_convertor(placement_order[Noms[i]]),
        )  # Display the newly placed rugbymen on the board
        R[i] = [pos[0], pos[1]]
        i += 1
    R_with_rugbymen = []
    # R_with_rugbymen is the list of the positions of the rugbymen with the type of the rugbymen
    for i in range(n_rugbymen):
        R_with_rugbymen.append(R[i] + [placement_order[Noms[i]]])

    return R_with_rugbymen


def move_rugbyman( ball,rugbyman,Possible_moves,Graphisme):
        """
        Move the rugbyman
        
        """
        pos2 = front.Graphique.get_hitbox_for_back(Graphisme)

        new_posx=pos2[0]
        new_posy=pos2[1]  
        posx=rugbyman.get_posx()
        posy=rugbyman.get_posy()
        
        if pos2 in Possible_moves:
            if rugbyman.get_possesion():
                ball.set_position(pos2)
            rugbymen.Rugbyman.set_posx(rugbyman,new_posx)
            rugbymen.Rugbyman.set_posy(rugbyman,new_posy)
            #The following line isnt correct it doesnt take into account the obstacles
            rugbymen.Rugbyman.actualize_move_left(rugbyman,abs(new_posx - posx) + abs(new_posy - posy))
            return rugbyman
        else:
            print("You can't move to this position")
        return False




### Fonctions de Francois ###
def ask_if_action_finished():
    while True:
        finished_move = input(
            "Type 'no' if you haven't finished the action of this rugbyman, type 'yes' if you have finished"
        )
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
    for x in range(current_x - scope, current_x + scope + 1):
        for y in range(current_y - scope, current_y + scope + 1):
            if (
                game.is_position_valid([x, y])
                and (abs(current_x - x) + abs(current_y - y)) <= scope
            ):  # and game.is_position_unoccupied([x, y])
                available.append([x, y])
    return available



def available_backward_pass( rugbyman ,Game):
    available = []

    current_x = rugbyman.get_posx()
    current_y = rugbyman.get_posy()

    pass_scope = Game.get_back_pass_scope()

    if rugbyman.get_color() is Color.RED:
        for x in range(current_x - pass_scope, current_x + pass_scope+1):
            for y in range( current_y - pass_scope, current_y):
                if Game.is_position_correct(x, y):
                    available.append([x, y])

    if rugbyman.get_color() is Color.BLUE:
        for x in range(current_x - pass_scope, current_x + pass_scope+1):
            for y in range( current_y +1, current_y+pass_scope+1):
                if Game.is_position_correct(x, y):
                    available.append([x, y])

    return available

def available_forward_pass( rugbyman ,Game):
    available = []

    current_x = rugbyman.get_posx()
    current_y = rugbyman.get_posy()

    pass_scope = Game.get_forward_pass_scope()

    cond = True
    
    if rugbyman.get_color() is Color.BLUE:
        for rugbyman in Game.rugbymen():
            if rugbyman.get_posy()<current_y:
                print("caca")
                cond = False

        if cond :
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y - pass_scope, current_y):
                    if Game.is_position_correct(x, y):
                        available.append([x, y])

    if rugbyman.get_color() is Color.RED:
        for rugbyman in Game.get_player_turn().get_rugbymen():
            if rugbyman.get_posy()>current_y:
                cond = False
        if cond :
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y +1, current_y+pass_scope+1):
                    if Game.is_position_correct(x, y):
                        available.append([x, y])

    return available

def available_pass( Game):
    rugbyman=Game.is_rugbyman_on_ball()

    return available_forward_pass(rugbyman ,Game)+available_backward_pass(rugbyman ,Game)


def make_pass(Game,Graph,Possible_passes):
    pos=front.Graphique.get_hitbox_for_back(Graph)
    if pos in Possible_passes:
        Game.is_rugbyman_on_ball().set_possesion(False)
        Game.get_ball().set_position(pos)
        if Game.is_rugbyman_on_ball()!=False:
            Game.is_rugbyman_on_ball().set_possesion(True)



    



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
                new_position = [
                    intermediate_position[0] + delta[0],
                    intermediate_position[1] + delta[1],
                    moves_executed,
                ]
                if not (
                    (new_position in available)
                    and game.is_position_correct(new_position)
                    and game.is_position_occupied_by_team(color, new_position, game)
                ):
                    available.append(intermediate_position)
        moves_executed += 1
    return available


def pick_card(player):
    cards = player.pick_card()


def input_tackle(available_move_positions):
    while True:
        cancel = input("If you don't want to move the ball anymore, type 'cancel'")
        if cancel is "cancel":
            return False
        input_x = input(
            "Choisis la nouvelle abcisse de la balle parmi celles proposées: par exemple tape 3"
        )
        input_y = input(
            "Choisis la nouvelle ordonnée de la balle parmi celles proposées: par exemple tape 5"
        )
        if [input_x, input_y] in available_move_positions:
            return [input_x, input_y]


def tackle(rugbyman, game):
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    color = rugbyman.color()
    scope = rugbyman.move_points()
    available_move_positions = available_tackle_positions(
        color, current_x, current_y, scope, game
    )
    input_x, input_y = input_tackle(available_move_positions)
    if [input_x, input_y] in available_tackle_positions:
        game.ball.new_carrier(None)
        game.ball.moved([input_x, input_y])
        for rugbyman_ball_potential_owner in game.players():
            if (
                rugbyman_ball_potential_owner.posx() == input_x
                and rugbyman_ball_potential_owner.posy() == input_y
            ):
                game.ball.new_carrier(rugbyman_ball_potential_owner)



def forward_pass(rugbyman, game):
    color = rugbyman.color()
    current_x = rugbyman.posx()
    current_y = rugbyman.posy()
    forward_pass_scope = game.forward_pass_scope()
    available_forward_pass = available_forward_pass(
        color, current_x, current_y, forward_pass_scope, game
    )
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