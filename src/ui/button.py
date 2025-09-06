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
        
        # Enhanced visual effects
        self.glow_alpha = 0
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.animation_time = 0
        self.shadow_offset = 3
        self.gradient_enabled = True
        
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
        """Draw the button on the given surface with enhanced visual effects"""
        # Update visual effects
        self.update_visual_effects()
        
        # Create a copy of the button rect for drawing calculations
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Apply hover scale effect
        if self.hover:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
        
        # Apply scaling
        if self.hover_scale != 1.0:
            scaled_width = int(self.width * self.hover_scale)
            scaled_height = int(self.height * self.hover_scale)
            x_offset = (scaled_width - self.width) // 2
            y_offset = (scaled_height - self.height) // 2
            button_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, scaled_width, scaled_height)
        
        # Apply pulsing effect if active
        actual_width = button_rect.width
        actual_height = button_rect.height
        if self.pulsing:
            self.update_pulse()
            scale_factor = 1.0 + self.pulse_amount
            actual_width = int(button_rect.width * scale_factor)
            actual_height = int(button_rect.height * scale_factor)
            # Adjust position to keep button centered during pulse
            x_offset = (actual_width - button_rect.width) // 2
            y_offset = (actual_height - button_rect.height) // 2
            button_rect = pygame.Rect(button_rect.x - x_offset, button_rect.y - y_offset, actual_width, actual_height)
        
        # Draw enhanced shadow
        if not self.clicked:
            self.draw_enhanced_shadow(surface, button_rect)
        
        # Draw glow effect
        self.draw_enhanced_glow(surface, button_rect)
        
        # Draw button background with gradient or solid color
        color = self.color
        if self.hover:
            # Brighten color on hover with pulse effect
            import math
            pulse = math.sin(self.animation_time) * 0.5 + 0.5
            pulse_amount = int(30 * pulse)
            color = tuple(min(255, c + 20 + pulse_amount) for c in self.color)
        
        # Try gradient background first
        if not self.draw_gradient_background(surface, button_rect):
            # Fallback to solid color
            pygame.draw.rect(surface, color, button_rect, border_radius=int(min(actual_width, actual_height) * 0.2))
        
        # Draw button border with enhanced style
        border_width = max(1, int(2 * self.scale_factors['uniform']))
        border_color = tuple(min(255, c + 50) for c in color)
        pygame.draw.rect(surface, border_color, button_rect, width=border_width, border_radius=int(min(actual_width, actual_height) * 0.2))
        
        # Draw icon if present
        if self.icon_surface:
            icon_rect = self.icon_surface.get_rect(center=button_rect.center)
            surface.blit(self.icon_surface, icon_rect)
        
        # Draw text with shadow effect
        if self.text:
            # Scale font based on button size
            font_size = int(min(actual_height * 0.6, 36) * self.scale_factors['font'])
            try:
                font = pygame.font.SysFont('Arial', font_size, bold=True)
                
                # Draw text shadow
                shadow_surface = font.render(self.text, True, (0, 0, 0))
                shadow_rect = shadow_surface.get_rect(center=(button_rect.centerx + 1, button_rect.centery + 1))
                surface.blit(shadow_surface, shadow_rect)
                
                # Draw main text
                text_surface = font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=button_rect.center)
                if self.clicked:
                    text_rect.y += 1  # Pressed effect
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

    def update_visual_effects(self, dt=0.016):
        """Update visual effects animations."""
        self.animation_time += dt * 5
        
        # Update hover scale animation
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * 0.1
        
        # Update glow effect
        if self.hover:
            self.glow_alpha = min(100, self.glow_alpha + dt * 200)
        else:
            self.glow_alpha = max(0, self.glow_alpha - dt * 150)

    def draw_enhanced_shadow(self, surface, button_rect):
        """Draw enhanced shadow effect."""
        shadow_rect = button_rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        
        try:
            shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 80))
            pygame.draw.rect(shadow_surface, (0, 0, 0, 80), (0, 0, shadow_rect.width, shadow_rect.height),
                           border_radius=int(min(shadow_rect.width, shadow_rect.height) * 0.2))
            surface.blit(shadow_surface, shadow_rect)
        except:
            # Fallback shadow
            pygame.draw.rect(surface, (0, 0, 0), shadow_rect,
                           border_radius=int(min(shadow_rect.width, shadow_rect.height) * 0.2))

    def draw_enhanced_glow(self, surface, button_rect):
        """Draw glow effect around button."""
        if self.glow_alpha <= 0:
            return
            
        glow_size = 10
        for i in range(glow_size, 0, -2):
            glow_alpha = int(self.glow_alpha * (glow_size - i) / glow_size)
            if glow_alpha > 5:
                glow_rect = button_rect.inflate(i * 2, i * 2)
                glow_color = (*self.color, glow_alpha)
                try:
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_rect.width, glow_rect.height),
                                   border_radius=int(min(glow_rect.width, glow_rect.height) * 0.2 + i))
                    surface.blit(glow_surface, glow_rect)
                except:
                    break

    def draw_gradient_background(self, surface, button_rect):
        """Draw button with gradient background."""
        if not self.gradient_enabled:
            return False
            
        # Create gradient from lighter to darker
        light_color = tuple(min(255, c + 30) for c in self.color)
        dark_color = tuple(max(0, c - 20) for c in self.color)
        
        try:
            gradient_surface = pygame.Surface((button_rect.width, button_rect.height))
            
            for y in range(button_rect.height):
                ratio = y / button_rect.height
                r = int(light_color[0] + (dark_color[0] - light_color[0]) * ratio)
                g = int(light_color[1] + (dark_color[1] - light_color[1]) * ratio)
                b = int(light_color[2] + (dark_color[2] - light_color[2]) * ratio)
                pygame.draw.line(gradient_surface, (r, g, b), (0, y), (button_rect.width, y))
            
            surface.blit(gradient_surface, button_rect)
            return True
        except:
            return False