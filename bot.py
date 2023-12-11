import pygame
import front
import rugbymen
import random
import game
import numpy as np
import constants

class Bot:
    def __init__(self):
        self.Rugbyman_1 = rugbymen.Rugbyman(front.Color.RED)
        self.Rugbyman_2 = rugbymen.Rugbyman(front.Color.RED)
        self.StrongRugbyman = rugbymen.StrongRugbyman(front.Color.RED)
        self.HardRugbyman = rugbymen.HardRugbyman(front.Color.RED)
        self.SmartRugbyman = rugbymen.SmartRugbyman(front.Color.RED)
        self.FastRugbyman = rugbymen.FastRugbyman(front.Color.RED)
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
        self.policy = np.zeros((constants.number_of_rows, constants.number_of_columns))


        def tour(self, Game):
            A = np.zeros((constants.number_of_rows, constants.number_of_columns))
            for i in range(constants.number_of_rows):
                for j in range(constants.number_of_columns):
                    for Rugbymen in Game.rugbymen():
                        if Rugbymen.get_pos_x() == i and Rugbymen.get_pos_y() == j:
                            if Rugbymen.color == front.Color.RED:
                                A[i][j] = 1
                            else:
                                A[i][j] = -1


