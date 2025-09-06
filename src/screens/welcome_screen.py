import pygame
import random
import math
import colorsys
from constants import *
from utils import draw_text, get_cage_rect, draw_animated_text

class WelcomeScreen:
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
            "Ready to learn and have fun?",
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

    @property
    def title_font(self):
        """Get the title font, ensuring it's initialized."""
        return FONT_TITLE
    
    @property
    def subtitle_font(self):
        """Get the subtitle font, ensuring it's initialized."""
        return FONT_MEDIUM

    def setup_additional_properties(self):
        """Setup additional properties that were being initialized after property methods."""
        # All necessary initializations have been moved to the proper location in __init__
        pass

    def update_dimensions(self, width, height):
        """Update screen dimensions when window is resized."""
        self.screen_width = width
        self.screen_height = height
        
        # Get scaling factors based on new dimensions
        from utils import get_scale_factors
        self.scale_factors = get_scale_factors(width, height)
        
        # Scale UI elements based on screen size
        button_width = int(200 * self.scale_factors['uniform'])
        button_height = int(50 * self.scale_factors['uniform'])
        
        # Position elements relative to screen dimensions
        start_button_x = (width // 2) - (button_width // 2)
        start_button_y = height // 2 + int(50 * self.scale_factors['y'])
        
        self.start_button_rect = pygame.Rect(
            start_button_x, start_button_y, button_width, button_height
        )
        
        # Scale and position utility buttons
        button_size = int(40 * self.scale_factors['uniform'])
        self.sound_button_rect = pygame.Rect(width - button_size - int(20 * self.scale_factors['x']), 
                                           int(20 * self.scale_factors['y']), 
                                           button_size, button_size)
                                           
        self.tutorial_button_rect = pygame.Rect(width - button_size - int(20 * self.scale_factors['x']), 
                                              int(70 * self.scale_factors['y']), 
                                              button_size, button_size)
        
        # Update snake properties for title animation
        self.title_snake_size = int(15 * self.scale_factors['uniform'])
        self.title_snake_speed = max(1, int(2 * self.scale_factors['uniform']))
        
        # Reset and regenerate all screen elements
        self.setup_character_buttons()
        self.generate_background()
        self.generate_decorations()
        self.initialize_title_snake()

    def generate_background(self):
        """Generate a colorful gradient background."""
        height = self.screen_height
        self.background_colors = []
        for y in range(0, height, 2):
            # Create a gentle rainbow gradient
            hue = (y / height) * 0.3 + 0.5  # Range from 0.5 to 0.8 (blue to purple-ish)
            saturation = 0.6
            value = 0.8
            # Convert HSV to RGB
            h_i = int(hue * 6)
            f = hue * 6 - h_i
            p = value * (1 - saturation)
            q = value * (1 - f * saturation)
            t = value * (1 - (1 - f) * saturation)
            
            if h_i == 0:
                r, g, b = value, t, p
            elif h_i == 1:
                r, g, b = q, value, p
            elif h_i == 2:
                r, g, b = p, value, t
            elif h_i == 3:
                r, g, b = p, q, value
            elif h_i == 4:
                r, g, b = t, p, value
            else:
                r, g, b = value, p, q
                
            self.background_colors.append((int(r * 255), int(g * 255), int(b * 255)))

    def initialize_title_snake(self):
        """Initialize the animated snake for the title screen."""
        # Start the snake in the middle left of the screen
        start_x = self.screen_width // 4
        start_y = self.screen_height // 3
        
        # Create initial segments
        self.title_snake_segments = []
        for i in range(self.title_snake_length):
            self.title_snake_segments.append(
                (start_x - i * self.title_snake_size, start_y)
            )

    def generate_decorations(self):
        """Generate decorative stars and bubbles."""
        # Stars - create wonder and magic
        self.stars = []
        for _ in range(30):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height // 3)  # Keep stars in upper part
            size = random.uniform(1, 3)
            pulse_speed = random.uniform(0.05, 0.1)
            self.stars.append({
                'pos': (x, y),
                'size': size,
                'base_size': size,
                'pulse_speed': pulse_speed,
                'angle': random.uniform(0, 6.28)  # Random initial angle
            })
        
        # Bubbles - create playful atmosphere
        self.bubbles = []
        for _ in range(15):
            x = random.randint(0, self.screen_width)
            y = random.randint(self.screen_height // 2, self.screen_height)
            size = random.randint(10, 30)
            speed = random.uniform(0.5, 1.5)
            self.bubbles.append({
                'pos': (x, y),
                'size': size,
                'speed': speed,
                'wobble': random.uniform(0, 6.28)
            })

    def setup_character_buttons(self):
        """Set up character selection buttons."""
        self.character_buttons = []
        button_size = 60
        spacing = 10
        total_width = len(self.character_colors) * (button_size + spacing) - spacing
        start_x = (self.screen_width - total_width) // 2
        
        for i, color in enumerate(self.character_colors):
            button_rect = pygame.Rect(
                start_x + i * (button_size + spacing),
                self.screen_height // 2 - 80,
                button_size,
                button_size
            )
            self.character_buttons.append(button_rect)

    def generate_balloons(self, count):
        """Generate floating balloon particles."""
        self.balloon_particles = []
        for _ in range(count):
            x = random.randint(0, self.screen_width)
            y = random.randint(self.screen_height, self.screen_height + 200)
            
            balloon = {
                "pos": [x, y],
                "vel": [random.uniform(-0.3, 0.3), random.uniform(-1.5, -0.7)],
                "size": random.randint(30, 50),
                "color": random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]),
                "rotation": random.uniform(0, math.pi * 2),
                "rotation_speed": random.uniform(-0.02, 0.02),
                "string_length": random.randint(20, 40)
            }
            self.balloon_particles.append(balloon)

    def setup_dancing_letters(self, text):
        """Setup dancing letters animation for title."""
        self.dancing_letters = []
        x_offset = self.screen_width // 2 - (len(text) * 30) // 2
        
        for i, letter in enumerate(text):
            self.dancing_letters.append({
                "letter": letter,
                "base_x": x_offset + i * 30,
                "y": self.screen_height // 4 + 40,
                "offset_y": 0,
                "phase": random.uniform(0, math.pi * 2),
                "speed": random.uniform(0.05, 0.1),
                "amplitude": random.uniform(5, 10),
                "scale": 1.0,
                "color": (
                    random.randint(200, 255),
                    random.randint(200, 255),
                    random.randint(100, 255)
                )
            })

    def setup_decorative_icons(self):
        """Setup decorative icons around the screen."""
        self.icon_positions = []
        icons = ["🍎", "🎈", "🌟", "🐢", "🦋", "🌈"]
        
        # Position icons around the edge of the screen
        for i in range(8):
            angle = i * math.pi / 4
            distance = min(self.screen_width, self.screen_height) * 0.4
            x = self.screen_width // 2 + distance * math.cos(angle)
            y = self.screen_height // 2 + distance * math.sin(angle)
            
            self.icon_positions.append({
                "icon": random.choice(icons),
                "pos": [x, y],
                "angle": 0,
                "spin_speed": random.uniform(-0.03, 0.03),
                "pulse": 0,
                "pulse_speed": random.uniform(0.02, 0.04)
            })

    def add_color_splash(self, position, color=None):
        """Add a color splash animation at the given position."""
        if color is None:
            color = random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE])
            
        self.color_splashes.append({
            "pos": position,
            "color": color,
            "radius": 0,
            "max_radius": random.randint(30, 80),
            "growth_speed": random.randint(2, 5),
            "alpha": 255
        })

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

    def begin_transition(self):
        """Start the transition animation to the next screen."""
        self.transition_active = True
        self.transition_progress = 0
        self.transition_direction = 1

    def animate_character_selection(self, character_index):
        """Animate the character selection with a burst effect."""
        # In a full implementation, this would create particle effects
        # For now, just update the selected character
        self.selected_character = character_index

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

    def trigger_surprise(self):
        """Trigger a surprise animation element."""
        self.surprise_active = True
        self.surprise_position = (
            random.randint(100, self.screen_width - 100),
            random.randint(100, self.screen_height - 100)
        )
        
        # Choose a surprise type
        self.surprise_type = random.choice([
            "star", "rainbow", "butterfly", "balloon_pop", "flower"
        ])
        
        self.surprise_scale = 0.1
        self.surprise_active_time = 0

    def update_surprise(self):
        """Update the active surprise element."""
        self.surprise_active_time += 1
        
        # Grow quickly, then linger, then shrink
        if self.surprise_active_time < 20:
            self.surprise_scale = min(1.0, self.surprise_scale + 0.05)
        elif self.surprise_active_time > 60:
            self.surprise_scale -= 0.05
            if self.surprise_scale <= 0:
                self.surprise_active = False
                self.surprise_timer = random.randint(180, 300)

    def update_title_snake(self):
        """Update the animated title snake."""
        # Move the snake head
        head_x, head_y = self.title_snake_segments[0]
        
        # Change direction occasionally to create interesting patterns
        if random.random() < 0.02:
            options = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            opposite = (-self.title_snake_direction[0], -self.title_snake_direction[1])
            if opposite in options:
                options.remove(opposite)  # Don't allow reversing
            self.title_snake_direction = random.choice(options)
            
        # Move in current direction
        new_head_x = head_x + self.title_snake_direction[0] * self.title_snake_speed
        new_head_y = head_y + self.title_snake_direction[1] * self.title_snake_speed
        
        # Bounce off edges
        buffer = 50  # Keep away from absolute edge
        if new_head_x < buffer:
            new_head_x = buffer
            self.title_snake_direction = (1, self.title_snake_direction[1])
        elif new_head_x > self.screen_width - buffer:
            new_head_x = self.screen_width - buffer
            self.title_snake_direction = (-1, self.title_snake_direction[1])
            
        if new_head_y < buffer:
            new_head_y = buffer
            self.title_snake_direction = (self.title_snake_direction[0], 1)
        elif new_head_y > self.screen_height - buffer:
            new_head_y = self.screen_height - buffer
            self.title_snake_direction = (self.title_snake_direction[0], -1)
            
        # Add new head
        self.title_snake_segments.insert(0, (new_head_x, new_head_y))
        
        # Remove tail to maintain length
        while len(self.title_snake_segments) > self.title_snake_length:
            self.title_snake_segments.pop()
            
        # Update color shift animation
        self.title_snake_color_shift = (self.title_snake_color_shift + 1) % 360

    def update_decorations(self):
        """Update animated decorative elements."""
        # Update stars
        for star in self.stars:
            star['angle'] += star['pulse_speed']
            pulse_factor = 0.5 + 0.5 * math.sin(star['angle'])
            star['size'] = star['base_size'] * (1 + pulse_factor)
            
        # Update rising bubbles
        for bubble in self.bubbles:
            bubble['pos'] = (
                bubble['pos'][0] + math.sin(bubble['wobble']) * 0.5,
                bubble['pos'][1] - bubble['speed']
            )
            bubble['wobble'] += 0.05
            
            # Reset bubbles that rise off screen
            if bubble['pos'][1] < -bubble['size']:
                bubble['pos'] = (
                    random.randint(0, self.screen_width),
                    self.screen_height + bubble['size']
                )
                bubble['wobble'] = random.uniform(0, 6.28)

    def update_transition(self):
        """Update the transition animation."""
        self.transition_progress += 0.02 * self.transition_direction
        
        if self.transition_progress >= 1.0:
            # Transition complete - move to next screen
            self.game_state.current_state = STATE_LEVEL_SELECT
            self.transition_active = False
            self.transition_progress = 0

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
        self.draw_enhanced_title()
        
        # Draw character selection with improved visuals
        self.draw_character_selection()
        
        # Draw enhanced start button
        self.draw_enhanced_start_button()
        
        # Draw utility buttons
        self.draw_utility_buttons()
        
        # Draw mouse trail effect
        self.draw_mouse_trail()

    def draw_enhanced_background(self):
        """Draw an animated gradient background."""
        try:
            from ui.enhanced_graphics import create_animated_background
            animated_bg = create_animated_background(
                self.screen_width, 
                self.screen_height, 
                self.background_time, 
                self.gradient_colors
            )
            self.screen.blit(animated_bg, (0, 0))
        except ImportError:
            # Fallback to original gradient
            for y in range(0, self.screen_height, 2):
                if y < len(self.background_colors):
                    pygame.draw.line(
                        self.screen,
                        self.background_colors[y],
                        (0, y),
                        (self.screen_width, y)
                    )

    def draw_floating_particles(self):
        """Draw floating decorative particles."""
        # Add new particles occasionally
        if random.random() < 0.05:  # 5% chance per frame
            self.floating_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height + 10,
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(2, 6),
                'color': random.choice([YELLOW, WHITE, BRIGHT_CYAN, LIGHT_YELLOW]),
                'alpha': 255,
                'rotation': 0,
                'rotation_speed': random.uniform(-0.1, 0.1)
            })
        
        # Update and draw particles
        particles_to_keep = []
        for particle in self.floating_particles:
            particle['y'] -= particle['speed']
            particle['rotation'] += particle['rotation_speed']
            particle['alpha'] = max(0, particle['alpha'] - 1)
            
            if particle['y'] > -10 and particle['alpha'] > 0:
                # Draw particle with alpha
                try:
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    color_with_alpha = (*particle['color'], particle['alpha'])
                    pygame.draw.circle(particle_surface, color_with_alpha, 
                                     (particle['size'], particle['size']), particle['size'])
                    
                    # Rotate the particle
                    rotated_surface = pygame.transform.rotate(particle_surface, math.degrees(particle['rotation']))
                    rot_rect = rotated_surface.get_rect(center=(particle['x'], particle['y']))
                    self.screen.blit(rotated_surface, rot_rect)
                except:
                    # Fallback to simple circle
                    pygame.draw.circle(self.screen, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), particle['size'])
                
                particles_to_keep.append(particle)
        
        self.floating_particles = particles_to_keep

    def draw_enhanced_start_button(self):
        """Draw the start button with enhanced visual effects."""
        if self.start_button_rect:
            # Draw button shadow
            shadow_rect = self.start_button_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            try:
                shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 100))
                self.screen.blit(shadow_surface, shadow_rect)
            except:
                pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=15)
            
            # Draw button with gradient effect
            button_color = BRIGHT_GREEN
            if hasattr(self, 'start_button_hovered') and self.start_button_hovered:
                button_color = (0, 255, 100)  # Brighter green on hover
                # Add glow effect
                glow_rect = self.start_button_rect.inflate(10, 10)
                try:
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    glow_surface.fill((*button_color, 50))
                    self.screen.blit(glow_surface, glow_rect)
                except:
                    pass
            
            # Draw main button
            pygame.draw.rect(self.screen, button_color, self.start_button_rect, border_radius=15)
            pygame.draw.rect(self.screen, WHITE, self.start_button_rect, width=3, border_radius=15)
            
            # Draw button text with shadow
            button_text = "Start!"
            button_font = self.button_font or FONT_MEDIUM
            
            # Text shadow
            shadow_surface = button_font.render(button_text, True, BLACK)
            shadow_rect = shadow_surface.get_rect(center=(self.start_button_rect.centerx + 2, self.start_button_rect.centery + 2))
            self.screen.blit(shadow_surface, shadow_rect)
            
            # Main text
            text_surface = button_font.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.start_button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def draw_utility_buttons(self):
        """Draw utility buttons with enhanced visuals."""
        # Sound button
        if hasattr(self, 'sound_button_rect'):
            pygame.draw.rect(self.screen, GREY, self.sound_button_rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, self.sound_button_rect, width=2, border_radius=8)
            
            # Draw sound icon
            self.draw_sound_icon(self.sound_button_rect.centerx, self.sound_button_rect.centery)
        
        # Tutorial button
        if hasattr(self, 'tutorial_button_rect'):
            pygame.draw.rect(self.screen, GREY, self.tutorial_button_rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, self.tutorial_button_rect, width=2, border_radius=8)
            
            # Draw question mark
            font = FONT_SMALL or pygame.font.Font(None, 24)
            text_surface = font.render("?", True, BLACK)
            text_rect = text_surface.get_rect(center=self.tutorial_button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Draw character selection
        self.draw_character_selection()
        
        # Draw the start button with a pulsing effect
        button_scale = 1.0 + 0.05 * math.sin(self.animation_frame * 0.1)
        scaled_width = int(self.start_button_rect.width * button_scale)
        scaled_height = int(self.start_button_rect.height * button_scale)
        scaled_x = self.start_button_rect.centerx - scaled_width // 2
        scaled_y = self.start_button_rect.centery - scaled_height // 2
        
        scaled_button_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        pygame.draw.rect(self.screen, YELLOW, scaled_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, scaled_button_rect, 3, border_radius=10)
        
        draw_text(
            self.screen, 
            "Start!", 
            (scaled_button_rect.centerx, scaled_button_rect.centery), 
            self.subtitle_font, 
            BLACK, 
            center=True
        )
        
        # Draw sound toggle button
        sound_color = GREEN if self.sound_enabled else RED
        pygame.draw.rect(self.screen, sound_color, self.sound_button_rect, border_radius=5)
        
        # Draw sound icon
        self.draw_sound_icon(self.sound_button_rect.centerx, self.sound_button_rect.centery)
        
        # Draw tutorial button
        pygame.draw.rect(self.screen, BLUE, self.tutorial_button_rect, border_radius=5)
        draw_text(
            self.screen, 
            "?", 
            (self.tutorial_button_rect.centerx, self.tutorial_button_rect.centery), 
            self.subtitle_font, 
            WHITE, 
            center=True
        )
        
        # Draw transition effect if active
        if self.transition_active:
            self.draw_transition()
        
        # Draw mouse trail first (behind other elements)
        self.draw_mouse_trail()
        
        # Draw color splashes
        self.draw_color_splashes()
        
        # Draw decorative balloons
        self.draw_balloons()
        
        # Draw the title with enhanced pulsing and dancing letters
        self.draw_enhanced_title()
        
        # Draw decorative icons
        self.draw_decorative_icons()
        
        # Draw surprise element if active
        if self.surprise_active:
            self.draw_surprise()

    def draw_decorations(self):
        """Draw decorative stars and bubbles."""
        # Draw stars with pulsing effect
        for star in self.stars:
            pygame.draw.circle(
                self.screen,
                (255, 255, 200),  # Light yellow
                (int(star['pos'][0]), int(star['pos'][1])),
                int(star['size'])
            )
            
        # Draw bubbles
        for bubble in self.bubbles:
            pygame.draw.circle(
                self.screen,
                (200, 200, 255, 100),  # Semi-transparent light blue
                (int(bubble['pos'][0]), int(bubble['pos'][1])),
                int(bubble['size']),
                1  # Draw as outline
            )
            # Draw highlight on bubble for 3D effect - children respond to depth cues
            highlight_size = bubble['size'] * 0.3
            highlight_offset = bubble['size'] * 0.2
            pygame.draw.circle(
                self.screen,
                (230, 230, 255),  # White-ish highlight
                (int(bubble['pos'][0] - highlight_offset), 
                 int(bubble['pos'][1] - highlight_offset)),
                int(highlight_size)
            )

    def draw_title_snake(self):
        """Draw the animated snake in the title screen."""
        # Create rainbow effect by cycling through hues
        for i, segment in enumerate(self.title_snake_segments):
            # Offset hue by segment index and animation frame
            hue = (self.title_snake_color_shift + i * 10) % 360 / 360.0
            
            # Convert HSV to RGB
            c = hue * 6.0
            x = (1 - abs(c % 2 - 1))
            r, g, b = 0, 0, 0
            
            if 0 <= c < 1: r, g, b = 1, x, 0
            elif 1 <= c < 2: r, g, b = x, 1, 0
            elif 2 <= c < 3: r, g, b = 0, 1, x
            elif 3 <= c < 4: r, g, b = 0, x, 1
            elif 4 <= c < 5: r, g, b = x, 0, 1
            else: r, g, b = 1, 0, x
            
            color = (int(r * 255), int(g * 255), int(b * 255))
            
            # Draw segment
            pygame.draw.circle(
                self.screen,
                color,
                (int(segment[0]), int(segment[1])),
                self.title_snake_size
            )
            
            # Draw eyes on head segment
            if i == 0:
                # Draw white eye backgrounds
                eye_offset = 4
                pygame.draw.circle(
                    self.screen,
                    WHITE,
                    (int(segment[0]) + eye_offset, int(segment[1]) - eye_offset),
                    self.title_snake_size // 3
                )
                pygame.draw.circle(
                    self.screen,
                    WHITE,
                    (int(segment[0]) - eye_offset, int(segment[1]) - eye_offset),
                    self.title_snake_size // 3
                )
                
                # Draw black pupils with blinking
                if self.animation_frame % 120 < 110:  # Eyes open most of the time
                    pygame.draw.circle(
                        self.screen,
                        BLACK,
                        (int(segment[0]) + eye_offset, int(segment[1]) - eye_offset),
                        self.title_snake_size // 6
                    )
                    pygame.draw.circle(
                        self.screen,
                        BLACK,
                        (int(segment[0]) - eye_offset, int(segment[1]) - eye_offset),
                        self.title_snake_size // 6
                    )
                else:  # Occasionally blink
                    eye_y = int(segment[1]) - eye_offset
                    left_eye_x = int(segment[0]) - eye_offset
                    right_eye_x = int(segment[0]) + eye_offset
                    eye_size = self.title_snake_size // 3
                    
                    pygame.draw.line(
                        self.screen,
                        BLACK,
                        (left_eye_x - eye_size, eye_y),
                        (left_eye_x + eye_size, eye_y),
                        2
                    )
                    pygame.draw.line(
                        self.screen,
                        BLACK,
                        (right_eye_x - eye_size, eye_y),
                        (right_eye_x + eye_size, eye_y),
                        2
                    )
                
                # Draw a smile - friendly expressions engage children
                mouth_y = int(segment[1]) + 5
                pygame.draw.arc(
                    self.screen,
                    BLACK,
                    (int(segment[0]) - 7, mouth_y - 3, 14, 6),
                    0, math.pi,
                    2
                )

    def draw_character_selection(self):
        """Draw character selection buttons."""
        # Draw section title
        draw_text(
            self.screen, 
            "Choose Your Snake:", 
            (self.screen_width // 2, self.character_buttons[0].top - 30), 
            FONT_MEDIUM, 
            WHITE, 
            center=True
        )
        
        # Draw character buttons
        for i, rect in enumerate(self.character_buttons):
            # Draw button background
            button_color = self.character_colors[i]
            highlight = 2 if i == self.selected_character else 1
            
            # Create a pulsing effect for the selected character
            if i == self.selected_character:
                pulse = 1.0 + 0.1 * math.sin(self.animation_frame * 0.2)
                scaled_size = int(rect.width * pulse)
                offset = (scaled_size - rect.width) // 2
                pygame.draw.rect(
                    self.screen,
                    button_color,
                    (rect.x - offset, rect.y - offset, scaled_size, scaled_size),
                    border_radius=10
                )
                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (rect.x - offset, rect.y - offset, scaled_size, scaled_size),
                    3,
                    border_radius=10
                )
            else:
                pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
                pygame.draw.rect(self.screen, BLACK, rect, 1, border_radius=10)
            
            # Draw simple snake face on the button
            center_x, center_y = rect.centerx, rect.centery
            
            # Eyes
            eye_offset = rect.width // 5
            pygame.draw.circle(self.screen, WHITE, (center_x - eye_offset, center_y - 5), 5)
            pygame.draw.circle(self.screen, WHITE, (center_x + eye_offset, center_y - 5), 5)
            pygame.draw.circle(self.screen, BLACK, (center_x - eye_offset, center_y - 5), 2)
            pygame.draw.circle(self.screen, BLACK, (center_x + eye_offset, center_y - 5), 2)
            
            # Smile
            pygame.draw.arc(
                self.screen, 
                BLACK if i != self.selected_character else WHITE, 
                (center_x - 10, center_y, 20, 10), 
                0, math.pi, 
                2
            )
            
            # Draw character name
            draw_text(
                self.screen, 
                self.character_names[i], 
                (rect.centerx, rect.bottom + 15), 
                FONT_SMALL, 
                WHITE, 
                center=True
            )

    def draw_sound_icon(self, x, y):
        """Draw a simple sound icon."""
        # Draw speaker
        pygame.draw.rect(self.screen, BLACK, (x - 7, y - 5, 4, 10))
        
        # Draw sound waves or X
        if self.sound_enabled:
            # Draw sound waves
            for i in range(1, 3):
                pygame.draw.arc(
                    self.screen,
                    BLACK,
                    (x - 5, y - i * 5, i * 10, i * 10),
                    -math.pi / 3,
                    math.pi / 3,
                    2
                )
        else:
            # Draw X over speaker
            pygame.draw.line(self.screen, BLACK, (x + 5, y - 5), (x + 10, y + 5), 2)
            pygame.draw.line(self.screen, BLACK, (x + 10, y - 5), (x + 5, y + 5), 2)

    def draw_transition(self):
        """Draw transition animation effect."""
        # Create a radial wipe effect
        radius = int(self.transition_progress * math.sqrt(self.screen_width**2 + self.screen_height**2))
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        # Fill with semi-transparent black
        overlay.fill((0, 0, 0, 200))
        
        # Create a circle mask that grows from the center
        pygame.draw.circle(
            overlay,
            (0, 0, 0, 0),  # Transparent
            (self.screen_width // 2, self.screen_height // 2),
            radius
        )
        
        # Draw the overlay
        self.screen.blit(overlay, (0, 0))

    def draw_mouse_trail(self):
        """Draw trail that follows the mouse cursor."""
        if len(self.mouse_trail) < 2:
            return
            
        for i in range(1, len(self.mouse_trail)):
            # Calculate alpha and thickness based on position in trail
            alpha = 255 * (i / len(self.mouse_trail))
            thickness = max(1, int(i / 3))
            
            # Calculate color - rainbow effect
            hue = (self.animation_frame + i * 10) % 360 / 360.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            color = (int(r * 255), int(g * 255), int(b * 255))
            
            # Draw line segment
            pygame.draw.line(
                self.screen,
                color,
                self.mouse_trail[i-1],
                self.mouse_trail[i],
                thickness
            )
            
            # Draw small circle at each point
            pygame.draw.circle(
                self.screen,
                color,
                self.mouse_trail[i],
                thickness // 2 + 1
            )

    def draw_color_splashes(self):
        """Draw color splash animations."""
        for splash in self.color_splashes:
            # Create a surface with per-pixel alpha
            surf_size = int(splash["radius"] * 2) + 2
            surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
            
            # Draw filled and outlined circle with fade-out
            color_with_alpha = (*splash["color"][:3], splash["alpha"])
            pygame.draw.circle(
                surf,
                color_with_alpha,
                (surf_size // 2, surf_size // 2),
                splash["radius"]
            )
            
            # Draw outline
            outline_alpha = min(255, splash["alpha"] + 50)
            outline_color = (*splash["color"][:3], outline_alpha)
            pygame.draw.circle(
                surf,
                outline_color,
                (surf_size // 2, surf_size // 2),
                splash["radius"],
                max(1, int(splash["radius"] / 10))
            )
            
            # Position and draw
            pos = (int(splash["pos"][0] - surf_size // 2),
                   int(splash["pos"][1] - surf_size // 2))
            self.screen.blit(surf, pos)

    def draw_balloons(self):
        """Draw decorative balloons."""
        for balloon in self.balloon_particles:
            # Draw the balloon
            pygame.draw.circle(
                self.screen,
                balloon["color"],
                (int(balloon["pos"][0]), int(balloon["pos"][1])),
                balloon["size"]
            )
            
            # Draw the highlight on the balloon
            highlight_size = balloon["size"] * 0.3
            highlight_x = balloon["pos"][0] - balloon["size"] * 0.3
            highlight_y = balloon["pos"][1] - balloon["size"] * 0.3
            pygame.draw.circle(
                self.screen,
                (255, 255, 255, 180),  # Semi-transparent white
                (int(highlight_x), int(highlight_y)),
                int(highlight_size)
            )
            
            # Draw the balloon string
            string_end_x = balloon["pos"][0]
            string_end_y = balloon["pos"][1] + balloon["size"] + balloon["string_length"]
            
            # Make string wavy
            points = []
            num_points = 10
            for i in range(num_points + 1):
                t = i / num_points
                x = balloon["pos"][0] + math.sin(t * math.pi * 2 + self.animation_frame * 0.05) * (balloon["size"] / 3)
                y = balloon["pos"][1] + balloon["size"] + t * balloon["string_length"]
                points.append((int(x), int(y)))
                
            # Draw segmented string
            if len(points) > 1:
                pygame.draw.lines(self.screen, WHITE, False, points, 1)

    def draw_enhanced_title(self):
        """Draw title with enhanced animation effects."""
        # First draw the dancing letters
        for letter in self.dancing_letters:
            # Calculate size with pulsing effect
            size = int(72 * letter["scale"] * (1.0 + self.title_pulse))
            
            try:
                letter_font = pygame.font.SysFont("Arial", size, bold=True)
                letter_surf = letter_font.render(letter["letter"], True, letter["color"])
                
                # Position with vertical bounce
                x = letter["base_x"]
                y = letter["y"] + letter["offset_y"]
                
                letter_rect = letter_surf.get_rect(center=(x, y))
                
                # Draw shadow first
                shadow_rect = letter_rect.copy()
                shadow_rect.x += 3
                shadow_rect.y += 3
                shadow_surf = letter_font.render(letter["letter"], True, BLACK)
                self.screen.blit(shadow_surf, shadow_rect)
                
                # Draw the letter
                self.screen.blit(letter_surf, letter_rect)
                
            except Exception as e:
                print(f"Error rendering letter: {e}")

        # Draw the title text with enhanced effects
        title_y = 100
        title_scale = 1.0 + self.title_pulse
        title_size = int(72 * title_scale)
        
        try:
            title_font = pygame.font.SysFont("Arial", title_size, bold=True)
            title_text = title_font.render("Kindergarten", True, WHITE)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, title_y))
            
            # Draw with glow effect
            glow_size = 10
            glow_surf = pygame.Surface(
                (title_rect.width + glow_size * 2, title_rect.height + glow_size * 2),
                pygame.SRCALPHA
            )
            
            # Draw multiple times with increasing size for glow
            for i in range(3):
                glow_color = (50, 50, 255, 100 - i * 30)  # Blue glow with decreasing alpha
                pygame.draw.rect(
                    glow_surf,
                    glow_color,
                    (glow_size - i * 2, glow_size - i * 2,
                     title_rect.width + i * 4, title_rect.height + i * 4),
                    border_radius=10
                )
            
            # Draw text to glow surface
            glow_surf.blit(title_text, (glow_size, glow_size))
            
            # Draw glow surface to screen
            glow_rect = glow_surf.get_rect(center=(self.screen_width // 2, title_y))
            self.screen.blit(glow_surf, glow_rect)
            
        except Exception as e:
            # Fallback if fancy rendering fails
            draw_text(
                self.screen, 
                "Kindergarten Snake!",
                (self.screen_width // 2, title_y), 
                self.title_font, 
                WHITE, 
                center=True, 
                shadow=True
            )

    def draw_decorative_icons(self):
        """Draw decorative icons around the screen."""
        for icon in self.icon_positions:
            # Calculate scale with pulsing
            scale = 1.0 + 0.2 * math.sin(icon["pulse"])
            size = int(36 * scale)
            
            try:
                # Render the icon
                icon_font = pygame.font.SysFont("Arial", size)
                icon_surf = icon_font.render(icon["icon"], True, WHITE)
                
                # Rotate the icon
                rotated_surf = pygame.transform.rotate(
                    icon_surf, 
                    icon["angle"] * (180 / math.pi)
                )
                
                # Position the icon
                rect = rotated_surf.get_rect(center=icon["pos"])
                self.screen.blit(rotated_surf, rect)
                
                # Add a pulsing glow sometimes
                if random.random() < 0.05:  # 5% chance per frame per icon
                    glow_radius = int(size * 0.7)
                    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    
                    pygame.draw.circle(
                        glow_surf,
                        (255, 255, 255, 50),  # White glow
                        (glow_radius, glow_radius),
                        glow_radius
                    )
                    
                    glow_pos = (
                        int(icon["pos"][0] - glow_radius),
                        int(icon["pos"][1] - glow_radius)
                    )
                    self.screen.blit(glow_surf, glow_pos, special_flags=pygame.BLEND_ADD)
                
            except Exception as e:
                print(f"Error rendering icon: {e}")

    def draw_surprise(self):
        """Draw the surprise animation element."""
        # Scale based on animation state
        size = int(80 * self.surprise_scale)
        if size <= 0:
            return
            
        x, y = self.surprise_position
        
        if self.surprise_type == "star":
            # Draw a colorful star
            points = []
            num_points = 10
            
            for i in range(num_points):
                angle = math.pi/2 + i * (2*math.pi/num_points)
                radius = size if i % 2 == 0 else size * 0.4
                point_x = x + radius * math.cos(angle)
                point_y = y + radius * math.sin(angle)
                points.append((point_x, point_y))
            
            # Create gradient fill
            gradient_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            
            for i in range(size):
                progress = i / size
                r = int(255 * progress)
                g = int(255 * (1-progress))
                b = int(128 + 127 * math.sin(progress * math.pi))
                
                pygame.draw.circle(
                    gradient_surf,
                    (r, g, b, 200),
                    (size, size),
                    size - i
                )
                
            # Position and draw gradient
            self.screen.blit(
                gradient_surf,
                (x - size, y - size)
            )
            
            # Draw star outline
            pygame.draw.polygon(
                self.screen,
                YELLOW,
                points,
                3  # Outline width
            )
            
            # Add text inside
            try:
                font_size = max(10, int(size * 0.4))
                font = pygame.font.SysFont("Arial", font_size, bold=True)
                text = font.render("WOW!", True, WHITE)
                text_rect = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rect)
            except Exception:
                pass
                
        elif self.surprise_type == "rainbow":
            # Draw rainbow arcs
            for i in range(6):
                color = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE][i]
                radius = size - i * (size//8)
                thickness = max(3, size // 15)
                
                pygame.draw.arc(
                    self.screen,
                    color,
                    (x - radius, y - radius, radius * 2, radius * 2),
                    0, math.pi,
                    thickness
                )
                
            # Add sparkles around the rainbow
            for _ in range(8):
                spark_angle = random.uniform(0, math.pi)
                spark_radius = random.uniform(0.8, 1.2) * size
                spark_x = x + math.cos(spark_angle) * spark_radius
                spark_y = y + math.sin(spark_angle) * spark_radius * 0.8
                spark_size = max(1, int(size / 15))
                
                pygame.draw.circle(
                    self.screen,
                    WHITE,
                    (int(spark_x), int(spark_y)),
                    spark_size
                )
                
        elif self.surprise_type == "butterfly":
            # Draw butterfly wings
            wing_color1 = (200, 100, 200)  # Purple
            wing_color2 = (255, 150, 200)  # Pink
            
            # Draw wings as overlapping circles
            wing_radius = int(size * 0.7)
            wing_offset = int(size * 0.4)
            
            # Left wings
            pygame.draw.circle(
                self.screen,
                wing_color1,
                (int(x - wing_offset), int(y - wing_offset)),
                wing_radius
            )
            pygame.draw.circle(
                self.screen,
                wing_color2,
                (int(x - wing_offset), int(y + wing_offset)),
                wing_radius
            )
            
            # Right wings
            pygame.draw.circle(
                self.screen,
                wing_color2,
                (int(x + wing_offset), int(y - wing_offset)),
                wing_radius
            )
            pygame.draw.circle(
                self.screen,
                wing_color1,
                (int(x + wing_offset), int(y + wing_offset)),
                wing_radius
            )
            
            # Body
            pygame.draw.line(
                self.screen,
                BLACK,
                (x, y - int(size * 0.6)),
                (x, y + int(size * 0.6)),
                max(3, int(size * 0.1))
            )
            
            # Antennae
            ant_length = int(size * 0.4)
            pygame.draw.line(
                self.screen,
                BLACK,
                (x, y - int(size * 0.5)),
                (x - int(size * 0.3), y - int(size * 0.7)),
                2
            )
            pygame.draw.line(
                self.screen,
                BLACK,
                (x, y - int(size * 0.5)),
                (x + int(size * 0.3), y - int(size * 0.7)),
                2
            )
            
        elif self.surprise_type == "balloon_pop":
            # Draw balloon fragments
            fragments = 12
            for i in range(fragments):
                angle = i * (2 * math.pi / fragments)
                distance = size * self.surprise_scale * 3  # Fly outward with scale
                frag_x = x + math.cos(angle) * distance
                frag_y = y + math.sin(angle) * distance
                
                pygame.draw.line(
                    self.screen,
                    RED,
                    (x, y),
                    (frag_x, frag_y),
                    2
                )
                
                # Draw fragment end
                pygame.draw.circle(
                    self.screen,
                    RED,
                    (int(frag_x), int(frag_y)),
                    3
                )
                
            # Draw "POP!" text
            try:
                font = pygame.font.SysFont("Impact", size, bold=True)
                text = font.render("POP!", True, RED)
                text_rect = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rect)
            except Exception:
                pass
                
        elif self.surprise_type == "flower":
            # Draw flower petals
            num_petals = 8
            petal_color = (255, 150, 200)  # Pink
            
            for i in range(num_petals):
                angle = i * (2 * math.pi / num_petals)
                petal_x = x + math.cos(angle) * size
                petal_y = y + math.sin(angle) * size
                
                pygame.draw.circle(
                    self.screen,
                    petal_color,
                    (int(petal_x), int(petal_y)),
                    int(size * 0.4)
                )
                
            # Draw center
            pygame.draw.circle(
                self.screen,
                YELLOW,
                (int(x), int(y)),
                int(size * 0.3)
            )
            
            # Draw a happy face in the center
            center_radius = int(size * 0.3)
            eye_radius = max(1, center_radius // 5)
            
            # Eyes
            eye_offset = center_radius // 2
            pygame.draw.circle(
                self.screen,
                BLACK,
                (int(x - eye_offset), int(y - eye_offset // 2)),
                eye_radius
            )
            pygame.draw.circle(
                self.screen,
                BLACK,
                (int(x + eye_offset), int(y - eye_offset // 2)),
                eye_radius
            )
            
            # Smile
            pygame.draw.arc(
                self.screen,
                BLACK,
                (int(x - center_radius * 0.6), int(y - center_radius * 0.3), 
                 int(center_radius * 1.2), int(center_radius * 0.8)),
                0, math.pi,
                max(1, eye_radius // 2)
            )