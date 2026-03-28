# enhanced_graphics.py
# Advanced graphics utilities for improved visual effects
import pygame
import math
import random
from typing import Tuple, List, Optional
from core.lazy_loader import get_cached_resource

def create_gradient_surface(width: int, height: int, start_color: Tuple[int, int, int], 
                          end_color: Tuple[int, int, int], direction: str = "vertical") -> pygame.Surface:
    """Create a gradient surface for backgrounds and effects."""
    cache_key = f"gradient:{width}:{height}:{start_color}:{end_color}:{direction}"

    def _create_surface():
        surface = pygame.Surface((width, height))
    
        if direction == "vertical":
            for y in range(height):
                ratio = y / height
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        elif direction == "horizontal":
            for x in range(width):
                ratio = x / width
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        elif direction == "radial":
            center_x, center_y = width // 2, height // 2
            max_distance = math.sqrt(center_x**2 + center_y**2)
            
            for y in range(height):
                for x in range(width):
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(distance / max_distance, 1.0)
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                    surface.set_at((x, y), (r, g, b))
        return surface

    return get_cached_resource(cache_key, _create_surface)

def draw_glow_circle(surface: pygame.Surface, center: Tuple[int, int], radius: int, 
                    color: Tuple[int, int, int], glow_radius: int = 10, alpha: int = 128):
    """Draw a circle with a glowing effect."""
    if glow_radius <= 0:
        pygame.draw.circle(surface, color, center, radius)
        return

    cache_key = f"glow:{radius}:{color}:{glow_radius}:{alpha}"

    def _create_glow_surface():
        glow_size = radius * 2 + glow_radius * 2
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)

        # Draw multiple circles with decreasing alpha for glow effect
        for i in range(glow_radius, 0, -2):
            glow_alpha = int(alpha * (glow_radius - i) / glow_radius * 0.3)
            if glow_alpha > 0:
                pygame.draw.circle(
                    glow_surface,
                    (*color, glow_alpha),
                    (radius + glow_radius, radius + glow_radius),
                    radius + i,
                )

        return glow_surface

    glow_surface = get_cached_resource(cache_key, _create_glow_surface)
    surface.blit(glow_surface, (center[0] - radius - glow_radius, center[1] - radius - glow_radius))
    
    # Draw the main circle
    pygame.draw.circle(surface, color, center, radius)

def draw_shadow_rect(surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int], 
                    shadow_offset: Tuple[int, int] = (3, 3), shadow_color: Tuple[int, int, int] = (0, 0, 0), 
                    shadow_alpha: int = 100):
    """Draw a rectangle with a drop shadow."""
    # Create shadow surface
    shadow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shadow_surface.fill((*shadow_color, shadow_alpha))
    
    # Draw shadow
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset[0]
    shadow_rect.y += shadow_offset[1]
    surface.blit(shadow_surface, shadow_rect)
    
    # Draw main rectangle
    pygame.draw.rect(surface, color, rect)

def draw_rounded_rect(surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int], 
                     radius: int = 10, border_color: Optional[Tuple[int, int, int]] = None, 
                     border_width: int = 0):
    """Draw a rectangle with rounded corners."""
    if radius <= 0:
        pygame.draw.rect(surface, color, rect)
        if border_color and border_width > 0:
            pygame.draw.rect(surface, border_color, rect, border_width)
        return
    
    # Create a surface for the rounded rectangle
    rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Draw the rounded rectangle on the temporary surface
    pygame.draw.rect(rounded_surface, color, (0, 0, rect.width, rect.height))
    
    # Create corners
    corner_rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    
    # Top-left corner
    pygame.draw.rect(rounded_surface, (0, 0, 0, 0), corner_rect)
    pygame.draw.circle(rounded_surface, color, (radius, radius), radius)
    
    # Top-right corner
    corner_rect.x = rect.width - radius * 2
    pygame.draw.rect(rounded_surface, (0, 0, 0, 0), corner_rect)
    pygame.draw.circle(rounded_surface, color, (rect.width - radius, radius), radius)
    
    # Bottom-left corner
    corner_rect.x = 0
    corner_rect.y = rect.height - radius * 2
    pygame.draw.rect(rounded_surface, (0, 0, 0, 0), corner_rect)
    pygame.draw.circle(rounded_surface, color, (radius, rect.height - radius), radius)
    
    # Bottom-right corner
    corner_rect.x = rect.width - radius * 2
    pygame.draw.rect(rounded_surface, (0, 0, 0, 0), corner_rect)
    pygame.draw.circle(rounded_surface, color, (rect.width - radius, rect.height - radius), radius)
    
    # Blit to main surface
    surface.blit(rounded_surface, rect)
    
    # Draw border if specified
    if border_color and border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width)

