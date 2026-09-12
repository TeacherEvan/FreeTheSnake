# welcome_character.py
# Extracted from WelcomeScreen via surgical-implementation refactor.
import pygame
import random
import math
import colorsys
from constants import *
from utils import draw_text, draw_animated_text


class WelcomeCharacter:
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

