
import actions
import rugbymen 
from game import *
import pygame
from typing import Any

image_path = "Images/plateau.png"
image = pygame.image.load(image_path)

#A function that translates a path into a object of rugbyman
def path_to_player_type(path):
    if path.endswith("bleu.png"):
        color = "blue"
    elif path.endswith("rouge.png"):
        color = "red"
    if path == "Images/Costaud_bleu.png" or path == "Images/Costaud_rouge.png":
        return rugbymen.StrongRugbyman(color)
    elif path == "Images/Dur_bleu.png" or path == "Images/Dur_rouge.png":
        return rugbymen.HardRugbyman(color)
    elif path == "Images/Fute_bleu.png" or path == "Images/Fute_rouge.png":
        return rugbymen.SmartRugbyman(color)
    elif path == "Images/Rapide_bleu.png" or path == "Images/Rapide_rouge.png":
        return rugbymen.FastRugbyman(color)
    elif path == "Images/Ordinaire_bleu.png" or path == "Images/Ordinaire_rouge.png":
        return rugbymen.Rugbyman(color)
    
    
#A function that translates a type of player into a path
def player_type_to_path(player_type):
    if player_type.spec() == rugbymen.Spec.STRONG:
        if player_type.color() == "blue":
            return "Images/Costaud_bleu.png"
        elif player_type.color() == "red":
            return "Images/Costaud_rouge.png"
    elif player_type.spec() == rugbymen.Spec.SMART:
        if player_type.color() == "blue":
            return "Images/Intelligent_bleu.png"
        elif player_type.color() == "red":
            return "Images/Intelligent_rouge.png"
    elif player_type.spec() == rugbymen.Spec.FAST:
        if player_type.color() == "blue":
            return "Images/Rapide_bleu.png"
        elif player_type.color() == "red":
            return "Images/Rapide_rouge.png"
    elif player_type.spec() == rugbymen.Spec.HARD:
        if player_type.color() == "blue":
            return "Images/Dur_bleu.png"
        elif player_type.color() == "red":
            return "Images/Dur_rouge.png"
    elif player_type.spec() == rugbymen.Spec.NORMAL:
        if player_type.color() == "blue":
            return "Images/Ordinaire_bleu.png"
        elif player_type.color() == "red":
            return "Images/Ordinaire_rouge.png"
        
class RugbymanToken(pygame.sprite.Sprite):
    # Class of the rugbymen tokens

    def __init__(self, picture_path, scale_x=46.8, scale_y=46.5):
        ### RugbymanToken attributes ###
        #  image : surface of the token sprite (see pygame.sprite.Sprite)
        #  rect : hitbox and position of the token sprite (see pygame.sprite.Sprite)
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
        self.rect = self.image.get_rect()
        self.player_type = path_to_player_type(picture_path)

    def move(self, new_pos):
        self.rect.center = new_pos

    def follow_cursor(self, tokens_group, background_image, screen):
        # Make the token follow the cursor
        # tokens_group must contains all sprites that should be drawn
        screen.blit(background_image, (0, 0))
        self.rect.center = pygame.mouse.get_pos()
        tokens_group.draw(screen)
        pygame.display.flip()
        # For now, the sprites in tokens_group just follow the mouse (could eventually be used to make Tokens follow the mouse while moving them)
    def get_hitbox(self, hitbox):  # Can you explain this ? Wouldn't it be simpler just adding a self.hitbox attribut to any token ? (I'm really not sure)
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(self.rect.center):
                if i < 88:
                    return [i, (i % 11, i // 11)]
                else:
                    return [i]
    def select(self, tokens_group, background_image, game, graphique, hitbox):
        print("Début")
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            list_move = actions.available_move_positions(
                self.get_hitbox(hitbox)[1][0],
                self.get_hitbox(hitbox)[1][1],
                game,
                self.player_type.moves
            )  # moves_left
            while True:
                graphique.highlight_move(list_move)
                self.follow_cursor(tokens_group, background_image, graphique.screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.follow_cursor(tokens_group, background_image, graphique.screen)
                        for box in hitbox:
                            if box.collidepoint(pygame.mouse.get_pos()) and actions.hitbox_to_coord(hitbox.index(box)) in list_move:
                                self.rect.center = box.center
                                print(False)
                                return False
        else:
            return True