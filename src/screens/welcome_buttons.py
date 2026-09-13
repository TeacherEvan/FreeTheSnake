# welcome_buttons.py
# Extracted from WelcomeScreen via surgical-implementation refactor.
import pygame
import math
from constants import *
from utils import draw_text, draw_animated_text


class WelcomeButtons:
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
            button_font = getattr(self, 'button_font', None) or FONT_MEDIUM
            
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

