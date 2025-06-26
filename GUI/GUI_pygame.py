import pygame
from main_menu import MainMenu
import webbrowser
from Game_scene_sprite import *
"""holds the main loop that updates the pygame window, buttons, main menu, etc."""
class PyGameGUI:
    def __init__(self, game_screen):
        self.game_screen = game_screen

    def resume_scroll(self):
        text_list = list()

        GUI_text = list()
        text_rects = list()
        text_y_value = 125
        with open('Images/Johnaton Bullock Resume.txt') as file:
            f_contents = file.readlines()
            for line in f_contents:
                text_list.append(line.strip())

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

    def portfolio(self):
        webbrowser.open("https://johnatonbullock1.wixsite.com/johnatonbullock")

    def main_screen(self, sprite_x = 0, sprite_y = 0):
        # pygame.display.set_caption("Johnaton Bullock's: Graveyard Shift")
        play = None
        quit_button = None


        main_menu = MainMenu(self.game_screen)
        main_menu.menu_load_up()
        running = True
        resume_pop_up = False
        start_game = False
        gaming_time = False
        in_menu = True
        world_choices = None
        py_event = None
        while running:
            mouse_pos = pygame.mouse.get_pos()
            if in_menu:
                play, quit_button = main_menu.menu_options(mouse_pos)


            pygame.key.set_repeat(100, 100)
            for event in pygame.event.get():
                py_event = event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play is not None and quit_button is not None:
                        if play.button_clicked(mouse_pos):
                            world_choices = GameScreen(self.game_screen)
                            sprite_x, sprite_y = world_choices.sprite_coords()
                            start_game = True
                            in_menu = False
                        if quit_button.button_clicked(mouse_pos):
                            pygame.quit()
                            quit()
                elif event.type == pygame.KEYDOWN:
                    if in_menu is False:
                        if sprite_y > 0:
                            resume_pop_up = False
                        if sprite_x > 930: sprite_x = 0
                        if sprite_x < -2:
                            in_menu = True
                            main_menu.menu_load_up()
                        if sprite_y > 930:
                            resume_pop_up = False
                            self.portfolio()
                            sprite_y = -25
                        if  0 > sprite_y:
                            resume_pop_up = True
                            if sprite_y < -30:
                                sprite_y = 931
                        if event.key == pygame.K_ESCAPE:
                            in_menu = True
                        if event.key == pygame.K_UP:

                            sprite_y -= 10
                        elif event.key == pygame.K_DOWN:
                            sprite_y += 10
                        elif event.key == pygame.K_LEFT:
                            sprite_x -= 17
                        elif event.key == pygame.K_RIGHT:
                            sprite_x += 17
            if start_game and in_menu is False:
                if world_choices.gaming_fade_in():
                    world_choices.gaming_scene()
                    gaming_time = True
            if gaming_time and in_menu is False:
                world_choices.sprite_movement(sprite_x, sprite_y, py_event)
            if resume_pop_up and in_menu is False:
                self.resume_scroll()


            pygame.display.update()
            relo.tick(60)

def new_surface():
    some_canvas = pygame.Surface((900, 900))
    some_canvas.fill("Yellow")
    return some_canvas



if __name__ == '__main__':
    pygame.init()
    relo = pygame.time.Clock()
    screen = pygame.display.set_mode((900, 900))
    ignition_key = PyGameGUI(screen)
    ignition_key.main_screen()


"""Operation: Graveyard Shift tank vs zombie game, forest setting, each zombie has info about me, after all the info, user can keep playing"""