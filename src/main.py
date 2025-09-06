"""
Kindergarten Snake Game - Main Game File
This is the entry point for the kindergarten snake game.
"""
import pygame
import sys
import traceback
from constants import *
from game_state import GameState
from screens.welcome_screen import WelcomeScreen
from screens.level_select_screen import LevelSelectScreen
from screens.game_screen import GameScreen
from screens.win_animation_screen import WinAnimationScreen
from screens.win_congrats_screen import WinCongratsScreen
from screens.game_over_screen import GameOverScreen
from screens.menu_select_screen import MenuSelectScreen

def main():
    pygame.init()
    pygame.font.init()
    
    screen_width, screen_height = SCREEN_WIDTH_INIT, SCREEN_HEIGHT_INIT
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Kindergarten Snake Game")
    clock = pygame.time.Clock()
    
    # Initialize fonts before creating screen objects
    from constants import initialize_fonts
    initialize_fonts()

    game_state = GameState()
    game_state.screen_width = screen_width
    game_state.screen_height = screen_height

    welcome_screen = WelcomeScreen(screen, game_state)
    level_select_screen = LevelSelectScreen(screen, game_state)
    game_screen = GameScreen(screen, game_state)
    win_animation_screen = WinAnimationScreen(screen, game_state)
    win_congrats_screen = WinCongratsScreen(screen, game_state)
    game_over_screen = GameOverScreen(screen, game_state)
    menu_select_screen = MenuSelectScreen(screen, game_state)

    running = True
    dt = 0

    while running:
        try:
            events = pygame.event.get()
        except pygame.error as e:
            print(f"Error getting events: {e}. Skipping frame.")
            continue

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize event
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                
                # Update screen dimensions in game state
                game_state.screen_width = screen_width
                game_state.screen_height = screen_height
                
                # Update all screens with new dimensions
                welcome_screen.update_dimensions(screen_width, screen_height)
                level_select_screen.update_dimensions(screen_width, screen_height)
                game_screen.update_dimensions(screen_width, screen_height)
                win_animation_screen.update_dimensions(screen_width, screen_height)
                
                # Update other components as needed
                pygame.display.flip()

            if game_state.current_state == STATE_WELCOME:
                welcome_screen.handle_events(event)
            elif game_state.current_state == STATE_LEVEL_SELECT:
                level_select_screen.handle_events(event)
            elif game_state.current_state == STATE_PLAYING:
                game_screen.handle_events(event)
            elif game_state.current_state == STATE_MENU_SELECT:
                menu_select_screen.handle_events(event)
            elif game_state.current_state == STATE_WIN_LEVEL_ANIMATING:
                win_animation_screen.handle_events(event)
            elif game_state.current_state == STATE_WIN_LEVEL_CONGRATS:
                win_congrats_screen.handle_events(event)
            elif game_state.current_state == STATE_GAME_OVER:
                game_over_screen.handle_events(event)

        try:
            if game_state.current_state == STATE_WELCOME:
                welcome_screen.update()
                welcome_screen.draw()
            elif game_state.current_state == STATE_LEVEL_SELECT:
                level_select_screen.update()
                level_select_screen.draw()
            elif game_state.current_state == STATE_PLAYING:
                game_screen.update(dt)
                game_screen.draw()
            elif game_state.current_state == STATE_MENU_SELECT:
                game_screen.draw(update_timer=False)
                menu_select_screen.draw()
            elif game_state.current_state == STATE_WIN_LEVEL_ANIMATING:
                win_animation_screen.update()
                win_animation_screen.draw()
            elif game_state.current_state == STATE_WIN_LEVEL_CONGRATS:
                win_congrats_screen.update()
                win_congrats_screen.draw()
            elif game_state.current_state == STATE_GAME_OVER:
                game_over_screen.draw()

        except Exception as e:
            print(f"Error drawing current state: {e}")
            traceback.print_exc()
            screen.fill(RED)
            font = pygame.font.Font(None, 30)
            text = font.render(f"Error in state {game_state.current_state}: {str(e)[:50]}...", True, WHITE)
            screen.blit(text, (20, screen_height // 2))

        try:
            pygame.display.flip()
        except pygame.error as e:
            print(f"Error flipping display: {e}")

        dt = clock.tick(FPS) / 1000.0

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
