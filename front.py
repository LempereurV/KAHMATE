from typing import Any
import pygame
import sys
import game
import rugbymen
import actions
import color
import random
from constants import *
import cards 

# Initialisation de Pygame
pygame.init()
clock = pygame.time.Clock()

# Chargement de l'image, chemin relatif
image_path = "Images/plateau.png"
image = pygame.image.load(image_path)
# Définition de la taille de la fenêtre
size = image.get_size()



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

    def highlight_button_after_click(self, Color):
        if Color==color.Color.RED:
            button = pygame.image.load("Images/Khamate_red_highlited.png")
            button = pygame.transform.scale(button,(4*self.hitbox[0].width,self.hitbox[0].height))
            self.screen.blit(button, self.hitbox[(Constants.number_of_rows+1)*(Constants.number_of_columns+2)].topleft)
        elif Color==color.Color.BLUE:
            button = pygame.image.load("Images/Khamate_blue_highlited.png")
            button = pygame.transform.scale(button,(4*self.hitbox[0].width,self.hitbox[0].height))
            self.screen.blit(button, self.hitbox[Constants.number_of_columns-2].topleft)
        pygame.display.flip()
        pygame.time.delay(100)
                

    


    def highlight_pass(self, passes):
        s = pygame.Surface(self.hitbox[0].size)  # the size of your rect
        s.set_alpha(100)  # alpha level
        s.fill((255, 255, 0))
        for pass_ in passes:
            screen.blit(s, self.hitbox[pass_[0]*(Constants.number_of_columns+2) + pass_[1]].topleft)
        pygame.display.flip()


    def highlight_move_FElIX(self, list_move):
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

    def display_back_decks(self):
        back = pygame.image.load("Images/Carte_Endurance.png")
        back = pygame.transform.scale(back, (100,200))
        self.screen.blit(back, (570, 430))
        self.screen.blit(back, (40, 430))

    def display_front_deck(self, deck):
        Cards_hitbox = []
        for i in range(len(deck)):
            self.screen.blit(pygame.transform.scale(pygame.image.load(deck[i].get_image()), (100, 180)), (27 + i * 108, 150))
            Cards_hitbox.append(pygame.Rect(27 + i * 108, 150, 100, 180))
        pygame.display.flip()
        return Cards_hitbox

    def get_hitbox_card(self, Cards_hitbox):
        cond = True
        while cond:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cond = False
                    for i in range(len(Cards_hitbox)):
                        if Cards_hitbox[i].collidepoint(pygame.mouse.get_pos()):
                            return i
                    cond = True
        return None
    
    def remove_card(self, i, Cards_hitbox):
        new_hitboxes = []
        for i in range(len(Cards_hitbox)):
            new_hitbox = pygame.Rect(27 + i * 108, 150, 100, 180)
            new_hitboxes.append(new_hitbox)
        Cards_hitbox = new_hitboxes


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