def draw_animated_border(surface: pygame.Surface, rect: pygame.Rect, colors: List[Tuple[int, int, int]], 
                        animation_offset: float = 0, border_width: int = 3):
    """Draw an animated rainbow border."""
    if not colors:
        return
    
    perimeter = 2 * (rect.width + rect.height)
    segment_length = perimeter / len(colors)
    
    # Top edge
    for x in range(rect.width):
        progress = (x + animation_offset) % perimeter
        color_index = int((progress / segment_length) % len(colors))
        color = colors[color_index]
        for i in range(border_width):
            if rect.y + i >= 0:
                surface.set_at((rect.x + x, rect.y + i), color)
    
    # Right edge
    for y in range(rect.height):
        progress = (rect.width + y + animation_offset) % perimeter
        color_index = int((progress / segment_length) % len(colors))
        color = colors[color_index]
        for i in range(border_width):
            if rect.x + rect.width - 1 - i >= 0:
                surface.set_at((rect.x + rect.width - 1 - i, rect.y + y), color)
    
    # Bottom edge
    for x in range(rect.width - 1, -1, -1):
        progress = (rect.width + rect.height + (rect.width - x) + animation_offset) % perimeter
        color_index = int((progress / segment_length) % len(colors))
        color = colors[color_index]
        for i in range(border_width):
            if rect.y + rect.height - 1 - i >= 0:
                surface.set_at((rect.x + x, rect.y + rect.height - 1 - i), color)
    
    # Left edge
    for y in range(rect.height - 1, -1, -1):
        progress = (2 * rect.width + rect.height + (rect.height - y) + animation_offset) % perimeter
        color_index = int((progress / segment_length) % len(colors))
        color = colors[color_index]
        for i in range(border_width):
            if rect.x + i >= 0:
                surface.set_at((rect.x + i, rect.y + y), color)

def create_pulsing_effect(base_color: Tuple[int, int, int], pulse_time: float, 
                         intensity: float = 0.3) -> Tuple[int, int, int]:
    """Create a pulsing color effect."""
    pulse = (math.sin(pulse_time) + 1) / 2  # Normalize to 0-1
    multiplier = 1 + intensity * pulse
    
    r = min(255, int(base_color[0] * multiplier))
    g = min(255, int(base_color[1] * multiplier))
    b = min(255, int(base_color[2] * multiplier))
    
    return (r, g, b)

def draw_star_burst(surface: pygame.Surface, center: Tuple[int, int], inner_radius: int, 
                   outer_radius: int, points: int, color: Tuple[int, int, int], rotation: float = 0):
    """Draw a star burst shape."""
    star_points = []
    
    for i in range(points * 2):
        angle = rotation + (i * math.pi / points)
        if i % 2 == 0:
            # Outer point
            radius = outer_radius
        else:
            # Inner point
            radius = inner_radius
        
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        star_points.append((x, y))
    
    if len(star_points) >= 3:
        pygame.draw.polygon(surface, color, star_points)

def interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                     t: float) -> Tuple[int, int, int]:
    """Interpolate between two colors."""
    t = max(0, min(1, t))  # Clamp t to 0-1
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

def create_animated_background(width: int, height: int, time: float, 
                             base_colors: List[Tuple[int, int, int]]) -> pygame.Surface:
    """Create an animated gradient background."""
    if len(base_colors) < 2:
        base_colors = [(50, 50, 100), (100, 50, 150)]  # Default colors
    
    # Cycle through colors based on time
    color_cycle_speed = 0.01
    color_index = (time * color_cycle_speed) % len(base_colors)
    color1_idx = int(color_index) % len(base_colors)
    color2_idx = (color1_idx + 1) % len(base_colors)
    t = color_index - int(color_index)
    
    start_color = interpolate_color(base_colors[color1_idx], base_colors[color2_idx], t)
    end_color = interpolate_color(base_colors[color2_idx], base_colors[color1_idx], t)
    
    return create_gradient_surface(width, height, start_color, end_color, "radial")