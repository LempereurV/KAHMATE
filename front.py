from typing import Any
import pygame
import sys
import game
import rugbymen
import actions
import color
import random
from constants import *

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
        self.plateau = pygame.image.load(image_path)
        # Définition de la taille de la fenêtre
        self.size = self.plateau.get_size()

        # Création de la fenêtre
        self.screen = pygame.display.set_mode(self.size)

        # Création de la hitbox
        self.hitbox = create_hitbox(self.screen)

        # Affichage de l'image dans la fenêtre
        self.screen.blit(self.plateau, (0, 0))

    ### A supprrimer###

    def draw_last_row(self):
        for i in range (len(self.hitbox)):
            if i//(Constants.number_of_columns+2)==Constants.number_of_rows+1:
                pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox[i], 0)
        pygame.display.flip()

    ### FIn a supprimer #####
    
    def get_hitbox_on_click(self):
        cond=False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ValueError("The player has quit the game")
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
        
        
    
    def display_rugbyman(self, rugbyman):
        path=path_convertor(rugbyman)
        pos=rugbyman.get_pos()
        player = pygame.image.load(path)
        player = pygame.transform.scale(player,
                                         (Constants.square_width_normalized*self.screen.get_width(),
                                           Constants.square_height_normalized*self.screen.get_height()))
        
        self.screen.blit(player, self.hitbox[pos[0]*(Constants.number_of_columns+2)+pos[1]].topleft)


    # Affiche un joueur au centre de la hitbox
    


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
        self.screen.blit(self.plateau, (0, 0))
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



