from constants import *
from game_state import GameState
import pygame
import random
from utils import draw_text, get_cage_rect

class LevelSelectScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.level_buttons = []
        self.selected_level = 1
        self.create_level_buttons()

    def create_level_buttons(self):
        button_width = 150
        button_height = 50
        padding = 20
        for level in range(1, MAX_LEVEL + 1):
            x = (self.screen.get_width() - button_width) // 2
            y = 100 + (level - 1) * (button_height + padding)
            self.level_buttons.append(pygame.Rect(x, y, button_width, button_height))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.level_buttons):
                if button.collidepoint(mouse_pos):
                    self.selected_level = i + 1
                    self.game_state.reset_level(self.selected_level, self.screen.get_width(), self.screen.get_height(), get_cage_rect(self.screen.get_width(), self.screen.get_height()))
                    self.game_state.current_state = STATE_PLAYING

    def update(self):
        pass

    def draw(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "Select Level", (self.screen.get_width() // 2, 50), FONT_TITLE, color=BLACK, center=True)

        for i, button in enumerate(self.level_buttons):
            pygame.draw.rect(self.screen, GREEN if self.selected_level == i + 1 else DARK_GREY, button)
            draw_text(self.screen, f"Level {i + 1}", button.topleft, FONT_MEDIUM, color=WHITE, center=True)

        pygame.display.flip()