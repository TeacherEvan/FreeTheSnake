# particles.py
import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, size, lifetime, velocity=None, gravity=0.1, particle_type="circle"):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.particle_type = particle_type
        
        # Enhanced physics
        if velocity is None:
            # Random velocity for more natural movement
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.velocity_x = math.cos(angle) * speed
            self.velocity_y = math.sin(angle) * speed
        else:
            self.velocity_x, self.velocity_y = velocity
            
        self.gravity = gravity
        self.bounce_factor = 0.7  # For bouncing particles
        self.fade_rate = 255 / lifetime  # For smooth alpha fading
        self.alpha = 255
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.2, 0.2)
        
        # Additional visual properties
        self.original_size = size
        self.pulsate_speed = random.uniform(0.05, 0.15)
        self.trail_positions = []  # For trail effects

    def update(self, bounds=None):
        self.age += 1
        
        # Update position with physics
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        
        # Add trail position
        if len(self.trail_positions) > 5:
            self.trail_positions.pop(0)
        self.trail_positions.append((self.x, self.y))
        
        # Handle boundaries (bouncing)
        if bounds:
            width, height = bounds
            if self.x <= 0 or self.x >= width:
                self.velocity_x *= -self.bounce_factor
                self.x = max(0, min(width, self.x))
            if self.y >= height:
                self.velocity_y *= -self.bounce_factor
                self.y = height
                
        # Update visual properties
        self.rotation += self.rotation_speed
        
        # Fade out over time
        fade_progress = self.age / self.lifetime
        self.alpha = max(0, 255 * (1 - fade_progress))
        
        # Size changes based on type
        if self.particle_type == "shrinking":
            self.size = max(0, self.original_size * (1 - fade_progress))
        elif self.particle_type == "pulsating":
            pulse = math.sin(self.age * self.pulsate_speed)
            self.size = self.original_size + pulse * 2
        elif self.particle_type == "growing":
            self.size = self.original_size * (1 + fade_progress * 0.5)

    def is_alive(self):
        return self.age < self.lifetime and self.alpha > 0

class EnhancedParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 500  # Performance limit

    def emit_burst(self, x, y, color, count=15, size_range=(2, 8), lifetime_range=(30, 60), particle_type="circle"):
        """Create a burst of particles for celebrations."""
        for _ in range(count):
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed - 2)  # Slight upward bias
            
            particle = Particle(x, y, color, size, lifetime, velocity, 
                              gravity=random.uniform(0.05, 0.15), particle_type=particle_type)
            self.particles.append(particle)

    def emit_fountain(self, x, y, color, count=10, height=5):
        """Create a fountain effect shooting upward."""
        for _ in range(count):
            size = random.uniform(3, 7)
            lifetime = random.randint(40, 80)
            velocity_x = random.uniform(-1, 1)
            velocity_y = random.uniform(-height, -height/2)
            velocity = (velocity_x, velocity_y)
            
            particle = Particle(x, y, color, size, lifetime, velocity, 
                              gravity=0.1, particle_type="shrinking")
            self.particles.append(particle)

    def emit_sparkles(self, x, y, color, count=8):
        """Create sparkling effect for achievements."""
        for _ in range(count):
            size = random.uniform(1, 4)
            lifetime = random.randint(20, 40)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            
            # Add some sparkle colors
            sparkle_colors = [color, (255, 255, 255), (255, 255, 0)]
            sparkle_color = random.choice(sparkle_colors)
            
            particle = Particle(x, y, sparkle_color, size, lifetime, velocity, 
                              gravity=0, particle_type="pulsating")
            self.particles.append(particle)

    def emit_trail(self, x, y, color, direction, count=5):
        """Create a trailing effect behind moving objects."""
        for i in range(count):
            size = random.uniform(2, 5) * (1 - i * 0.2)
            lifetime = random.randint(15, 25)
            offset_x = direction[0] * (i + 1) * -0.5 + random.uniform(-1, 1)
            offset_y = direction[1] * (i + 1) * -0.5 + random.uniform(-1, 1)
            
            particle = Particle(x + offset_x, y + offset_y, color, size, lifetime, 
                              (0, 0), gravity=0, particle_type="shrinking")
            self.particles.append(particle)

    def update(self, bounds=None):
        # Remove excess particles for performance
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
            
        for particle in self.particles[:]:
            particle.update(bounds)
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            if particle.alpha <= 0:
                continue
                
            # Create color with alpha
            color_with_alpha = (*particle.color[:3], int(particle.alpha))
            
            try:
                if particle.particle_type == "circle":
                    # Create a surface for alpha blending
                    particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, color_with_alpha, 
                                     (particle.size, particle.size), int(particle.size))
                    surface.blit(particle_surface, (particle.x - particle.size, particle.y - particle.size))
                    
                elif particle.particle_type == "star":
                    # Draw a simple star shape
                    self._draw_star(surface, (int(particle.x), int(particle.y)), 
                                  int(particle.size), color_with_alpha, particle.rotation)
                    
                elif particle.particle_type == "square":
                    # Draw rotated square
                    rect_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                    rect = pygame.Rect(0, 0, particle.size * 2, particle.size * 2)
                    pygame.draw.rect(rect_surface, color_with_alpha, rect)
                    
                    # Rotate the surface
                    rotated_surface = pygame.transform.rotate(rect_surface, math.degrees(particle.rotation))
                    rot_rect = rotated_surface.get_rect(center=(particle.x, particle.y))
                    surface.blit(rotated_surface, rot_rect)
                    
                else:  # Default to circle
                    particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, color_with_alpha, 
                                     (particle.size, particle.size), int(particle.size))
                    surface.blit(particle_surface, (particle.x - particle.size, particle.y - particle.size))
                    
            except Exception:
                # Fallback to simple circle if alpha blending fails
                pygame.draw.circle(surface, particle.color[:3], 
                                 (int(particle.x), int(particle.y)), int(particle.size))

    def _draw_star(self, surface, center, size, color, rotation):
        """Draw a star shape."""
        points = []
        for i in range(10):  # 5 points, each with inner and outer vertex
            angle = rotation + (i * math.pi / 5)
            if i % 2 == 0:
                # Outer point
                radius = size
            else:
                # Inner point
                radius = size * 0.5
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            try:
                star_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
                adjusted_points = [(p[0] - center[0] + size * 1.5, p[1] - center[1] + size * 1.5) for p in points]
                pygame.draw.polygon(star_surface, color, adjusted_points)
                surface.blit(star_surface, (center[0] - size * 1.5, center[1] - size * 1.5))
            except Exception:
                # Fallback to circle
                pygame.draw.circle(surface, color[:3], center, int(size))

# Legacy compatibility
ParticleSystem = EnhancedParticleSystem