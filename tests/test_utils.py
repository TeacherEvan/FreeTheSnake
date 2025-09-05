import unittest
import pygame
from src.utils import draw_text, get_cage_rect, get_left_item_area_rect, get_right_item_area_rect

class TestUtils(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.font.init()
        self.screen_width = 800
        self.screen_height = 600

    def test_draw_text(self):
        # Test drawing text functionality
        surface = pygame.Surface((self.screen_width, self.screen_height))
        font = pygame.font.Font(None, 36)
        text_rect = draw_text(surface, "Hello", (100, 100), font)
        self.assertEqual(text_rect.topleft, (100, 100))

    def test_get_cage_rect(self):
        # Test cage rectangle calculation
        cage_rect = get_cage_rect(self.screen_width, self.screen_height)
        # The cage width should be cage_height * 0.8, where cage_height = screen_height * 0.55
        expected_width = min(self.screen_height * 0.55 * 0.8, self.screen_width - 20)
        self.assertEqual(cage_rect.width, expected_width)
        self.assertEqual(cage_rect.height, max(50, self.screen_height * 0.55))

    def test_get_left_item_area_rect(self):
        # Test left item area rectangle calculation
        left_rect = get_left_item_area_rect(self.screen_width, self.screen_height)
        self.assertTrue(left_rect.width > 0)
        self.assertTrue(left_rect.height > 0)

    def test_get_right_item_area_rect(self):
        # Test right item area rectangle calculation
        right_rect = get_right_item_area_rect(self.screen_width, self.screen_height)
        self.assertTrue(right_rect.width > 0)
        self.assertTrue(right_rect.height > 0)

if __name__ == '__main__':
    unittest.main()