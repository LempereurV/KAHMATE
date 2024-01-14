import tensorflow as tf
import numpy as np
import states
from states import *
from constants import Constants
import game
import front


class DQNAgent:
    def __init__(self, input_shape, color):
        self.player = color
        self.input_size = input_shape
        self.memory = []  # Utilisez une structure de mémoire pour stocker les expériences passées
        self.gamma = 0.95  # Facteur de remise pour les récompenses futures
        self.epsilon = 1.0  # Taux d'exploration initial
        self.epsilon_decay = 0.995  # Taux de décroissance de l'exploration
        self.epsilon_min = 0.01  # Taux d'exploration minimum
        self.learning_rate = 0.001
        self.model = self.build_model() # Modèle du réseau neuronal

    def build_model(self):
        """
        Creation of the neural network model: 2 hidden layers of 24 neurons with relu activation function and a linear output layer.
        The input is a grid of the game state and a possible action in that state.
        The output is the estimated Q-value of choosing this action in that state.
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(2, 8, 11)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def remember(self, state, action, reward, next_state, next_state_actions, done):
        """
        Used later to train the model with past episodes (whole games).
        """
        self.memory.append((state, action, reward, next_state, next_state_actions, done))

    def exploration(self, available_actions):
        """
        Exploration approach: choose randomly a possible action.
        """
        num_actions_rugbyman = [len(actions) - 2 for actions in available_actions]  # -2 to exclude rugbyman and his neutral action

        # Ponderate the probabilities of chosing each rugbyman by number of possible actions of rugbyman
        probabilities = num_actions_rugbyman / np.sum(num_actions_rugbyman)

        # Select randomly a rugbyman
        random_rugbyman_index = np.random.choice(len(available_actions), p=probabilities)
        random_rugbyman_choice = available_actions[random_rugbyman_index]

        # Select an action among possible actions of the selected rugbyman
        random_action_index = np.random.choice(len(random_rugbyman_choice) - 2)  # -2 to exclude rugbyman and his neutral action
        selected_action = random_rugbyman_choice[random_action_index + 2]  # +2 to exclude rugbyman and his neutral action
        return random_rugbyman_choice[0], [selected_action[0] - 1, selected_action[1] - 1]

    def exploitation(self, available_actions, state):
        """
        Exploitation approach: choose possible action with best estimated Q-value.
        """
        max_q_value = -np.inf
        for rugbyman_actions in available_actions: #ATTENTION, NE FONCTIONNE QUE POUR LES MOVES DE RUGBYMEN
            rugbyman = rugbyman_actions[0]
            for i in range(2, len(rugbyman_actions)):
                action_position = [rugbyman_actions[i][0], rugbyman_actions[i][1]] #position de la case d'arrivée de l'action
                action = RL_action_from_game(rugbyman, action_position)
                input_data = np.array([state, action])
                q_value = self.model.predict(input_data.reshape(1, 2, 8, 11))[0][0]
                if q_value > max_q_value:
                    max_q_value = q_value
                    greedy_rugbyman = rugbyman
                    greedy_action = rugbyman_actions[i]
        return greedy_rugbyman, greedy_action

    def act(self, game, player, state):
        """
        Returns the chosen action using epsilon-greedy approach.
        """
        available_actions = game.every_possible_move(player)
        if np.random.rand() <= self.epsilon:
            action = self.exploration(available_actions)
            return action
        else:
            action = self.exploitation(available_actions, state)
            return action

    def replay(self, batch_size):
        """
        Model learns from an episode of the game with reinforcement learning.
        """
        minibatch = np.random.choice(len(self.memory), batch_size, replace=True)

        for index in minibatch:
            state, action, reward, next_state, next_state_actions, done = self.memory[index]
            input_data = [np.array([state, action]).reshape(1, 2, 8, 11) for action in next_state_actions]
            next_state_rewards = np.array([self.model.predict(input)[0][0] for input in input_data])
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(next_state_rewards)

            target_f = target

            # Entraînez le modèle avec l'échantillon
            input_data = np.stack([state, action])
            print(input_data)
            print(target_f)
            self.model.fit(input_data.reshape(1, 2, 8, 11), target_f.reshape(1))

        # Réduisez l'exploration au fil du temps
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

"""
def rl_bot_tf(game, player):
    #available_moves = game.every_possible_move(player)
    #RL_available_moves = RL_available_actions(available_moves)
    current_state = states.State(Constants.number_of_rows, Constants.number_of_columns)
    current_state.get_RL_state_from_game(game)
    current_state.random_state()
    state = current_state.get_state()
    action = RL_available_actions(game.every_possible_move(game.get_player_red()))[1]
    print("L'état initial est: ")
    print(state)
    print("L'action choisie est: ")
    print(action)
    current_state.next_step_from_action(action)
    new_state = current_state.get_state()
    print("L'état final est: ")
    print(new_state)
    print(game.every_possible_move(game.get_player_red()))
    #action = agent.act(game, player, state)
    #return action


#print(rl_bot_tf(game, game.get_player_red()))
"""

input_shape = (2, 8, 11)
agent = DQNAgent(input_shape, Color.RED)

graphique = front.Graphique()
state = State(Constants.number_of_rows, Constants.number_of_columns)
next_state = State(Constants.number_of_rows, Constants.number_of_columns)

# Entraînement de l'IA sur plusieurs épisodes
for episode in range(1000):
    game = game.Game(graphique)
    player = game.get_player_red()
    for time in range(100): 
        done = game.is_game_over()
        if not done[0]:
            state.get_RL_state_from_game(game)
            action = agent.act(game, player, state.get_state())
            RL_action = RL_action_from_game(action[0], action[1])
            reward = -1
            #game.play_from_RL(action) # A DEFINIR
            next_state.get_RL_state_from_game(game)
            next_state_actions = game.every_possible_move(game.get_player_red())
            RL_next_state_actions = RL_available_actions(next_state_actions)
            done = False
        else:
            action = None
            next_state = None
            next_state_actions = None
            if done[1].get_color() == Color.RED:
                reward = 1000
            else:
                reward = -1000
            done = True
        """if time == 0:
            print("state")
            print(state.get_state())
            print("RL action")
            print(RL_action)
            print("Reward")
            print(reward)
            print("Next state")
            print(next_state.get_state())
            print("RL next state actions")
            print(RL_next_state_actions)
            print("Done")
            print(done)"""
        agent.remember(state.get_state(), RL_action, reward, next_state.get_state(), RL_next_state_actions, done)
        state = next_state
        if done:
            break
    if len(agent.memory) > 32:  # Taille minimale de la mémoire pour commencer la formation
        agent.replay(32)  # Taille du lot pour la formation"""

