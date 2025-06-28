import pygame

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
        if not self.arena:
            self.world_choices.gaming_scene()

        else:
            self.arena_load_in()
            self.zombie.spawn_zombie()

        sprite_x, sprite_y = self.sprite.sprite_coords()
        if self.gaming_time:
            self.crossroads_fade()
            self.gaming_time = False

        if event.type == pygame.KEYDOWN:
            if self.in_menu is False and not self.arena:
                if sprite_y > 0:
                    self.resume_pop_up = False
                if sprite_x > 930:
                    if not self.arena:
                        self.arena = True
                    self.sprite._x = 0
                if sprite_x < -2:
                    if not self.arena:
                        self.in_menu = True
                        main_menu.menu_load_up()
                    else:
                        self.sprite._x = 900
                if sprite_y > 930:

                    self.resume_pop_up = False
                    self.portfolio()
                    self.sprite._y = -25
                if 0 > sprite_y:
                    if not self.arena:
                        self.resume_pop_up = True
                    if sprite_y < -30:
                        self.sprite._y = 931

                if event.key == pygame.K_ESCAPE:
                    self.in_menu = True
                elif event.key == pygame.K_UP:
                    self.sprite.going_up()
                    self.sprite._y -= 15
                elif event.key == pygame.K_DOWN:
                    self.sprite.going_down()
                    self.sprite._y += 15
                elif event.key == pygame.K_LEFT:
                    self.sprite.going_left()
                    self.sprite._x -= 15
                elif event.key == pygame.K_RIGHT:
                    self.sprite.going_right()
                    self.sprite._x += 15
            elif self.arena:
                if event.key == pygame.K_ESCAPE:
                    self.in_menu = True
                elif event.key == pygame.K_UP:
                    self.sprite.going_up()
                    if self.sprite._y > 110:
                        self.sprite._y -= 15
                elif event.key == pygame.K_DOWN:
                    self.sprite.going_down()
                    if self.sprite._y < 800:
                        self.sprite._y += 15
                elif event.key == pygame.K_LEFT:
                    self.sprite.going_left()
                    if self.sprite._x > 105:
                        self.sprite._x -= 15
                elif event.key == pygame.K_RIGHT:
                    self.sprite.going_right()
                    if self.sprite._x < 800:
                        self.sprite._x += 15

        self.sprite.sprite_movement()
        # if self.arena:
        #     self.zombie.spawn_zombie()
    """The main loop of the game, receives input, updates the main game window every 60 frames"""
    def main(self):
        play = None
        quit_button = None

        pygame.time.set_timer(self.zombie.spawn_event, self.zombie.spawn_timer)


        main_menu = MainMenu(self.game_screen)
        main_menu.menu_load_up()
        running = True

        pygame.key.set_repeat(75, 100)
        while running:
            mouse_pos = pygame.mouse.get_pos()
            if self.in_menu:
                play, quit_button = main_menu.menu_options(mouse_pos)
            elif not self.in_menu:
                if self.resume_pop_up:
                    self.resume_scroll()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play is not None and quit_button is not None:
                        if play.button_clicked(mouse_pos):
                            self.crossroads_fade()
                            self.world_choices.gaming_scene()
                            self.in_menu = False
                            self.gaming_time = False
                        if quit_button.button_clicked(mouse_pos):
                            pygame.quit()
                            quit()
                elif event.type == pygame.KEYDOWN and not self.in_menu:
                    self.game_movement(main_menu, event)
                if event.type == self.zombie.spawn_event and self.arena:
                    self.zombie.spawn_zombie()
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

