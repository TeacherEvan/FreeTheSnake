# welcome_transitions.py
# Extracted from WelcomeScreen via surgical-implementation refactor.
import pygame
import math
from constants import *
from utils import draw_text, draw_animated_text


class WelcomeTransitions:
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

