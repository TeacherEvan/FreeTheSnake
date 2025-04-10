from constants import *
from utils import draw_text, get_scale_factors

class GameOverScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        
        # Get initial screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Calculate scaling factors
        self.scale_factors = get_scale_factors(self.screen_width, self.screen_height)
        
        # Animation properties
        self.animation_frame = 0
        self.particles = []
        self.init_particles()
        
    def update_dimensions(self, width, height):
        """Update screen dimensions when window is resized."""
        self.screen_width = width
        self.screen_height = height
        
        # Recalculate scaling factors
        self.scale_factors = get_scale_factors(width, height)
        
        # Regenerate particles for new dimensions
        self.particles = []
        self.init_particles()

    def init_particles(self):
        """Initialize particles for background animation."""
        # Create falling particles (tears/raindrops) - contextually appropriate for game over
        for _ in range(30):
            self.particles.append({
                "x": random.randint(0, self.screen_width),
                "y": random.randint(-50, self.screen_height),
                "speed": random.uniform(1, 3) * self.scale_factors['uniform'],
                "size": random.uniform(2, 5) * self.scale_factors['uniform'],
                "color": (100, 149, 237)  # Cornflower blue (tear color)
            })
    
    def handle_events(self, event):
        """Process input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the level
                self.game_state.reset_level(
                    self.game_state.current_level,
                    self.screen_width,
                    self.screen_height,
                    get_cage_rect(self.screen_width, self.screen_height)
                )

    def update(self):
        """Update the game over screen state."""
        # Increment animation frame
        self.animation_frame += 1
        
        # Update falling particles
        for particle in self.particles:
            particle["y"] += particle["speed"]
            
            # Reset particles that fall off screen
            if particle["y"] > self.screen_height:
                particle["y"] = random.randint(-50, -10)
                particle["x"] = random.randint(0, self.screen_width)

    def draw(self):
        """Draw the game over screen with responsive layout."""
        # Fill the screen with a dark background
        self.screen.fill(BLACK)
        
        # Draw background particles
        for particle in self.particles:
            pygame.draw.circle(
                self.screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                int(particle["size"])
            )
        
        # Calculate scaled and positioned text elements
        title_y = int(self.screen_height * 0.35)
        message_y = int(self.screen_height * 0.45)
        instruction_y = int(self.screen_height * 0.6)
        
        # Apply pulsing animation to title
        scale_factor = 1.0 + 0.1 * math.sin(self.animation_frame * 0.05)
        title_size = int(72 * self.scale_factors['font'] * scale_factor)
        
        try:
            # Draw title with scaling
            title_font = pygame.font.SysFont("Arial", title_size, bold=True)
            title_text = title_font.render("Game Over!", True, WHITE)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, title_y))
            self.screen.blit(title_text, title_rect)
            
            # Draw encouraging message - keeps morale high
            message_font = pygame.font.SysFont("Arial", int(36 * self.scale_factors['font']))
            message_text = message_font.render("Try Again!", True, WHITE)
            message_rect = message_text.get_rect(center=(self.screen_width // 2, message_y))
            self.screen.blit(message_text, message_rect)
            
            # Draw restart instruction with animated movement
            instruction_offset = 5 * math.sin(self.animation_frame * 0.1)
            instruction_font = pygame.font.SysFont("Arial", int(24 * self.scale_factors['font']))
            instruction_text = instruction_font.render("Press R to Restart", True, WHITE)
            instruction_rect = instruction_text.get_rect(
                center=(self.screen_width // 2, instruction_y + instruction_offset)
            )
            self.screen.blit(instruction_text, instruction_rect)
            
            # Draw a helpful growth mindset message for kindergarteners
            growth_messages = [
                "Mistakes help us learn!",
                "You'll do better next time!",
                "Every try makes you better!",
                "Practice makes progress!",
                "Try a different way!"
            ]
            growth_message = random.choice(growth_messages)
            growth_y = int(self.screen_height * 0.75)
            growth_font = pygame.font.SysFont("Arial", int(20 * self.scale_factors['font']))
            growth_text = growth_font.render(growth_message, True, (100, 200, 100))
            growth_rect = growth_text.get_rect(center=(self.screen_width // 2, growth_y))
            self.screen.blit(growth_text, growth_rect)
            
        except Exception as e:
            print(f"Error rendering game over screen: {e}")
            fallback_font = pygame.font.Font(None, 36)
            fallback_text = fallback_font.render("Game Over! Press R to Restart", True, WHITE)
            fallback_rect = fallback_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(fallback_text, fallback_rect)