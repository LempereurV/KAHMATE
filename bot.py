import pygame
import color
import rugbymen
import random
import game
import numpy as np
import constants
import color
import actions

#Pour l'instant, les ordis ne peuvent être que rouges

class Bot:
    def __init__(self):
        self.Rugbyman_1 = rugbymen.Rugbyman(color.Color.RED)
        self.Rugbyman_2 = rugbymen.Rugbyman(color.Color.RED)
        self.StrongRugbyman = rugbymen.StrongRugbyman(color.Color.RED)
        self.HardRugbyman = rugbymen.HardRugbyman(color.Color.RED)
        self.SmartRugbyman = rugbymen.SmartRugbyman(color.Color.RED)
        self.FastRugbyman = rugbymen.FastRugbyman(color.Color.RED)
        A = [i for i in range(8)]
        self.Rugbyman_1.set_pos_x(5)
        self.Rugbyman_1.set_pos_y(A.pop(random.randint(0,7)))
        self.Rugbyman_2.set_pos_x(5)
        self.Rugbyman_2.set_pos_y(A.pop(random.randint(0,6)))
        self.StrongRugbyman.set_pos_x(5)
        self.StrongRugbyman.set_pos_y(A.pop(random.randint(0,5)))
        self.HardRugbyman.set_pos_x(5)
        self.HardRugbyman.set_pos_y(A.pop(random.randint(0,4)))
        self.SmartRugbyman.set_pos_x(5)
        self.SmartRugbyman.set_pos_y(A.pop(random.randint(0,3)))
        self.FastRugbyman.set_pos_x(5)
        self.FastRugbyman.set_pos_y(A.pop(random.randint(0,2)))


def compute_reward(game):
    R = np.zeros((constants.Constants.number_of_rows, constants.Constants.number_of_columns))
    A = game.tour_joueurs() #une matrice qui indique en +1 les joueurs amis(rouges) et -1 les ennemis
    B = game.tour_balle() #Une matrice qui indique en +1 la balle
    x,y = np.where(B == 1)
    if len(x) > 0 and len(y) > 0:
        x, y = x[0], y[0]
        S = A[x, y]
    #S=1 if the bot has the ball, -1 if the player has it and 0 if nobody have it
    if S == 1:
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                if j>=y:
                    #R croît vers la ligne d'essai
                    R[i][j] = 3*np.exp(2*(j-y)/constants.Constants.number_of_columns)
                    #R privilégie la ligne droite
                    R[i][j] += np.exp(-(i-x)**2/constants.Constants.number_of_rows)
                for Rugbymen in game.rugbymen():
                    if Rugbymen.get_pos_x() == i+1 and Rugbymen.get_pos_y() == j+1:
                        if Rugbymen.color == color.Color.RED:
                            R[i][j] = 0
                            #Impossible de passer sur un joueur allié
                        else:
                            for k in range(Rugbymen.move_points):
                                for l in range(Rugbymen.move_points):
                                    if i+k < constants.Constants.number_of_rows and j+l < constants.Constants.number_of_columns:
                                        R[i+k][j+l] -= 0.5*np.exp(((k)**2)/constants.Constants.number_of_rows) + 0.5*np.exp(((l)**2)/constants.Constants.number_of_columns)
                                        #Les zones autour des joueurs adverses sont à éviter
                
    if S == -1:
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                #R croit vers le joueur adverse possédant la balle
                R[i][j] = np.exp(-(j-y)**2/constants.Constants.number_of_columns)
                R[i][j] += np.exp(-(i-x)**2/constants.Constants.number_of_rows)
    if S == 0:
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                #R croit vers la balle
                R[i][j] = np.exp(-(j-y)**2/constants.Constants.number_of_columns)
                R[i][j] += np.exp(-(i-x)**2/constants.Constants.number_of_rows)
    return R
   
