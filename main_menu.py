
import sys
from main_menu_button import Button
import pygame 

class MainMenu:
    def __init__(self,game,graphic) :
        self.game = game
        self.graphic = graphic

        self.BG = pygame.image.load("assets/Background.png")
        self.screen = graphic.screen
        pygame.display.set_caption("Menu")

        self.center_center_pos = (self.BG.get_size()[0]/2,self.BG.get_size()[1]/2-30)
        self.center_down_pos = (self.BG.get_size()[0]/2,self.BG.get_size()[1]/10*9)
        self.left_center_pos = (self.BG.get_size()[0]/4+50,self.BG.get_size()[1]/2)
        self.right_center_pos = (self.BG.get_size()[0]/4*3,self.BG.get_size()[1]/2-20)
        self.right_center_upper_pos = (self.BG.get_size()[0]/4*3,self.BG.get_size()[1]/4*1)
        self.right_center_lower_pos = (self.BG.get_size()[0]/4*3,self.BG.get_size()[1]/4*2.5)
        self.center_up_pos = (self.BG.get_size()[0]/2,self.BG.get_size()[1]/10*2)


    def get_font(self,size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def play(self):
        while True:
            upper_left = (self.center_center_pos[0]-150, self.center_center_pos[1]-100)
            lower_right = (self.center_center_pos[0]+150, self.center_center_pos[1]+100)
            upper_right = (self.center_center_pos[0]+150, self.center_center_pos[1]-100)
            lower_left = (self.center_center_pos[0]-150, self.center_center_pos[1]+100)
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            PLAY_1 = Button(image=None, pos=upper_left,
                                text_input="NO AI", font=self.get_font(50), base_color="Black", hovering_color="Green")
            PLAY_1.changeColor(OPTIONS_MOUSE_POS)

            PLAY_2 = Button(image=None, pos=upper_right, 
                                text_input="AI DETERMINISTIC", font=self.get_font(50), base_color="Black", hovering_color="Green")
            PLAY_2.changeColor(OPTIONS_MOUSE_POS)

            PLAY_3 = Button(image=None, pos=lower_left, 
                                text_input="AI MINMAX", font=self.get_font(50), base_color="Black", hovering_color="Green")
            PLAY_3.changeColor(OPTIONS_MOUSE_POS)

            PLAY_4 = Button(image=None, pos=lower_right, 
                                text_input="AI Q-LEARNING", font=self.get_font(50), base_color="Black", hovering_color="Green")
            PLAY_4.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(self.screen)
            PLAY_1.update(self.screen)
            PLAY_2.update(self.screen)
            PLAY_3.update(self.screen)
            PLAY_4.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if PLAY_1.checkForInput(OPTIONS_MOUSE_POS):
                        return True #NO AI
                    if PLAY_2.checkForInput(OPTIONS_MOUSE_POS):
                        return True #AI DETERMINISTIC
                    if PLAY_3.checkForInput(OPTIONS_MOUSE_POS):
                        return True    #AI MINMAX
                    if PLAY_4.checkForInput(OPTIONS_MOUSE_POS):
                        return True #AI Q-LEARNING

            pygame.display.update()
    
    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="1 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)
            

            OPTIONS_TEXT_1 = pygame.image.load("assets/regle.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=self.center_center_pos)
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)


            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                       self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_7()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_2()

            pygame.display.update()

    def options_2(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="2 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_TEXT_1 = pygame.image.load("assets/deplacer_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = pygame.image.load("assets/deplacer_2.png")
            OPTIONS_TEXT_2 = pygame.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
            
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=self.right_center_upper_pos)
            
            self.screen.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

            OPTIONS_TEXT_3 = pygame.image.load("assets/deplacer_3.png")
            OPTIONS_TEXT_3 = pygame.transform.scale(OPTIONS_TEXT_3, (OPTIONS_TEXT_3.get_size()[0]/2,OPTIONS_TEXT_3.get_size()[1]/2))
            
            OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=self.right_center_lower_pos)
            
            self.screen.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_3()

            pygame.display.update()

    def options_3(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="3 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_TEXT_1 = pygame.image.load("assets/forcer_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = pygame.image.load("assets/forcer_2.png")
            OPTIONS_TEXT_2 = pygame.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
            
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=self.right_center_pos)
            
            self.screen.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_2()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_4()

            pygame.display.update()

    def options_4(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            
            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="4 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_TEXT_1 = pygame.image.load("assets/passer_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = pygame.image.load("assets/passer_2.png")
            OPTIONS_TEXT_2 = pygame.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
            
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=self.right_center_pos)

            self.screen.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)


            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_3()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_5()

            pygame.display.update()

    def options_5(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            OPTIONS_TEXT_1 = pygame.image.load("assets/interseption_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=self.center_center_pos)
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="5 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_4()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_6()

            pygame.display.update()

    def options_6(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="6 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_TEXT_1 = pygame.image.load("assets/plaquer_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = pygame.image.load("assets/plaquer_2.png")
            OPTIONS_TEXT_2 = pygame.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
            
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=self.right_center_upper_pos)
            
            self.screen.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

            OPTIONS_TEXT_3 = pygame.image.load("assets/plaquer_3.png")
            OPTIONS_TEXT_3 = pygame.transform.scale(OPTIONS_TEXT_3, (OPTIONS_TEXT_3.get_size()[0]/2,OPTIONS_TEXT_3.get_size()[1]/2))
            
            OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=self.right_center_lower_pos)
            
            self.screen.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_5()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_7()

            pygame.display.update()

    def options_7(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))

            page = Button(image=None, pos=(self.center_down_pos[0],self.center_down_pos[1]+30), 
                                text_input="7 of 7", font=self.get_font(30), base_color="Black", hovering_color="Black")
            
            page.update(self.screen)

            OPTIONS_TEXT_1 = pygame.image.load("assets/pied_1.png")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(self.left_center_pos[0],self.left_center_pos[1]-30))
            
            self.screen.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = pygame.image.load("assets/pied_2.png")
            OPTIONS_TEXT_2 = pygame.transform.scale(OPTIONS_TEXT_2, (OPTIONS_TEXT_2.get_size()[0]/2,OPTIONS_TEXT_2.get_size()[1]/2))
            
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=self.right_center_pos)
            
            self.screen.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

            OPTIONS_BACK = Button(image=None, pos=self.center_down_pos, 
                                text_input="BACK", font=self.get_font(50), base_color="Black", hovering_color="Green")
            left_arrow = pygame.image.load("assets/arrow_left.png")
            left_arrow = pygame.transform.scale(left_arrow, (left_arrow.get_size()[0]/10,left_arrow.get_size()[1]/10))
            OPTIONS_LEFT = Button(image=left_arrow, pos=(self.center_down_pos[0]-100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            right_arrow = pygame.image.load("assets/arrow_right.png")
            right_arrow = pygame.transform.scale(right_arrow, (right_arrow.get_size()[0]/10, right_arrow.get_size()[1]/10))
            OPTIONS_RIGHT = Button(image=right_arrow, pos=(self.center_down_pos[0]+100, self.center_down_pos[1] - 7),text_input="", font=self.get_font(50), base_color="Black", hovering_color="Green") 
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            OPTIONS_LEFT.update(self.screen)
            OPTIONS_RIGHT.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options_6()
                    if OPTIONS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                        self.options()

            pygame.display.update()

    def main_menu(self):
        while True:
            self.screen.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = pygame.image.load("assets/logo.png") #get_font(100).render("KAHMATE", True, "#000000")
            MENU_TEXT = pygame.transform.scale(MENU_TEXT, (MENU_TEXT.get_size()[0]/2,MENU_TEXT.get_size()[1]/2))
            
            MENU_RECT = MENU_TEXT.get_rect(center=(self.BG.get_size()[0]/2, self.BG.get_size()[1]/8*1))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(self.BG.get_size()[0]/2, self.BG.get_size()[1]/8*3), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(self.BG.get_size()[0]/2, self.BG.get_size()[1]/8*5), 
                                text_input="RULES", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(self.BG.get_size()[0]/2, self.BG.get_size()[1]/8*7), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return self.play()
                        #main2() #### AATTTENTION##
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    