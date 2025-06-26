import pygame
from main_menu import MainMenu
class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pygame.Surface((900, 900))
        self.canvas.fill("Black")
        self.canvas.set_alpha(0)
        self._x_tank = 525
        self._y_tank = 500
    def sprite_coords(self):
        return self._x_tank, self._y_tank
    def gaming_scene(self):
        pygame.display.set_caption("Graveyard Shift")

        title_font = pygame.font.Font('Fonts/KiwiSoda.ttf', 50)
        resume_tunnel = title_font.render("Resume", True, "White")
        play_tunnel = title_font.render("Play", True, "White")
        menu_tunnel = title_font.render("Main Menu", True, "White")
        portfolio_tunnel = title_font.render("Portfolio", True, "White")
        # pygame.transform.flip(resume_tunnel, True, True)

        resume_road_label = pygame.transform.rotate(resume_tunnel, 90)
        portfolio_tunnel_label = pygame.transform.rotate(portfolio_tunnel, 90)
        game_setting = pygame.image.load('Images/Platform.png').convert()
        resume_rect = resume_road_label.get_rect(center = (450, 100))
        play_st = play_tunnel.get_rect(center=(800, 450))
        menu_st = menu_tunnel.get_rect(center=(150, 450))
        portfolio_st = portfolio_tunnel.get_rect(center=(525, 700))
        self.screen.blit( pygame.transform.scale(game_setting, (900, 900)), (0, 0))

        self.screen.blit(resume_road_label, resume_rect)
        self.screen.blit(play_tunnel, play_st)
        self.screen.blit(menu_tunnel, menu_st)
        self.screen.blit(portfolio_tunnel_label, portfolio_st)



    def sprite_movement(self, x_sprite, y_sprite, event_type):
        tank_sprite = pygame.image.load("Images/PixelTank.png").convert_alpha()
        moving_sprite = tank_sprite
        if event_type == pygame.K_LEFT:
            moving_sprite = pygame.transform.flip(moving_sprite, True, False)
        elif event_type == pygame.K_RIGHT:
            moving_sprite = tank_sprite
        elif event_type == pygame.K_UP:
            moving_sprite = pygame.transform.rotate(moving_sprite, 180)
        elif event_type == pygame.K_DOWN:
            moving_sprite = pygame.transform.rotate(moving_sprite, 90)
        tank_sprite = pygame.transform.scale(tank_sprite, (150, 100))
        tank_sprite_rect = tank_sprite.get_rect(midbottom=(x_sprite, y_sprite))
        self.screen.blit(tank_sprite, tank_sprite_rect)

    def gaming_fade_in(self):
        alpha = self.canvas.get_alpha()
        alpha = min(255, self.canvas.get_alpha() + 5)

        self.canvas.set_alpha(alpha)

        self.screen.blit(self.canvas, (0, 0))
        return alpha >= 255
    def gaming_fade_out(self):
        main_menu = MainMenu(self.screen)
        main_menu.menu_load_up()
        pass


__all__ = ["GameScreen"]