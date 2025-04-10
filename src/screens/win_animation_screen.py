# filepath: kindergarten-snake-game/kindergarten-snake-game/src/screens/win_animation_screen.py
import pygame
import random
import math
import colorsys
from constants import *
from utils import draw_text, get_cage_rect, create_reward_burst, update_particles, draw_particles

class WinAnimationScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        
        # Screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Animation state variables
        self.animation_timer = 0
        self.animation_duration = 180  # Duration in frames (3 seconds at 60fps)
        self.animation_phase = 0  # Different phases of the animation
        
        # Cage breaking animation variables
        self.cage_pieces = []
        self.initial_cage_rect = None
        self.cage_break_sound_played = False
        
        # Snake freedom animation variables
        self.freedom_path = []
        self.freedom_progress = 0
        self.joy_particles = []
        
        # Celebration particles
        self.particles = []
        
        # Achievement celebration elements - children love achievements
        self.achievement_text = ""
        self.achievement_icon = "🏆"
        self.achievement_scale = 1.0
        
        # Growth mindset messages - encourage effort and persistence
        self.growth_messages = [
            "Your brain got stronger!",
            "You learned so much!",
            "Look how much you've grown!",
            "Your practice paid off!",
            "Your hard work helped you win!"
        ]
        self.current_growth_message = random.choice(self.growth_messages)
        
        # Animated characters - for social/emotional connection
        self.celebration_characters = []
        self.generate_celebration_characters()
        
        # Star particles for reward system
        self.stars = []
        self.generate_stars()
        
        # Create colorful confetti particles
        self.generate_confetti()
        
        # Fireworks - visual reinforcement
        self.fireworks = []
        self.firework_timer = 0
        
        # Rainbow path - vibrant visuals appeal to early childhood
        self.rainbow_path_points = []
        self.generate_rainbow_path()
        
        # Sound indicators (visual cues for sounds)
        self.sound_indicators = []
        
    def update_dimensions(self, width, height):
        """Update dimensions when screen is resized."""
        self.screen_width = width
        self.screen_height = height
    
    def handle_events(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Skip animation and go directly to congratulations screen
            if self.animation_phase >= 2:  # Only allow skipping after cage break
                self.game_state.current_state = STATE_WIN_LEVEL_CONGRATS

    def update(self):
        """Update the animation state."""
        # Increment animation timer
        self.animation_timer += 1
        
        # Get scaled time values based on animation_duration
        if self.animation_timer >= self.animation_duration:
            # Move to congratulations screen when animation completes
            self.game_state.current_state = STATE_WIN_LEVEL_CONGRATS
            return
        
        # Calculate animation progress
        animation_progress = self.animation_timer / self.animation_duration
        
        # Different animation phases
        if animation_progress < 0.3:  # Phase 1: Cage shaking
            self.animation_phase = 0
            self.update_cage_shake(animation_progress / 0.3)
        elif animation_progress < 0.6:  # Phase 2: Cage breaking
            self.animation_phase = 1
            self.update_cage_break((animation_progress - 0.3) / 0.3)
        else:  # Phase 3: Snake freedom
            self.animation_phase = 2
            self.update_snake_freedom((animation_progress - 0.6) / 0.4)
        
        # Update celebration particles
        self.particles = update_particles(self.particles)
        
        # Update stars
        self.update_stars()
        
        # Update fireworks
        self.update_fireworks()
        
        # Update celebration characters
        self.update_celebration_characters()
        
    def generate_celebration_characters(self):
        """Create animated characters that celebrate around the edges.
        Children respond well to expressive characters."""
        self.celebration_characters = []
        
        # Create 5-8 characters
        for _ in range(random.randint(5, 8)):
            # Position around the edges of the screen
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, self.screen_width)
                y = -50
            elif side == "bottom":
                x = random.randint(0, self.screen_width)
                y = self.screen_height + 50
            elif side == "left":
                x = -50
                y = random.randint(0, self.screen_height)
            else:  # right
                x = self.screen_width + 50
                y = random.randint(0, self.screen_height)
            
            # Choose a random character type
            character_type = random.choice(["star", "heart", "happy", "sun"])
            
            # Choose a color based on type
            if character_type == "star":
                color = YELLOW
                symbol = "⭐"
            elif character_type == "heart":
                color = BRIGHT_RED
                symbol = "❤️"
            elif character_type == "happy":
                color = BRIGHT_GREEN
                symbol = "😊"
            else:  # sun
                color = ORANGE
                symbol = "🌞"
            
            # Add to collection
            self.celebration_characters.append({
                "pos": [x, y],
                "target": [
                    random.randint(100, self.screen_width - 100),
                    random.randint(100, self.screen_height - 100)
                ],
                "color": color,
                "symbol": symbol,
                "size": random.randint(30, 50),
                "angle": 0,
                "spin_speed": random.uniform(-0.05, 0.05),
                "entry_progress": 0,
                "bounce_offset": 0,
                "bounce_speed": random.uniform(0.05, 0.1)
            })
    
    def generate_stars(self):
        """Generate star particles."""
        self.stars = []
        
        from utils import get_scale_factors
        if not hasattr(self, 'scale_factors'):
            self.scale_factors = get_scale_factors(self.screen_width, self.screen_height)
            
        # Scale star count and size with screen dimensions
        star_count = int(50 * self.scale_factors['uniform'])
        
        for _ in range(star_count):
            self.stars.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.uniform(3, 15) * self.scale_factors['uniform'],
                'points': random.randint(4, 7),
                'rotation': random.uniform(0, 6.28),
                'rotation_speed': random.uniform(-0.03, 0.03),
                'alpha': 0,  # Start invisible
                'color': random.choice([YELLOW, WHITE, (255, 200, 100)])  # Yellow, white, or gold
            })
    
    def generate_confetti(self):
        """Generate confetti particles.
        Visual reinforcement of accomplishment is important for motivation."""
        self.particles = []
        
        # Create a burst of particles from the center
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        for _ in range(150):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            
            # Random particle properties
            self.particles.append({
                "pos": [center_x, center_y],
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "size": random.randint(5, 12),
                "color": random.choice(PARTICLE_COLORS),
                "rotation": random.uniform(0, math.pi * 2),
                "rotation_speed": random.uniform(-0.2, 0.2),
                "shape": random.choice(["circle", "square", "triangle"]),
                "lifetime": random.randint(120, 240)
            })
    
    def generate_rainbow_path(self):
        """Generate a rainbow path for the snake to follow to freedom.
        Colorful visuals are engaging for kindergarten students."""
        # Start at the center
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Create a curvy path to a point near the edge
        target_x = random.randint(50, self.screen_width - 50)
        target_y = random.randint(50, 100)  # Near the top
        
        # Generate control points for a Bezier curve
        control1_x = random.randint(center_x - 100, center_x + 100)
        control1_y = random.randint(center_y - 100, center_y)
        control2_x = random.randint(target_x - 100, target_x + 100)
        control2_y = random.randint(center_y, target_y + 100)
        
        # Sample points along the curve
        points = []
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            # Cubic Bezier formula
            x = (1-t)**3 * center_x + 3*(1-t)**2*t * control1_x + 3*(1-t)*t**2 * control2_x + t**3 * target_x
            y = (1-t)**3 * center_y + 3*(1-t)**2*t * control1_y + 3*(1-t)*t**2 * control2_y + t**3 * target_y
            points.append((x, y))
        
        self.rainbow_path_points = points