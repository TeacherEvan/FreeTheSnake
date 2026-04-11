import unittest
from types import SimpleNamespace

import pygame

from src.constants import initialize_fonts
from src.game_state import GameState
from src.screens.game_draw_helpers import draw_game_ui, get_food_sprite
from src.screens.game_screen import GameScreen


class TestGameScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()
        initialize_fonts()
        self.surface = pygame.Surface((800, 600))

    def test_update_advances_animation_frame(self):
        game_state = GameState()
        setattr(game_state, "screen_width", 800)
        setattr(game_state, "screen_height", 600)
        setattr(game_state, "score", 0)
        screen = GameScreen(self.surface, game_state)
        screen.food_items = []

        screen.update(1 / 60)

        self.assertEqual(screen.animation_frame, 1)

    def test_food_sprite_cache_reuses_surface(self):
        first = get_food_sprite("A", (255, 0, 0), 18)
        second = get_food_sprite("A", (255, 0, 0), 18)

        self.assertIs(first, second)

    def test_draw_game_ui_updates_surface(self):
        before = pygame.image.tostring(self.surface, "RGB")
        game = SimpleNamespace(
            screen=self.surface,
            screen_width=800,
            screen_height=600,
            animation_frame=30,
            surprise_active=True,
            surprise_type="speed_boost",
            surprise_duration=7.2,
            game_state=SimpleNamespace(score=4, current_level=2, score_in_row=3),
        )

        draw_game_ui(game)

        after = pygame.image.tostring(self.surface, "RGB")
        self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
