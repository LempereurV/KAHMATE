from typing import Any
import pygame
import sys
import game
import rugbymen
import actions
import color
import random
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

new_coords = []
for j in range(16):
    for i in range(22):
        new_coords.append((92 + i * 46.8/2, 62 + j * 46.5/2))


ball_coords=[]
for j in range(8):
    for i in range(11):
        ball_coords.append((92 + i * 46.8+46.8/2, 62 + j * 46.5+46.5/2))

new_hitbox = []
for i in range(len(new_coords)):
    new_hitbox.append(pygame.Rect(new_coords[i][0], new_coords[i][1], 46.8/2, 46.5/2))

ball_hitbox = []
for i in range(88):
    ball_hitbox.append(pygame.Rect(ball_coords[i][0], ball_coords[i][1], 46.8/2, 46.5/2))


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
        # Affichage de l'image dans la fenêtre
        self.screen.blit(self.plateau, (0, 0))

    def draw_ball_hitboxes(self):
        for i in range(88):
            pygame.draw.rect(screen, pygame.Color(128, 128, 128, 1), ball_hitbox[i])
        pygame.display.flip()
   
    def draw_new_hitboxes(self):
        for i in range(len(new_coords)):
            pygame.draw.rect(screen, pygame.Color(random.randint(1,255), random.randint(1,255), random.randint(1,255)), new_hitbox[i])
        pygame.display.flip()
             

    def get_hitbox_for_back(self):
        cond = True
        while cond:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cond = False
                    for i in range(len(hitbox)):
                        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                            if i < 88:
                                return [i // 11, i % 11]
                    cond = True
        return None
    
    def get_new_hitbox_for_back(self):
        cond = True
        while cond:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cond = False
                    for i in range(len(new_hitbox)):
                        if new_hitbox[i].collidepoint(pygame.mouse.get_pos()):
                            if i < len(new_hitbox):
                                if i//22%2==1:# on est en bad de la case
                                    if i%22%2==1: #On est à droite de la case 
                                        return [i // 22, i % 22]
                            return [(i // 22) , (i % 22)]
                            
                    cond = True
        return None

    def display_ball(self, ball):
        ball_graph = pygame.image.load("Images/Ballon.png")
        ball_graph = pygame.transform.scale(ball_graph, (ball_hitbox[0].width, ball_hitbox[0].height))
        self.screen.blit(ball_graph, ball_coords[ball.get_position_x() * 11 + ball.get_position_y()])
        pygame.display.flip()
    
    # Affiche un joueur au centre de la hitbox
    def affiche_joueur(self, n_hit, path):
        joueur = pygame.image.load(path)
        joueur = pygame.transform.scale(joueur, (46.8, 46.5))
        self.screen.blit(joueur, coords[n_hit])
        pygame.display.flip()


    def highlight_move_FElIX(self, list_move):
        s = pygame.Surface(hitbox[0].size)  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((200, 200, 200))
        for move in list_move:
            screen.blit(
                s, hitbox[move[0] * 11 + move[1]].topleft
            )  # (0,0) are the top-left coordinates
            # pygame.draw.rect(screen,pygame.Color(128, 128, 128, 1),hitbox[move[0]*11+move[1]] )
        pygame.display.flip()

    def draw_board(self, G):
        self.screen.blit(self.plateau, (0, 0))
        for rugbyman in game.Game.rugbymen(G):
                self.affiche_joueur(rugbymen.Rugbyman.get_posx(rugbyman) * 11 + rugbymen.Rugbyman.get_posy(rugbyman), path_convertor(rugbyman))
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


def is_pos_bottom_right(pos):
    if pos[0]%2==1:# on est en bas de la case
        if pos[1]%2==1: #On est à droite de la case
            return True

def convert_new_hitbox_to_hitbox(pos):
    return [pos[0]//2,pos[1]//2]
