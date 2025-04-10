# particles.py
import pygame
import random

class Particle:
    def __init__(self, x, y, color, size, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.age += 1
        self.size = max(0, self.size - 0.1)  # Gradually shrink
        self.y -= 1  # Move upwards

    def is_alive(self):
        return self.age < self.lifetime

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, size, count=10, lifetime=30):
        for _ in range(count):
            particle = Particle(x, y, color, size, lifetime)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle.color, (int(particle.x), int(particle.y)), int(particle.size))