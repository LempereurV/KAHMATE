from typing import Any
import pygame
import sys
from actions import *
from rugbymen import *
from game import *

# Initialisation de Pygame
pygame.init()

clock = pygame.time.Clock()

#Chargement de l'image, chemin relatif
image_path = "Images/plateau.png"
image = pygame.image.load(image_path)
# Définition de la taille de la fenêtre
size = image.get_size()


##### TEST SPRITE #####
#A function that translates a path into a object of rugbyman
def path_to_player_type(path):
    if path.endswith("bleu.png"):
        color = "blue"
    elif path.endswith("rouge.png"):
        color = "red"
    if path == "Images/Costaud_bleu.png" or path == "Images/Costaud_rouge.png":
        return StrongRugbyman(color)
    elif path == "Images/Dur_bleu.png" or path == "Images/Dur_rouge.png":
        return HardRugbyman(color)
    elif path == "Images/Fute_bleu.png" or path == "Images/Fute_rouge.png":
        return SmartRugbyman(color)
    elif path == "Images/Rapide_bleu.png" or path == "Images/Rapide_rouge.png":
        return FastRugbyman(color)
    elif path == "Ordinaire_bleu.png" or path == "Ordinaire_rouge.png":
        return Rugbyman(color)
    
    
#A function that translates a type of player into a path
def player_type_to_path(player_type):
    if player_type.spec() == Spec.STRONG:
        if player_type.color() == "blue":
            return "Images/Costaud_bleu.png"
        elif player_type.color() == "red":
            return "Images/Costaud_rouge.png"
    elif player_type.spec() == Spec.SMART:
        if player_type.color() == "blue":
            return "Images/Intelligent_bleu.png"
        elif player_type.color() == "red":
            return "Images/Intelligent_rouge.png"
    elif player_type.spec() == Spec.FAST:
        if player_type.color() == "blue":
            return "Images/Rapide_bleu.png"
        elif player_type.color() == "red":
            return "Images/Rapide_rouge.png"
    elif player_type.spec() == Spec.HARD:
        if player_type.color() == "blue":
            return "Images/Dur_bleu.png"
        elif player_type.color() == "red": 
            return "Images/Dur_rouge.png"
    elif player_type.spec() == Spec.ORDINARY:
        if player_type.color() == "blue":
            return "Images/Ordinaire_bleu.png"
        elif player_type.color() == "red":
            return "Images/Ordinaire_rouge.png"


class PlayerTokens(pygame.sprite.Sprite):
    def __init__(self, picture_path, scale_x=46.8, scale_y=46.5):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
        self.rect = self.image.get_rect()
        self.player_type = path_to_player_type(picture_path)
    def update(self, tokens_group):
        screen.blit(image, (0, 0))
        self.rect.center = pygame.mouse.get_pos()
        tokens_group.draw(screen)
        pygame.display.flip()
        # For now, the sprites in tokens_group just follow the mouse (could eventually be used to make Tokens follow the mouse while moving them)
    def get_hitbox(self):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(self.rect.center):
                if i<88:
                    return [i,(i%11, i//11)]
                else:
                    return [i]
    def select(self, tokens_group, game):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #list_move = actions.available_forward_pass(self.get_hitbox[1](0),self.get_hitbox[1](1),self.player_type.moove_points,game) #moves_left
            while True:
                self.update(tokens_group)
                #self.highlight_move(list_move)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.update(tokens_group)
                        for box in hitbox:
                            if box.collidepoint(pygame.mouse.get_pos()):
                                self.rect.center = box.center
                        return
                    
              

##### #####

# Création de la fenêtre
screen = pygame.display.set_mode(size)
#surf = pygame.surface.Surface(size)

print(type(screen))
#Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

image_costaud_rouge = pygame.image.load("Images/Costaud_bleu.png")
screen.blit(image_costaud_rouge, (10, 10))
#surf.blit(image_costaud_rouge, (10, 10))

# Dessiner un point rouge
# pygame.draw.circle(screen, (255, 0, 0), (92,62), 2)

# Dessiner un point bleu
# pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)


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

    # Displays the number on the screen of the hitbox when you click on it
    def display_number(self):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i < 88:
                    print(i % 11, i // 11)
                else:
                    print(i)
            else:
                pass

    def get_hitbox(self):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i<88:
                    return [i,(i%11, i//11)]
                else:
                    return [i,i]
            else:
                return None

    # Affiche un point rouge pour 5s quand on clique quelque part
    def display_point(self):
        pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
        pygame.display.flip()
        pygame.time.wait(500)
        self.screen.blit(self.plateau, (0, 0))
        pygame.display.flip()

    # Affiche un joueur au centre de la hitbox
    def affiche_joueur(self, n_hit, path):
        joueur = pygame.image.load(path)
        joueur = pygame.transform.scale(joueur, (46.8, 46.5))
        self.screen.blit(joueur, coords[n_hit])
        pygame.display.flip()

    #Met en surbrillance les cases où le joueur peut se déplacer
    def highlight_move(self, list_move):
        for i in range(len(list_move)):
            pygame.draw.circle(self.screen, (20, 255, 167), (coords[list_move[i]][0]+46.8/2,coords[list_move[i]][1]+46.5/2),10)
        pygame.display.flip()

    def create_dropdown_menu(self, options, menu_pos, menu_size):
        self.menu_options = options
        self.menu_rect = pygame.Rect(menu_pos, menu_size)
        self.menu_open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos):
                self.menu_open = not self.menu_open
            elif self.menu_open:
                for i, option in enumerate(self.menu_options):
                    if pygame.Rect(self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height, self.menu_rect.width, self.menu_rect.height).collidepoint(event.pos):
                        print(f"You clicked {option}")
                        self.menu_open = False

    def draw_menu(self):
        if self.menu_open:
            for i, option in enumerate(self.menu_options):
                pygame.draw.rect(self.screen, (255, 255, 255), (self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height, self.menu_rect.width, self.menu_rect.height))
                self.screen.blit(pygame.font.Font(None, 32).render(option, True, (0, 0, 0)), (self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height))

    # Rafraîchissement de la fenêtre
    def refresh(self):
        pygame.display.flip()

    # Boucle principale
    def main_loop(self, Game):
        # Players tokens sprites initialisation
        playertoken1 = PlayerTokens("Images/Costaud_bleu.png")
        playertoken2 = PlayerTokens("Images/Costaud_rouge.png")
        tokens_group = pygame.sprite.Group()
        tokens_group.add(playertoken1)
        tokens_group.add(playertoken2)
        i=0
        for tokens in tokens_group:
            tokens.rect.center = hitbox[i].center
            i+=1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_number()
                    self.display_point()
                    for token in tokens_group:
                        token.select(tokens_group, Game)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            screen.blit(image, (0, 0))
            tokens_group.draw(screen) 
            clock.tick(60)

if __name__ == "__main__":
    graph = Graphique()
    graph.main_loop(Game)