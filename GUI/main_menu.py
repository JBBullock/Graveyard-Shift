import pygame
from Buttons import Button
"""MainMenu: the first thing you see when you open the pygame
  holds all the menu options, and menu screen
  pressing escape on your keyboard brings you back to the main menu"""
class MainMenu:
    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.menu_surface = None
        self.title = None
        self.author_title = None
        self.play_button = None
        self.quit_button = None
    def menu_load_up(self):
        title_font = pygame.font.Font('Fonts/KiwiSoda.ttf', 50)
        pygame.display.set_caption("Main Menu")
        self.menu_surface = pygame.image.load('Images/Graveyard.png').convert()
        pygame.transform.scale(self.menu_surface, (900, 900))
        self.title = title_font.render("Graveyard Shift", True, "#b68f40")
        self.author_title = title_font.render("Johnaton Bullock", True, "#b68f40")
        self.game_screen.blit(self.menu_surface, (0, 0))
        self.game_screen.blit(self.title, (300, 100))
        self.game_screen.blit(self.author_title, (250, 800))


    def menu_options(self, mouse_position):
        title_font = pygame.font.Font('Fonts/KiwiSoda.ttf', 50)
        start_image = pygame.image.load("Images/Start.png").convert()
        # print(start_image.get_alpha())
        self.play_button = Button((450, 500), "Start", title_font, base_color="White", hovering_color="Gold")
        self.quit_button = Button((450, 550), "Quit", title_font, base_color="White", hovering_color="Gold")

        button_list = [self.play_button, self.quit_button]

        for button in button_list:
            button.button_hue(mouse_position)
            button.update(self.game_screen)
        return self.play_button, self.quit_button
        pass

__all__ = ["MainMenu"]
