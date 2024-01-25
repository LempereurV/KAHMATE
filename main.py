import front
import players
from color import Color
import rugbymen
import game
import actions 
import bot
import pygame



import minimax
import time
import cProfile
import matplotlib.pyplot as plt
import pstats
### Initializations ###
from io import StringIO

import pandas as pd


kahmate_graphics = front.Graphic()
kahmate_game = game.Game(kahmate_graphics)
kahmate_actions = actions.Action(kahmate_game,kahmate_graphics)

kahmate_graphics.display_ball(kahmate_game.get_ball())
#front.pykahmate_game.display.flip()# A changer 




AI=True    

while not kahmate_game.is_game_over():
    #We record the time it takes

    active_player = kahmate_game.get_player_turn()

 
    if AI and active_player.get_color()==Color.RED:
            ### Partie IA####
            moves=[None,None,None]
        
                
            minimax.minimax(kahmate_game,2,True,-float("inf"),float("inf"),kahmate_game.get_player_turn(),moves,graph)
         

            kahmate_graphics.draw_board(game)
            
            if moves[2]!=None:
                kahmate_game.get_ball().set_pos(moves[2])
            
            for move in moves[:2]:
                if move!=False:
                    kahmate_actions.move_rugbyman([move[1],move[2]],move[0],kahmate_game.get_ball(),move[3])
            kahmate_graphics.draw_board(game)
            active_player.set_can_play(False)
            kahmate_game.refresh_players_rugbymen_stats()
            kahmate_game.change_player_turn()
            continue


            ### ####


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
                
                kahmate_graphics.highlight_move_FElIX( possible_move)
                rugbyman_or_ball_or_bool=kahmate_actions.action_rugbyman(rugbyman_or_ball_or_bool,possible_move)
            
            #If the player hasnt chosen his two rugbyman yet
            elif active_player.get_n_rugbymen()<2:
                kahmate_graphics.highlight_move_FElIX(possible_move)
                
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

    print("Fin du jeu")

##### MENU
import sys
from main_menu_button import Button

BG = pykahmate_game.image.load("assets/Background.png")

SCREEN = kahmate_graphics.screen
pykahmate_game.display.set_caption("Menu")

center_center_pos = (BG.get_size()[0]/2,BG.get_size()[1]/2-30)
center_down_pos = (BG.get_size()[0]/2,BG.get_size()[1]/10*9)
left_center_pos = (BG.get_size()[0]/4+50,BG.get_size()[1]/2)
right_center_pos = (BG.get_size()[0]/4*3,BG.get_size()[1]/2-20)
right_center_upper_pos = (BG.get_size()[0]/4*3,BG.get_size()[1]/4*1)
right_center_lower_pos = (BG.get_size()[0]/4*3,BG.get_size()[1]/4*2.5)
center_up_pos = (BG.get_size()[0]/2,BG.get_size()[1]/10*2)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pykahmate_game.font.Font("assets/font.ttf", size)

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="1 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)
        

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/regle.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=center_center_pos)
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)


        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_7()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_2()

        pykahmate_game.display.update()

def options_2():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="2 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/deplacer_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(left_center_pos[0],left_center_pos[1]-30))
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        OPTIONS_TEXT_2 = pykahmate_game.image.load("assets/deplacer_2.png")
        OPTIONS_TEXT_2 = pykahmate_game.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
        
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=right_center_upper_pos)
        
        SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

        OPTIONS_TEXT_3 = pykahmate_game.image.load("assets/deplacer_3.png")
        OPTIONS_TEXT_3 = pykahmate_game.transform.scale(OPTIONS_TEXT_3, (OPTIONS_TEXT_3.get_size()[0]/2,OPTIONS_TEXT_3.get_size()[1]/2))
        
        OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=right_center_lower_pos)
        
        SCREEN.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)

        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_3()

        pykahmate_game.display.update()

def options_3():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="3 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/forcer_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(left_center_pos[0],left_center_pos[1]-30))
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        OPTIONS_TEXT_2 = pykahmate_game.image.load("assets/forcer_2.png")
        OPTIONS_TEXT_2 = pykahmate_game.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
        
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=right_center_pos)
        
        SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_2()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_4()

        pykahmate_game.display.update()

