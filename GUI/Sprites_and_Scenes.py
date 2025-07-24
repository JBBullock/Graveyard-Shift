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
        pygame.display.set_caption("Graveyard Shift")

        self.title_font = pygame.font.Font('Fonts/KiwiSoda.ttf', 50)
        self.resume_tunnel = self.title_font.render("Resume", True, "White")
        self.play_tunnel = self.title_font.render("Play", True, "White")
        self.menu_tunnel = self.title_font.render("Main Menu", True, "White")
        self.portfolio_tunnel = self.title_font.render("Portfolio", True, "White")
        self.game_setting = pygame.image.load('Images/Platform.png').convert()

    def gaming_scene(self):

        # pygame.transform.flip(resume_tunnel, True, True)

        resume_road_label = pygame.transform.rotate(self.resume_tunnel, 90)
        portfolio_tunnel_label = pygame.transform.rotate(self.portfolio_tunnel, 90)

        resume_rect = resume_road_label.get_rect(center = (450, 100))
        play_st = self.play_tunnel.get_rect(center=(800, 450))
        menu_st = self.menu_tunnel.get_rect(center=(150, 450))
        portfolio_st = self.portfolio_tunnel.get_rect(center=(525, 700))
        self.screen.blit(pygame.transform.scale(self.game_setting, (900, 900)), (0, 0))
        self.screen.blit(resume_road_label, resume_rect)
        self.screen.blit(self.play_tunnel, play_st)
        self.screen.blit(self.menu_tunnel, menu_st)
        self.screen.blit(portfolio_tunnel_label, portfolio_st)

    def gaming_fade_in(self):

        alpha = self.canvas.get_alpha()
        alpha = min(255, self.canvas.get_alpha() + 3)

        self.canvas.set_alpha(alpha)

        self.screen.blit(self.canvas, (0, 0))
        return alpha >= 255

    def game_arena(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.arena, (900, 900)), (0, 0))


class TankSprite(GameScreen, pygame.sprite.Sprite):
    def __init__(self, game_display):
        self.tank_sprite_image_load = pygame.image.load("Images/green_top_down.png")
        self.x = 450
        self.y = 450
        self.tank_scale = pygame.transform.scale(self.tank_sprite_image_load, (350, 280))
        self.tank = pygame.transform.rotate(self.tank_scale, 0)
        self.flip = 0
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        super().__init__(game_display)

    def going_right(self):
        self.x += 15
        if self.flip != 270:
            self.flip = 270
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)
        self.right = False
        return self.flip == 270
    def going_up(self):

        self.y -= 15

        if self.flip != 0:
            self.flip = 0
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)
        self.up = False
        return self.flip == 0
        # self.tank = facing_up.get_rect(center=(self._x, self._y))
    def going_down(self):
        self.y += 15
        if self.flip is not True:
            self.flip = True
            self.tank = pygame.transform.flip(self.tank_scale, False, True)
        self.down = False
        return self.flip == False
        # self.tank = facing_down.get_rect(center=(self._x, self._y))
    def going_left(self):
        self.x -= 15
        if self.flip != 90:
            self.flip = 90
            self.tank = pygame.transform.rotate(self.tank_scale, self.flip)
        self.left = False
        return self.flip == 90
        # self.tank = flipped_sprite_x.get_rect(center=(self._x, self._y))

    def sprite_coords(self):
        return self.x, self.y

    def sprite_movement(self):
        tank_rect = self.tank.get_rect(center = (self.x, self.y))
        self.screen.blit(self.tank, tank_rect)
    def fire_bullet(self):
        tank_rect = self.tank.get_rect(center=(self.x, self.y))
        direction = self.flip
        x, y = self.sprite_coords()

        if direction == 0:  # up
            bullet_x = x
            bullet_y = y
        elif direction == 90:  # left
            bullet_x = x
            bullet_y = y
        elif direction == 270:  # right
            bullet_x = x
            bullet_y = y
        elif direction is True:  # down
            bullet_x = x
            bullet_y = y
        else:  # fallback
            bullet_x, bullet_y = x, y

        return Bullet(bullet_x, bullet_y, direction)


class ZombieSprite(GameScreen, pygame.sprite.Sprite):

    def __init__(self, game_display):
        super().__init__(game_display)
        self.spawn_timer = 100
        self.spawn_event = pygame.USEREVENT + 1
        self.zombie_horde = list()

        self.zombie_image = pygame.image.load("Images/IdleZombie.png").convert_alpha()
        self.zombie_image = pygame.transform.scale(self.zombie_image, (50, 50))

        self.zombie_step = pygame.image.load("Images/WalkZombie.png").convert_alpha()
        self.zombie_step = pygame.transform.scale(self.zombie_step, (50, 50))
        self.zombie_index = 0

        self.walk = [self.zombie_image, self.zombie_step]
        self.spawn_delay = 60
        self.spawn_counter = 0

    def zombie_sprite(self):
        zombie_start_x = randint(400, 500)
        zombie_start_y = 901
        # self.zombie_image = self.walk[self.zombie_index]
        zombie_rect = self.zombie_image.get_rect(center = (zombie_start_x, zombie_start_y))


        return zombie_rect

    def zombie_stepping(self):
        self.zombie_index += 0.05
        if self.zombie_index >= len(self.walk):
            self.zombie_index = 0
        self.zombie_image = self.walk[int(self.zombie_index)]



    def spawn_zombie(self):

        self.spawn_counter += 1
        self.zombie_stepping()
        if self.spawn_counter >= self.spawn_delay:
            self.spawn_counter = 0
            new_zombie = self.zombie_sprite()
            self.zombie_horde.append(new_zombie)

        updated_horde = []
        for zombie_rectangle in self.zombie_horde:
            zombie_rectangle.y -= float(0.7)
            if zombie_rectangle.y > 375:
                updated_horde.append(zombie_rectangle)
            self.screen.blit(self.zombie_image, zombie_rectangle)
        self.zombie_horde = updated_horde

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.speed = 10


        # Base bullet image is horizontal (right-facing)
        base_image = pygame.Surface((10, 4))
        base_image.fill((255, 255, 0))

        # Rotate bullet based on direction
        if direction == 0:       # Up
            self.image = pygame.transform.rotate(base_image, 90)
        elif direction == 90:    # Left
            self.image = pygame.transform.rotate(base_image, 180)
        elif direction == 270:   # Right
            self.image = base_image
        elif direction is True:  # Down
            self.image = pygame.transform.rotate(base_image, -90)
        else:
            self.image = base_image

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 90:
            self.rect.x -= self.speed
        elif self.direction == 270:
            self.rect.x += self.speed
        elif self.direction is True:
            self.rect.y += self.speed

        # Remove bullet if off-screen
        if not (0 <= self.rect.x <= 900 and 0 <= self.rect.y <= 900):
            self.kill()







__all__ = ["GameScreen", "TankSprite", "ZombieSprite", "Bullet"]