from typing import Any
import pygame
import sys
<<<<<<< HEAD
import game
import rugbymen
import actions
import color
import random
from constants import *
import cards 
=======
import actions
from rugbymen import *
from game import *

# Tokens and menu class import (can be import * as they are only used in front.py)
from tokens import *
from menu import *
>>>>>>> main

# Initialisation de Pygame
pygame.init()
clock = pygame.time.Clock()

# Chargement de l'image, chemin relatif
image_path = "Images/plateau.png"
image = pygame.image.load(image_path)
# Définition de la taille de la fenêtre
size = image.get_size()


<<<<<<< HEAD

# Création de la fenêtre
screen = pygame.display.set_mode(size)
# surf = pygame.surface.Surface(size)


def create_hitbox(screen):

    """
        
    """
    #La hitbox contient chaque case du terrain, ainsi que les bords du terrain (les bords sont des cases de tailles identiques au damier classique)
    #Chaque hitbox est divisé par 4 pour avoir une hitbox plus petite (permet de  cliquer sur le ballon )
    full_hitbox = []
    for j in range((Constants.number_of_rows+2)):
        for i in range((Constants.number_of_columns+2)):
            full_hitbox.append(pygame.Rect((Constants.edge_width_normalized + i * Constants.square_width_normalized)*screen.get_width(), 
                                        (Constants.edge_height_normalized + j * Constants.square_height_normalized)*screen.get_height(),
                                        Constants.square_width_normalized*screen.get_width(), 
                                        Constants.square_height_normalized*screen.get_height()))
    return full_hitbox
        


=======
# Création de la fenêtre
screen = pygame.display.set_mode(size)
>>>>>>> main


class Graphique:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Chargement de l'image, chemin relatif
        image_path = "Images/plateau.png"
        self.board = pygame.image.load(image_path)

        
        # Définition de la taille de la fenêtre
        #width = int(self.board.get_width() * Constants.scale_factor)
        #height = int(self.board.get_height() * Constants.scale_factor)
        

        


        # Création de la fenêtre
        #self.screen = pygame.display.set_mode(self.size)
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,pygame.RESIZABLE)

        width=pygame.display.Info().current_w
        height=pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)

        self.board = pygame.transform.scale(self.board, (width, height))



        # Création de la hitbox
        self.hitbox = create_hitbox(self.screen)

        # Affichage de l'image dans la fenêtre
        self.screen.blit(self.board, (0, 0))

<<<<<<< HEAD
    ### A supprrimer###

    def draw_last_row(self):
        for i in range (len(self.hitbox)):
            if i//(Constants.number_of_columns+2)==Constants.number_of_rows+1:
                pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox[i], 0)
        pygame.display.flip()

    ### FIn a supprimer #####


    def is_board_being_resized(self,event):
        if event.type == pygame.VIDEORESIZE:
            print("The window has been resized")
            size = event.size
            self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            self.board = pygame.transform.scale(self.board, size)
            self.hitbox = create_hitbox(self.screen)
            return True
        return False


    def get_hitbox_on_click(self):
        cond=False
        while True:
