import pygame
from Buttons import Button
from main_menu import MainMenu
import webbrowser
from Sprites_and_Scenes import *

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
        self.main_menu = None
        self.release_zombies = False
        self.bullets = pygame.sprite.Group()

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
            if event.key == pygame.K_SPACE and len(self.bullets) < 2:
                bullet = Bullet(self.sprite.x, self.sprite.y, self.sprite.flip)
                self.bullets.add(bullet)


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
    def main(self):

        """ FIX BUTTONS"""
        pygame.time.set_timer(self.zombie.spawn_event, self.zombie.spawn_timer)

        running = True
        play, quit_button =  None, None
        pygame.key.set_repeat(75, 100)
        pygame.time.set_timer(self.zombie.spawn_event, self.zombie.spawn_timer)

        while running:
            mouse_pos = pygame.mouse.get_pos()
            """---event catching, clicking play or quit, going left, down, right, up---"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play is not None and quit_button is not None:
                        if play.button_clicked(mouse_pos):
                            # self.game_view = "GAME"
                            self.in_menu = False
                            self.gaming_time = True
                            self.main_menu = None
                            play = None
                        if quit_button.button_clicked(mouse_pos):
                            pygame.quit()
                            quit()
                if event.type == self.zombie.spawn_event:
                    self.release_zombies = True
                if event.type == pygame.KEYDOWN:
                    self.game_movement(self.main_menu, event)

            """Movement of the tank sprite in the crossroads or arena"""
            if not self.in_menu:
                if not self.arena:
                    self.world_crossroads_movement()
                elif self.arena:
                    self.arena_movement()
            """behavior of the program inside the main menu"""
            if self.in_menu:
                if self.main_menu is None:
                    self.crossroads_fade()
                    self.main_menu = MainMenu(self.game_screen)
                self.resume_pop_up = False
                play, quit_button = self.main_menu.menu_options(mouse_pos)
                self.main_menu.menu_load_up()
                play.update(self.game_screen)
                quit_button.update(self.game_screen)

            """ updating the crossroads window with pop-ups, screens, and movement"""
            if not self.in_menu:
                if not self.arena:
                    self.crossroads_fade()
                    scroll = None
                    scroll_pos = None
                    scroll_text = None
                    scroll_text_pos = None
                    if self.resume_pop_up:

                        scroll, scroll_pos, scroll_text, scroll_text_pos = self.resume_scroll()
                        print('scroll_text', len(scroll_text), 'scroll_text_pos', len(scroll_text_pos))
                    if self.resume_pop_up and scroll is not None:
                        self.world_choices.gaming_scene()

                        self.game_screen.blit(scroll, scroll_pos)
                        for text, rect in zip(scroll_text, scroll_text_pos):
                            self.game_screen.blit(text, rect)
                        self.sprite.sprite_movement()
                    else:
                        self.world_choices.gaming_scene()
                        self.sprite.sprite_movement()
                """handles all spawning and movement once player reaches the arena"""
                if self.arena:
                    self.arena_load_in()
                    self.sprite.sprite_movement()
                    if self.release_zombies:

                        self.zombie.spawn_zombie()

                    self.sprite.sprite_movement()

                    self.bullets.update()
                    self.bullets.draw(self.game_screen)
                    for bullet in self.bullets:
                        for zombie_rect in self.zombie.zombie_horde:
                            if bullet.rect.colliderect(zombie_rect):
                                self.bullets.update()
                                self.bullets.draw(screen)

            pygame.display.update()
            relo.tick(60)

    """Displays resume scroll"""
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
                resume_text = resume_text_font.render(text, True, (0,0,0))
                text_rect = resume_text.get_rect(midtop=(450, text_y_value))
                GUI_text.append(resume_text)
                text_rects.append(text_rect)
                text_y_value += 13
            scroll_image = pygame.image.load('Images/scroll_pixel.png').convert_alpha()
            scroll_image = pygame.transform.scale(scroll_image, (650, 900))
            scroll_rect = scroll_image.get_rect(midtop=(450, 0))

            return scroll_image, scroll_rect, GUI_text, text_rects





"""Starts the program"""
if __name__ == '__main__':
    pygame.init()
    relo = pygame.time.Clock()
    screen = pygame.display.set_mode((900, 900))
    ignition_key = PyGameGUI(screen)
    ignition_key.main()

