import pygame
from pygame import Rect, draw, font

BUTTON_COLOR = (200, 200, 200)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, text_color=BLACK, icon=None, scale_factors=None):
        self.x = x
        self.y = y
        self.base_width = width
        self.base_height = height
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        self.clicked = False
        self.icon = icon
        self.icon_surface = None
        self.pulsing = False
        self.pulse_amount = 0
        self.pulse_direction = 1
        self.scale_factors = scale_factors or {'x': 1.0, 'y': 1.0, 'uniform': 1.0, 'font': 1.0}
        
        # Apply initial scaling
        self.apply_scaling()
        
        if icon:
            self.load_icon(icon)
    
    def apply_scaling(self):
        """Apply current scaling factors to button dimensions"""
        if self.scale_factors:
            self.width = int(self.base_width * self.scale_factors['uniform'])
            self.height = int(self.base_height * self.scale_factors['uniform'])
    
    def update_scaling(self, new_scale_factors):
        """Update button scaling when screen dimensions change"""
        self.scale_factors = new_scale_factors
        self.apply_scaling()
        
        # Reload icon with new scale if applicable
        if self.icon:
            self.load_icon(self.icon)
    
    def load_icon(self, icon_path):
        """Load and scale an icon for the button"""
        try:
            original_icon = pygame.image.load(icon_path)
            # Scale icon based on button size
            icon_size = int(min(self.width, self.height) * 0.6)
            self.icon_surface = pygame.transform.scale(original_icon, (icon_size, icon_size))
        except pygame.error:
            print(f"Could not load icon: {icon_path}")
            self.icon_surface = None
    
    def draw(self, surface):
        """Draw the button on the given surface with current scaling applied"""
        # Create a copy of the button rect for drawing calculations
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Apply pulsing effect if active
        actual_width = self.width
        actual_height = self.height
        if self.pulsing:
            self.update_pulse()
            scale_factor = 1.0 + self.pulse_amount
            actual_width = int(self.width * scale_factor)
            actual_height = int(self.height * scale_factor)
            # Adjust position to keep button centered during pulse
            x_offset = (actual_width - self.width) // 2
            y_offset = (actual_height - self.height) // 2
            button_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, actual_width, actual_height)
        
        # Draw button background
        color = self.color
        if self.hover:
            # Brighten color on hover
            color = tuple(min(255, c + 20) for c in self.color)
        pygame.draw.rect(surface, color, button_rect, border_radius=int(min(actual_width, actual_height) * 0.2))
        
        # Draw button border
        border_width = max(1, int(2 * self.scale_factors['uniform']))
        pygame.draw.rect(surface, BLACK, button_rect, width=border_width, border_radius=int(min(actual_width, actual_height) * 0.2))
        
        # Draw icon if present
        if self.icon_surface:
            icon_rect = self.icon_surface.get_rect(center=button_rect.center)
            surface.blit(self.icon_surface, icon_rect)
        
        # Draw text
        if self.text:
            # Scale font based on button size
            font_size = int(min(actual_height * 0.6, 36) * self.scale_factors['font'])
            try:
                font = pygame.font.SysFont('Arial', font_size, bold=True)
                text_surface = font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=button_rect.center)
                surface.blit(text_surface, text_rect)
            except pygame.error as e:
                print(f"Error rendering text on button: {e}")
    
    def update_pulse(self):
        """Update pulsing animation"""
        if self.pulse_direction > 0:
            self.pulse_amount += 0.01
            if self.pulse_amount >= 0.1:  # Maximum 10% larger
                self.pulse_direction = -1
        else:
            self.pulse_amount -= 0.01
            if self.pulse_amount <= 0:
                self.pulse_direction = 1
                if not self.hover and not self.clicked:
                    self.pulsing = False  # Stop pulsing if not interacting
    
    def start_pulse(self):
        """Start the pulsing animation"""
        self.pulsing = True
        self.pulse_amount = 0
        self.pulse_direction = 1
    
    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over the button"""
        # Create rect accounting for any pulsing
        width_with_pulse = self.width
        height_with_pulse = self.height
        if self.pulsing:
            width_with_pulse = int(self.width * (1.0 + self.pulse_amount))
            height_with_pulse = int(self.height * (1.0 + self.pulse_amount))
        
        button_rect = pygame.Rect(
            self.x - (width_with_pulse - self.width) // 2,
            self.y - (height_with_pulse - self.height) // 2,
            width_with_pulse,
            height_with_pulse
        )
        
        was_hovering = self.hover
        self.hover = button_rect.collidepoint(mouse_pos)
        
        # Start pulsing when mouse enters
        if not was_hovering and self.hover:
            self.start_pulse()
        
        return self.hover
    
    def check_click(self, mouse_pos, mouse_click):
        """Check if button is clicked and return True if clicked"""
        if self.check_hover(mouse_pos) and mouse_click:
            self.clicked = True
            # Generate a stronger pulse on click
            self.pulsing = True
            self.pulse_amount = 0.05
            self.pulse_direction = 1
            return True
        return False
    
    def is_clicked(self):
        """Return if button was clicked and reset clicked state"""
        clicked = self.clicked
        self.clicked = False
        return clicked
    
    def set_position(self, x, y):
        """Set new button position"""
        self.x = x
        self.y = y