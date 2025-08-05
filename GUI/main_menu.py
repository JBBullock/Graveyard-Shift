
import pygame
from Buttons import Button

# s
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
        self.title_font = pygame.font.Font('../Fonts/KiwiSoda.ttf', 50)
        self.tips = ["You only have 5 bullets, use them wisely!", "Get in there and Tank them out!"]

    """This creates the main menu screen"""
    def menu_load_up(self):
        pygame.display.set_caption("Main Menu")
        self.menu_surface = pygame.image.load('../Images/Graveyard.png').convert()
        pygame.transform.scale(self.menu_surface, (900, 900))
        self.title = self.title_font.render("Graveyard Shift", True, "#b68f40")
        self.author_title = self.title_font.render("Johnaton Bullock", True, "#b68f40")
        self.game_screen.blit(self.menu_surface, (0, 0))
        self.game_screen.blit(self.title, (300, 100))
        self.game_screen.blit(self.author_title, (250, 800))

    """The menu options, made into buttons, one starts and the other quits the game"""
    def menu_options(self, mouse_position):
        title_font = pygame.font.Font('../Fonts/KiwiSoda.ttf', 50)
        # start_image = pygame.image.load("../Images/Start.png").convert()
        # print(start_image.get_alpha())
        self.play_button = Button((450, 500), "Start", title_font, base_color="White", hovering_color="Gold")
        self.quit_button = Button((450, 550), "Quit", title_font, base_color="White", hovering_color="Gold")

        button_list = [self.play_button, self.quit_button]

        for button in button_list:
            button.button_hue(mouse_position)
            button.update(self.game_screen)
        return self.play_button, self.quit_button

        pass

    def game_over(self):
        pygame.display.set_caption("Graveyard Shift")
        self.menu_surface = pygame.image.load('../Images/Graveyard.png').convert()
        pygame.transform.scale(self.menu_surface, (900, 900))
        game_over_text = self.title_font.render("Game Over", True, "#b68f40")


        self.game_screen.blit(self.menu_surface, (0, 0))
        self.game_screen.blit(game_over_text, (350,370))

    def game_over_options(self, mouse_position, lost_game = None):
        losing_message, winner_message = None, None
        title_font = pygame.font.Font('../Fonts/KiwiSoda.ttf', 40)
        quit_button = Button((450, 550), "Quit", self.title_font, base_color="White", hovering_color="Gold")
        if not lost_game:
            winner_message = title_font.render("You won!", True, "#b68f40")
            restart = Button((450, 500), "Restart", self.title_font, base_color="White", hovering_color="Gold")

        else:
            losing_message = title_font.render("Zombies invaded the temple! Try Again?", True, "#b68f40")
            restart = Button((450, 500), "Try Again", self.title_font, base_color="White", hovering_color="Gold")


        self.game_over()
        if losing_message:
            self.game_screen.blit(losing_message, (130, 650))
        if winner_message:
            self.game_screen.blit(winner_message, (375, 650))

        button_list = [restart, quit_button]

        for button in button_list:
            button.button_hue(mouse_position)
            button.update(self.game_screen)

        return restart, quit_button

__all__ = ["MainMenu"]
