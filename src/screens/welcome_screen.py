# welcome_screen.py
# WelcomeScreen -- thin coordinator. Drawing/state logic lives in mixin modules.
import pygame
import random
import math
import colorsys
from constants import *
from utils import draw_text, draw_animated_text

from .welcome_decorations import WelcomeDecorations
from .welcome_buttons import WelcomeButtons
from .welcome_character import WelcomeCharacter
from .welcome_title import WelcomeTitle
from .welcome_transitions import WelcomeTransitions


class WelcomeScreen(WelcomeDecorations, WelcomeButtons, WelcomeCharacter,
                    WelcomeTitle, WelcomeTransitions):
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.start_button_rect = None
        
        # Screen dimensions for positioning
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Animation variables
        self.animation_frame = 0
        self.background_colors = []
        
        # Snake animation parameters for title screen - initialize before update_dimensions
        self.title_snake_segments = []
        self.title_snake_direction = (1, 0)
        self.title_snake_speed = 2
        self.title_snake_size = 15
        self.title_snake_length = 10
        self.title_snake_color_shift = 0
        
        # Character selection - initialize before calling update_dimensions
        self.selected_character = 0
        self.character_colors = [
            (34, 139, 34),   # Green
            (65, 105, 225),  # Royal Blue
            (255, 69, 0),    # Red-Orange
            (147, 112, 219), # Medium Purple
            (255, 215, 0)    # Gold
        ]
        self.character_names = ["Slinky", "Bubbles", "Flame", "Violet", "Sunny"]
        self.character_buttons = []
        
        # Decorative elements - initialize before update_dimensions
        self.stars = []
        self.bubbles = []
        
        # Add pulse effects on title - initialize before update_dimensions
        self.title_pulse = 0
        self.title_pulse_direction = 1
        
        # Enhanced visual effects
        self.background_time = 0
        self.gradient_colors = [
            (30, 40, 80),   # Deep blue
            (40, 20, 60),   # Purple
            (20, 50, 40),   # Teal
            (50, 30, 70)    # Violet
        ]
        self.floating_particles = []
        self.glow_effects = []
        
        # Initialize mouse trail
        self.mouse_trail = []
        self.mouse_position = (0, 0)
        
        # Add a surprise element that appears randomly
        self.surprise_timer = random.randint(180, 300)  # 3-5 seconds at 60fps
        self.surprise_active = False
        self.surprise_position = (0, 0)
        self.surprise_scale = 0
        self.surprise_type = None
        self.surprise_active_time = 0
        
        # Add color splash animations
        self.color_splashes = []
        
        # Now safe to call update_dimensions
        self.update_dimensions(self.screen_width, self.screen_height)
        
        # Generate background and decorations after dimensions are set
        self.generate_background()
        self.initialize_title_snake()
        self.generate_decorations()
        
        # Sound buttons (placeholder - no actual sounds loaded)
        self.sound_button_rect = pygame.Rect(self.screen_width - 60, 20, 40, 40)
        self.sound_enabled = True
        
        # Tutorial button - helps kindergarteners learn game controls
        self.tutorial_button_rect = pygame.Rect(self.screen_width - 60, 70, 40, 40)
        
        # Transitional animations
        self.transition_active = False
        self.transition_progress = 0
        self.transition_direction = 1  # 1 for in, -1 for out
        
        # Motivational messages that appear randomly
        self.motivational_messages = [
            "You're going to do great!",
            WELCOME_MSG_LEARN_AND_FUN,
            "Your brain grows when you try new things!",
            "Everyone starts somewhere!",
            "Mistakes help us learn!"
        ]
        self.current_message = random.choice(self.motivational_messages)
        self.message_timer = 0
        
        # Add more engaging visual elements specific to kindergartners
        self.balloon_particles = []
        self.generate_balloons(12)
        
        # Add dancing letters effect
        self.dancing_letters = []
        self.setup_dancing_letters("SNAKE!")
        
        # Add decorative icons that kids respond to
        self.icon_positions = []
        self.setup_decorative_icons()

    def handle_events(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if the start button was clicked
            if self.start_button_rect.collidepoint(mouse_pos):
                self.begin_transition()
            
            # Check if sound button was clicked
            elif self.sound_button_rect.collidepoint(mouse_pos):
                self.sound_enabled = not self.sound_enabled
                
            # Check if tutorial button was clicked
            elif self.tutorial_button_rect.collidepoint(mouse_pos):
                # Would show tutorial here - for now just print
                print("Tutorial would be shown here")
                
            # Check character selection
            for i, rect in enumerate(self.character_buttons):
                if rect.collidepoint(mouse_pos):
                    self.selected_character = i
                    # Would update snake color in game_state here
                    self.game_state.snake_color = self.character_colors[i]
                    # Visual feedback for selection
                    self.animate_character_selection(i)
            
            # Always create a color splash when clicking
            self.add_color_splash(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            # Track mouse for interactive elements
            self.mouse_position = event.pos
            
            # 5% chance to create a color splash when mouse moves
            if random.random() < 0.05:
                self.add_color_splash(event.pos)

    def update(self):
        """Update animations and states."""
        # Increment animation frame
        self.animation_frame += 1
        
        # Update background animation time
        self.background_time += 0.016  # Assuming 60 FPS
        
        # Update title snake movement
        self.update_title_snake()
        
        # Update decorative elements
        self.update_decorations()
        
        # Update transition if active
        if self.transition_active:
            self.update_transition()
            
        # Cycle motivational messages
        self.message_timer += 1
        if self.message_timer > 300:  # Change message every 5 seconds (at 60 FPS)
            self.current_message = random.choice(self.motivational_messages)
            self.message_timer = 0
        
        # Update balloon particles
        for balloon in self.balloon_particles:
            # Move balloons upward
            balloon["pos"][0] += balloon["vel"][0]
            balloon["pos"][1] += balloon["vel"][1]
            
            # Add slight wobble
            balloon["pos"][0] += math.sin(self.animation_frame * 0.03) * 0.5
            
            # Rotate balloons
            balloon["rotation"] += balloon["rotation_speed"]
            
            # Reset balloons that float off the top
            if balloon["pos"][1] < -balloon["size"] - balloon["string_length"]:
                balloon["pos"][0] = random.randint(0, self.screen_width)
                balloon["pos"][1] = self.screen_height + balloon["size"]
        
        # Update dancing letters
        for letter in self.dancing_letters:
            letter["phase"] += letter["speed"]
            letter["offset_y"] = math.sin(letter["phase"]) * letter["amplitude"]
            
            # Pulse scale occasionally
            if random.random() < 0.01:  # 1% chance each frame
                letter["scale"] = 1.2
            else:
                letter["scale"] = max(1.0, letter["scale"] - 0.01)
        
        # Update decorative icons
        for icon in self.icon_positions:
            icon["angle"] += icon["spin_speed"]
            icon["pulse"] = (icon["pulse"] + icon["pulse_speed"]) % (math.pi * 2)
        
        # Update title pulse
        if self.title_pulse_direction > 0:
            self.title_pulse = min(0.15, self.title_pulse + 0.005)
            if self.title_pulse >= 0.15:
                self.title_pulse_direction = -1
        else:
            self.title_pulse = max(0, self.title_pulse - 0.005)
            if self.title_pulse <= 0:
                self.title_pulse_direction = 1
        
        # Update mouse trail
        self.mouse_trail.append(self.mouse_position)
        if len(self.mouse_trail) > 15:  # Keep only recent positions
            self.mouse_trail.pop(0)
            
        # Update surprise element
        if not self.surprise_active:
            self.surprise_timer -= 1
            if self.surprise_timer <= 0:
                self.trigger_surprise()
        else:
            self.update_surprise()
            
        # Update color splashes
        new_splashes = []
        for splash in self.color_splashes:
            splash["radius"] += splash["growth_speed"]
            
            # Fade out as it grows
            if splash["radius"] > splash["max_radius"] * 0.6:
                splash["alpha"] = max(0, splash["alpha"] - 8)
                
            # Keep if still visible
            if splash["radius"] < splash["max_radius"] and splash["alpha"] > 0:
                new_splashes.append(splash)
                
        self.color_splashes = new_splashes

    def draw(self):
        """Draw the welcome screen with enhanced visual effects."""
        # Draw animated gradient background
        self.draw_enhanced_background()
        
        # Draw floating particles
        self.draw_floating_particles()
        
        # Draw decorative elements
        self.draw_decorations()
        
        # Draw the animated title snake
        self.draw_title_snake()
        
        # Draw enhanced title with glow effects
        try:
            self.draw_enhanced_title()
        except Exception as e:
            # Fallback to basic title drawing
            title_y = 100
            from utils import draw_text, draw_animated_text
            draw_text(
                self.screen, 
                "Kindergarten Snake!",
                (self.screen_width // 2, title_y), 
                self.title_font, 
                WHITE, 
                center=True, 
                shadow=True,
                shadow_color=BLACK
            )
            
            # Draw the motivational message with animation
            draw_animated_text(
                self.screen, 
                getattr(self, 'current_message', WELCOME_MSG_LEARN_AND_FUN),
                (self.screen_width // 2, title_y + 80), 
                self.subtitle_font, 
                YELLOW, 
                getattr(self, 'animation_frame', 0)
            )
        
        # Draw character selection with improved visuals
        try:
            self.draw_character_selection()
        except Exception as e:
            # Fallback to basic character selection
            char_y = 200
            from utils import draw_text
            draw_text(self.screen, "Choose Your Snake:", (self.screen_width // 2, char_y), 
                     self.subtitle_font, WHITE, center=True)
        
        # Draw enhanced start button
        try:
            self.draw_enhanced_start_button()
        except Exception as e:
            # Fallback to basic start button
            if hasattr(self, 'start_button_rect') and self.start_button_rect:
                pygame.draw.rect(self.screen, BRIGHT_GREEN, self.start_button_rect)
                pygame.draw.rect(self.screen, BLACK, self.start_button_rect, 2)
                
                font = FONT_MEDIUM or pygame.font.Font(None, 36)
                text_surface = font.render("Start!", True, WHITE)
                text_rect = text_surface.get_rect(center=self.start_button_rect.center)
                self.screen.blit(text_surface, text_rect)
        
        # Draw utility buttons
        try:
            self.draw_utility_buttons()
        except Exception as e:
            # Fallback - skip utility buttons if they fail
            pass
        
        # Draw mouse trail effect
        try:
            self.draw_mouse_trail()
        except Exception as e:
            # Fallback - skip mouse trail if it fails
            pass

