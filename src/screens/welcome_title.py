# welcome_title.py
# Extracted from WelcomeScreen via surgical-implementation refactor.
import pygame
from constants import *
from utils import draw_text, draw_animated_text


class WelcomeTitle:
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

