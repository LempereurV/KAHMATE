import tensorflow as tf
import numpy as np
import states
from states import *
from constants import Constants
import game
import front


class DQNAgent:
    def __init__(self, state_size):
        self.player = Color.RED
        self.state_size = state_size
        self.memory = []  # Utilisez une structure de mémoire pour stocker les expériences passées
        self.gamma = 0.95  # Facteur de remise pour les récompenses futures
        self.epsilon = 1.0  # Taux d'exploration initial
        self.epsilon_decay = 0.995  # Taux de décroissance de l'exploration
        self.epsilon_min = 0.01  # Taux d'exploration minimum
        self.learning_rate = 0.001
        self.available_actions = np.zeros((1, 8, 11)) #Tableau des actions possibles en l'état actuel du jeu
        # Modèle du réseau neuronal
        self.model = self.build_model()

    def set_available_actions(self, game, state):
        available_actions = game.every_possible_move(self.player)
        RL_available_actions = RL_available_actions(available_actions)
        self.available_actions = RL_available_actions

    def masked_loss(self, y_true, y_pred):
        valid_mask = self.available_actions
        masked_y_true = tf.boolean_mask(y_true, valid_mask)
        masked_y_pred = tf.boolean_mask(y_pred, valid_mask)
        loss = tf.keras.losses.mean_squared_error(masked_y_true, masked_y_pred)
        return loss

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(8, 11)),  # Couche d'entrée pour les tableaux 2D
            tf.keras.layers.Flatten(),  # Aplatit le tableau en 1D
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(88*4, activation='sigmoid')  # Couche de sortie linéaire pour la valeur Q
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss = lambda y_true, y_pred: self.masked_loss(y_true, y_pred, self.available_actions))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, game, player, state):
        # epsilon-greedy approach
        available_actions = game.every_possible_move(player)
        if np.random.rand() >= self.epsilon: #<=
            action_index = np.random.choice(len(available_actions))
            return available_actions[action_index]
        q_values = self.model.predict(np.expand_dims(state, axis=0))[0]
        rugbyman_arrived = q_values[0:88]
        rugbyman_left = q_values[88:2*88]
        ball_arrived = q_values[2*88:3*88]
        ball_left = q_values[3*88:4*88]
        i_rugbyman_arrived = 0
        for i in range(1, 88):
            if rugbyman_arrived[i] > rugbyman_arrived[i_rugbyman_arrived]:
                i_rugbyman_arrived = i
        i_rugbyman_left = 0
        for i in range(1, 88):
            if rugbyman_left[i] > rugbyman_left[i_rugbyman_left]:
                i_rugbyman_left = i
        i_ball_arrived = 0
        for i in range(1, 88):
            if ball_arrived[i] > ball_arrived[i_ball_arrived]:
                i_ball_arrived = i
        i_ball_left = 0
        for i in range(1, 88):
            if ball_left[i] > ball_left[i_ball_left]:
                i_ball_left = i
        
        #vérifier si l'action peut être réalisée
        action = np.zeros((8, 11))
        if rugbyman_arrived[i_rugbyman_arrived] * rugbyman_left[i_rugbyman_left] > ball_arrived[i_ball_arrived] * ball_left[i_ball_left]:            
            action[i_rugbyman_left // 11, i_rugbyman_left % 11] = -1
            action[i_rugbyman_arrived // 11, i_rugbyman_arrived % 11] = 1
            return action
        else:
            action[i_ball_left // 11, i_ball_left % 11] = -10
            action[i_ball_arrived // 11, i_ball_arrived % 11] = 10
            return action

    def replay(self, batch_size):
        minibatch = np.random.choice(len(self.memory), batch_size, replace=True)

        for index in minibatch:
            state, action, reward, next_state, done = self.memory[index]

            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            target_f = self.model.predict(state)
            target_f[0][action] = target

            # Entraînez le modèle avec l'échantillon
            self.model.fit(state, target_f)

        # Réduisez l'exploration au fil du temps
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# Exemple d'utilisation avec un environnement de jeu fictif
state_size = (8, 11)  # Changer en fonction de votre état de jeu
agent = DQNAgent(state_size)

graphique = front.Graphique()
game = game.Game(graphique)


def rl_bot_tf(game, player):
    #available_moves = game.every_possible_move(player)
    #RL_available_moves = RL_available_actions(available_moves)
    current_state = states.State(Constants.number_of_rows, Constants.number_of_columns)
    current_state.get_RL_state_from_game(game)
    state = current_state.get_state()
    print(state)
    print(RL_available_actions(game.every_possible_move(game.get_player_red()))[0])
    #action = agent.act(game, player, state)
    #return action


print(rl_bot_tf(game, game.get_player_red()))

"""# Entraînement de l'IA sur plusieurs épisodes
for episode in range(1000):
    state = State(Constants.number_of_rows, Constants.number_of_columns)
    state.get_RL_state_from_game(game)  # Exemple d'état fictif
    for time in range(100):  # Limite d'itérations par épisode
        action = agent.act(state)
        next_state = np.random.random((1, state_size))  # Exemple d'état fictif suivant
        reward = np.random.random()  # Exemple de récompense fictive
        done = False  # Indicateur de fin de partie fictif
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
    if len(agent.memory) > 32:  # Taille minimale de la mémoire pour commencer la formation
        agent.replay(32)  # Taille du lot pour la formation"""
