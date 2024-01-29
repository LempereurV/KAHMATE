import sys

sys.path.append("..")
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import numpy as np
from RL_bot.states import *
import tensorflow as tf


class DQNAgent:
    def __init__(self, input_shape, color, model=None, epsilon=1.0):
        self.player = color
        self.input_size = input_shape
        self.memory = []  # Memory of past episodes for future training
        self.gamma = 0.95  # Discount factor of future rewards
        self.epsilon = epsilon  # Initial exploration rate
        self.epsilon_decay = 0.995  # Exploration rate decay
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.learning_rate = 0.2  # Learning rate
        if model is None:
            self.model = self.build_model()
        else:
            self.model = model

    def get_model(self):
        return self.model

    def build_model(self):
        """
        Creation of a neural network: 2 hidden layers of 24 neurons.
        The input is a grid of the game state and a possible action in that state.
        The output is the estimated Q-value of choosing this action in that state.
        """
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(2, 8, 13)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(24, activation="relu"),
                tf.keras.layers.Dense(24, activation="relu"),
                tf.keras.layers.Dense(1, activation="linear"),
            ]
        )

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss="mse",
        )
        return model

    def remember(self, memory):
        """
        Adds the episode data to agent's memory for training.
        """
        for memory_item in memory:
            self.memory.append(memory_item)

    def exploration(self, available_actions):
        """
        Exploration approach: choose randomly a possible action.
        """

        # Selection of a rugbyman among all rugbyman with probabilities proportional to the number of possible actions
        number_of_actions_rugbyman = [
            len(actions) - 2 for actions in available_actions
        ]  # -2 to exclude rugbyman and his neutral action
        probabilities = number_of_actions_rugbyman / np.sum(number_of_actions_rugbyman)
        random_rugbyman_index = np.random.choice(
            len(available_actions), p=probabilities
        )
        random_rugbyman_choice = available_actions[random_rugbyman_index]

        # Select an action among possible actions of the selected rugbyman
        random_action_index = np.random.choice(
            len(random_rugbyman_choice) - 2
        )  # -2 to exclude rugbyman and his neutral action
        selected_action = random_rugbyman_choice[random_action_index + 2]
        return random_rugbyman_choice[0], selected_action

    def exploitation(self, available_actions, state):
        """
        Exploitation approach: choose possible action with best estimated Q-value.
        """
        max_q_value = -np.inf
        for rugbyman_actions in available_actions:
            rugbyman = rugbyman_actions[0]
            for i in range(2, len(rugbyman_actions)):
                new_position_with_action = [
                    rugbyman_actions[i][0] - 1,
                    rugbyman_actions[i][1] - 1,
                ]
                action = RL_action_from_game(rugbyman, new_position_with_action)
                input_data = np.array([state, action])
                q_value = self.model.predict(
                    input_data.reshape(1, 2, 8, 13), verbose=None
                )[0][0]
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

            input_data = [
                np.array([next_state, action]).reshape(1, 2, 8, 13)
                for action in next_state_actions
            ]
            next_state_rewards = np.array(
                [self.model.predict(input, verbose=None)[0][0] for input in input_data]
            )
            target = reward
            if not done:
                target = reward + self.learning_rate * (
                    self.gamma * np.amax(next_state_rewards) - target
                )
            target_f = target

            # Entraînez le modèle avec l'échantillon
            input_data = np.array([state, action])
            self.model.fit(input_data.reshape(1, 2, 8, 13), target_f.reshape(1))

        # Réduisez l'exploration au fil du temps
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
