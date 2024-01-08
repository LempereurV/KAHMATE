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
    A = game.tour_joueurs()
    B = game.tour_balle()
    x,y = np.where(B == 1)
    if len(x) > 0 and len(y) > 0:
        x, y = x[0], y[0]
        S = A[x, y]
    print(S)
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
    nb_joueurs = 0
    if S == 1:
        Poss = game.is_rugbyman_on_ball()
        #we want to go to the highest reward zone possible
        MAP = []
        COORD = []
        for i in range(constants.Constants.number_of_rows):
            for j in range(constants.Constants.number_of_columns):
                MAP.append(R[i][j])
                COORD.append((i,j))
        #sort the rewards in descending order, then the coordinates in the same order
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
                for Rugbyman in game.rugbymen() and rugbymen.get_color() == color.Color.RED:
                    if COORD[i] in game.available_move_position(Rugbyman) and Rugbyman not in Liste_rugbymen:
                        Liste_rugbymen.append(Rugbyman)
                for Rugbyman in Liste_rugbymen:
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
                    MAP.append(R[i][j])
                    COORD.append((i,j))
                for Rugbyman in game.rugbymen() and rugbymen.get_color() == color.Color.RED:
                        if COORD[i] in game.available_move_position(Rugbyman):
                            actions.action_rugbyman_bot(game, Rugbyman, COORD[i], Graph)
                            nb_joueurs += 1
                            break
                        
                        