import pygame
from Buttons import Button
from GUI.Game_scene_sprite import *
from main_menu import MainMenu
import webbrowser
from Game_scene_sprite import *

"""Housing the main game loop, updates the general game window"""
class PyGameGUI:
    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.arena = False
        self.resume_pop_up = False
        self.start_game = False
        self.gaming_time = False
        self.in_menu = True
        self.world_choices = self.crossroads_init()
        self.sprite = TankSprite(self.game_screen)
        self.zombie = ZombieSprite(self.game_screen)
        self.game_view = "MENU"
        self.main_menu = MainMenu(self.game_screen)

    """Takes user to web portfolio"""
    def portfolio(self):
        webbrowser.open("https://johnatonbullock1.wixsite.com/johnatonbullock")

    """Creates the object for different game states"""
    def crossroads_init(self):
        world_choices = GameScreen(self.game_screen)

        return world_choices
    """Fades out whichever state the user is in """
    def crossroads_fade(self):
        self.world_choices.gaming_fade_in()

    """The main game arena, e.g. level 1"""
    def arena_load_in(self):
        self.world_choices.game_arena()
    """Updates the position of the tank, based on user input passed from main()"""
    def game_movement(self, main_menu, event):
        # if not self.arena:
        #     self.world_choices.gaming_scene()
        #
        # if self.gaming_time:
        #     self.crossroads_fade()
        #     self.gaming_time = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.in_menu = True
            elif event.key == pygame.K_UP:
                self.sprite.up = True
            elif event.key == pygame.K_DOWN:
                self.sprite.down = True
            elif event.key == pygame.K_LEFT:
                self.sprite.left = True
            elif event.key == pygame.K_RIGHT:
                self.sprite.right = True

    # def setup_menu_buttons(self):
    #     font = pygame.font.Font('Fonts/KiwiSoda.ttf', 50)
    #     play_button = Button((400, 300), "Play", font, (255, 255, 255), (0, 255, 0))
    #     quit_button = Button((400, 400), "Quit", font, (255, 255, 255), (255, 0, 0))
    #     return play_button, quit_button

    """The main loop of the game, receives input, updates the main game window every 60 frames"""
    def main(self):

        """ FIX BUTTONS"""
        pygame.time.set_timer(self.zombie.spawn_event, self.zombie.spawn_timer)


        # main_menu.menu_load_up()
        running = True
        play, quit_button =  None, None

        pygame.key.set_repeat(75, 100)
        while running:
            mouse_pos = pygame.mouse.get_pos()
            if self.in_menu:
                play, quit_button = self.main_menu.menu_options(mouse_pos)
                self.main_menu.menu_load_up()
                play, quit_button = self.main_menu.menu_options(mouse_pos)
            if not self.in_menu:
                if self.resume_pop_up:
                    self.resume_scroll()



            for event in pygame.event.get():
                # play, quit_button = main_menu.menu_options(mouse_pos)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # if self.game_view == "MENU":

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.in_menu:
                        if play is not None and quit_button is not None:
                            print(play.button_clicked(mouse_pos))
                            print(quit_button.button_clicked(mouse_pos))

                            if play.button_clicked(mouse_pos):
                                # self.game_view = "GAME"
                                self.in_menu = False
                                self.gaming_time = True

                            if quit_button.button_clicked(mouse_pos):
                                pygame.quit()
                                quit()
                # elif self.game_view == "GAME":
                if event.type == pygame.KEYDOWN:
                    self.game_movement(self.main_menu, event)


            if not self.arena and not self.in_menu:

                if self.sprite.x > 930:
                    self.arena = True
                    self.sprite.x = 0
                elif self.sprite.x < -2:
                    self.in_menu = True
                    self.game_view = "MENU"
                    self.main_menu = MainMenu(self.game_screen)
                    # main_menu.menu_load_up()


                if 0 < self.sprite.y < 800:
                    self.resume_pop_up = False

                if self.sprite.y > 930:
                    self.resume_pop_up = False
                    self.portfolio()
                    self.sprite.y = -25
                elif 0 > self.sprite.y:
                    self.resume_pop_up = True
                    if self.sprite.y < -30:
                        self.sprite.y = 925
                if self.sprite.up:
                    self.sprite.going_up()
                elif self.sprite.down:
                    self.sprite.going_down()
                elif self.sprite.left:
                    self.sprite.going_left()
                elif self.sprite.right:
                    self.sprite.going_right()

            if self.arena and not self.in_menu:

                if self.sprite.up:
                    if self.sprite.y > 110:
                        self.sprite.going_up()
                elif self.sprite.down:

                    if self.sprite.y < 800:
                        self.sprite.going_down()
                elif self.sprite.left:
                    if self.sprite.x > 90:
                        self.sprite.going_left()
                elif self.sprite.right:
                    if self.sprite.x < 800:
                        self.sprite.going_right()
            # if self.in_menu and not self.gaming_time:
            #
            #     self.world_choices.gaming_scene()
            if self.game_view == "GAME":
                self.world_choices.gaming_scene()
                self.sprite.sprite_movement()
            if self.arena and not self.in_menu:
                self.arena_load_in()
                self.sprite.sprite_movement()
            pygame.display.update()
            relo.tick(60)

    """Displays my resume in a form scroll with pixel font"""
    def resume_scroll(self):
        text_list = list()

        GUI_text = list()
        text_rects = list()
        text_y_value = 125
        with open('Images/Johnaton Bullock Resume.txt') as file:
            f_contents = file.readlines()
            for line in f_contents:
                text_list.append(line.strip('\n'))

        resume_text_font = pygame.font.Font("Fonts/Purl.ttf", 18)
        for text in text_list:
            resume_text = resume_text_font.render(text, True, "Black")
            text_rect = resume_text.get_rect(midtop=(450, text_y_value))
            GUI_text.append(resume_text)
            text_rects.append(text_rect)
            text_y_value += 13


        scroll_image = pygame.image.load('Images/scroll_pixel.png').convert_alpha()
        pygame.transform.scale(scroll_image, (100, 100))
        scroll_rect = scroll_image.get_rect(midtop = (450, 0))
        self.game_screen.blit(scroll_image, scroll_rect)
        for text, rect in zip(GUI_text, text_rects):
            self.game_screen.blit(text, rect)



"""Starts the program"""
if __name__ == '__main__':
    pygame.init()
    relo = pygame.time.Clock()
    screen = pygame.display.set_mode((900, 900))
    ignition_key = PyGameGUI(screen)
    ignition_key.main()

