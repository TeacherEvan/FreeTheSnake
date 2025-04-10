from constants import *
from utils import draw_text

class WinCongratsScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = FONT_TITLE

    def update(self):
        pass  # No updates needed for this screen

    def draw(self):
        self.screen.fill(WHITE)  # Clear the screen with a white background
        draw_text(self.screen, "Congratulations!", (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50), self.font, color=GREEN, center=True)
        draw_text(self.screen, "You freed the snake!", (self.screen.get_width() // 2, self.screen.get_height() // 2), self.font, color=BRIGHT_GREEN, center=True)
        draw_text(self.screen, "Press any key to continue...", (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50), FONT_MEDIUM, color=BLACK, center=True)