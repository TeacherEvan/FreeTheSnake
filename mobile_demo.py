#!/usr/bin/env python3
"""
Mobile Adaptability Demo for FreeTheSnake
Demonstrates mobile features and captures screenshots
"""
import sys
import os
import pygame
import argparse

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mobile_adapter import initialize_mobile_adapter
from event_tracker import initialize_event_tracker
from config_manager import game_config
from logger_setup import setup_logging, get_logger
from constants import *

def main():
    parser = argparse.ArgumentParser(description='Demo FreeTheSnake mobile adaptability')
    parser.add_argument('--demo', choices=[
        'responsive_ui', 'touch_targets', 'event_tracking', 'mobile_presets'
    ], default='responsive_ui', help='Choose demo type')
    parser.add_argument('--screenshots', action='store_true', help='Capture screenshots')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level='INFO', log_to_file=True)
    logger = get_logger(__name__)
    
    if args.headless:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        logger.info("Running in headless mode")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    if args.demo == 'responsive_ui':
        demo_responsive_ui(logger, args.screenshots)
    elif args.demo == 'touch_targets':
        demo_touch_targets(logger, args.screenshots)
    elif args.demo == 'event_tracking':
        demo_event_tracking(logger)
    elif args.demo == 'mobile_presets':
        demo_mobile_presets(logger, args.screenshots)
    
    pygame.quit()
    logger.info("Demo completed")

