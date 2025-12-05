# animations.py
# Enhanced animation utilities for polished micro-interactions
# These animations are designed to create a premium, engaging experience
# for kindergarten-age users.

import pygame
import random
import math
from typing import Tuple, List, Optional, Dict, Any


# TODO: [OPTIMIZATION] Consider using sprite batching for particle animations
# to improve rendering performance when many particles are active


def draw_bouncing_ball(
    surface: pygame.Surface, 
    position: Tuple[float, float], 
    radius: int, 
    color: Tuple[int, int, int], 
    speed: Tuple[float, float]
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Draw a bouncing ball with physics simulation.
    
    Args:
        surface: Target pygame surface
        position: Current position (x, y)
        radius: Ball radius in pixels
        color: RGB color tuple
        speed: Current velocity (vx, vy)
        
    Returns:
        Tuple of (new_position, new_speed)
    """
    new_position = (position[0] + speed[0], position[1] + speed[1])
    
    # Bounce off walls
    if new_position[0] - radius < 0 or new_position[0] + radius > surface.get_width():
        speed = (-speed[0], speed[1])
    if new_position[1] - radius < 0 or new_position[1] + radius > surface.get_height():
        speed = (speed[0], -speed[1])
    
    new_position = (position[0] + speed[0], position[1] + speed[1])
    
    pygame.draw.circle(surface, color, (int(new_position[0]), int(new_position[1])), radius)
    
    return new_position, speed


def draw_sparkles(
    surface: pygame.Surface, 
    position: Tuple[int, int], 
    sparkle_count: int,
    colors: Optional[List[Tuple[int, int, int]]] = None
) -> None:
    """
    Draw sparkle effects at a position - children respond to visual rewards.
    
    Args:
        surface: Target pygame surface
        position: Center position for sparkles
        sparkle_count: Number of sparkles to draw
        colors: Optional list of colors for variation
    """
    if colors is None:
        colors = [(255, 255, 0), (255, 215, 0), (255, 255, 255)]
    
    for _ in range(sparkle_count):
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        sparkle_pos = (position[0] + offset_x, position[1] + offset_y)
        sparkle_color = random.choice(colors)
        sparkle_size = random.randint(2, 5)
        
        # Draw star shape for more visual appeal
        pygame.draw.circle(surface, sparkle_color, sparkle_pos, sparkle_size)
        
        # Add cross lines for star effect
        line_length = sparkle_size + 2
        pygame.draw.line(
            surface, sparkle_color,
            (sparkle_pos[0] - line_length, sparkle_pos[1]),
            (sparkle_pos[0] + line_length, sparkle_pos[1]), 1
        )
        pygame.draw.line(
            surface, sparkle_color,
            (sparkle_pos[0], sparkle_pos[1] - line_length),
            (sparkle_pos[0], sparkle_pos[1] + line_length), 1
        )


def animate_snake_growth(
    surface: pygame.Surface, 
    snake_segments: List[Tuple[int, int]], 
    growth_rate: int
) -> None:
    """
    Animate snake segment growth.
    
    Args:
        surface: Target pygame surface
        snake_segments: List of segment positions
        growth_rate: Size of each segment
    """
    for segment in snake_segments:
        pygame.draw.rect(surface, (34, 139, 34), (*segment, growth_rate, growth_rate))


# --- Enhanced Micro-Interaction Animations ---

def create_pulse_animation(
    current_time: float, 
    base_scale: float = 1.0, 
    pulse_amount: float = 0.1, 
    speed: float = 2.0
) -> float:
    """
    Create a pulsing scale value for elements.
    
    Args:
        current_time: Current time in seconds
        base_scale: Base scale value
        pulse_amount: Amount of pulse (0.1 = 10%)
        speed: Speed of the pulse animation
        
    Returns:
        Current scale value
    """
    return base_scale + pulse_amount * math.sin(current_time * speed)


def create_hover_transition(
    is_hovered: bool, 
    current_value: float, 
    target_value: float, 
    transition_speed: float = 0.15
) -> float:
    """
    Create a smooth hover transition for UI elements.
    
    Args:
        is_hovered: Whether element is currently hovered
        current_value: Current transition value (0.0-1.0)
        target_value: Target value based on hover state
        transition_speed: Speed of transition
        
    Returns:
        New transition value
    """
    target = target_value if is_hovered else 0.0
    return current_value + (target - current_value) * transition_speed


def draw_ripple_effect(
    surface: pygame.Surface,
    center: Tuple[int, int],
    current_radius: float,
    max_radius: float,
    color: Tuple[int, int, int],
    line_width: int = 2
) -> Optional[float]:
    """
    Draw a ripple effect emanating from a point.
    
    Args:
        surface: Target pygame surface
        center: Center point of ripple
        current_radius: Current radius of ripple
        max_radius: Maximum radius before ripple disappears
        color: RGB color tuple
        line_width: Width of ripple line
        
    Returns:
        New radius value, or None if animation complete
    """
    if current_radius >= max_radius:
        return None
    
    # Calculate alpha based on radius progress
    progress = current_radius / max_radius
    alpha = int(255 * (1 - progress))
    
    if alpha > 10:
        try:
            ripple_surface = pygame.Surface(
                (int(current_radius * 2 + line_width * 2), 
                 int(current_radius * 2 + line_width * 2)),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                ripple_surface,
                (*color, alpha),
                (int(current_radius + line_width), int(current_radius + line_width)),
                int(current_radius),
                line_width
            )
            surface.blit(
                ripple_surface,
                (center[0] - current_radius - line_width, 
                 center[1] - current_radius - line_width)
            )
        except pygame.error:
            pass
    
    return current_radius + 2.0  # Expand ripple


def draw_success_burst(
    surface: pygame.Surface,
    center: Tuple[int, int],
    particles: List[Dict[str, Any]],
    frame_count: int
) -> List[Dict[str, Any]]:
    """
    Draw a success celebration burst effect.
    
    Args:
        surface: Target pygame surface
        center: Center point of burst
        particles: List of particle dictionaries
        frame_count: Current animation frame
        
    Returns:
        Updated list of particles (with dead particles removed)
    """
    remaining_particles = []
    
    for particle in particles:
        # Update particle position
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.1  # Gravity
        particle['lifetime'] -= 1
        
        if particle['lifetime'] > 0:
            # Calculate alpha based on remaining lifetime
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            
            # Draw particle
            try:
                pygame.draw.circle(
                    surface,
                    particle['color'],
                    (int(particle['x']), int(particle['y'])),
                    max(1, int(particle['size']))
                )
            except pygame.error:
                pass
            
            remaining_particles.append(particle)
    
    return remaining_particles


def create_success_particles(
    center: Tuple[int, int],
    count: int = 15,
    colors: Optional[List[Tuple[int, int, int]]] = None
) -> List[Dict[str, Any]]:
    """
    Create particles for a success celebration effect.
    
    Args:
        center: Center point for particle origin
        count: Number of particles to create
        colors: Optional list of colors
        
    Returns:
        List of particle dictionaries
    """
    if colors is None:
        colors = [
            (255, 215, 0),   # Gold
            (255, 255, 0),   # Yellow
            (0, 255, 0),     # Green
            (255, 165, 0),   # Orange
            (255, 255, 255), # White
        ]
    
    particles = []
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)
        
        particles.append({
            'x': center[0],
            'y': center[1],
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed - 3,  # Upward bias
            'size': random.uniform(3, 7),
            'color': random.choice(colors),
            'lifetime': random.randint(30, 60),
            'max_lifetime': 60,
        })
    
    return particles


def create_loading_animation(
    surface: pygame.Surface,
    center: Tuple[int, int],
    radius: int,
    progress: float,
    color: Tuple[int, int, int] = (100, 100, 255)
) -> None:
    """
    Draw a circular loading animation.
    
    Args:
        surface: Target pygame surface
        center: Center of loading circle
        radius: Radius of the loading circle
        progress: Current progress (0.0-1.0)
        color: RGB color tuple
    """
    # Draw background circle
    pygame.draw.circle(surface, (50, 50, 50), center, radius, 3)
    
    # Draw progress arc
    if progress > 0:
        start_angle = -math.pi / 2  # Start from top
        end_angle = start_angle + (2 * math.pi * progress)
        
        # Draw arc segments
        segments = max(1, int(progress * 36))  # More segments = smoother arc
        for i in range(segments):
            angle = start_angle + (end_angle - start_angle) * i / segments
            next_angle = start_angle + (end_angle - start_angle) * (i + 1) / segments
            
            start_point = (
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle)
            )
            end_point = (
                center[0] + radius * math.cos(next_angle),
                center[1] + radius * math.sin(next_angle)
            )
            
            pygame.draw.line(surface, color, start_point, end_point, 4)