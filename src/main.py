"""
Kindergarten Snake Game - Main Game File
This is the entry point for the kindergarten snake game.

This module implements lazy loading for game screens to optimize
startup time and memory usage. Screens are loaded on-demand when
first accessed.
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
from mobile_adapter import initialize_mobile_adapter, get_mobile_adapter
from event_tracker import initialize_event_tracker, get_event_tracker
from mobile_tester import initialize_mobile_tester, get_mobile_tester

# TODO: [OPTIMIZATION] Consider implementing asset preloading during splash screen
# to improve perceived performance for initial game load

# Lazy-loaded screen imports - these are imported on-demand to improve startup time
_screen_cache = {}

def _get_screen_class(screen_name):
    """
    Lazily import and cache screen classes to reduce initial load time.
    
    Args:
        screen_name: Name of the screen class to load
        
    Returns:
        The screen class
    """
    if screen_name not in _screen_cache:
        if screen_name == 'WelcomeScreen':
            from screens.welcome_screen import WelcomeScreen
            _screen_cache[screen_name] = WelcomeScreen
        elif screen_name == 'LevelSelectScreen':
            from screens.level_select_screen import LevelSelectScreen
            _screen_cache[screen_name] = LevelSelectScreen
        elif screen_name == 'GameScreen':
            from screens.game_screen import GameScreen
            _screen_cache[screen_name] = GameScreen
        elif screen_name == 'WinAnimationScreen':
            from screens.win_animation_screen import WinAnimationScreen
            _screen_cache[screen_name] = WinAnimationScreen
        elif screen_name == 'WinCongratsScreen':
            from screens.win_congrats_screen import WinCongratsScreen
            _screen_cache[screen_name] = WinCongratsScreen
        elif screen_name == 'GameOverScreen':
            from screens.game_over_screen import GameOverScreen
            _screen_cache[screen_name] = GameOverScreen
        elif screen_name == 'MenuSelectScreen':
            from screens.menu_select_screen import MenuSelectScreen
            _screen_cache[screen_name] = MenuSelectScreen
    return _screen_cache.get(screen_name)

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

        # Initialize mobile adaptability system
        mobile_adapter = initialize_mobile_adapter(screen_width, screen_height)
        logger.info("Mobile adapter initialized")
        
        # Initialize event tracking system
        event_tracker = initialize_event_tracker()
        logger.info("Event tracking initialized")
        
        # Initialize mobile testing system
        mobile_tester = initialize_mobile_tester()
        logger.info("Mobile testing system initialized")

        game_state = GameState()
        game_state.screen_width = screen_width
        game_state.screen_height = screen_height
        logger.info("Game state initialized")

        # Initialize screens lazily - only create when first accessed
        # This improves startup time by deferring expensive screen initialization
        logger.info("Setting up lazy screen initialization...")
        
        # Screen instance cache - screens are created on first access
        screen_instances = {}
        
        def get_screen_instance(screen_name):
            """
            Get or create a screen instance lazily.
            
            Args:
                screen_name: Name of the screen to get/create
                
            Returns:
                The screen instance
            """
            if screen_name not in screen_instances:
                logger.debug(f"Lazy loading screen: {screen_name}")
                screen_class = _get_screen_class(screen_name)
                if screen_class:
                    screen_instances[screen_name] = screen_class(screen, game_state)
                else:
                    logger.error(f"Failed to load screen class: {screen_name}")
                    return None
            return screen_instances[screen_name]
        
        # Pre-load only the welcome screen for immediate display
        # Other screens will be loaded on-demand
        welcome_screen = get_screen_instance('WelcomeScreen')
        logger.info("Welcome screen initialized (other screens lazy-loaded)")

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
                    
                    # Update mobile adapter
                    mobile_adapter.update_dimensions(screen_width, screen_height)
                    
                    # Track mobile adaptation events
                    event_tracker.track_mobile_adaptation(
                        (screen_width, screen_height),
                        mobile_adapter.get_orientation(),
                        mobile_adapter.ui_scale
                    )
                    
                    logger.debug(f"Window resized to {screen_width}x{screen_height}")
                    
                    # Update all loaded screens with new dimensions
                    for screen_name, screen_inst in screen_instances.items():
                        if hasattr(screen_inst, 'update_dimensions'):
                            screen_inst.update_dimensions(screen_width, screen_height)
                    
                    # Update other components as needed
                    pygame.display.flip()
                
                # Track pygame events for debugging
                event_tracker.track_pygame_event(event)
                
                # Process touch events through mobile adapter
                mobile_adapter.handle_touch_event(event)

                # Handle events for the current screen (lazy load screens as needed)
                if game_state.current_state == STATE_WELCOME:
                    welcome_screen.handle_events(event)
                elif game_state.current_state == STATE_LEVEL_SELECT:
                    level_select_screen = get_screen_instance('LevelSelectScreen')
                    level_select_screen.handle_events(event)
                elif game_state.current_state == STATE_PLAYING:
                    game_screen = get_screen_instance('GameScreen')
                    game_screen.handle_events(event)
                elif game_state.current_state == STATE_MENU_SELECT:
                    menu_select_screen = get_screen_instance('MenuSelectScreen')
                    menu_select_screen.handle_events(event)
                elif game_state.current_state == STATE_WIN_LEVEL_ANIMATING:
                    win_animation_screen = get_screen_instance('WinAnimationScreen')
                    win_animation_screen.handle_events(event)
                elif game_state.current_state == STATE_WIN_LEVEL_CONGRATS:
                    win_congrats_screen = get_screen_instance('WinCongratsScreen')
                    win_congrats_screen.handle_events(event)
                elif game_state.current_state == STATE_GAME_OVER:
                    game_over_screen = get_screen_instance('GameOverScreen')
                    game_over_screen.handle_events(event)
                
                # Track screen transitions
                if game_state._previous_state != game_state.current_state:
                    event_tracker.track_screen_transition(game_state._previous_state, game_state.current_state)
                    game_state._previous_state = game_state.current_state

            try:
                # Update and draw screens based on current state (lazy load as needed)
                if game_state.current_state == STATE_WELCOME:
                    welcome_screen.update()
                    welcome_screen.draw()
                elif game_state.current_state == STATE_LEVEL_SELECT:
                    level_select_screen = get_screen_instance('LevelSelectScreen')
                    level_select_screen.update()
                    level_select_screen.draw()
                elif game_state.current_state == STATE_PLAYING:
                    game_screen = get_screen_instance('GameScreen')
                    game_screen.update(dt)
                    game_screen.draw()
                elif game_state.current_state == STATE_MENU_SELECT:
                    game_screen = get_screen_instance('GameScreen')
                    menu_select_screen = get_screen_instance('MenuSelectScreen')
                    game_screen.draw(update_timer=False)
                    menu_select_screen.draw()
                elif game_state.current_state == STATE_WIN_LEVEL_ANIMATING:
                    win_animation_screen = get_screen_instance('WinAnimationScreen')
                    win_animation_screen.update()
                    win_animation_screen.draw()
                elif game_state.current_state == STATE_WIN_LEVEL_CONGRATS:
                    win_congrats_screen = get_screen_instance('WinCongratsScreen')
                    win_congrats_screen.update()
                    win_congrats_screen.draw()
                elif game_state.current_state == STATE_GAME_OVER:
                    game_over_screen = get_screen_instance('GameOverScreen')
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
                # Track performance metrics
                event_tracker.track_performance_metric('fps', current_fps)

            frame_time_ms = dt * 1000
            mobile_adapter.track_performance(frame_time_ms)
            event_tracker.track_performance_metric('frame_time', frame_time_ms)
            
            dt = clock.tick(fps) / 1000.0

        logger.info("Game loop ended")
        
        # Log mobile compatibility information before shutdown
        event_tracker.log_mobile_compatibility_info(mobile_adapter)
        
        # Export tracking data
        event_tracker.cleanup()
        
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
