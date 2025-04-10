# shapes.py
import pygame
import random
from constants import *

def draw_shape(surface, shape_name, position, size, color):
    center = (position[0], position[1])
    half_size = size / 2

    if shape_name == "Square":
        pygame.draw.rect(surface, color, (center[0] - half_size, center[1] - half_size, size, size))
    elif shape_name == "Rectangle":
        pygame.draw.rect(surface, color, (center[0] - half_size, center[1] - half_size * 0.6, size, size * 0.6))
    elif shape_name == "Circle":
        pygame.draw.circle(surface, color, center, int(half_size))
    elif shape_name == "Triangle":
        points = [
            (center[0], center[1] - half_size),
            (center[0] - half_size, center[1] + half_size),
            (center[0] + half_size, center[1] + half_size)
        ]
        pygame.draw.polygon(surface, color, points)
    elif shape_name == "Pentagon":
        points = []
        for i in range(5):
            angle = 2 * math.pi / 5 * i - math.pi / 2
            x = center[0] + half_size * math.cos(angle)
            y = center[1] + half_size * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)

def random_shape_position(screen_width, screen_height):
    x = random.randint(50, screen_width - 50)
    y = random.randint(50, screen_height - 50)
    return (x, y)

def random_shape_color():
    return random.choice([RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE])