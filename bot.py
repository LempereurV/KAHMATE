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

def easy_coords(list_of_lists):
    new_list = [sublist[:2] for sublist in list_of_lists]
    return new_list

cards=[1,2,3,4,5,6]

def draw_card_bot(cards):
    a = random.choice(cards)
    if len(cards) > 1:
        cards.remove(a)
    else:
        cards = [1,2,3,4,5,6]
    return a

def compute_reward(game):
    R = np.zeros((constants.Constants.number_of_rows +1, constants.Constants.number_of_columns + 1))
    A = game.tour_joueurs() #A matrix indicating +1 for friendly players (in red) and -1 for enemies.
    B = game.tour_balle() #Matrix indicating +1 for the ball.
    x, y = np.where(B == 1)
    if len(x) > 0 and len(y) > 0:
        S = A[x, y]
        x, y = x[0], y[0]
    # S=1 if the bot has the ball, -1 if the player has it and 0 if nobody has it
    if S == 1:
        for i in range(constants.Constants.number_of_rows + 1):
            for j in range(y, constants.Constants.number_of_columns + 1):
                # R advances towards the try line.
                R[i][j] = 3 * np.exp(2 * (j - y) / constants.Constants.number_of_columns + 1)
                # R favors the straight line.
                #R[i][j] += np.exp(-(i - x) ** 2 / constants.Constants.number_of_rows + 1)
        for Rugbyman in game.rugbymen():
            if Rugbyman.get_pos_x() == x + 1 and Rugbyman.get_pos_y() == y + 1:
                if Rugbyman.color == color.Color.RED:
                    R[x][y] = 0
                    # Cannot pass through an allied player.
                else:
                    for k in range(Rugbyman.move_points):
                        for l in range(Rugbyman.move_points):
                            if x + k < constants.Constants.number_of_rows  and y + l < constants.Constants.number_of_columns + 1:
                                R[x + k][y + l] -= 0.05 * np.exp(((k) ** 2) / (constants.Constants.number_of_rows + 1)) + 0.05 * np.exp(((l) ** 2) /(constants.Constants.number_of_columns + 1))
                                # Areas around opposing players should be avoided but are not impassable obstacles.

    if S == -1:
        for i in range(constants.Constants.number_of_rows+1):
            for j in range(constants.Constants.number_of_columns + 1):
                # R moves towards the opposing player with the ball.
                R[i][j] = np.exp(-(j - y) ** 2 / (constants.Constants.number_of_columns + 1))
                R[i][j] += np.exp(-(i - x) ** 2 / (constants.Constants.number_of_rows + 1))

    if S == 0:
        for i in range(constants.Constants.number_of_rows+1):
            for j in range(constants.Constants.number_of_columns + 1):
                #R moves towards the ball.
                R[i][j] = np.exp(-(j-y)**2/(constants.Constants.number_of_columns + 1))
                R[i][j] += np.exp(-(i-x)**2/(constants.Constants.number_of_rows + 1))
    return R
   
