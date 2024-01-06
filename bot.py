import pygame
import color
import rugbymen
import random
import game
import numpy as np
import constants
import color

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
                #R croit vers le joueur adverse possédant la balle
                R[i][j] = np.exp(-(j-y)**2/constants.Constants.number_of_columns)
                R[i][j] += np.exp(-(i-x)**2/constants.Constants.number_of_rows)
    return R
   

