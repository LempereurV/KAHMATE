import constants
import game
import players
import numpy as np

class env:
    def __init__(self,player, Game):
        # tous les états que'il peut y avoir dans la partie
        # toutes les actions possibles
        # tous les états successeurs possibles
        # toutes les récompenses de chaque état

        self.actions=Game.every_possible_move(player)
        self.number_actions=Game.number_actions
        self.actions=Game.actions
        self.player=Game.player
        self.goal=Game.goal
        self.ball_pos=Game.ball_pos
        self.states = np.zeros(constants.number_of_rows, constants.number_of_columns)



class QLearningAgent:
    def __init__(self, learning_rate = 0.1, discount_factor = 0.9, exploration_rate = 0.1):
        self.q_values = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
    
    def get_action(self, state):
        # Retourne l'action choisie par l'agent en fonction de l'état actuel
        pass  # À implémenter

    def update_q_values(self, state, action, reward, next_state):
        # Met à jour les valeurs Q en fonction de la récompense obtenue
        pass  # À implémenter

def get_reward(board):
    # Retourne la récompense pour l'agent dans l'état actuel
    pass  # À implémenter

def train_q_learning_agent(agent, episodes):
    for episode in range(episodes):
        board = chess.Board()
        state = get_board_state(board)

        while not board.is_game_over():
            action = agent.get_action(state)
            next_board = execute_action(board, action)
            next_state = get_board_state(next_board)
            reward = get_reward(next_board)

            agent.update_q_values(state, action, reward, next_state)

            state = next_state

        print(f"Épisode {episode + 1} terminé.")
