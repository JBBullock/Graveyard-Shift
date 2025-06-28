import pygame

from GUI.Game_scene_sprite import TankSprite
from main_menu import MainMenu
import webbrowser
from Game_scene_sprite import *
# s
"""holds the main loop that updates the pygame window, buttons, main menu, etc."""
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

    def portfolio(self):
        webbrowser.open("https://johnatonbullock1.wixsite.com/johnatonbullock")

    def crossroads_init(self):
        world_choices = GameScreen(self.game_screen)

        return world_choices

    def crossroads_fade(self):
        self.world_choices.gaming_fade_in()


    def arena_load_in(self):
        self.world_choices.game_arena()

    def game_loop(self, main_menu, event):
        if not self.arena:
            self.world_choices.gaming_scene()

        else:
            self.arena_load_in()
        sprite_x, sprite_y = self.sprite.sprite_coords()
        if self.gaming_time:
            self.crossroads_fade()
            self.gaming_time = False

        if event.type == pygame.KEYDOWN:
            if self.in_menu is False:
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
                    if not self.arena:
                        self.resume_pop_up = False
                        self.portfolio()
                    self.sprite._y = -25
                if 0 > sprite_y:
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
        self.sprite.sprite_movement()

    def main_screen(self):
        play = None
        quit_button = None


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
                    self.game_loop(main_menu, event)
            pygame.display.update()
            relo.tick(60)
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
# def new_surface():
#     some_canvas = pygame.Surface((900, 900))
#     some_canvas.fill("Yellow")
#     return some_canvas



if __name__ == '__main__':
    pygame.init()
    relo = pygame.time.Clock()
    screen = pygame.display.set_mode((900, 900))
    ignition_key = PyGameGUI(screen)
    ignition_key.main_screen()


"""Operation: Graveyard Shift tank vs zombie game, forest setting, each zombie has info about me, after all the info, user can keep playing"""