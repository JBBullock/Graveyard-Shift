import pygame
from random import randint

class GameScreen:
    """creates the first canvas on the game window, all black"""
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pygame.Surface((900, 900))
        self.canvas.fill("Black")
        self.canvas.set_alpha(0)
        self.arena = pygame.image.load("Images/arena-shift.png").convert_alpha()


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
        self.screen.blit(pygame.transform.scale(game_setting, (900, 900)), (0, 0))

        self.screen.blit(resume_road_label, resume_rect)
        self.screen.blit(play_tunnel, play_st)
        self.screen.blit(menu_tunnel, menu_st)
        self.screen.blit(portfolio_tunnel_label, portfolio_st)
    def gaming_fade_in(self):

        alpha = self.canvas.get_alpha()
        alpha = min(255, self.canvas.get_alpha() + 3)

        self.canvas.set_alpha(alpha)

        self.screen.blit(self.canvas, (0, 0))
        return alpha >= 255

    def game_arena(self):
        self.screen.blit(pygame.transform.scale(self.arena, (900, 900)), (0, 0))

class TankSprite(GameScreen, pygame.sprite.Sprite):
    def __init__(self, game_display):
        self.tank_sprite_image_load = pygame.image.load("Images/green_top_down.png")
        self._x = 450
        self._y = 450
        self.tank_scale = pygame.transform.scale(self.tank_sprite_image_load, (350, 280))
        self.tank = pygame.transform.rotate(self.tank_scale, 0)
        self.flip = 0
        super().__init__(game_display)

    def going_right(self):
        if self.flip != 270:
            self.flip = 270
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)

        return self.flip == 270
    def going_up(self):
        if self.flip != 0:
            self.flip = 0
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)
        return self.flip == 0
        # self.tank = facing_up.get_rect(center=(self._x, self._y))
    def going_down(self):
        if self.flip != True:
            self.flip = True
            self.tank = pygame.transform.flip(self.tank_scale, False, True)
        return self.flip == False
        # self.tank = facing_down.get_rect(center=(self._x, self._y))
    def going_left(self):
        if self.flip != 90:
            self.flip = 90
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)
        return self.flip == 90
        # self.tank = flipped_sprite_x.get_rect(center=(self._x, self._y))

    def sprite_coords(self):
        return self._x, self._y

    def sprite_movement(self):
        tank_rect = self.tank.get_rect(center = (self._x, self._y))
        self.screen.blit(self.tank, tank_rect)

class ZombieSprite(GameScreen, pygame.sprite.Sprite):

    def __init__(self, game_display):
        super().__init__(game_display)
        self.spawn_timer = 3000
        self.spawn_event = pygame.USEREVENT + 1
        self.zombie_movement_frames = list()

    def zombie_sprite(self):
        idle_zombie = pygame.image.load("Images/IdleZombie.png").convert_alpha()
        scale_zombie = pygame.transform.scale(idle_zombie, (50, 50))
        idle_rect = scale_zombie.get_rect(center=(randint(445, 455), randint(900, 1100)))
        return scale_zombie, idle_rect
    def zombie_sprite_walk(self):
        walk_zombie = pygame.image.load("Images/WalkZombie.png").convert_alpha()
        return walk_zombie
    def zombie_movement_list(self, idle_rect):
        self.zombie_movement_frames.append(idle_rect)
        return self.zombie_movement_frames
    def spawn_zombie(self):
        z_image, z_rect = self.zombie_sprite()
        rect_list = self.zombie_movement_list(z_rect)
        for rect in rect_list:
            rect.y -= 5
            self.screen.blit(z_image, rect)
        return rect_list




__all__ = ["GameScreen", "TankSprite", "ZombieSprite"]