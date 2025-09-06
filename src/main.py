"""
Kindergarten Snake Game - Main Game File
This is the entry point for the kindergarten snake game.
"""
import pygame
import sys
import traceback
import os

# Setup configuration and logging before importing other modules
from config_manager import game_config
from logger_setup import setup_logging, get_logger

# Setup logging
setup_logging(
    log_level=game_config.get_str('Development', 'log_level', 'INFO'),
    log_to_file=True
)
logger = get_logger(__name__)

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
    logger.info("Starting FreeTheSnake game")
    
    try:
        pygame.init()
        pygame.font.init()
        logger.info("Pygame initialized successfully")
        
        # Get screen dimensions from config
        screen_width = game_config.get_int('Game', 'screen_width', SCREEN_WIDTH_INIT)
        screen_height = game_config.get_int('Game', 'screen_height', SCREEN_HEIGHT_INIT)
        fps = game_config.get_int('Game', 'fps', FPS)
        
        logger.info(f"Screen dimensions: {screen_width}x{screen_height}, FPS: {fps}")
        
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("FreeTheSnake - Kindergarten Snake Game")
        clock = pygame.time.Clock()
        
        # Initialize fonts before creating screen objects
        from constants import initialize_fonts
        initialize_fonts()
        logger.info("Fonts initialized")

        game_state = GameState()
        game_state.screen_width = screen_width
        game_state.screen_height = screen_height
        logger.info("Game state initialized")

        # Initialize all screen objects
        logger.info("Initializing game screens...")
        welcome_screen = WelcomeScreen(screen, game_state)
        level_select_screen = LevelSelectScreen(screen, game_state)
        game_screen = GameScreen(screen, game_state)
        win_animation_screen = WinAnimationScreen(screen, game_state)
        win_congrats_screen = WinCongratsScreen(screen, game_state)
        game_over_screen = GameOverScreen(screen, game_state)
        menu_select_screen = MenuSelectScreen(screen, game_state)
        logger.info("All screens initialized successfully")

        running = True
        dt = 0
        frame_count = 0
        logger.info("Starting main game loop")

        while running:
            frame_count += 1
            
            try:
                events = pygame.event.get()
            except pygame.error as e:
                logger.error(f"Error getting events: {e}. Skipping frame.")
                continue

            for event in events:
                if event.type == pygame.QUIT:
                    logger.info("Quit event received")
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize event
                    screen_width, screen_height = event.size
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    
                    # Update screen dimensions in game state
                    game_state.screen_width = screen_width
                    game_state.screen_height = screen_height
                    
                    logger.debug(f"Window resized to {screen_width}x{screen_height}")
                    
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
                logger.error(f"Error drawing current state {game_state.current_state}: {e}")
                if game_config.get_bool('Development', 'debug_mode', False):
                    traceback.print_exc()
                
                # Show error on screen
                screen.fill(RED)
                font = pygame.font.Font(None, 30)
                text = font.render(f"Error in state {game_state.current_state}: {str(e)[:50]}...", True, WHITE)
                screen.blit(text, (20, screen_height // 2))

            try:
                pygame.display.flip()
            except pygame.error as e:
                logger.error(f"Error flipping display: {e}")

            # Show FPS if enabled in development mode
            if game_config.get_bool('Development', 'show_fps', False) and frame_count % 60 == 0:
                current_fps = clock.get_fps()
                logger.debug(f"Current FPS: {current_fps:.1f}")

            dt = clock.tick(fps) / 1000.0

        logger.info("Game loop ended")
        pygame.quit()
        logger.info("Game shutdown complete")
        sys.exit()

    except Exception as e:
        logger.critical(f"Critical error in main(): {e}")
        if game_config.get_bool('Development', 'debug_mode', False):
            traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
