# filepath: kindergarten-snake-game/kindergarten-snake-game/src/screens/menu_select_screen.py
import pygame
from constants import *
from game_state import GameState
from utils import draw_text

class MenuSelectScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = FONT_MENU
        self.menu_items = ["Start Game", "Instructions", "Exit"]
        self.selected_index = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                self.select_menu_item()

    def select_menu_item(self):
        if self.selected_index == 0:  # Start Game
            self.game_state.current_state = STATE_LEVEL_SELECT
        elif self.selected_index == 1:  # Instructions
            self.show_instructions()
        elif self.selected_index == 2:  # Exit
            pygame.quit()
            exit()

    def show_instructions(self):
        # Placeholder for instructions display
        print("Instructions: Use UP and DOWN arrows to navigate the menu. Press ENTER to select.")

    def update(self):
        pass  # Update logic can be added here if needed

    def draw(self):
        self.screen.fill(BLACK)
        title_text = "Kindergarten Snake Game"
        draw_text(self.screen, title_text, (SCREEN_WIDTH_INIT // 2, SCREEN_HEIGHT_INIT // 4), self.font, color=WHITE, center=True)

        for index, item in enumerate(self.menu_items):
            color = BRIGHT_GREEN if index == self.selected_index else WHITE
            draw_text(self.screen, item, (SCREEN_WIDTH_INIT // 2, SCREEN_HEIGHT_INIT // 2 + index * 40), self.font, color=color, center=True)