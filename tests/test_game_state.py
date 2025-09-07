import unittest
from src.game_state import GameState

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_initial_state(self):
        self.assertEqual(self.game_state.current_state, 0)  # STATE_WELCOME
        self.assertEqual(self.game_state.lives, 3)
        self.assertEqual(self.game_state.score_in_row, 0)
        self.assertEqual(self.game_state.snake_size, 5)
        self.assertEqual(self.game_state.snake_segments, [])
        self.assertEqual(self.game_state.snake_direction, (1, 0))

    def test_reset_level(self):
        self.game_state.reset_level(1, 800, 600, None)
        self.assertEqual(self.game_state.current_level, 1)
        self.assertEqual(self.game_state.lives, 3)
        self.assertEqual(self.game_state.score_in_row, 0)
        self.assertEqual(self.game_state.snake_size, 25)  # Increased size for dramatic gameplay

    def test_assign_new_request(self):
        self.game_state.assign_new_request()
        self.assertIsInstance(self.game_state.snake_request, str)
        expected_items = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                         'α', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                         'Square', 'Triangle', 'Rectangle', 'Circle', 'Pentagon']
        self.assertIn(self.game_state.snake_request, expected_items)

    def test_check_win_condition(self):
        self.game_state.score_in_row = 3  # Simulate correct answers
        self.game_state.current_level = 1
        self.assertTrue(self.game_state.check_win_condition())

    def test_update_powerups(self):
        self.game_state.update_powerups(1.0)  # Simulate 1 second passing
        self.assertEqual(len(self.game_state.active_powerups), 0)  # No powerups should be active initially

if __name__ == '__main__':
    unittest.main()