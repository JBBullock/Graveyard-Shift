import unittest
import pygame
from unittest.mock import patch, MagicMock

from GUI_pygame import PyGameGUI
from Sprites_and_Scenes import *
from unittest.mock import patch

class TestGameMovement(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 900))
        self.clock = pygame.time.Clock()
        self.gui = PyGameGUI(self.screen, self.clock)

    def test_arrow_key_sets_tank_up(self):
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
        self.gui.game_movement(event)
        self.assertTrue(self.gui.sprite.up)

    def test_arrow_key_sets_tank_left(self):
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        self.gui.game_movement(event)
        self.assertTrue(self.gui.sprite.left)

    def test_bullet_is_fired_after_cooldown(self):
        self.gui.last_shot_time = 0  # simulate no shots yet
        self.gui.space_held = False
        self.gui.sprite.flip = False
        self.gui.sprite.x = 100
        self.gui.sprite.y = 100
        self.gui.world_choices.ammo_img_list = [1]  # simulate ammo

        self.gui.shoot_cooldown = 0  # simulate instant cooldown
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.gui.game_movement(event)

        self.assertEqual(len(self.gui.bullets), 1)
    def test_crossroads_to_arena_transition(self):
        self.gui.sprite.x = 950  # simulate crossing the right boundary
        self.gui.world_crossroads_movement()
        self.assertTrue(self.gui.arena)
        self.assertEqual(self.gui.sprite.x, 450)  # reset position



    @patch("webbrowser.open")
    def test_portfolio_opens_url(self, mock_open):
        self.gui.portfolio()
        mock_open.assert_called_with("https://johnatonbullock1.wixsite.com/johnatonbullock")


if __name__ == '__main__':
    unittest.main()