=======
    # Displays the number on the screen of the hitbox when you click on it
    def display_number(self, hitbox):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i < 88:
                    print(i % 11, i // 11)
                else:
                    print(i)
            else:
                pass

    def get_hitbox(self, hitbox):  # n'attends pas le clique du joueur
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i < 88:
                    return [i, (i % 11, i // 11)]
                else:
                    return [i, i]
            else:
                return None

    def get_hitbox_for_back(self, hitbox):
        cond = True
        while cond:
>>>>>>> main
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ValueError("The player has quit the game")
                elif self.is_board_being_resized(event):
                    return False,False
                    # usig continue works but i can t find a way to still display the board since i need Game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.hitbox)):
                        if self.hitbox[i].collidepoint(pygame.mouse.get_pos()):
                            #We check if the click was on the bottom right part of the hitbox
                            hitbox_center_x, hitbox_center_y=self.hitbox[i].center
                            mouse_x,mouse_y =pygame.mouse.get_pos()
                            if mouse_x>hitbox_center_x and mouse_y>hitbox_center_y:
                                cond=True
                            return [i//(Constants.number_of_columns+2),i%(Constants.number_of_columns+2)],cond

    
    def display_ball(self, ball):
        ball_graph = pygame.image.load("Images/Ballon.png")
        ball_graph = pygame.transform.scale(ball_graph, (self.hitbox[0].width/2, self.hitbox[0].height/2))

        self.screen.blit(ball_graph,self.hitbox[ball.get_pos_x()*(Constants.number_of_columns+2)+ball.get_pos_y()].center)
        pygame.display.flip()
        
    
    def draw_cards(self, player):
        for i in range (6):

            cond=False #Permet de savoir si la carte est dans le deck
            for card in player.get_deck():
                if cards.convert_card_to_int(card)==i+1:
                    cond=True
            if cond:
                path="Images/Carte"+str(i+1)+".png"
            else:
                path="Images/Carte_Endurance.png"
            card_graph = pygame.image.load(path)
            card_graph = pygame.image.load(path)
            card_graph = pygame.transform.scale(card_graph, (2*self.hitbox[0].width, 3*self.hitbox[0].height))

            if player.get_color()==color.Color.RED:
                if i<3:
                    self.screen.blit(card_graph,self.hitbox[2*(Constants.number_of_columns+2)+2*i].topleft)
                else:
                    self.screen.blit(card_graph,self.hitbox[5*(Constants.number_of_columns+2)+2*(i-3)].topleft)
            if player.get_color()==color.Color.BLUE:
                if i<3:
                    self.screen.blit(card_graph,self.hitbox[2*(Constants.number_of_columns+2)+(Constants.number_of_columns+2)//2+1+2*i].topleft)
                else:
                    self.screen.blit(card_graph,self.hitbox[5*(Constants.number_of_columns+2)+(Constants.number_of_columns+2)//2+1+2*(i-3)].topleft)
        pygame.display.flip()


    def display_rugbyman(self, rugbyman):
        path=path_convertor(rugbyman)
        pos=rugbyman.get_pos()
        player = pygame.image.load(path)
        player = pygame.transform.scale(player,(self.hitbox[0].width,self.hitbox[0].height))
        
        self.screen.blit(player, self.hitbox[pos[0]*(Constants.number_of_columns+2)+pos[1]].topleft)

    def draw_case(self):
        for i in range (len(self.hitbox)):
            if i//(Constants.number_of_columns+2)==Constants.number_of_rows+1:
                pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox[i], 0)
        pygame.display.flip()

<<<<<<< HEAD
    def highlight_button_after_click(self, Color):
        if Color==color.Color.RED:
            button = pygame.image.load("Images/Khamate_red_highlited.png")
            button = pygame.transform.scale(button,(4*self.hitbox[0].width,self.hitbox[0].height))
            self.screen.blit(button, self.hitbox[(Constants.number_of_rows+1)*(Constants.number_of_columns+2)].topleft)
        elif Color==color.Color.BLUE:
            button = pygame.image.load("Images/Khamate_blue_highlited.png")
            button = pygame.transform.scale(button,(4*self.hitbox[0].width,self.hitbox[0].height))
            self.screen.blit(button, self.hitbox[Constants.number_of_columns-2].topleft)
=======
    # Met en surbrillance les cases où le joueur peut se déplacer
    def highlight_move(self, list_move):
        for i in range(len(list_move)):
            pygame.draw.circle(
                self.screen,
                (20, 255, 167),
                (
                    (
                        92 + 46.8 / 2 + list_move[i][0] * 46.8,
                        62 + 46.5 / 2 + list_move[i][1] * 46.5,
                    )
                ),
                10,
            )
>>>>>>> main
        pygame.display.flip()
        pygame.time.delay(100)
                

    


    def highlight_pass(self, passes):
        s = pygame.Surface(self.hitbox[0].size)  # the size of your rect
        s.set_alpha(100)  # alpha level
        s.fill((255, 255, 0))
        for pass_ in passes:
            screen.blit(s, self.hitbox[pass_[0]*(Constants.number_of_columns+2) + pass_[1]].topleft)
        pygame.display.flip()


<<<<<<< HEAD
    def highlight_move_FElIX(self, list_move):
=======
    def highlight_move_FElIX(self, list_move, hitbox):
        s = pygame.Surface(hitbox[0].size)  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((150, 150, 150))
>>>>>>> main
        for move in list_move:
            if move[3]:
                self.highlight_move_annexe(move,(200, 200, 200))
            else:
                self.highlight_move_annexe(move,(72, 0, 72))
        pygame.display.flip()


    def highlight_move_annexe(self, move,color):
        s = pygame.Surface(self.hitbox[0].size)  # the size of your rect
        s.set_alpha(125)  # alpha level
        s.fill(color)
        screen.blit(s, self.hitbox[move[0] * (Constants.number_of_columns+2) + move[1]].topleft)  
        


    def draw_board(self, G):
        self.screen.blit(self.board, (0, 0))
        for rugbyman in game.Game.rugbymen(G):
                if rugbyman.get_KO() > 0:
                        self.display_rugbyman(rugbyman)

        #The double loop allows to draw the rugbyman not ko on top
        for rugbyman in game.Game.rugbymen(G):
                if rugbyman.get_KO() == 0:
                    self.display_rugbyman(rugbyman)

                
        self.display_ball(game.Game.get_ball(G))
        pygame.display.flip()


    # Rafraîchissement de la fenêtre
    def refresh(self):
        pygame.display.flip()

<<<<<<< HEAD
=======
    def test_menu(self):
        coords = []
        for j in range(8):
            for i in range(11):
                coords.append((92 + i * 46.8, 62 + j * 46.5))

        # Hitbox de chaque point
        hitbox = []
        for i in range(88):
            hitbox.append(pygame.Rect(coords[i][0], coords[i][1], 46.8, 46.5))
        hitbox.append(pygame.Rect(92 - 46.8, 62, 46.8, 46.5 * 8))
        hitbox.append(pygame.Rect(92 + 11 * 46.8, 62, 46.8, 46.5 * 8))
        ### Initialisation des jetons ###
        red_playertoken = RugbymanToken("Images/Costaud_bleu.png")
        blue_playertoken = RugbymanToken("Images/Costaud_rouge.png")
        tokens_group = pygame.sprite.Group()
        tokens_group.add(red_playertoken)
        tokens_group.add(blue_playertoken)
        i = 0
        for tokens in tokens_group:
            tokens.rect.center = hitbox[i].center
            i += 1

        ### Initialisation menu ###
        offscreen = (size[0] + 1, size[1] + 1)  # usefull to move the menu offscreen
        floating_menu = FloatingMenu(
            [
                "Move the player",
                "Pass the ball",
                "Tackle an opponent",
                "Kick the ball",
                "Score",
            ],
            (30, 40),
        )

        # WIP
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Collision must be checked in order of screen visibility (menu -> token -> empty case)
                    if floating_menu.is_on_screen(size):
                        collided_menu_hitbox = floating_menu.get_collision()
                        if (
                            collided_menu_hitbox != None
                        ):  # If the player clicked on the menu
                            if floating_menu.is_option_available(collided_menu_hitbox):
                                # DO THE CORRECT ACTION
                                print(
                                    """The action " """,
                                    floating_menu,
                                    """ " is triggered """,
                                )
                            else:
                                print("This action is not available")

                        else:  # The menu is on screen but the user didn't click on it
                            floating_menu.move(
                                offscreen
                            )  # The menu is offscreen and thus will be erased at the next screen refresh

                    else:  # The menu is offscreen (time for token collision check)
                        selected_hitbox = (
                            self.get_hitbox
                        )  # An hitbox is selected, let's see if it correspond to a Token Hitbox
                        for token in tokens_group:
                            if selected_hitbox == token.get_hitbox():
                                None  # Il faut afficher le menu au bon endroit

    def test_initialisation_board(self, game):
        coords = []
        for j in range(8):
            for i in range(11):
                coords.append((92 + i * 46.8, 62 + j * 46.5))

        # Hitbox de chaque point
        hitbox = []
        for i in range(88):
            hitbox.append(pygame.Rect(coords[i][0], coords[i][1], 46.8, 46.5))
        hitbox.append(pygame.Rect(92 - 46.8, 62, 46.8, 46.5 * 8))
        hitbox.append(pygame.Rect(92 + 11 * 46.8, 62, 46.8, 46.5 * 8))
        token_normal1_red = RugbymanToken("Images/Ordinaire_rouge.png")
        token_normal2_red = RugbymanToken("Images/Ordinaire_rouge.png")
        token_strong_red = RugbymanToken("Images/Costaud_rouge.png")
        token_hard_red = RugbymanToken("Images/Costaud_rouge.png")
        token_fast_red = RugbymanToken("Images/Rapide_rouge.png")
        token_smart_red = RugbymanToken("Images/Fute_rouge.png")
        red_tokens_group = pygame.sprite.Group()
        red_tokens_group.add(token_normal1_red)
        red_tokens_group.add(token_normal2_red)
        red_tokens_group.add(token_strong_red)
        red_tokens_group.add(token_hard_red)
        red_tokens_group.add(token_fast_red)
        red_tokens_group.add(token_smart_red)

        token_normal1_blue = RugbymanToken("Images/Ordinaire_bleu.png")
        token_normal2_blue = RugbymanToken("Images/Ordinaire_bleu.png")
        token_strong_blue = RugbymanToken("Images/Costaud_bleu.png")
        token_hard_blue = RugbymanToken("Images/Costaud_bleu.png")
        token_fast_blue = RugbymanToken("Images/Rapide_bleu.png")
        token_smart_blue = RugbymanToken("Images/Fute_bleu.png")
        blue_tokens_group = pygame.sprite.Group()
        blue_tokens_group.add(token_normal1_blue)
        blue_tokens_group.add(token_normal2_blue)
        blue_tokens_group.add(token_strong_blue)
        blue_tokens_group.add(token_hard_blue)
        blue_tokens_group.add(token_fast_blue)
        blue_tokens_group.add(token_smart_blue)

        red_positions = [(i, 10) for i in range(1, 7)]
        blue_positions = [(i, 10) for i in range(1, 7)]

        i = 11
        for token in red_tokens_group:
            token.rect.center = hitbox[i].center
            i += 11

        i = 11 + 10
        for token in blue_tokens_group:
            token.rect.center = hitbox[i].center
            i += 11

        test_menu = FloatingMenu(
            ["Coucou", "Rugby", "Move", "Pass", "Francois"], (30, 40)
        )
        flag_menu = 0

        while True:
            a = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_number(hitbox)
                    self.display_point()
                    for token in red_tokens_group:
                        a = token.select(red_tokens_group, image, game, self, hitbox)
                        if not a:
                            break
                    if a:
                        for token in blue_tokens_group:
                            a = token.select(blue_tokens_group, image, game, self, hitbox)
                            if not a:
                                break
                    flag_menu = 0
                    if test_menu.get_collision() == None and a:
                        test_menu.move(pygame.mouse.get_pos())
                        flag_menu = 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            screen.blit(image, (0, 0))
            if flag_menu:
                test_menu.draw(screen)
            red_tokens_group.draw(screen)
            blue_tokens_group.draw(screen)
            clock.tick(60)

    # Boucle principale
    def main_loop(self, game):
        # Players tokens sprites initialisation
        coords = []
        for j in range(8):
            for i in range(11):
                coords.append((92 + i * 46.8, 62 + j * 46.5))

    # Hitbox de chaque point
        hitbox = []
        for i in range(88):
            hitbox.append(pygame.Rect(coords[i][0], coords[i][1], 46.8, 46.5))
            hitbox.append(pygame.Rect(92 - 46.8, 62, 46.8, 46.5 * 8))
            hitbox.append(pygame.Rect(92 + 11 * 46.8, 62, 46.8, 46.5 * 8))

        playertoken1 = RugbymanToken("Images/Costaud_bleu.png")
        playertoken2 = RugbymanToken("Images/Costaud_rouge.png")
        tokens_group = pygame.sprite.Group()
        tokens_group.add(playertoken1)
        tokens_group.add(playertoken2)
        i = 0
        for tokens in tokens_group:
            tokens.rect.center = hitbox[i].center
            i += 1
            print(tokens.player_type.spec)

        test_menu = FloatingMenu(
            ["Coucou", "Rugby", "Move", "Pass", "Francois"], (30, 40)
        )
        flag_menu = 0

        while True:
            a = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_number()
                    self.display_point()
                    flag_menu = 0
                    for token in tokens_group:
                        a = token.select(tokens_group, image, game, self)
                        if not a:
                            break
                    print(a)
                    if test_menu.get_collision() == None and a:
                        test_menu.move(pygame.mouse.get_pos())
                        flag_menu = 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            screen.blit(image, (0, 0))
            if flag_menu:
                test_menu.draw(screen)
            tokens_group.draw(screen)
            clock.tick(60)

>>>>>>> main

# Fonction qui renvoit la position de l'image correspondant au rugbyman (surement à merge avec path_to_player_type)
def path_convertor(Rugbyman):
    if Rugbyman.get_KO()>0:
        if Rugbyman.get_color() == color.Color.RED:
            return "Images/Plaquage_rouge.png"
        if Rugbyman.get_color() == color.Color.BLUE:
            return "Images/Plaquage_bleu.png"
    else :
        if Rugbyman.spec == rugbymen.Spec.NORMAL:
            if Rugbyman.color == color.Color.RED:
                return "Images/Ordinaire_rouge.png"
            if Rugbyman.color == color.Color.BLUE:
                return "Images/Ordinaire_bleu.png"
        if Rugbyman.spec == rugbymen.Spec.STRONG:
            if Rugbyman.color == color.Color.RED:
                return "Images/Costaud_rouge.png"
            if Rugbyman.color == color.Color.BLUE:
                return "Images/Costaud_bleu.png"
        if Rugbyman.spec == rugbymen.Spec.HARD:
            if Rugbyman.color == color.Color.RED:
                return "Images/Dur_rouge.png"
            if Rugbyman.color == color.Color.BLUE:
                return "Images/Dur_bleu.png"
        if Rugbyman.spec == rugbymen.Spec.SMART:
            if Rugbyman.color == color.Color.RED:
                return "Images/Fute_rouge.png"
            if Rugbyman.color == color.Color.BLUE:
                return "Images/Fute_bleu.png"
        if Rugbyman.spec == rugbymen.Spec.FAST:
            if Rugbyman.color == color.Color.RED:
                return "Images/Rapide_rouge.png"
            if Rugbyman.color == color.Color.BLUE:
                return "Images/Rapide_bleu.png"


