import numpy as np
from color import Color
from rugbymen import StrongRugbyman, HardRugbyman, SmartRugbyman, FastRugbyman
from ball import Ball


def rugbyman_type(rugbyman):
    if isinstance(rugbyman, StrongRugbyman):
        return 2
    if isinstance(rugbyman, HardRugbyman):
        return 3
    if isinstance(rugbyman, SmartRugbyman):
        return 4
    if isinstance(rugbyman, FastRugbyman):
        return 5
    else: 
        return 1


def rugbyman_color(rugbyman):
    if rugbyman.color == Color.RED:
        return 1
    else:
        return -1


class State:
    def __init__(self, rows, columns):
        self.state = np.zeros((rows, columns))
    
    def get_RL_state_from_game(self, game): 
        "Converts the current game state into a state that can be used by the RL algorithm"
        state = np.zeros((len(self.state), len(self.state[0])))
        for rugbyman in game.rugbymen():
            color = rugbyman_color(rugbyman)
            type = rugbyman_type(rugbyman)
            state[rugbyman.get_pos_x() - 1, rugbyman.get_pos_y() - 1] = color * type
        ball = game.get_ball()
        state[ball.get_pos_x() - 1, ball.get_pos_y() - 1] += 0.5
        self.state = state
    
    def get_state(self):
        return self.state

    def next_step_from_action(self, action):
        "Converts the state into the next state given an action"
        for x in range(len(action)):
            for y in range(len(action[0])):
                if action[x, y] == -1:  # déplacement du rugbyman de cette case vers une autre
                    rugbyman = self.state[x, y]
                    self.state[x, y] = 0  # la case est maintenant vide
                if action[x, y] == -10:
                    self.state[x, y] -= 0.5  # la balle a quitté cette case
        for x in range(len(action)):
            for y in range(len(action[0])):
                if action[x, y] == 1:  # déplacement du rugbyman depuis une autre case vers celle-ci
                    self.state[x, y] = rugbyman + self.state[x, y] % 1  # le second terme permet de conserver la balle dans la case si elle s'y trouve
                if action[x, y] == 10:
                    self.state[x, y] += 0.5  # la balle a rejoint cette case


def RL_action_from_game(rugbyman, action):
    "Converts a game action into an action that can be used by the RL algorithm"
    # Only works for rugbyman moves, not ball moves yet
    RL_action = np.zeros((8, 11))
    RL_action[rugbyman.get_pos_x() - 1, rugbyman.get_pos_y() - 1] = -1
    RL_action[action[0], action[1]] = 1
    return RL_action


def RL_available_actions(actions):
    "Converts the available actions into a set of actions that can be used by the RL algorithm"
    RL_actions = []
    for rugbyman_actions in actions: # actions contient une liste dont chaque élement est [rugbyman, action1, action2...]
        rugbyman = rugbyman_actions[0]
        for i in range(2, len(rugbyman_actions)): #indice 0: instance du rugbyman, indice 1: rugbyman ne bouge pas
            action = [rugbyman_actions[i][0] - 1, rugbyman_actions[i][1] - 1]
            RL_actions.append(RL_action_from_game(rugbyman, action))
    RL_actions = np.array(RL_actions)
    return RL_actions


