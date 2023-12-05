import front
import players
from color import Color
import rugbymen
import game
import actions 

Initialisation = True
Game_ON = True

while Game_ON:
    for event in front.pygame.event.get():
        ### Partie Initialisation ###
        if Initialisation:
            Graph = front.Graphique()
            Game=game.Game(Graph)
            front.pygame.display.flip()
            Initialisation = False

        while players.Player.get_can_play(game.Game.get_player_red(Game)):
            
            

            pos = front.Graphique.get_hitbox_for_back(Graph)

            if ( (game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]) != False) and (rugbymen.Rugbyman.color(game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]))== Color.RED)):
                
                front.Graphique.draw_board(Graph, Game)
                possible_move = game.Game.available_move_position(Game, game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]))
                front.Graphique.highlight_move_FElIX(Graph, possible_move)

                if players.Player.get_n_rugbymen(game.Game.get_player_red(Game))<2:

                    
                    pos2_or_bool=actions.move_rugbyman(
                        game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]),
                        possible_move,
                        Graph)
                    if not pos2_or_bool ==False :
                        players.Player.add_choosen_rugbymen(
                            game.Game.get_player_red(Game), 
                            game.Game.which_rugbyman_in_pos(Game, pos2_or_bool[0], pos2_or_bool[1]))
                
                elif game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]) in players.Player.get_chosen_rugbymen(game.Game.get_player_red(Game)) :
                    actions.move_rugbyman(
                        game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]),
                        possible_move,
                        Graph)
                players.Player.actualize_can_play(game.Game.get_player_red(Game))
                    
                
                front.Graphique.draw_board(Graph, Game)
                players.Player.actualize_can_play(game.Game.get_player_red(Game))


        while players.Player.get_can_play(game.Game.get_player_blue(Game)):
            
            

            pos = front.Graphique.get_hitbox_for_back(Graph)

            if ( (game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]) != False) and (rugbymen.Rugbyman.color(game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]))== Color.BLUE)):
                
                front.Graphique.draw_board(Graph, Game)
                possible_move = game.Game.available_move_position(Game, game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]))
                front.Graphique.highlight_move_FElIX(Graph, possible_move)

                if players.Player.get_n_rugbymen(game.Game.get_player_blue(Game))<2:

                    
                    pos2_or_bool=actions.move_rugbyman(
                        game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]),
                        possible_move,
                        Graph)
                    if not pos2_or_bool ==False :
                        players.Player.add_choosen_rugbymen(
                            game.Game.get_player_blue(Game), 
                            game.Game.which_rugbyman_in_pos(Game, pos2_or_bool[0], pos2_or_bool[1]))
                
                elif game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]) in players.Player.get_chosen_rugbymen(game.Game.get_player_blue(Game)) :
                    actions.move_rugbyman(
                        game.Game.which_rugbyman_in_pos(Game, pos[0], pos[1]),
                        possible_move,
                        Graph)
                players.Player.actualize_can_play(game.Game.get_player_blue(Game))
                    
                
                front.Graphique.draw_board(Graph, Game)
                players.Player.actualize_can_play(game.Game.get_player_blue(Game))

        ### Partie reset quand les deux joueurs ont joué ###
        if not players.Player.get_can_play(game.Game.get_player_blue(Game)) and not players.Player.get_can_play(game.Game.get_player_blue(Game)):
            players.Player.reset_player_after_turn(game.Game.get_player_red(Game))
            players.Player.reset_player_after_turn(game.Game.get_player_blue(Game))
            Game.refresh_players_rugbymen_stats()

        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON = False
print("Fin du jeu")
