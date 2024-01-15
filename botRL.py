import tensorflow as tf
import numpy as np
import states
from states import *
from constants import Constants
import game
import front


class DQNAgent:
    def __init__(self, input_shape, color, model = None):
        self.player = color
        self.input_size = input_shape
        self.memory = []  # Utilisez une structure de mémoire pour stocker les expériences passées
        self.gamma = 0.95  # Facteur de remise pour les récompenses futures
        self.epsilon = 1.0  # Taux d'exploration initial
        self.epsilon_decay = 0.995  # Taux de décroissance de l'exploration
        self.epsilon_min = 0.01  # Taux d'exploration minimum
        self.learning_rate = 0.001
        if model is None:
            self.model = self.build_model() #Modèle du réseau neuronal
        else:
            self.model = model

    def get_model(self):
        return self.model
    
    def build_model(self):
        """
        Creation of the neural network model: 2 hidden layers of 24 neurons with relu activation function and a linear output layer.
        The input is a grid of the game state and a possible action in that state.
        The output is the estimated Q-value of choosing this action in that state.
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(2, 8, 13)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def remember(self, memory):
        """
        Used later to train the model with past episodes (whole games).
        """
        for memory_item in memory:
            self.memory.append(memory_item)

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
        return random_rugbyman_choice[0], selected_action

    def exploitation(self, available_actions, state):
        """
        Exploitation approach: choose possible action with best estimated Q-value.
        """
        max_q_value = -np.inf
        for rugbyman_actions in available_actions: #ATTENTION, NE FONCTIONNE QUE POUR LES MOVES DE RUGBYMEN
            rugbyman = rugbyman_actions[0]
            for i in range(2, len(rugbyman_actions)):
                action_position = [rugbyman_actions[i][0] - 1, rugbyman_actions[i][1] - 1] #position de la case d'arrivée de l'action
                action = RL_action_from_game(rugbyman, action_position)
                input_data = np.array([state, action])
                q_value = self.model.predict(input_data.reshape(1, 2, 8, 13))[0][0]
                if q_value >= max_q_value:
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
            state = self.memory[index][0]
            action = self.memory[index][1]
            reward = self.memory[index][2]
            next_state = self.memory[index][3]
            next_state_actions = self.memory[index][4]
            done = self.memory[index][5]

            input_data = [np.array([next_state, action]).reshape(1, 2, 8, 13) for action in next_state_actions]
            next_state_rewards = np.array([self.model.predict(input)[0][0] for input in input_data])
            target = reward
            if not done:
                target = reward + 0.2 * (self.gamma * np.amax(next_state_rewards) - target)

            target_f = target

            # Entraînez le modèle avec l'échantillon
            input_data = np.array([state, action])
            self.model.fit(input_data.reshape(1, 2, 8, 13), target_f.reshape(1))

        # Réduisez l'exploration au fil du temps
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


input_shape = (2, 8, 13)
agent_red = DQNAgent(input_shape, Color.RED)
agent_blue = DQNAgent(input_shape, Color.BLUE)

graphique = front.Graphique()
state = State(Constants.number_of_rows, Constants.number_of_columns + 2)
next_state = State(Constants.number_of_rows, Constants.number_of_columns + 2)
# Entraînement de l'IA sur plusieurs épisodes
for episode in range(1000):
    game_episode = game.Game(graphique)
    memorize_red_if_game_finished = []
    memorize_blue_if_game_finished = []
    for episode_step in range(300):
        graphique.draw_board(game_episode)
        done = game_episode.is_game_over()
        if not done[0]:
            player = game_episode.get_player_turn()
            player_color = game_episode.get_player_turn().color()
            state.get_RL_state_from_game(game_episode)
            if player_color == Color.RED:
                action = agent_red.act(game_episode, player, state.get_state()) #game coordinates, not RL coordinates
                RL_action = RL_action_from_game(action[0], action[1])
                reward = -1
                game_episode.play_from_RL(action)
                next_state.get_RL_state_from_game(game_episode)
                next_state_actions = game_episode.every_possible_move(game_episode.get_player_red())
                RL_next_state_actions = RL_available_actions(next_state_actions)
                done = False
            if player_color == Color.BLUE:
                action = agent_blue.act(game_episode, player, state.get_state()) #game coordinates, not RL coordinates
                RL_action = RL_action_from_game(action[0], action[1])
                reward = -1
                game_episode.play_from_RL(action)
                next_state.get_RL_state_from_game(game_episode)
                next_state_actions = game_episode.every_possible_move(game_episode.get_player_blue())
                RL_next_state_actions = RL_available_actions(next_state_actions)
                done = False
            if episode_step % 2 == 0:
                game_episode.refresh_players_rugbymen_stats()
                game_episode.change_player_turn()
        else:
            if player_color == Color.RED:
                action = None
                next_state_actions = None
                if done[1] == Color.RED:
                    reward = 1000
                else:
                    reward = -1000
                done = True
            if player_color == Color.BLUE:
                action = None
                next_state_actions = None
                if done[1] == Color.BLUE:
                    reward = -1000
                else:
                    reward = 1000
                done = True
        if player_color == Color.RED:
            memorize_red_if_game_finished.append((state.get_state(), RL_action, reward, next_state.get_state(), RL_next_state_actions, done))
        if player_color == Color.BLUE:
            memorize_blue_if_game_finished.append((state.get_state(), RL_action, reward, next_state.get_state(), RL_next_state_actions, done))
        state = next_state
        if done:
            agent_red.remember(memorize_red_if_game_finished)
            agent_blue.remember(memorize_blue_if_game_finished)
            agent_red.get_model().save('agent_red.keras')
            agent_blue.get_model().save('agent_blue.keras')
            break
    if len(agent_red.memory) > 32:  # Taille minimale de la mémoire pour commencer la formation
        agent_red.replay(32)  # Taille du lot pour la formation
    if len(agent_blue.memory) > 32:
        agent_blue.replay(32)