def compute_action(game, Graph):
    R = compute_reward(game)
    A = game.tour_joueurs()
    B = game.tour_balle()
    #if red has the ball, we want to know if we can advance with it or if we have to pass it
    x,y = np.where(B == 1)
    if len(x) > 0 and len(y) > 0:
        S = A[x,y]
        x, y = x[0]+1, y[0]+1
    print([x,y])
    nb_joueurs = [] #can't be over 2
    if S == 1:
        Poss = game.is_rugbyman_on_ball()
        print(Poss)
        #we want to go to the highest reward zone possible
        Rugbymen = []
        for Rugbyman in game.rugbymen():
            if Rugbyman.get_color() == color.Color.RED and Rugbyman.get_KO() == 0:
                scores = []
                ez_coords = easy_coords(game.available_move_position(Rugbyman))
                for i in range(constants.Constants.number_of_rows):
                    for j in range(constants.Constants.number_of_columns):
                        if [i,j] in ez_coords:
                            scores.append(R[i][j])
                score = max(scores)
                Rugbyman.set_score(score)
                Rugbymen.append(Rugbyman)
        Rugbymen = sorted(Rugbymen, key=lambda Rugbyman: Rugbyman.get_score(), reverse=True)
        #This list is sorted in descending order of the highest possible reward for all rugbymen
        if Poss.get_KO() == 0:
            if Poss != Rugbymen[0] and Poss != Rugbymen[1]:#if the ballkeeper can't attain the highest rewards, we will try to pass it
                Available_passes = actions.available_pass_bot(Poss, game)
                for i in range(len(Rugbymen)):
                    best_pos = Rugbymen[i].get_pos()
                    #get the coordinates of the rugbymen who can go to the highest reward zone using the Rugbymen list
                    if best_pos in Available_passes:
                        actions.make_pass_bot(game, Poss, Rugbymen[i])
                        coords = np.where(R == Rugbymen[i].get_score())
                        [x,y] = [coords[0][0], coords[1][0]]
                        print([x,y])
                        actions.action_rugbyman_bot([x,y], Rugbymen[i], game, Graph)
                        nb_joueurs.append(Rugbymen[i])
                        #then we play the others available rugbymen in the highest reward zone
                        if i == 0:
                            coords = np.where(R == Rugbymen[1].get_score())
                            [x,y] = [coords[0][0], coords[1][0]]
                            print([x,y])
                            actions.action_rugbyman_bot([x,y], Rugbymen[1], game, Graph)
                            nb_joueurs.append(Rugbymen[1])
                        else:
                            coords = np.where(R == Rugbymen[0].get_score())
                            [x,y] = [coords[0][0], coords[1][0]]
                            print([x,y])
                            actions.action_rugbyman_bot([x,y], Rugbymen[0], game, Graph)
                            nb_joueurs.append(Rugbymen[0])
            else:
                coords = np.where(R == Rugbymen[1].get_score())
                [x,y] = [coords[0][0], coords[1][0]]
                actions.action_rugbyman_bot([x,y], Poss, game, Graph)
                nb_joueurs.append(Poss)
                if Poss == Rugbymen[0]:
                    coords = np.where(R == Rugbymen[1].get_score())
                    [x,y] = [coords[0][0], coords[1][0]]
                    actions.action_rugbyman_bot([x,y], Rugbymen[1], game, Graph)
                    nb_joueurs.append(Rugbymen[1])
                else:
                    coords = np.where(R == Rugbymen[0].get_score())
                    [x,y] = [coords[0][0], coords[1][0]]
                    actions.action_rugbyman_bot([x,y], Rugbymen[0], game, Graph)
                    nb_joueurs.append(Rugbymen[0])

        if len(nb_joueurs)<2 and Poss not in nb_joueurs:
            coords = np.where(R == Poss.get_score())
            [x,y] = [coords[0][0], coords[1][0]]
            actions.action_rugbyman_bot([x,y], Poss, game, Graph)
            nb_joueurs.append(Poss)
    

    if S == 0:#no one has the ball
        Poss = game.is_rugbyman_on_ball()
        for Rugbyman in game.rugbymen():
            ez_coords = easy_coords(game.available_move_position(Rugbyman))
            #these are the coordinates of the squares that are available to move to
            if np.any(np.all(ez_coords == np.array([x, y]), axis=1)) and Rugbyman.get_color() == color.Color.RED and Rugbyman.get_KO() == 0:                
                actions.action_rugbyman_bot([x,y], Rugbyman, game, Graph)
                nb_joueurs.append(Rugbyman)
                Poss = Rugbyman
                break
        Rugbymen = []
        for Rugbyman in game.rugbymen():
            if Rugbyman.get_color() == color.Color.RED and Rugbyman != Poss:
                scores = []
                ez_coords = easy_coords(game.available_move_position(Rugbyman))
                for i in range(constants.Constants.number_of_rows):
                    for j in range(constants.Constants.number_of_columns):
                        if [i,j] in ez_coords:
                            scores.append(R[i][j])
                score = max(scores)
                Rugbyman.set_score(score)
                Rugbymen.append(Rugbyman)
        Rugbymen = sorted(Rugbymen, key=lambda Rugbyman: Rugbyman.get_score(), reverse=True)
        R = compute_reward(game)
        for i in range(2-len(nb_joueurs)):
            coords = np.where(R == Rugbymen[i].get_score())
            actions.action_rugbyman_bot(coords, Rugbymen[i], game, Graph)
            nb_joueurs.append(Rugbymen[i])

    if S == -1:#the enemy has the ball
        #if blue has the ball, we first want to know if we can claim it
        #we establish the list of rugbymen that can attain the ball
        a = False #represents if we have the ball or not
        for Rugbyman in game.rugbymen():
            ez_coords = easy_coords(game.available_move_position(Rugbyman))
            #these are the coordinates of the squares that are available to move to
            if np.any(np.all(ez_coords == np.array([x, y]), axis=1)) and Rugbyman.get_color() == color.Color.RED and Rugbyman.get_KO() == 0:                
                actions.action_rugbyman_bot([x,y], Rugbyman, game, Graph)
                nb_joueurs.append(Rugbyman)
                if Rugbyman.get_KO() == 0:#If the rugby player has successfully tackled.
                    Poss = Rugbyman
                    a = True
                break
        Rugbymen = []
        for Rugbyman in game.rugbymen():
                if Rugbyman.get_color() == color.Color.RED:
                    scores = []
                    ez_coords = easy_coords(game.available_move_position(Rugbyman))
                    for i in range(constants.Constants.number_of_rows):
                        for j in range(constants.Constants.number_of_columns):
                            if [i,j] in ez_coords:
                                scores.append(R[i][j])
                    score = max(scores)
                    Rugbyman.set_score(score)
                    Rugbymen.append(Rugbyman)
        Rugbymen = sorted(Rugbymen, key=lambda Rugbyman: Rugbyman.get_score(), reverse=True)
        R = compute_reward(game)
        if a:
            Rugbymen.remove(Poss)
            ez_coords = easy_coords(game.available_move_position(Rugbymen[0]))
            #these are the coordinates of the squares that are available to move to by the best rugbyman
            actions.action_rugbyman_bot(ez_coords, Rugbymen[0], game, Graph)
            nb_joueurs.append(Rugbymen[0])
        else:
            for i in range(2-len(nb_joueurs)):
                coords = np.where(R == Rugbymen[i].get_score())
                actions.action_rugbyman_bot(coords, Rugbymen[i], game, Graph)
                nb_joueurs.append(Rugbymen[i])
        
    print("bot's turn is over")
    print(nb_joueurs)
