import pygame
import math
import colorsys
import random
from constants import *

class Snake:
    def __init__(self, game_state):
        self.game_state = game_state
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (10, 0)  # Start moving to the right
        self.color = SNAKE_COLOR
        self.size = 10  # Base size that will be scaled based on screen
        self.base_step_size = 10  # Base movement step size
        self.step_size = 10  # Actual step size - will be dynamically scaled
        
        # Save initial screen dimensions to calculate scaling on resize
        self.initial_screen_width = game_state.screen_width if hasattr(game_state, 'screen_width') else 800
        self.initial_screen_height = game_state.screen_height if hasattr(game_state, 'screen_height') else 600
        
        # Calculate initial scale factors
        self.update_scaling()
        
        # Personality and engagement variables
        self.happiness = 1.0  # 0.0 to 1.0 scale
        self.emotion_state = "neutral"  # neutral, happy, excited, sad
        self.expression_timer = 0
        self.blinking = False
        self.blink_timer = 0
        
        # Animation variables for appeal to young children
        self.wiggle_offset = 0
        self.wiggle_speed = 0.2
        self.wiggle_amplitude = 3.0  # Controls how much the snake wiggles
        self.color_pulse_value = 0
        self.pulse_direction = 1
        self.eyes_size = 3
        
        # Add sparkle effects - children love sparkly things
        self.sparkle_timer = 0
        self.sparkle_positions = []
        self.show_sparkles = False
        
        # Rainbow trail effect
        self.rainbow_mode = False
        self.rainbow_timer = 0
        
        # Interactive feedback variables
        self.celebrating = False
        self.celebration_timer = 0
        
        # Enhanced visual effects
        self.trail_positions = []
        self.glow_intensity = 0.5
        self.segment_colors = []
        self.pattern_offset = 0
        self.pulse_timer = 0
        self.speed_trail_alpha = 100
        self.celebration_particles = []
        
        # Idle behaviors for continuous engagement
        self.idle_timer = 0
        self.current_idle_behavior = None
        self.idle_behaviors = ["look_around", "wiggle", "blink", "color_shift"]
        self.idle_duration = 60  # frames
        
        # Face features - anthropomorphizing increases engagement for kids
        self.mouth_open = False
        self.mouth_timer = 0
        self.eye_direction = (0, 0)
        self.expression = "smile"  # smile, neutral, excited
        
    def update_scaling(self):
        """Update snake scaling based on current screen dimensions."""
        if hasattr(self.game_state, 'screen_width') and hasattr(self.game_state, 'screen_height'):
            from utils import get_scale_factors
            
            # Get scale factors based on current screen size
            scale_factors = get_scale_factors(
                self.game_state.screen_width,
                self.game_state.screen_height
            )
            
            # Scale snake properties
            self.scaled_size = max(5, int(self.size * scale_factors['uniform']))
            self.step_size = max(3, int(self.base_step_size * scale_factors['uniform']))
            
            # Update direction to match step size
            dir_x, dir_y = self.direction
            if dir_x != 0:
                self.direction = (self.step_size if dir_x > 0 else -self.step_size, 0)
            elif dir_y != 0:
                self.direction = (0, self.step_size if dir_y > 0 else -self.step_size)
        else:
            # Default values if no screen dimensions available
            self.scaled_size = self.size
            self.step_size = self.base_step_size

    def move(self):
        # Get head position
        head_x, head_y = self.body[0]
        
        # Create new head position based on direction
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Insert new head at beginning of body list
        self.body.insert(0, new_head)
        
        # Remove the last segment to maintain size (unless growing)
        if len(self.body) > self.game_state.snake_size:
            self.body.pop()
            
        # Update wiggle offset for more appealing movement
        # Children respond well to organic, slightly unpredictable motion
        self.wiggle_offset += self.wiggle_speed
        
        # Occasionally generate sparkles along snake body
        self.sparkle_timer -= 1
        if self.sparkle_timer <= 0:
            self.show_sparkles = random.random() < 0.2  # 20% chance to show sparkles
            if self.show_sparkles:
                self.generate_sparkles()
            self.sparkle_timer = random.randint(30, 120)  # Random interval
        
        # Update color pulsing - vibrancy is appealing to kindergartners
        if self.pulse_direction > 0:
            self.color_pulse_value = min(30, self.color_pulse_value + 0.5)
            if self.color_pulse_value >= 30:
                self.pulse_direction = -1
        else:
            self.color_pulse_value = max(0, self.color_pulse_value - 0.5)
            if self.color_pulse_value <= 0:
                self.pulse_direction = 1
                
        # Rainbow mode effect countdown
        if self.rainbow_mode:
            self.rainbow_timer -= 1
            if self.rainbow_timer <= 0:
                self.rainbow_mode = False
        
        # Emotion state behavior
        self.expression_timer -= 1
        if self.expression_timer <= 0:
            if self.emotion_state != "neutral":
                # Return to neutral state after expressing emotion
                self.emotion_state = "neutral"
                self.expression = "smile"  # Default is friendly for kids
                
        # Handle blinking - adds liveliness that engages young children
        if self.blinking:
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.blinking = False
        elif random.random() < 0.005:  # Chance to start blinking
            self.blinking = True
            self.blink_timer = 10  # Blink for 10 frames
            
        # Mouth animation - children respond to expressive characters
        self.mouth_timer -= 1
        if self.mouth_timer <= 0:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = random.randint(30, 90)  # Random timing for natural look
            
        # Update idle behavior for continuous engagement
        self.update_idle_behavior()
        
        # Update celebration particles if celebrating
        if self.celebrating:
            self.update_celebration()

    def grow(self):
        # Create visual celebration when growing - immediate feedback
        self.start_celebration()
        
        # Show happiness when growing - children relate to emotions
        self.show_emotion("happy", 60)  # Happy for 1 second (60 frames)
        
        # Add a new segment at the tail
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        # Don't allow reversing on itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            # React with excitement to direction changes - reinforces agency
            if random.random() < 0.3:  # Don't react every time
                self.show_emotion("excited", 30)
            self.direction = new_direction

    def draw(self, surface):
        # Get pulsing color - vibrant colors maintain attention
        r, g, b = self.color
        pulsed_color = (
            min(255, r + self.color_pulse_value),
            min(255, g + self.color_pulse_value),
            min(255, b + self.color_pulse_value)
        )
        
        # Draw body segments with wave effect that appeals to kids
        for i, segment in enumerate(self.body):
            # Calculate wiggle offset for this segment - more pronounced wiggle
            wiggle_phase = self.wiggle_offset - (i * 0.3)  # Offset by segment position
            wiggle_amount = math.sin(wiggle_phase) * self.wiggle_amplitude  # Enhanced amplitude
            
            # Apply wiggle perpendicular to movement direction
            if self.direction[0] != 0:  # Moving horizontally
                wiggled_y = segment[1] + wiggle_amount
                wiggled_pos = (segment[0], wiggled_y)
            else:  # Moving vertically
                wiggled_x = segment[0] + wiggle_amount
                wiggled_pos = (wiggled_x, segment[1])
            
            # Handle rainbow mode - cycle through colors based on segment position
            segment_color = pulsed_color
            if self.rainbow_mode:
                hue = ((i * 15) + pygame.time.get_ticks() // 50) % 360 / 360.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                segment_color = (int(r * 255), int(g * 255), int(b * 255))
            elif i > 0:  # Make the body segments gradually darker
                darkness = 1.0 - (i / (len(self.body) * 1.5))  # Gradual darkening
                segment_color = (
                    max(0, int(pulsed_color[0] * darkness)),
                    max(0, int(pulsed_color[1] * darkness)),
                    max(0, int(pulsed_color[2] * darkness))
                )
            
            # Draw segment with rounded corners for a friendlier look
            pygame.draw.rect(surface, segment_color, 
                           (wiggled_pos[0], wiggled_pos[1], self.size, self.size),
                           border_radius=3)  # Rounded corners
            
            # Draw a friendly border around segments
            pygame.draw.rect(surface, BLACK, 
                           (wiggled_pos[0], wiggled_pos[1], self.size, self.size), 
                           1, border_radius=3)
        
        # Draw sparkles over snake body
        if self.show_sparkles:
            self.draw_sparkles(surface)
        
        # Draw head features (eyes, mouth) only if we have a body
        if len(self.body) > 0:
            self.draw_face(surface)
            
        # Draw celebration particles
        self.draw_celebration_particles(surface)

    def draw_face(self, surface):
        """Draw expressive facial features on the snake head.
        Anthropomorphized features increase emotional connection for children."""
        head = self.body[0]
        face_center = (head[0] + self.size/2, head[1] + self.size/2)
        
        # Determine eye position based on direction
        eye_offset_x = 0
        eye_offset_y = 0
        
        if self.direction == (10, 0):  # Right
            eye_offset_x = 2
            eye_offset_y = -2
        elif self.direction == (-10, 0):  # Left
            eye_offset_x = -2
            eye_offset_y = -2
        elif self.direction == (0, 10):  # Down
            eye_offset_x = 0
            eye_offset_y = 2
        elif self.direction == (0, -10):  # Up
            eye_offset_x = 0
            eye_offset_y = -2
            
        # Apply idle behavior eye modifications
        if self.current_idle_behavior == "look_around":
            eye_offset_x += math.sin(self.idle_timer * 0.1) * 2
            eye_offset_y += math.cos(self.idle_timer * 0.1) * 2
        
        # Calculate eye positions
        left_eye_pos = (face_center[0] - 3 + eye_offset_x, face_center[1] - 2 + eye_offset_y)
        right_eye_pos = (face_center[0] + 3 + eye_offset_x, face_center[1] - 2 + eye_offset_y)
        
        # Draw eyes - bigger eyes for excitement
        eye_size = self.eyes_size
        if self.emotion_state == "excited":
            eye_size += 1
        elif self.emotion_state == "sad":
            eye_size = max(1, eye_size - 1)
            
        # Don't show pupils during blinking
        if not self.blinking:
            # Draw eye whites
            pygame.draw.circle(surface, WHITE, (int(left_eye_pos[0]), int(left_eye_pos[1])), eye_size)
            pygame.draw.circle(surface, WHITE, (int(right_eye_pos[0]), int(right_eye_pos[1])), eye_size)
            
            # Draw pupils
            pupil_offset_x = 0.5 if self.direction[0] > 0 else (-0.5 if self.direction[0] < 0 else 0)
            pupil_offset_y = 0.5 if self.direction[1] > 0 else (-0.5 if self.direction[1] < 0 else 0)
            
            pupil_left = (int(left_eye_pos[0] + pupil_offset_x), int(left_eye_pos[1] + pupil_offset_y))
            pupil_right = (int(right_eye_pos[0] + pupil_offset_x), int(right_eye_pos[1] + pupil_offset_y))
            
            pygame.draw.circle(surface, BLACK, pupil_left, max(1, eye_size // 2))
            pygame.draw.circle(surface, BLACK, pupil_right, max(1, eye_size // 2))
        else:
            # Draw closed eyes (horizontal lines) when blinking
            pygame.draw.line(surface, BLACK, 
                            (int(left_eye_pos[0] - eye_size), int(left_eye_pos[1])),
                            (int(left_eye_pos[0] + eye_size), int(left_eye_pos[1])), 2)
            pygame.draw.line(surface, BLACK, 
                            (int(right_eye_pos[0] - eye_size), int(right_eye_pos[1])),
                            (int(right_eye_pos[0] + eye_size), int(right_eye_pos[1])), 2)
        
        # Draw mouth based on emotion state - helps kids recognize emotions
        mouth_center = (face_center[0], face_center[1] + 3)
        
        if self.emotion_state == "happy" or self.emotion_state == "excited":
            # Happy mouth (curving upward)
            pygame.draw.arc(surface, BLACK,
                           (int(mouth_center[0] - 4), int(mouth_center[1] - 2), 8, 6),
                           0, math.pi, 2)
        elif self.emotion_state == "sad":
            # Sad mouth (curving downward)
            pygame.draw.arc(surface, BLACK,
                           (int(mouth_center[0] - 4), int(mouth_center[1] - 4), 8, 8),
                           math.pi, 2 * math.pi, 2)
        else:
            # Neutral/default mouth
            if self.mouth_open:
                # Draw open mouth as a small circle
                pygame.draw.circle(surface, (150, 0, 0), 
                                   (int(mouth_center[0]), int(mouth_center[1])), 2)
            else:
                # Closed mouth as a line
                pygame.draw.line(surface, BLACK,
                                (int(mouth_center[0] - 2), int(mouth_center[1])),
                                (int(mouth_center[0] + 2), int(mouth_center[1])), 1)

    def show_emotion(self, emotion, duration=60):
        """Show an emotion for a duration (in frames).
        Expressive characters help children develop emotional intelligence."""
        self.emotion_state = emotion
        self.expression_timer = duration
        
        # Set expression based on emotion
        if emotion == "happy":
            self.expression = "smile"
        elif emotion == "excited":
            self.expression = "excited"
            self.eyes_size = 4  # Bigger eyes when excited
        elif emotion == "sad":
            self.expression = "sad"
        else:
            self.expression = "neutral"

    def start_celebration(self):
        """Start a celebration animation (particle burst).
        Celebrates success to build positive reinforcement."""
        self.celebrating = True
        self.celebration_timer = 60  # Celebrate for 1 second
        
        # Create celebratory particles around the snake's head
        if len(self.body) > 0:
            head_pos = (self.body[0][0] + self.size//2, self.body[0][1] + self.size//2)
            
            for _ in range(20):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(0.5, 2.0)
                size = random.uniform(2, 5)
                color = random.choice([YELLOW, ORANGE, BRIGHT_GREEN, BRIGHT_CYAN])
                
                self.celebration_particles.append({
                    'pos': list(head_pos),
                    'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                    'size': size,
                    'color': color,
                    'lifetime': random.randint(30, 60)
                })

    def update_celebration(self):
        """Update celebration animation state."""
        self.celebration_timer -= 1
        if self.celebration_timer <= 0:
            self.celebrating = False
        
        # Update particles
        particles_to_keep = []
        for particle in self.celebration_particles:
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                continue
                
            # Move particle
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            
            # Add gravity effect
            particle['vel'][1] += 0.04
            
            particles_to_keep.append(particle)
            
        self.celebration_particles = particles_to_keep

    def draw_celebration_particles(self, surface):
        """Draw celebration particles."""
        for particle in self.celebration_particles:
            alpha = min(255, particle['lifetime'] * 4)
            pygame.draw.circle(
                surface,
                particle['color'],
                (int(particle['pos'][0]), int(particle['pos'][1])),
                int(particle['size'])
            )

    def update_idle_behavior(self):
        """Update idle behaviors to keep the snake feeling alive and engaging."""
        # Increment idle timer
        self.idle_timer += 1
        
        # Start a new idle behavior if we're not doing one
        if self.current_idle_behavior is None and random.random() < 0.01:  # 1% chance per frame
            self.current_idle_behavior = random.choice(self.idle_behaviors)
            self.idle_timer = 0
        
        # End the current idle behavior if it's gone on long enough
        if self.current_idle_behavior and self.idle_timer > self.idle_duration:
            self.current_idle_behavior = None
            
        # Execute current idle behavior
        if self.current_idle_behavior == "look_around":
            # Eyes will move during the face drawing
            pass
        elif self.current_idle_behavior == "wiggle":
            # Increase wiggle speed temporarily
            self.wiggle_speed = 0.4
        elif self.current_idle_behavior == "blink":
            # Force a blink if we're in this idle state
            if self.idle_timer % 20 == 0:  # Blink every 20 frames during this state
                self.blinking = True
                self.blink_timer = 10
        elif self.current_idle_behavior == "color_shift":
            # Temporarily show rainbow pulsing
            hue = (self.idle_timer % 100) / 100.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            self.color = (int(r * 255), int(g * 255), int(b * 255))
        else:
            # Reset to default behavior
            self.wiggle_speed = 0.2
            self.color = SNAKE_COLOR

    def generate_sparkles(self):
        """Generate sparkle positions along the snake's body."""
        self.sparkle_positions = []
        # Add sparkles along every few segments
        for i in range(0, len(self.body), 2):
            if i < len(self.body) and random.random() < 0.5:
                segment = self.body[i]
                self.sparkle_positions.append((
                    segment[0] + random.randint(0, self.size),
                    segment[1] + random.randint(0, self.size),
                    random.randint(1, 3)  # Sparkle size
                ))

    def activate_rainbow_mode(self, duration=180):
        """Activate rainbow mode for specified duration in frames."""
        self.rainbow_mode = True
        self.rainbow_timer = duration
        self.show_sparkles = True
        self.generate_sparkles()

    def draw_sparkles(self, surface):
        """Draw sparkles along the snake's body."""
        for pos_x, pos_y, size in self.sparkle_positions:
            # Make sparkles twinkle
            if random.random() < 0.7:  # 70% chance to show each sparkle on each frame
                bright = random.randint(200, 255)
                color = (bright, bright, random.randint(100, 200))  # Golden sparkle color
                
                # Draw a simple star-like sparkle
                pygame.draw.line(surface, color, 
                               (pos_x - size, pos_y), 
                               (pos_x + size, pos_y), 2)
                pygame.draw.line(surface, color, 
                               (pos_x, pos_y - size), 
                               (pos_x, pos_y + size), 2)
                
                # Add diagonal lines for a star effect
                small_size = max(1, size - 1)
                pygame.draw.line(surface, color, 
                               (pos_x - small_size, pos_y - small_size), 
                               (pos_x + small_size, pos_y + small_size), 1)
                pygame.draw.line(surface, color, 
                               (pos_x - small_size, pos_y + small_size), 
                               (pos_x + small_size, pos_y - small_size), 1)

    def draw_enhanced_trail(self, surface):
        """Draw a fading trail behind the snake for enhanced visual appeal."""
        if not self.trail_positions:
            return
            
        for i, pos in enumerate(self.trail_positions):
            alpha = int(self.speed_trail_alpha * (i / len(self.trail_positions)))
            if alpha > 10:  # Only draw if visible enough
                trail_color = (*self.color, alpha)
                try:
                    # Create a surface for alpha blending
                    trail_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    trail_surface.fill(trail_color)
                    surface.blit(trail_surface, pos)
                except:
                    # Fallback to simple drawing
                    pygame.draw.rect(surface, self.color, (*pos, self.size, self.size))

    def draw_glow_effect(self, surface, segment, color, size):
        """Draw a glow effect around snake segments."""
        glow_radius = int(size * 0.3 * self.glow_intensity)
        for i in range(glow_radius, 0, -1):
            alpha = int(100 * self.glow_intensity * (glow_radius - i) / glow_radius)
            if alpha > 5:
                try:
                    glow_surface = pygame.Surface((size + i * 2, size + i * 2), pygame.SRCALPHA)
                    glow_color = (*color, alpha)
                    pygame.draw.rect(glow_surface, glow_color, (0, 0, size + i * 2, size + i * 2))
                    surface.blit(glow_surface, (segment[0] - i, segment[1] - i))
                except:
                    break

    def get_head_rect(self):
        """Return a pygame.Rect for the snake's head for collision detection."""
        if len(self.body) > 0:
            head = self.body[0]
            return pygame.Rect(head[0], head[1], self.size, self.size)
        return pygame.Rect(0, 0, self.size, self.size)

    def check_self_collision(self):
        """Check if the snake has collided with itself."""
        if len(self.body) > 4:  # Need at least 5 segments to collide with self
            head = self.body[0]
            for segment in self.body[4:]:  # Skip first few segments
                head_rect = pygame.Rect(head[0], head[1], self.size, self.size)
                segment_rect = pygame.Rect(segment[0], segment[1], self.size, self.size)
                if head_rect.colliderect(segment_rect):
                    return True
        return False