import sys
sys.path.append('..')
import game
import actions
from color import Color
from RL_bot.rl_agent import DQNAgent
from keras.models import load_model
from RL_bot.states import State, play_from_RL
from constants import Constants



def launch_game(graphic): # Launch the game
    kahmate_graphics = graphic
    kahmate_graphics.set_new_hitbox()

    kahmate_game=game.Game(kahmate_graphics,True)
    kahmate_actions=actions.Action(kahmate_game,kahmate_graphics)
    
    model = load_model('RL_bot/agent_blue.keras')
    agent = DQNAgent((2, 8, 13), Color.BLUE, model, epsilon = 0)
    state = State(Constants.number_of_rows, Constants.number_of_columns + 2)

    while not kahmate_game.is_game_over():

        active_player = kahmate_game.get_player_turn()

        print("Tour du joueur "+str(active_player.get_color()))

        if active_player.get_color()==Color.BLUE: #bot turn
            rugbyman_played = None #avoid same rugbyman playing twice
            for i in range(2):
                kahmate_graphics.draw_board(kahmate_game)
                state.get_RL_state_from_game(kahmate_game)
                action = agent.act(kahmate_game, active_player, state.get_state())
                if action[0] != rugbyman_played:
                    play_from_RL(kahmate_game, action, kahmate_graphics)
                rugbyman_played = action[0]
            print("Le bot a fini de jouer")


        else: #player turn
            while active_player.get_can_play():
                kahmate_graphics.draw_board(kahmate_game)

                # rugbyman_or_ball_or_bool can take 4 different values :
                # - a rugbyman
                # - the ball
                # - True if the player has resized the screen
                # - False if the player has clicked outside the board
                
                rugbyman_or_ball_or_bool=kahmate_game.what_is_in_pos(kahmate_graphics)



                if (rugbyman_or_ball_or_bool in active_player.get_rugbymen()):

                    possible_move = kahmate_game.available_move_position(rugbyman_or_ball_or_bool)

                    if rugbyman_or_ball_or_bool in active_player.get_chosen_rugbymen() :
                        
                        kahmate_graphics.highlight_move( possible_move)
                        rugbyman_or_ball_or_bool=kahmate_actions.action_rugbyman(rugbyman_or_ball_or_bool,possible_move)
                    
                    #If the player hasnt chosen his two rugbyman yet
                    elif active_player.get_n_rugbymen()<2:
                        kahmate_graphics.highlight_move(possible_move)
                        
                        #move_rugbyman returns false if the move is not possible, and the rugbyman otherwise
                        #Note that the move itself is made in the function
                        rugbyman_or_ball_or_bool=kahmate_actions.action_rugbyman(rugbyman_or_ball_or_bool,possible_move)
                        

                        #We add the rugbyman to the list of chosen rugbyman if the move is made
                        if rugbyman_or_ball_or_bool !=False :
                            active_player.add_choosen_rugbymen(rugbyman_or_ball_or_bool)

                elif (rugbyman_or_ball_or_bool ==kahmate_game.get_ball()):
                    available_pass=kahmate_actions.available_pass()
                    if len(available_pass)>0:
                        kahmate_graphics.highlight_pass( available_pass)
                        kahmate_actions.make_pass(available_pass)

                elif (rugbyman_or_ball_or_bool == True):
                    #If the player has resized the screen
                    break

                kahmate_game.is_rugbyman_on_ball()
                active_player.actualize_can_play()
                kahmate_graphics.draw_board(kahmate_game)
                #Redraw cards does not suffice

                

        ### Partie reset quand le joueur a fini de jouer  ###
        kahmate_game.refresh_players_rugbymen_stats()
        kahmate_game.change_player_turn()