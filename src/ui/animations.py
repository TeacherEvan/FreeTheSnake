# animations.py
import pygame
import random

def draw_bouncing_ball(surface, position, radius, color, speed):
    new_position = (position[0] + speed[0], position[1] + speed[1])
    
    if new_position[0] - radius < 0 or new_position[0] + radius > surface.get_width():
        speed = (-speed[0], speed[1])
    if new_position[1] - radius < 0 or new_position[1] + radius > surface.get_height():
        speed = (speed[0], -speed[1])
    
    new_position = (position[0] + speed[0], position[1] + speed[1])
    
    pygame.draw.circle(surface, color, (int(new_position[0]), int(new_position[1])), radius)
    
    return new_position, speed

def draw_sparkles(surface, position, sparkle_count):
    for _ in range(sparkle_count):
        sparkle_pos = (position[0] + random.randint(-10, 10), position[1] + random.randint(-10, 10))
        pygame.draw.circle(surface, (255, 255, 0), sparkle_pos, random.randint(2, 5))

def animate_snake_growth(surface, snake_segments, growth_rate):
    for segment in snake_segments:
        pygame.draw.rect(surface, (34, 139, 34), (*segment, growth_rate, growth_rate))