def compute_action(game, Graph):
    R = compute_reward(game)
    A = game.tour_joueurs()
    B = game.tour_balle()
    #if red has the ball, we want to know if we can advance with it or if we have to pass it
    x,y = np.where(B == 1)
    if len(x) > 0 and len(y) > 0:
        x, y = x[0], y[0]
        S = A[x, y]
    nb_joueurs = 0 #can't be over 2
    if S == 1:
        Poss = game.is_rugbyman_on_ball()
        #we want to go to the highest reward zone possible
        MAP = []
        COORD = []
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                for Rugbyman in game.rugbymen():
                    if [i,j] in game.available_move_position(Rugbyman) and Rugbyman.get_color == color.Color.RED:
                        MAP.append(R[i][j])
                        COORD.append((i,j))
        #sort the accessible rewards zones in descending order, then the coordinates in the same order
        MAP, COORD = zip(*sorted(zip(MAP, COORD), reverse=True))
        for i in range(len(MAP)):
            #if we can move to the zone, we do it
            if COORD[i] in game.available_move_position(Poss):
                actions.action_rugbyman_bot(game, Poss, COORD[i], Graph)
                nb_joueurs += 1
                break
            else:
                Liste_rugbymen = []
                #compute the list of rugbymen who can go to the best reward
                for Rugbyman in game.rugbymen():
                    if COORD[i] in game.available_move_position(Rugbyman) and Rugbyman not in Liste_rugbymen  and rugbymen.get_color() == color.Color.RED:
                        Liste_rugbymen.append(Rugbyman)
                for Rugbyman in Liste_rugbymen: #we look if we can pass the ball to someone that can go to the highest reward zone
                    if Rugbyman.get_pos() in actions.available_pass(game):
                        game.get_ball().set_carrier(Rugbyman)
                        game.get_ball().set_pos(Rugbyman.get_pos())
                        Poss = Rugbyman
                        break
        #at most, only one rugbyman did move, so we repeat the process
        R = compute_reward(game)
        A = game.tour_joueurs()
        B = game.tour_balle()
        MAP = []
        COORD = []
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                for Rugbyman in game.rugbymen():
                    if [i,j] in game.available_move_position(Rugbyman) and Rugbyman.get_color == color.Color.RED:
                        MAP.append(R[i][j])
                        COORD.append((i,j))
        #sort the rewards in descending order, then the coordinates in the same order
        MAP, COORD = zip(*sorted(zip(MAP, COORD), reverse=True))
        for i in range(len(MAP)):
            #if we can move to the zone, we do it
            #we don't make a pass because we already did
            if COORD[i] in game.available_move_position(Poss):
                actions.action_rugbyman_bot(game, Poss, COORD[i], Graph)
                nb_joueurs += 1
                break
        if nb_joueurs <= 2:
            R = compute_reward(game)
            MAP = []
            COORD = []
            for i in range(constants.Constants.number_of_rows):
                for j in range(constants.Constants.number_of_columns):
                    for Rugbyman in game.rugbymen():
                        if [i,j] in game.available_move_position(Rugbyman) and Rugbyman.get_color == color.Color.RED:
                            MAP.append(R[i][j])
                            COORD.append((i,j))
            MAP, COORD = zip(*sorted(zip(MAP, COORD), reverse=True))
            k = 0
            for Rugbyman in game.rugbymen():
                    if COORD[k] in game.available_move_position(Rugbyman) and rugbymen.get_color() == color.Color.RED:
                        actions.action_rugbyman_bot(game, Rugbyman, COORD[k], Graph)
                        nb_joueurs += 1
                        break
                    else: k += 1
    if S == 0:#no one has the ball
        for Rugbyman in game.rugbymen():
            if [x, y] in game.available_move_position(Rugbyman) and rugbymen.get_color() == color.Color.RED:
                actions.action_rugbyman_bot([x,y], Rugbyman, game, Graph)
                nb_joueurs += 1
                if Rugbyman.get_moves_left() > 0:
                    R = compute_reward(game)
                    for pos in Rugbyman.available_move_position():
                        if R[pos] > R[Rugbyman.get_pos()]:
                            actions.action_rugbyman_bot(pos, Rugbyman, game, Graph)
                            break
        while nb_joueurs <= 2:
            R = compute_reward(game)
            MAP = []
            COORD = []
            for i in range(constants.Constants.number_of_rows):
                for j in range(constants.Constants.number_of_columns):
                    for Rugbyman in game.rugbymen():
                        if [i,j] in game.available_move_position(Rugbyman) and Rugbyman.get_color == color.Color.RED:
                            MAP.append(R[i][j])
                            COORD.append((i,j))
            A = game.tour_joueurs()
            B = game.tour_balle()
            MAP, COORD = zip(*sorted(zip(MAP, COORD), reverse=True))
            #if red has the ball, we want to know if we can advance with it or if we have to pass it
            x,y = np.where(B == 1)
            if len(x) > 0 and len(y) > 0:
                x, y = x[0], y[0]
                S = A[x, y]
            if S == 0:      #No rugbyman can attain the ball, so we move those who can to the highest reward zone
                k = 0
                for Rugbyman in game.rugbymen():
                    if rugbymen.get_color == color.Color.RED:
                        if COORD[k] in game.available_move_position(Rugbyman):
                            actions.action_rugbyman_bot(COORD[k], Rugbyman, game, Graph) #game, Rugbyman, COORD[k], Graph
                            nb_joueurs += 1
                            break
                        else: k += 1
    if S == -1:#the enemy has the ball
        #if blue has the ball, we first want to know if we can claim it
        #we establish the list of rugbymen that can attain the ball
        Available = []
        for Rugbyman in game.rugbymen() and Rugbyman.get_color == color.Color.RED:
            if game.get_ball().get_pos() in game.available_move_position(Rugbyman):
                Available.append(Rugbyman)
        #we prefer to go with hard or stong because they have an offensive bonus
        if len(Available) > 0: #it means we can go charge an enemy
            a = True
            for Rugbyman in Available:
                if Rugbyman.spec == rugbymen.Spec.HARD or Rugbyman.spec == rugbymen.Spec.STRONG:
                    a = False
                    actions.action_rugbyman_bot([x,y], Rugbyman, game, Graph)
                    nb_joueurs += 1
                    break
            if a:
                r = random.randint(0,len(Available)-1)
                actions.action_rugbyman_bot([x,y], Available[r], game, Graph) #we play a random rugbyman on the list
                nb_joueurs += 1
        B = game.tour_balle()
        A = game.tour_joueurs
        R = compute_reward(game)
        x,y = np.where(B == 1)
        if len(x) > 0 and len(y) > 0:
            x, y = x[0], y[0]
            S = A[x, y]
        #checks if we gained the ball from the previous actions
        if S == 0 or S == -1:#we didn't gain the ball, so we go to the highest reward square
            MAP = []
            COORD = []
            Rugbymen = []
            for i in range(constants.Constants.number_of_rows):
                for j in range(constants.Constants.number_of_columns):
                    for Rugbyman in game.rugbymen():
                        if [i,j] in game.available_move_position(Rugbyman) and Rugbyman.get_color == color.Color.RED:
                            MAP.append(R[i][j])
                            COORD.append((i,j))
                            Rugbymen.append(Rugbyman)
        MAP, COORD, Rugbymen = zip(*sorted(zip(MAP, COORD, Rugbymen), reverse=True))

            

            