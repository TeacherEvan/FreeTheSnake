#!/usr/bin/env python3
"""
Mobile Testing Script for FreeTheSnake
Run the game with various mobile configurations for testing
"""
import sys
import os
import argparse
import pygame

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mobile_adapter import initialize_mobile_adapter
from mobile_tester import initialize_mobile_tester
from config_manager import game_config
from logger_setup import setup_logging, get_logger

def main():
    parser = argparse.ArgumentParser(description='Test FreeTheSnake mobile adaptability')
    parser.add_argument('--preset', choices=[
        'mobile_portrait', 'mobile_landscape', 
        'tablet_portrait', 'tablet_landscape',
        'iphone_se', 'iphone_12', 'ipad_mini'
    ], help='Use a predefined mobile screen preset')
    
    parser.add_argument('--width', type=int, help='Custom screen width')
    parser.add_argument('--height', type=int, help='Custom screen height')
    parser.add_argument('--mobile-mode', action='store_true', help='Enable mobile mode')
    parser.add_argument('--test-all', action='store_true', help='Run all mobile compatibility tests')
    parser.add_argument('--screenshots', action='store_true', help='Capture screenshots for all presets')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode (testing only)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level='DEBUG', log_to_file=True)
    logger = get_logger(__name__)
    
    logger.info("Starting mobile testing script")
    
    # Set headless mode if requested
    if args.headless:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        logger.info("Running in headless mode")
    
    # Initialize pygame
    pygame.init()
    
    # Determine screen dimensions
    if args.preset:
        width, height = get_preset_dimensions(args.preset)
    elif args.width and args.height:
        width, height = args.width, args.height
    else:
        width, height = 800, 600  # Default
    
    logger.info(f"Using screen dimensions: {width}x{height}")
    
    # Initialize mobile systems
    mobile_adapter = initialize_mobile_adapter(width, height)
    mobile_tester = initialize_mobile_tester()
    
    # Enable mobile mode if requested
    if args.mobile_mode:
        mobile_adapter.mobile_mode = True
        logger.info("Mobile mode enabled")
    
    if args.test_all:
        run_all_tests(mobile_adapter, mobile_tester)
    elif args.screenshots:
        capture_all_screenshots(mobile_adapter, mobile_tester, width, height)
    else:
        run_single_test(mobile_adapter, width, height)
    
    pygame.quit()
    logger.info("Mobile testing completed")

def get_preset_dimensions(preset):
    """Get dimensions for predefined presets"""
    presets = {
        'mobile_portrait': (390, 844),
        'mobile_landscape': (844, 390),
        'tablet_portrait': (768, 1024),
        'tablet_landscape': (1024, 768),
        'iphone_se': (375, 667),
        'iphone_12': (390, 844),
        'ipad_mini': (768, 1024)
    }
    return presets.get(preset, (800, 600))

def run_all_tests(mobile_adapter, mobile_tester):
    """Run comprehensive mobile compatibility tests"""
    logger = get_logger(__name__)
    logger.info("Running comprehensive mobile compatibility tests...")
    
    # Create a dummy screen for testing
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    
    # Mock game state for testing
    class MockGameState:
        def __init__(self):
            self.screen_width = 800
            self.screen_height = 600
    
    game_state = MockGameState()
    
    # Run tests
    test_results = mobile_tester.run_mobile_compatibility_tests(screen, game_state, mobile_adapter)
    
    # Generate report
    report = mobile_tester.generate_mobile_compatibility_report(test_results)
    print("\n" + report)
    
    logger.info("Mobile compatibility tests completed")

def capture_all_screenshots(mobile_adapter, mobile_tester, width, height):
    """Capture screenshots for all mobile presets"""
    logger = get_logger(__name__)
    logger.info("Capturing screenshots for mobile presets...")
    
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    
    # Mock game state
    class MockGameState:
        def __init__(self):
            self.screen_width = width
            self.screen_height = height
    
    game_state = MockGameState()
    
    # Capture screenshots
    screenshots = mobile_tester.capture_mobile_screenshots(screen, game_state, mobile_adapter, [])
    
    logger.info(f"Captured {len(screenshots)} screenshots")
    for screenshot in screenshots:
        print(f"Screenshot saved: {screenshot['filename']} ({screenshot['dimensions']})")

def run_single_test(mobile_adapter, width, height):
    """Run a single test with specified dimensions"""
    logger = get_logger(__name__)
    logger.info(f"Testing with dimensions: {width}x{height}")
    
    mobile_adapter.update_dimensions(width, height)
    
    # Display mobile adapter status
    status = mobile_adapter.get_status_info()
    print("\nMobile Adapter Status:")
    print("-" * 30)
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # Test touch target scaling
    print("\nTouch Target Scaling:")
    print("-" * 30)
    test_sizes = [20, 30, 40, 50]
    for size in test_sizes:
        scaled = mobile_adapter.scale_ui_element(size)
        print(f"{size}px → {scaled}px")
    
    # Test font scaling
    print("\nFont Scaling:")
    print("-" * 30)
    font_sizes = [12, 16, 24, 36]
    for size in font_sizes:
        adaptive = mobile_adapter.get_adaptive_font_size(size)
        print(f"{size}px → {adaptive}px")

if __name__ == "__main__":
    main()