def options_4():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))
        
        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="4 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/passer_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(left_center_pos[0],left_center_pos[1]-30))
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        OPTIONS_TEXT_2 = pykahmate_game.image.load("assets/passer_2.png")
        OPTIONS_TEXT_2 = pykahmate_game.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
        
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=right_center_pos)

        SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)


        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_3()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_5()

        pykahmate_game.display.update()

def options_5():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/interseption_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=center_center_pos)
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="5 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_4()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_6()

        pykahmate_game.display.update()

def options_6():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="6 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/plaquer_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(left_center_pos[0],left_center_pos[1]-30))
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        OPTIONS_TEXT_2 = pykahmate_game.image.load("assets/plaquer_2.png")
        OPTIONS_TEXT_2 = pykahmate_game.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
        
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=right_center_upper_pos)
        
        SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

        OPTIONS_TEXT_3 = pykahmate_game.image.load("assets/plaquer_3.png")
        OPTIONS_TEXT_3 = pykahmate_game.transform.scale(OPTIONS_TEXT_3, (OPTIONS_TEXT_3.get_size()[0]/2,OPTIONS_TEXT_3.get_size()[1]/2))
        
        OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=right_center_lower_pos)
        
        SCREEN.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)

        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_5()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options_7()

        pykahmate_game.display.update()

def options_7():
    while True:
        OPTIONS_MOUSE_POS = pykahmate_game.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        page = Button(image=None, pos=(center_down_pos[0],center_down_pos[1]+30), 
                            text_input="7 of 7", font=get_font(30), base_color="Black", hovering_color="Black")
        
        page.update(SCREEN)

        OPTIONS_TEXT_1 = pykahmate_game.image.load("assets/pied_1.png")
        OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(left_center_pos[0],left_center_pos[1]-30))
        
        SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

        OPTIONS_TEXT_2 = pykahmate_game.image.load("assets/pied_2.png")
        OPTIONS_TEXT_2 = pykahmate_game.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
        
        OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=right_center_pos)
        
        SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

        OPTIONS_BACK = Button(image=None, pos=center_down_pos, 
                            text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")
        left_arrow = pykahmate_game.image.load("assets/arrow_left.png")
        left_arrow = pykahmate_game.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
        OPTIONS_LEFT = Button(image=left_arrow, pos=(center_down_pos[0]-100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        right_arrow = pykahmate_game.image.load("assets/arrow_right.png")
        right_arrow = pykahmate_game.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
        OPTIONS_RIGHT = Button(image=right_arrow, pos=(center_down_pos[0]+100, center_down_pos[1] - 7),text_input="", font=get_font(50), base_color="Black", hovering_color="Green") 
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT.update(SCREEN)
        OPTIONS_RIGHT.update(SCREEN)

        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(graph, game)
                if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    options_6()
                if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    options()

        pykahmate_game.display.update()

def main_menu(graph, game):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pykahmate_game.mouse.get_pos()

        MENU_TEXT = pykahmate_game.image.load("assets/logo.png") #get_font(100).render("KAHMATE", True, "#000000")
        MENU_TEXT = pykahmate_game.transform.scale(MENU_TEXT, (MENU_TEXT.get_size()[0]/2,MENU_TEXT.get_size()[1]/2))
        
        MENU_RECT = MENU_TEXT.get_rect(center=(BG.get_size()[0]/2, BG.get_size()[1]/8*1))

        PLAY_BUTTON = Button(image=pykahmate_game.image.load("assets/rect.png"), pos=(BG.get_size()[0]/2, BG.get_size()[1]/8*3), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pykahmate_game.image.load("assets/rect.png"), pos=(BG.get_size()[0]/2, BG.get_size()[1]/8*5), 
                            text_input="RULES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pykahmate_game.image.load("assets/rect.png"), pos=(BG.get_size()[0]/2, BG.get_size()[1]/8*7), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pykahmate_game.event.get():
            if event.type == pykahmate_game.QUIT:
                pykahmate_game.quit()
                sys.exit()
            if event.type == pykahmate_game.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main(graph, game)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pykahmate_game.quit()
                    sys.exit()

        pykahmate_game.display.update()



def main(graph, game):
    while not kahmate_game.is_game_over():
        print(kahmate_game.tour_balle())
        print(bot.compute_reward(game))
        active_player = kahmate_game.get_player_turn()
