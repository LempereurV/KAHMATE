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
            state[rugbyman.get_pos_x(), rugbyman.get_pos_y()] = color * type
        ball = game.get_ball()
        state[ball.get_pos_x(), ball.get_pos_y()] += 0.5
        self.state = state

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


def RL_action_from_game(action):
    "Converts a game action into an action that can be used by the RL algorithm"
    # Only works for rugbyman moves, not ball moves yet
    RL_action = np.zeros((len(action), len(action[0])))
    rugbyman = action[0]
    RL_action[rugbyman.get_pos_x(), rugbyman.get_pos_y()] = -1
    RL_action[action[1], action[2]] = 1
    return RL_action


def RL_available_actions(actions):
    "Converts the available actions into a set of actions that can be used by the RL algorithm"
    RL_actions = np.array([])
    for action in actions:
        RL_actions.append(actions, RL_action_from_game(action))
    return RL_actions


