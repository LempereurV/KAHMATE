### Class used for the main menu, from which the game is launched ###

import sys
from main_menu_button import Button
import pygame 
import game
import actions 
from color import Color
import minimax
import front 
class MainMenu:
    def __init__(self,graphic) :
        self.graphic = graphic

        width = graphic.board.get_width()
        height = graphic.board.get_height()

        self.background = pygame.image.load("assets/Background.png")
        self.background = pygame.transform.scale(self.background, (width, height))
        self.screen = graphic.screen
        pygame.display.set_caption("Menu")

        # Used to position the buttons and images
        self.center_center_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/2-30)
        self.center_down_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/10*9)
        self.left_center_pos = (self.background.get_size()[0]/4+50,self.background.get_size()[1]/2)
        self.right_center_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/2-20)
        self.right_center_upper_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/4*1)
        self.right_center_lower_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/4*2.5)
        self.center_up_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/10*2)


    def get_font(self,size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def resize_BG_and_buttons(self,event): # Resize the background and the buttons when the window is resized
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            self.background = pygame.transform.scale(self.background, size)

            self.center_center_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/2-30)
            self.center_down_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/10*9)
            self.left_center_pos = (self.background.get_size()[0]/4+50,self.background.get_size()[1]/2)
            self.right_center_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/2-20)
            self.right_center_upper_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/4*1)
            self.right_center_lower_pos = (self.background.get_size()[0]/4*3,self.background.get_size()[1]/4*2.5)
            self.center_up_pos = (self.background.get_size()[0]/2,self.background.get_size()[1]/10*2)

        
    def play(self): # Display the gamemode selection menu
        while True:
            # Used to position the buttons
            upper_left = (self.center_center_pos[0]-150, self.center_center_pos[1]-100)
            lower_right = (self.center_center_pos[0]+150, self.center_center_pos[1]+100)
            upper_right = (self.center_center_pos[0]+150, self.center_center_pos[1]-100)
            lower_left = (self.center_center_pos[0]-150, self.center_center_pos[1]+100)

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            # Create the buttons for the different gamemodes and the back button
            play_no_ai = Button(image=None, pos=upper_left,
                                text_input="NO AI", font=self.get_font(50), base_color="Black", hovering_color="Green")
            play_no_ai.changeColor(mouse_pos)

            play_ai_deterministic = Button(image=None, pos=upper_right, 
                                text_input="AI DETERMINISTIC", font=self.get_font(50), base_color="Black", hovering_color="Green")
            play_ai_deterministic.changeColor(mouse_pos)

            play_ai_minmax = Button(image=None, pos=lower_left, 
                                text_input="AI MINMAX", font=self.get_font(50), base_color="Black", hovering_color="Green")
            play_ai_minmax.changeColor(mouse_pos)

            play_ai_Q_learning = Button(image=None, pos=lower_right, 
                                text_input="AI Q-LEARNING", font=self.get_font(50), base_color="Black", hovering_color="Green")
            play_ai_Q_learning.changeColor(mouse_pos)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            go_back.changeColor(mouse_pos)

            go_back.update(self.screen)
            play_no_ai.update(self.screen)
            play_ai_deterministic.update(self.screen)
            play_ai_minmax.update(self.screen)
            play_ai_Q_learning.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if play_no_ai.checkForInput(mouse_pos):
                        self.launch_game()
                    if play_ai_deterministic.checkForInput(mouse_pos):
                        #AI DETERMINISTIC
                        True
                    if play_ai_minmax.checkForInput(mouse_pos):
                        #AI MINMAX
                        True
                    if play_ai_Q_learning.checkForInput(mouse_pos):
                        #AI Q-LEARNING
                        True

            pygame.display.update()
    
    def rules_1(self):  # Display the first page of rules
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            # Diplays the page number
            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="1 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)
            

            image_1 = pygame.image.load("assets/regle.png")
            rect_1 = image_1.get_rect(center=self.center_center_pos)
            
            self.screen.blit(image_1, rect_1)

            # create the buttons for the arrows and the back button
            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                       self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_7()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_2()

            pygame.display.update()

    def rules_2(self): # Display the second page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="2 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            image_1 = pygame.image.load("assets/deplacer_1.png")
            rect_1 = image_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(image_1, rect_1)

            image_2 = pygame.image.load("assets/deplacer_2.png")
            image_2 = pygame.transform.scale(image_2, (image_2.get_size()[0]/2,image_2.get_size()[1]/2))
            
            rect_2 = image_2.get_rect(center=self.right_center_upper_pos)
            
            self.screen.blit(image_2, rect_2)

            image_3 = pygame.image.load("assets/deplacer_3.png")
            image_3 = pygame.transform.scale(image_3, (image_3.get_size()[0]/2,image_3.get_size()[1]/2))
            
            rect_3 = image_3.get_rect(center=self.right_center_lower_pos)
            
            self.screen.blit(image_3, rect_3)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_1()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_3()

            pygame.display.update()

    def rules_3(self): # Display the third page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="3 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            image_1 = pygame.image.load("assets/forcer_1.png")
            rect_1 = image_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(image_1, rect_1)

            image_2 = pygame.image.load("assets/forcer_2.png")
            image_2 = pygame.transform.scale(image_2, (image_2.get_size()[0]/2,image_2.get_size()[1]/2))
            
            rect_2 = image_2.get_rect(center=self.right_center_pos)
            
            self.screen.blit(image_2, rect_2)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_2()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_4()

            pygame.display.update()

    def rules_4(self): # Display the fourth page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))
            
            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="4 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            image_1 = pygame.image.load("assets/passer_1.png")
            rect_1 = image_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(image_1, rect_1)

            image_2 = pygame.image.load("assets/passer_2.png")
            image_2 = pygame.transform.scale(image_2, (image_2.get_size()[0]/2,image_2.get_size()[1]/2))
            
            rect_2 = image_2.get_rect(center=self.right_center_pos)

            self.screen.blit(image_2, rect_2)


            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_3()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_5()

            pygame.display.update()

    def rules_5(self): # Display the fifth page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            image_1 = pygame.image.load("assets/interseption_1.png")
            rect_1 = image_1.get_rect(center=self.center_center_pos)
            self.screen.blit(image_1, rect_1)

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="5 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_4()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_6()

            pygame.display.update()

    def rules_6(self): # Display the sixth page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="6 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            image_1 = pygame.image.load("assets/plaquer_1.png")
            rect_1 = image_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(image_1, rect_1)

            image_2 = pygame.image.load("assets/plaquer_2.png")
            image_2 = pygame.transform.scale(image_2, (image_2.get_size()[0]/2,image_2.get_size()[1]/2))
            
            rect_2 = image_2.get_rect(center=self.right_center_upper_pos)
            
            self.screen.blit(image_2, rect_2)

            image_3 = pygame.image.load("assets/plaquer_3.png")
            image_3 = pygame.transform.scale(image_3, (image_3.get_size()[0]/2,image_3.get_size()[1]/2))
            
            rect_3 = image_3.get_rect(center=self.right_center_lower_pos)
            
            self.screen.blit(image_3, rect_3)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_5()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_7()

            pygame.display.update()

    def rules_7(self): # Display the seventh page of rules
        # for more information about the rules, see the rules_1 function
        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="7 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            image_1 = pygame.image.load("assets/pied_1.png")
            rect_1 = image_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(image_1, rect_1)

            image_2 = pygame.image.load("assets/pied_2.png")
            image_2 = pygame.transform.scale(image_2, (image_2.get_size()[0]/2,image_2.get_size()[1]/2))
            
            rect_2 = image_2.get_rect(center=self.right_center_pos)
            
            self.screen.blit(image_2, rect_2)

            go_back = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            arrow_left = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            arrow_right = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            go_back.changeColor(mouse_pos)
            go_back.update(self.screen)
            arrow_left.update(self.screen)
            arrow_right.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back.checkForInput(mouse_pos):
                        self.main_menu()
                    if arrow_left.checkForInput(mouse_pos):
                        self.rules_6()
                    if arrow_right.checkForInput(mouse_pos):
                        self.rules_1()

            pygame.display.update()

    def main_menu(self): # Display the main menu
        while True:
            self.screen.blit(self.background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            logo_image = pygame.image.load("assets/logo.png") #get_font(100).render("KAHMATE", True, "#000000")
            logo_image = pygame.transform.scale(logo_image, (logo_image.get_size()[0]/2,logo_image.get_size()[1]/2))
            
            logo_rect = logo_image.get_rect(center=(self.background.get_size()[0]/2, self.background.get_size()[1]/8*1))

            play_button = Button(image=pygame.image.load("assets/rect.png"), pos=(self.background.get_size()[0]/2, self.background.get_size()[1]/8*3), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            rules_button = Button(image=pygame.image.load("assets/rect.png"), pos=(self.background.get_size()[0]/2, self.background.get_size()[1]/8*5), 
                                text_input="RULES", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load("assets/rect.png"), pos=(self.background.get_size()[0]/2, self.background.get_size()[1]/8*7), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(logo_image, logo_rect)
            for button in [play_button, rules_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize_BG_and_buttons(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.play()
                    if rules_button.checkForInput(mouse_pos):
                        self.rules_1()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def launch_game(self): # Launch the game
        kahmate_graphics = self.graphic
        kahmate_graphics.set_new_hitbox()

        kahmate_game=game.Game(kahmate_graphics)
        kahmate_actions=actions.Action(kahmate_game,kahmate_graphics)
        kahmate_minimax_actions=actions.ActionMiniMax(kahmate_game,kahmate_graphics)
        kahmate_minimax=minimax.Minimax(kahmate_game,kahmate_game.get_player_red(),
                                        kahmate_actions,kahmate_minimax_actions,kahmate_graphics)
        AI=False    

        while not kahmate_game.is_game_over():

            active_player = kahmate_game.get_player_turn()

            print("Tour du joueur "+str(active_player.get_color()))
            if AI and active_player.get_color()==Color.RED:
                    ### Partie IA####
                    print("IA")
                    moves=[None,None,None]
                
                        
                    kahmate_minimax.minimax(kahmate_minimax.get_depth(),-float("inf"),float("inf"),moves)
                

                    kahmate_graphics.draw_board(kahmate_game)
                    
                    if moves[2]!=None:
                        kahmate_game.get_ball().set_pos(moves[2])
                    
                    for move in moves[:2]:
                        if move!=False:
                            kahmate_actions.move_rugbyman([move[1],move[2]],move[0],move[3])
                    kahmate_graphics.draw_board(kahmate_game)
                    active_player.set_can_play(False)
                    kahmate_game.refresh_players_rugbymen_stats()
                    kahmate_game.change_player_turn()
                    continue




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

    