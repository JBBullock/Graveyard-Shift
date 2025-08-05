import pygame
from main_menu import MainMenu
import webbrowser
from Sprites_and_Scenes import *

"""Housing the main game loop, updates the general game window"""
class PyGameGUI:
    def __init__(self, game_screen, reloj):
        self.game_screen = game_screen
        self.arena = False
        self.resume_pop_up = False
        self.start_game = False
        self.gaming_time = False
        self.in_menu = True
        self.world_choices = self.crossroads_init()
        self.sprite = TankSprite(self.game_screen)
        self.zombie = ZombieSprite(self.game_screen, self.world_choices)
        self.main_menu = None
        self.release_zombies = False
        self.bullets = pygame.sprite.Group()
        self.zombie_group = pygame.sprite.Group()
        self.last_shot_time = 0  # track time in milliseconds
        self.shoot_cooldown = 5000
        self.space_held = False
        self.relo = reloj
        self.level_2 = False
        self.delay_start_time = None
        self.delay_duration = 1500
        self.trigger_game_over = False
        self.showing_delayed_screen = False
        self.game_over = False
        self.lost_game = False

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
    def game_movement(self, event):
        # print("game movement was called")
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
        elif event.key == pygame.K_SPACE and len(self.bullets) < 2:
            current_time = pygame.time.get_ticks()
            if not self.space_held:
                if current_time - self.last_shot_time >= self.shoot_cooldown:
                    bullet = Bullet(self.sprite.x, self.sprite.y, self.sprite.flip)
                    self.bullets.add(bullet)
                    self.space_held = True
                    self.world_choices.ammo_img_list.pop()




    def world_crossroads_movement(self):
        if self.sprite.x > 900:
            self.arena = True
            self.sprite.x = 450
            self.sprite.y = 365
        elif self.sprite.x < -2:
            self.in_menu = True
            self.main_menu = None
            self.sprite.x = 450
            self.sprite.y = 450

        if 750> self.sprite.y > 0:
            self.resume_pop_up = False
        if self.sprite.y > 990:
            self.resume_pop_up = False
            self.portfolio()
            self.sprite.y = -25
        elif 0 > self.sprite.y:
            self.resume_pop_up = True
            if self.sprite.y < -60:
                self.sprite.y = 970

        if self.sprite.up:
            self.sprite.going_up()
        elif self.sprite.down:
            self.sprite.going_down()
        elif self.sprite.left:
            self.sprite.going_left()
        elif self.sprite.right:
            self.sprite.going_right()
    def arena_movement(self):
        self.sprite.x = max(90, min(self.sprite.x, 800))
        self.sprite.y = max(110, min(self.sprite.y, 800))

        if self.sprite.up:
            if self.sprite.y >= 110:
                self.sprite.going_up()
        if self.sprite.down:
            if self.sprite.y <= 800:
                self.sprite.going_down()
        if self.sprite.left:
            if self.sprite.x >= 90:
                self.sprite.going_left()
        if self.sprite.right:
            if self.sprite.x <= 800:
                self.sprite.going_right()

    """The main loop of the game, receives input, updates the main game window every 60 frames"""
    def main_loop(self):

        pygame.time.set_timer(self.zombie.spawn_event, self.zombie.spawn_timer)
        pygame.key.set_repeat(75, 100)

        pre_menu = MainMenu(self.game_screen)
        running = True
        play = quit_button = restart_button = final_quit_button = None

        while running:


            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        if restart_button and restart_button.button_clicked(mouse_pos):
                            main()
                        elif final_quit_button and final_quit_button.button_clicked(mouse_pos):
                            quit()
                    elif play and quit_button:
                        if play.button_clicked(mouse_pos):
                            self.in_menu = False
                            self.gaming_time = True
                            self.main_menu = None
                            play = quit_button = None
                        elif quit_button.button_clicked(mouse_pos):
                            pygame.quit()
                            quit()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and self.world_choices.ammo_img_list:
                        self.space_held = False

                elif event.type == self.zombie.spawn_event:
                    self.release_zombies = True

                elif event.type == pygame.KEYDOWN:
                    self.game_movement(event)

            if not self.in_menu:
                if not self.arena:
                    self.world_crossroads_movement()
                else:
                    self.arena_movement()

            if self.in_menu:
                if self.main_menu is None:
                    self.crossroads_fade()
                    self.main_menu = MainMenu(self.game_screen)

                self.resume_pop_up = False
                play, quit_button = self.main_menu.menu_options(mouse_pos)
                self.main_menu.menu_load_up()
                play.update(self.game_screen)
                quit_button.update(self.game_screen)
                pygame.display.update()

            elif not self.arena:
                self.crossroads_fade()
                self.world_crossroads_movement()

                if self.resume_pop_up:
                    scroll, scroll_rect, scroll_text, text_rects = self.resume_scroll()
                    if scroll:
                        self.world_choices.gaming_scene()
                        self.game_screen.blit(scroll, scroll_rect)
                        for text, rect in zip(scroll_text, text_rects):
                            self.game_screen.blit(text, rect)
                else:
                    self.world_choices.gaming_scene()

                self.sprite.sprite_movement()

            elif self.arena:
                self.arena_load_in()
                self.sprite.sprite_movement()

                if self.release_zombies:
                    self.zombie.spawn_zombie()

                self.sprite.sprite_movement()

                if len(self.world_choices.ammo_img_list) > -1:
                    self.bullets.update()
                    self.bullets.draw(self.game_screen)

                for bullet in self.bullets:
                    for zombie_rect in self.zombie.zombie_horde.copy():
                        if bullet.rect.colliderect(zombie_rect):
                            bullet.kill()
                            self.zombie.zombie_horde.remove(zombie_rect)
                            self.world_choices.kill_plus_one = True
                            break

            if self.world_choices.current_temple_health <= 0:
                restart_button, final_quit_button = pre_menu.game_over_options(mouse_pos, True)
                self.lost_game = True
                self.game_over = True

            if self.world_choices.zombies_killed_score == self.world_choices.level_up_amount:
                restart_button, final_quit_button = pre_menu.game_over_options(mouse_pos, False)
                self.game_over = True

            pygame.display.update()
            self.relo.tick(60)


    """Displays resume scroll"""

    def resume_scroll(self):
        try:
            with open('../Images/Johnaton Bullock Resume.txt') as file:
                lines = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("Resume file not found.")
            return None, None, [], []

        font = pygame.font.Font("../Fonts/Purl.ttf", 18)

        rendered_text = []
        text_rects = []
        y_offset = 125
        for line in lines:
            surface = font.render(line, True, (0, 0, 0))
            rect = surface.get_rect(midtop=(450, y_offset))
            rendered_text.append(surface)
            text_rects.append(rect)
            y_offset += 13

        scroll_image = pygame.image.load('../Images/scroll_pixel.png').convert_alpha()
        scroll_image = pygame.transform.scale(scroll_image, (650, 900))
        scroll_rect = scroll_image.get_rect(midtop=(450, 0))

        return scroll_image, scroll_rect, rendered_text, text_rects

"""Starts the program"""
def main():
    pygame.init()
    relo = pygame.time.Clock()
    screen = pygame.display.set_mode((900, 900))
    ignition_key = PyGameGUI(screen, relo)
    ignition_key.main_loop()