def demo_responsive_ui(logger, capture_screenshots):
    """Demonstrate responsive UI scaling"""
    logger.info("Demonstrating responsive UI scaling...")
    
    # Test different screen sizes
    test_sizes = [
        ('Mobile Portrait', 390, 844),
        ('Mobile Landscape', 844, 390),
        ('Tablet Portrait', 768, 1024),
        ('Desktop', 1024, 768)
    ]
    
    for name, width, height in test_sizes:
        logger.info(f"Testing {name}: {width}x{height}")
        
        # Initialize mobile adapter
        mobile_adapter = initialize_mobile_adapter(width, height)
        
        # Create screen
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(f"FreeTheSnake - {name}")
        
        # Draw responsive UI demo
        screen.fill(WHITE)
        
        # Draw title with adaptive font size
        title_size = mobile_adapter.get_adaptive_font_size(36)
        font_title = pygame.font.Font(None, title_size)
        title_text = font_title.render("Mobile Adaptability Demo", True, BLACK)
        title_rect = title_text.get_rect(center=(width//2, height//6))
        screen.blit(title_text, title_rect)
        
        # Draw mobile info
        info_size = mobile_adapter.get_adaptive_font_size(18)
        font_info = pygame.font.Font(None, info_size)
        
        info_lines = [
            f"Screen: {width}x{height}",
            f"Orientation: {mobile_adapter.get_orientation()}",
            f"UI Scale: {mobile_adapter.ui_scale:.2f}",
            f"Touch Friendly: {mobile_adapter.touch_friendly}",
            f"Is Mobile: {mobile_adapter.is_mobile_resolution()}"
        ]
        
        y_offset = height//3
        for line in info_lines:
            text_surface = font_info.render(line, True, DARK_BLUE)
            text_rect = text_surface.get_rect(center=(width//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += mobile_adapter.get_mobile_ui_spacing() * 2
        
        # Draw touch target examples
        button_width = mobile_adapter.scale_ui_element(120)
        button_height = mobile_adapter.scale_ui_element(40)
        button_x = (width - button_width) // 2
        button_y = height * 2 // 3
        
        # Draw touch-friendly button
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, button_rect)
        pygame.draw.rect(screen, DARK_GREY, button_rect, 2)
        
        button_text = font_info.render("Touch Button", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        # Draw touch area indicator
        touch_rect = mobile_adapter.create_touch_friendly_rect(button_rect)
        if touch_rect != button_rect:
            pygame.draw.rect(screen, LIGHT_YELLOW, touch_rect, 1)
        
        pygame.display.flip()
        
        # Capture screenshot if requested
        if capture_screenshots:
            screenshot_dir = "logs/mobile_demo"
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"responsive_ui_{name.lower().replace(' ', '_')}.png"
            filepath = os.path.join(screenshot_dir, filename)
            pygame.image.save(screen, filepath)
            logger.info(f"Screenshot saved: {filepath}")
        
        pygame.time.wait(500)  # Brief pause between demos

def demo_touch_targets(logger, capture_screenshots):
    """Demonstrate touch target scaling"""
    logger.info("Demonstrating touch target scaling...")
    
    width, height = 390, 844  # Mobile portrait
    mobile_adapter = initialize_mobile_adapter(width, height)
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Touch Target Demo")
    
    screen.fill(WHITE)
    
    # Title
    title_size = mobile_adapter.get_adaptive_font_size(24)
    font_title = pygame.font.Font(None, title_size)
    title_text = font_title.render("Touch Target Scaling", True, BLACK)
    title_rect = title_text.get_rect(center=(width//2, 50))
    screen.blit(title_text, title_rect)
    
    # Draw various button sizes
    test_sizes = [20, 30, 40, 50, 60]
    y_start = 120
    spacing = mobile_adapter.get_mobile_ui_spacing() * 3
    
    font_label = pygame.font.Font(None, mobile_adapter.get_adaptive_font_size(16))
    
    for i, base_size in enumerate(test_sizes):
        y_pos = y_start + i * spacing
        
        # Original size button
        orig_rect = pygame.Rect(50, y_pos, base_size, base_size)
        pygame.draw.rect(screen, RED, orig_rect)
        pygame.draw.rect(screen, BLACK, orig_rect, 1)
        
        # Touch-friendly size button
        touch_size = mobile_adapter.scale_ui_element(base_size)
        touch_rect = pygame.Rect(150, y_pos, touch_size, touch_size)
        pygame.draw.rect(screen, GREEN, touch_rect)
        pygame.draw.rect(screen, BLACK, touch_rect, 1)
        
        # Labels
        label_text = font_label.render(f"{base_size}px → {touch_size}px", True, BLACK)
        screen.blit(label_text, (250, y_pos + base_size//2 - 8))
    
    # Legend
    legend_y = height - 100
    font_legend = pygame.font.Font(None, mobile_adapter.get_adaptive_font_size(14))
    
    # Red legend
    pygame.draw.rect(screen, RED, (50, legend_y, 20, 20))
    pygame.draw.rect(screen, BLACK, (50, legend_y, 20, 20), 1)
    legend_text = font_legend.render("Original Size", True, BLACK)
    screen.blit(legend_text, (80, legend_y + 3))
    
    # Green legend
    pygame.draw.rect(screen, GREEN, (50, legend_y + 30, 20, 20))
    pygame.draw.rect(screen, BLACK, (50, legend_y + 30, 20, 20), 1)
    legend_text = font_legend.render("Touch-Friendly Size", True, BLACK)
    screen.blit(legend_text, (80, legend_y + 33))
    
    pygame.display.flip()
    
    if capture_screenshots:
        screenshot_dir = "logs/mobile_demo"
        os.makedirs(screenshot_dir, exist_ok=True)
        filepath = os.path.join(screenshot_dir, "touch_targets_demo.png")
        pygame.image.save(screen, filepath)
        logger.info(f"Screenshot saved: {filepath}")
    
    pygame.time.wait(1000)

def demo_event_tracking(logger):
    """Demonstrate event tracking system"""
    logger.info("Demonstrating event tracking system...")
    
    # Initialize systems
    mobile_adapter = initialize_mobile_adapter(800, 600)
    event_tracker = initialize_event_tracker()
    
    # Simulate various events
    logger.info("Simulating touch events...")
    
    # Simulate touch gestures
    event_tracker.track_touch_gesture("tap", (100, 100), (100, 100), 0.2)
    event_tracker.track_touch_gesture("swipe", (100, 100), (200, 100), 0.5)
    event_tracker.track_touch_gesture("long_press", (150, 150), (150, 150), 1.0)
    
    # Simulate screen transitions
    event_tracker.track_screen_transition("welcome", "game")
    event_tracker.track_screen_transition("game", "game_over")
    
    # Simulate performance metrics
    event_tracker.track_performance_metric("fps", 60.0)
    event_tracker.track_performance_metric("frame_time", 16.7)
    
    # Simulate mobile adaptation
    event_tracker.track_mobile_adaptation((390, 844), "portrait", 0.6)
    
    # Get session summary
    summary = event_tracker.get_session_summary()
    logger.info(f"Event tracking summary: {summary}")
    
    # Export session data
    exported_file = event_tracker.export_session_data()
    logger.info(f"Event data exported to: {exported_file}")

def demo_mobile_presets(logger, capture_screenshots):
    """Demonstrate mobile presets"""
    logger.info("Demonstrating mobile presets...")
    
    presets = [
        ('iPhone SE', 375, 667),
        ('iPhone 12', 390, 844),
        ('iPad Mini', 768, 1024),
        ('Android Tablet', 800, 1280)
    ]
    
    for name, width, height in presets:
        logger.info(f"Demo preset: {name} ({width}x{height})")
        
        mobile_adapter = initialize_mobile_adapter(width, height)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(f"FreeTheSnake - {name}")
        
        # Draw preset demo
        screen.fill(LIGHT_YELLOW)
        
        # Title
        title_size = mobile_adapter.get_adaptive_font_size(28)
        font_title = pygame.font.Font(None, title_size)
        title_text = font_title.render(f"{name} Preset", True, BLACK)
        title_rect = title_text.get_rect(center=(width//2, height//8))
        screen.blit(title_text, title_rect)
        
        # Preset info
        info_size = mobile_adapter.get_adaptive_font_size(16)
        font_info = pygame.font.Font(None, info_size)
        
        info_text = f"Resolution: {width}x{height}"
        text_surface = font_info.render(info_text, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center=(width//2, height//4))
        screen.blit(text_surface, text_rect)
        
        orientation_text = f"Orientation: {mobile_adapter.get_orientation()}"
        text_surface = font_info.render(orientation_text, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center=(width//2, height//4 + 30))
        screen.blit(text_surface, text_rect)
        
        # Sample game elements at scale
        # Draw a sample snake segment
        segment_size = mobile_adapter.scale_ui_element(20)
        segment_x = width//2 - segment_size//2
        segment_y = height//2
        
        pygame.draw.rect(screen, GREEN, (segment_x, segment_y, segment_size, segment_size))
        pygame.draw.rect(screen, DARK_GREY, (segment_x, segment_y, segment_size, segment_size), 2)
        
        # Label for snake segment
        label_text = font_info.render(f"Snake segment: {segment_size}px", True, BLACK)
        label_rect = label_text.get_rect(center=(width//2, segment_y + segment_size + 20))
        screen.blit(label_text, label_rect)
        
        pygame.display.flip()
        
        if capture_screenshots:
            screenshot_dir = "logs/mobile_demo"
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"preset_{name.lower().replace(' ', '_')}.png"
            filepath = os.path.join(screenshot_dir, filename)
            pygame.image.save(screen, filepath)
            logger.info(f"Screenshot saved: {filepath}")
        
        pygame.time.wait(800)

if __name__ == "__main__":
    main()