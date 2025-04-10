# game_screen.py
import pygame
import random
import math
import colorsys
from constants import *
from entities.snake import Snake
from utils import (draw_text, get_cage_rect, create_reward_burst, update_particles, 
                  draw_particles, get_motivational_message, draw_animated_text,
                  create_progress_indicator, display_instructor_feedback, update_difficulty,
                  show_variable_reward, apply_growth_mindset_message, avoid_learned_helplessness)

class GameScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = FONT_MEDIUM
        
        # Create the snake object
        self.snake = Snake(game_state)
        
        # Initialize rewards and feedback systems
        self.particles = []
        self.floating_messages = []
        self.message_frame = 0
        self.consecutive_failures = 0
        self.instructor_message = None
        self.instructor_timer = 0
        self.show_hint = False
        self.hint_timer = 0
        
        # Positive reinforcement tracking
        self.last_success_time = 0
        self.encouragement_timer = 0
        self.last_encouragement = ""
        
        # Variables for dynamic progress visualization
        self.progress_animation = 0
        self.progress_stars = []
        
        # Store screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Goals and targets - visual goal setting important for children
        self.current_goal = ""
        self.goal_progress = 0
        self.goal_target = 3  # Start with small achievable goal
        
        # Initialize food items
        self.food_items = []
        self.generate_new_food(3)  # Start with 3 food items
        
        # Achievement system - badges and visual markers of success
        self.achievements = []
        self.earned_achievements = []
        self.achievement_celebration = None
        self.achievement_milestones = {
            "first_food": {
                "name": "First Bite!",
                "description": "You ate your first food!",
                "icon": "🍎",
                "earned": False
            },
            "three_in_a_row": {
                "name": "Triple Treat!",
                "description": "You got three foods in a row!",
                "icon": "🔥",
                "earned": False
            },
            "level_master": {
                "name": "Level Master!",
                "description": "You're ready for the next level!",
                "icon": "🏆",
                "earned": False
            },
            "speed_demon": {
                "name": "Speed Demon!",
                "description": "You're moving so fast!",
                "icon": "⚡",
                "earned": False
            },
            "super_snake": {
                "name": "Super Snake!",
                "description": "Look how big you've grown!",
                "icon": "🐍",
                "earned": False
            }
        }
        
        # Streaks system - encourages continuous engagement
        self.current_streak = 0
        self.highest_streak = 0
        self.streak_messages = ["Good start!", "Keep going!", "Amazing streak!"]
        
        # Surprise mechanics - creates excitement and novelty
        self.surprise_timer = random.uniform(15, 30)  # Random time until first surprise
        self.surprise_active = False
        self.surprise_type = None
        self.surprise_duration = 0
        self.surprise_effects = {
            "rainbow_mode": {"active": False, "timer": 0},
            "speed_boost": {"active": False, "timer": 0},
            "food_party": {"active": False, "timer": 0},
            "giant_snake": {"active": False, "timer": 0, "original_size": 0}
        }
        
        # Add background animation elements - visual interest without sound
        self.background_shapes = []
        self.generate_background_shapes(15)  # Create initial background elements
        
        # Enhanced visual reward system
        self.last_reward_time = 0
        self.reward_animations = []
        
        # Add floating bubbles - creates a playful atmosphere
        self.bubbles = []
        self.generate_bubbles(10)
        
        # Add shimmer effect on food items - draws attention
        self.shimmer_offset = 0
        
        # Add congratulatory emojis that appear when hitting achievements
        self.emojis = []
        
        # Background color mood - changes subtly based on game state
        self.bg_hue = 0.6  # Start with calm blue
        self.target_bg_hue = 0.6
        
        # Border animation for cage
        self.border_animation_offset = 0
        
        # Countdown visual effects
        self.countdown_active = False
        self.countdown_value = 0
        self.countdown_scale = 1.0
        self.countdown_color = WHITE

    def update_dimensions(self, width, height):
        """Update screen dimensions when window is resized."""
        self.screen_width = width
        self.screen_height = height
        
    def generate_new_food(self, count=1):
        """Generate new food items for the snake."""
        cage_rect = get_cage_rect(self.screen_width, self.screen_height)
        padding = 20  # Keep food away from edges
        
        for _ in range(count):
            # Choose a food type - each type has unique psychological appeal
            food_type = random.choice(["number", "letter", "shape"])
            
            if food_type == "number":
                value = str(random.randint(1, 10))
                color = BRIGHT_BLUE
            elif food_type == "letter":
                value = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                color = BRIGHT_PURPLE
            else:  # shape
                value = random.choice(SHAPE_NAMES)
                color = BRIGHT_GREEN
                
            # Position food within the cage area
            x = random.randint(cage_rect.left + padding, cage_rect.right - padding)
            y = random.randint(cage_rect.top + padding, cage_rect.bottom - padding)
            
            # Size that's appealing and visible for young children
            size = random.randint(15, 25)
            
            # Add wiggle and pulse for visual interest - movement attracts attention
            wiggle_speed = random.uniform(0.05, 0.15)
            wiggle_amount = random.uniform(3, 7)
            
            # Each food item has unique properties for varied engagement
            self.food_items.append({
                "type": food_type,
                "value": value,
                "pos": (x, y),
                "color": color,
                "size": size,
                "wiggle_offset": random.uniform(0, 6.28),  # Random phase
                "wiggle_speed": wiggle_speed,
                "wiggle_amount": wiggle_amount,
                "pulse": 0,
                "pulse_dir": 1
            })

    def generate_background_shapes(self, count):
        """Generate floating background shapes for visual interest."""
        self.background_shapes = []
        for _ in range(count):
            shape_type = random.choice(["circle", "square", "triangle", "star"])
            size = random.randint(10, 30)
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            color = (random.randint(20, 50), random.randint(20, 50), random.randint(20, 50))
            speed = random.uniform(0.2, 1.0)
            direction = random.uniform(0, math.pi * 2)
            
            self.background_shapes.append({
                "type": shape_type,
                "size": size,
                "pos": [x, y],
                "color": color,
                "speed": speed,
                "direction": direction,
                "rotation": 0,
                "rotation_speed": random.uniform(-0.02, 0.02)
            })

    def generate_bubbles(self, count):
        """Generate floating bubbles for decoration."""
        self.bubbles = []
        for _ in range(count):
            size = random.randint(5, 20)
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(0.3, 1.0)
            wobble_speed = random.uniform(0.02, 0.1)
            
            self.bubbles.append({
                "size": size,
                "pos": [x, y],
                "speed": speed,
                "wobble": 0,
                "wobble_speed": wobble_speed
            })
    
    def add_emoji(self, emoji, position, duration=120):
        """Add a congratulatory emoji at the given position."""
        self.emojis.append({
            "emoji": emoji,
            "pos": list(position),
            "lifetime": duration,
            "scale": 0.1,  # Start small and grow
            "vel": [0, -1],  # Float upward
            "rotation": random.uniform(0, math.pi * 2),
            "rotation_speed": random.uniform(-0.05, 0.05)
        })

    def handle_events(self, event):
        """Process input events."""
        if event.type == pygame.KEYDOWN:
            # Arrow key controls - simple directional input for young children
            if event.key == pygame.K_UP:
                self.snake.change_direction((0, -10))
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction((0, 10))
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction((-10, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction((10, 0))
            # Pause menu with P
            elif event.key == pygame.K_p:
                self.game_state.current_state = STATE_MENU_SELECT
                
    def update(self, dt):
        """Update game state."""
        # Update time-based variables
        self.message_frame += 1
        self.encouragement_timer -= dt
        self.instructor_timer -= dt
        if self.show_hint:
            self.hint_timer -= dt
            if self.hint_timer <= 0:
                self.show_hint = False
        
        # Update surprise mechanics timer
        if not self.surprise_active:
            self.surprise_timer -= dt
            if self.surprise_timer <= 0:
                self.trigger_surprise()
        else:
            self.surprise_duration -= dt
            if self.surprise_duration <= 0:
                self.end_surprise()
        
        # Update active surprise effects
        self.update_surprise_effects(dt)
        
        # Move the snake
        self.snake.move()
        
        # Check for food collisions
        self.check_food_collisions()
        
        # Update particles
        self.particles = update_particles(self.particles)
        
        # Update floating messages
        self.update_floating_messages()
        
        # Update progress animation
        self.progress_animation += dt * 2  # Speed factor for animation
        
        # Check win condition
        if self.game_state.score_in_row >= self.game_state.current_level * 3:  # Level-based target
            self.game_state.current_state = STATE_WIN_LEVEL_ANIMATING
            
        # Update food animations
        self.update_food_animations()
        
        # Add periodic encouragement if player hasn't succeeded recently
        current_time = pygame.time.get_ticks() / 1000  # In seconds
        time_since_success = current_time - self.last_success_time
        
        # If it's been a while since success and encouragement timer expired
        if time_since_success > 10 and self.encouragement_timer <= 0:
            self.add_floating_message(
                "You can do it! Keep trying!",
                (self.screen_width // 2, self.screen_height // 2 - 50),
                BRIGHT_GREEN
            )
            self.encouragement_timer = 8  # Wait 8 seconds before another encouragement
            
            # 50% chance to also show instructor hint
            if random.random() < 0.5:
                self.show_instructor_message("encouragement")
                
        # Occasionally show a growth mindset message
        if random.random() < 0.001:  # 0.1% chance per frame
            apply_growth_mindset_message(self.game_state, success=True)
        
        # Update background shapes
        for shape in self.background_shapes:
            # Move shapes slowly across screen
            shape["pos"][0] += math.cos(shape["direction"]) * shape["speed"]
            shape["pos"][1] += math.sin(shape["direction"]) * shape["speed"]
            
            # Update rotation
            shape["rotation"] += shape["rotation_speed"]
            
            # Wrap around screen edges
            if shape["pos"][0] < -shape["size"]:
                shape["pos"][0] = self.screen_width + shape["size"]
            elif shape["pos"][0] > self.screen_width + shape["size"]:
                shape["pos"][0] = -shape["size"]
                
            if shape["pos"][1] < -shape["size"]:
                shape["pos"][1] = self.screen_height + shape["size"]
            elif shape["pos"][1] > self.screen_height + shape["size"]:
                shape["pos"][1] = -shape["size"]
        
        # Update bubbles
        for bubble in self.bubbles:
            # Update position - bubbles rise up
            bubble["pos"][1] -= bubble["speed"]
            
            # Add subtle wobble for organic movement
            bubble["wobble"] += bubble["wobble_speed"]
            wobble_x = math.sin(bubble["wobble"]) * 1.5
            bubble["pos"][0] += wobble_x
            
            # Reset bubbles that go off top of screen
            if bubble["pos"][1] + bubble["size"] < 0:
                bubble["pos"][1] = self.screen_height + bubble["size"]
                bubble["pos"][0] = random.randint(0, self.screen_width)
        
        # Update shimmer effect on food
        self.shimmer_offset += 0.1
        
        # Update reward animations
        remaining_rewards = []
        for reward in self.reward_animations:
            reward["lifetime"] -= dt
            if reward["lifetime"] <= 0:
                continue
                
            # Update position
            reward["pos"][0] += reward["velocity"][0]
            reward["pos"][1] += reward["velocity"][1]
            
            # Apply gravity to falling particles
            if reward["type"] == "particle":
                reward["velocity"][1] += 0.1  # Gravity
            
            remaining_rewards.append(reward)
        self.reward_animations = remaining_rewards
        
        # Update emoji animations
        remaining_emojis = []
        for emoji in self.emojis:
            emoji["lifetime"] -= 1
            if emoji["lifetime"] <= 0:
                continue
                
            # Update position
            emoji["pos"][0] += emoji["vel"][0]
            emoji["pos"][1] += emoji["vel"][1]
            
            # Update scale - grow quickly then stabilize
            if emoji["scale"] < 1.0:
                emoji["scale"] = min(1.0, emoji["scale"] + 0.05)
                
            # Update rotation
            emoji["rotation"] += emoji["rotation_speed"]
            
            remaining_emojis.append(emoji)
        self.emojis = remaining_emojis
        
        # Update border animation
        self.border_animation_offset += 0.5
        
        # Update background hue - smooth transition toward target
        if abs(self.bg_hue - self.target_bg_hue) > 0.01:
            self.bg_hue += (self.target_bg_hue - self.bg_hue) * 0.01
            
        # Update countdown animation if active
        if self.countdown_active:
            self.countdown_scale -= 0.02
            if self.countdown_scale <= 0:
                self.countdown_active = False

    def trigger_surprise(self):
        """Trigger a surprise gameplay mechanic to maintain engagement."""
        # Choose a surprise type - variety maintains interest
        surprise_types = ["rainbow_mode", "food_party", "speed_boost", "giant_snake"]
        self.surprise_type = random.choice(surprise_types)
        self.surprise_active = True
        
        # Duration varies by surprise type - unpredictable timing increases excitement
        if self.surprise_type == "rainbow_mode":
            self.surprise_duration = 10.0  # 10 seconds
            self.surprise_effects["rainbow_mode"]["active"] = True
            self.surprise_effects["rainbow_mode"]["timer"] = self.surprise_duration
            
            # Visual feedback for surprise activation
            self.add_floating_message(
                "✨ RAINBOW SNAKE! ✨",
                (self.screen_width // 2, self.screen_height // 2 - 50),
                YELLOW,
                size=36,
                lifetime=180
            )
            
            # Activate rainbow mode on snake
            if hasattr(self.snake, 'activate_rainbow_mode'):
                self.snake.activate_rainbow_mode(600)  # 10 seconds at 60fps
                
        elif self.surprise_type == "food_party":
            self.surprise_duration = 5.0  # 5 seconds
            self.surprise_effects["food_party"]["active"] = True
            self.surprise_effects["food_party"]["timer"] = self.surprise_duration
            
            # Visual feedback
            self.add_floating_message(
                "🎉 FOOD PARTY! 🎉",
                (self.screen_width // 2, self.screen_height // 2 - 50),
                BRIGHT_GREEN,
                size=36,
                lifetime=180
            )
            
            # Add extra food items
            self.generate_new_food(8)
            
        elif self.surprise_type == "speed_boost":
            self.surprise_duration = 7.0  # 7 seconds
            self.surprise_effects["speed_boost"]["active"] = True
            self.surprise_effects["speed_boost"]["timer"] = self.surprise_duration
            
            # Visual feedback
            self.add_floating_message(
                "⚡ SUPER SPEED! ⚡",
                (self.screen_width // 2, self.screen_height // 2 - 50),
                BRIGHT_CYAN,
                size=36,
                lifetime=180
            )
            
            # Store original speed of food items to restore later
            for food in self.food_items:
                food["original_wiggle_speed"] = food["wiggle_speed"]
                food["wiggle_speed"] *= 3  # Triple the wiggle animation speed
            
        elif self.surprise_type == "giant_snake":
            self.surprise_duration = 8.0  # 8 seconds
            self.surprise_effects["giant_snake"]["active"] = True
            self.surprise_effects["giant_snake"]["timer"] = self.surprise_duration
            
            # Visual feedback
            self.add_floating_message(
                "🐍 GIANT SNAKE! 🐍",
                (self.screen_width // 2, self.screen_height // 2 - 50),
                PURPLE,
                size=36,
                lifetime=180
            )
            
            # This would normally change the snake's size, but for now
            # we'll just add visual effects
            self.add_reward_effect((self.screen_width//2, self.screen_height//2), "confetti")
            
        # Reset surprise timer for next surprise
        self.surprise_timer = random.uniform(20, 40)  # 20-40 seconds until next surprise

    def end_surprise(self):
        """End active surprise effect and reset."""
        self.surprise_active = False
        
        # Reset specific surprise effects
        if self.surprise_type == "food_party":
            # Leave extra food for player to collect
            pass
            
        elif self.surprise_type == "speed_boost":
            # Reset food wiggle speed
            for food in self.food_items:
                if hasattr(food, "original_wiggle_speed"):
                    food["wiggle_speed"] = food.get("original_wiggle_speed", food["wiggle_speed"])
        
        # Clear all active surprise effects
        for effect in self.surprise_effects:
            self.surprise_effects[effect]["active"] = False
            self.surprise_effects[effect]["timer"] = 0
            
        # Visual feedback that surprise has ended
        self.add_floating_message(
            "Surprise ended!",
            (self.screen_width // 2, self.screen_height // 2 + 50),
            WHITE,
            lifetime=60
        )

    def update_surprise_effects(self, dt):
        """Update active surprise effects."""
        # Update rainbow mode
        if self.surprise_effects["rainbow_mode"]["active"]:
            self.surprise_effects["rainbow_mode"]["timer"] -= dt
            if self.surprise_effects["rainbow_mode"]["timer"] <= 0:
                self.surprise_effects["rainbow_mode"]["active"] = False
            
        # Update food party effect
        if self.surprise_effects["food_party"]["active"]:
            self.surprise_effects["food_party"]["timer"] -= dt
            if self.surprise_effects["food_party"]["timer"] <= 0:
                self.surprise_effects["food_party"]["active"] = False
                
        # Update speed boost
        if self.surprise_effects["speed_boost"]["active"]:
            self.surprise_effects["speed_boost"]["timer"] -= dt
            if self.surprise_effects["speed_boost"]["timer"] <= 0:
                self.surprise_effects["speed_boost"]["active"] = False
                
        # Update giant snake
        if self.surprise_effects["giant_snake"]["active"]:
            self.surprise_effects["giant_snake"]["timer"] -= dt
            if self.surprise_effects["giant_snake"]["timer"] <= 0:
                self.surprise_effects["giant_snake"]["active"] = False

    def add_floating_message(self, text, pos, color, size=24, lifetime=120, velocity=(0, -1)):
        """Add a floating message to the screen."""
        self.floating_messages.append({
            "text": text,
            "pos": list(pos),
            "color": color,
            "size": size,
            "lifetime": lifetime,
            "velocity": velocity,
            "scale": 0.1,  # Start small
            "growth_dir": 1,  # 1=growing, -1=shrinking
            "angle": random.uniform(-0.1, 0.1)  # Slight tilt
        })

    def update_floating_messages(self):
        """Update floating message animations."""
        updated_messages = []
        
        for msg in self.floating_messages:
            # Update lifetime
            msg["lifetime"] -= 1
            if msg["lifetime"] <= 0:
                continue
                
            # Update position
            msg["pos"][0] += msg["velocity"][0]
            msg["pos"][1] += msg["velocity"][1]
            
            # Update scale - grow quickly then stabilize
            if msg["scale"] < 1.0 and msg["growth_dir"] > 0:
                msg["scale"] = min(1.0, msg["scale"] + 0.1)
            
            # Start shrinking near the end of lifetime
            if msg["lifetime"] < 30:
                msg["scale"] = max(0.1, msg["scale"] - 0.03)
                
            updated_messages.append(msg)
            
        self.floating_messages = updated_messages

    def draw_floating_messages(self):
        """Draw floating message animations."""
        for msg in self.floating_messages:
            # Calculate size based on scale and animation
            font_size = int(msg["size"] * msg["scale"])
            if font_size < 8:  # Skip if too small
                continue
                
            try:
                # Create font and render text
                font = pygame.font.SysFont("Arial", font_size, bold=True)
                text_surf = font.render(msg["text"], True, msg["color"])
                
                # Rotate slightly for visual appeal
                rotated_surf = pygame.transform.rotate(text_surf, msg["angle"] * 10)
                
                # Position the text
                text_rect = rotated_surf.get_rect(center=msg["pos"])
                
                # Draw shadow for better visibility
                shadow_surf = pygame.font.SysFont("Arial", font_size, bold=True).render(
                    msg["text"], True, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(msg["pos"][0] + 2, msg["pos"][1] + 2))
                self.screen.blit(shadow_surf, shadow_rect)
                
                # Draw the text
                self.screen.blit(rotated_surf, text_rect)
                
            except Exception as e:
                print(f"Error rendering floating message: {e}")

    def check_food_collisions(self):
        """Check if snake has collided with food items."""
        if not self.food_items:
            return
            
        snake_head = self.snake.body[0]
        head_rect = pygame.Rect(snake_head[0], snake_head[1], self.snake.size, self.snake.size)
        
        for i, food in enumerate(self.food_items):
            food_x, food_y = food["pos"]
            food_size = food["size"]
            food_rect = pygame.Rect(
                food_x - food_size/2, 
                food_y - food_size/2,
                food_size, 
                food_size
            )
            
            if head_rect.colliderect(food_rect):
                # Remove this food item
                collected_food = self.food_items.pop(i)
                
                # Increase score and grow snake
                self.game_state.score += 1
                self.game_state.score_in_row += 1
                self.game_state.snake_size += 1
                self.snake.grow()
                
                # Update last success time
                self.last_success_time = pygame.time.get_ticks() / 1000  # In seconds
                
                # Create visual rewards
                self.celebrate_food_collected(food)
                
                # Check for achievements
                self.check_achievements()
                
                # Create surprise rewards occasionally
                if random.random() < 0.3:  # 30% chance
                    self.add_reward_effect(food["pos"], "stars")
                    
                # Add new food items - always keep at least 3 on screen
                if len(self.food_items) < 3:
                    self.generate_new_food(random.randint(1, 3))
                    
                # Show countdown animation occasionally
                if random.random() < 0.3:  # 30% chance 
                    self.show_countdown(random.randint(1, 5))
                
                # Reset failure counter
                self.consecutive_failures = 0
                break

    def celebrate_food_collected(self, food):
        """Create celebration effects when food is collected."""
        # Determine celebration type based on food type
        celebration_type = food["type"]
        position = food["pos"]
        
        # Create reward burst particles
        self.particles.extend(create_reward_burst(
            position,
            color=food["color"],
            count=30,
            success=True
        ))
        
        # Create floating message with motivational text
        message = get_motivational_message(
            correct_count=self.game_state.score,
            score_streak=self.game_state.score_in_row
        )
        
        self.add_floating_message(
            message,
            (position[0], position[1] - 30),
            BRIGHT_GREEN,
            velocity=(random.uniform(-0.3, 0.3), -1.5)
        )
        
        # Show the food value collected
        self.add_floating_message(
            f"+{food['value']}",
            (position[0], position[1]),
            YELLOW,
            size=32,
            velocity=(0, -2)
        )
        
        # Add emoji based on the food type - kids love emojis
        if food["type"] == "number":
            emoji = "🔢"
        elif food["type"] == "letter":
            emoji = "🔤"
        else:  # shape
            emoji = "🔷"
            
        # Show emoji animation
        self.add_emoji(emoji, position)
        
        # Check for streak rewards
        if self.game_state.score_in_row >= 3:
            # Start rainbow effect on 3+ streak
            if hasattr(self.snake, 'activate_rainbow_mode') and random.random() < 0.5:
                self.snake.activate_rainbow_mode(120)  # 2 second rainbow effect
                
        # Apply growth mindset message
        if random.random() < 0.3:  # 30% chance
            apply_growth_mindset_message(self.game_state, success=True)

    def update_food_animations(self):
        """Update animations for food items."""
        for food in self.food_items:
            # Update wiggle offset
            food["wiggle_offset"] += food["wiggle_speed"]
            
            # Update pulse animation
            if food["pulse_dir"] > 0:
                food["pulse"] = min(5, food["pulse"] + 0.2)
                if food["pulse"] >= 5:
                    food["pulse_dir"] = -1
            else:
                food["pulse"] = max(-2, food["pulse"] - 0.2)
                if food["pulse"] <= -2:
                    food["pulse_dir"] = 1

    def check_achievements(self):
        """Check and award achievements."""
        # First food achievement
        if self.game_state.score == 1 and not self.achievement_milestones["first_food"]["earned"]:
            self.award_achievement("first_food")
            
        # Three in a row achievement
        if self.game_state.score_in_row >= 3 and not self.achievement_milestones["three_in_a_row"]["earned"]:
            self.award_achievement("three_in_a_row")
            
        # Level master achievement - approaching level completion
        target_score = self.game_state.current_level * 3
        if self.game_state.score_in_row >= target_score - 1 and not self.achievement_milestones["level_master"]["earned"]:
            self.award_achievement("level_master")
            
        # Snake length achievement
        if self.game_state.snake_size >= 10 and not self.achievement_milestones["super_snake"]["earned"]:
            self.award_achievement("super_snake")

    def show_instructor_message(self, message_type):
        """Show an instructor message of the specified type."""
        self.instructor_message = message_type
        self.instructor_timer = 5.0  # Show for 5 seconds

    def draw_hint(self, cage_rect):
        """Draw a visual hint to help the player."""
        if not self.food_items:
            return
            
        # Choose the first food item to hint toward
        target_food = self.food_items[0]
        food_pos = target_food["pos"]
        
        # Get snake head position
        snake_head = self.snake.body[0] if self.snake.body else (0, 0)
        head_pos = (snake_head[0] + self.snake.size/2, snake_head[1] + self.snake.size/2)
        
        # Calculate direction
        dx = food_pos[0] - head_pos[0]
        dy = food_pos[1] - head_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Calculate arrow start and end points
            start_x = head_pos[0] + dx * self.snake.size
            start_y = head_pos[1] + dy * self.snake.size
            
            end_x = head_pos[0] + dx * min(distance, 100)
            end_y = head_pos[1] + dy * min(distance, 100)
            
            # Draw arrow line with pulsing effect
            pulse = 0.75 + 0.25 * math.sin(self.animation_frame * 0.1)
            arrow_color = (
                min(255, int(YELLOW[0] * pulse)),
                min(255, int(YELLOW[1] * pulse)),
                min(255, int(YELLOW[2] * pulse))
            )
            
            pygame.draw.line(
                self.screen,
                arrow_color,
                (int(start_x), int(start_y)),
                (int(end_x), int(end_y)),
                3
            )
            
            # Draw arrowhead
            arrowhead_length = 10
            angle = math.atan2(dy, dx)
            pygame.draw.polygon(
                self.screen,
                arrow_color,
                [
                    (int(end_x), int(end_y)),
                    (int(end_x - arrowhead_length * math.cos(angle - math.pi/6)),
                     int(end_y - arrowhead_length * math.sin(angle - math.pi/6))),
                    (int(end_x - arrowhead_length * math.cos(angle + math.pi/6)),
                     int(end_y - arrowhead_length * math.sin(angle + math.pi/6)))
                ]
            )
            
            # Draw pulsing circle around target food
            circle_pulse = 0.5 + 0.5 * math.sin(self.animation_frame * 0.2)
            circle_radius = target_food["size"] * (1 + circle_pulse * 0.5)
            
            pygame.draw.circle(
                self.screen,
                arrow_color,
                (int(food_pos[0]), int(food_pos[1])),
                int(circle_radius),
                2
            )

    def draw_ui(self, cage_rect):
        """Draw UI elements."""
        # Draw score in top left
        score_text = f"Score: {self.game_state.score}"
        draw_text(self.screen, score_text, (20, 20), FONT_MEDIUM, WHITE)
        
        # Draw current level in top center
        level_text = f"Level {self.game_state.current_level}"
        draw_text(self.screen, level_text, 
                 (self.screen_width // 2, 20), FONT_MEDIUM, WHITE, center=True)
        
        # Draw progress bar for level completion
        target_items = self.game_state.current_level * 3
        progress_width = 200
        progress_height = 20
        progress_x = (self.screen_width - progress_width) // 2
        progress_y = 50
        
        # Background bar
        pygame.draw.rect(
            self.screen,
            DARK_GREY,
            (progress_x, progress_y, progress_width, progress_height),
            border_radius=progress_height // 2
        )
        
        # Calculate progress
        progress_ratio = min(1.0, self.game_state.score_in_row / target_items)
        fill_width = int(progress_width * progress_ratio)
        
        # Progress fill with animated gradient
        if fill_width > 0:
            # Create gradient based on progress
            if progress_ratio < 0.5:
                color = BLUE  # Blue for starting
            elif progress_ratio < 0.8:
                color = GREEN  # Green for good progress
            else:
                # Rainbow effect near completion - children love this visual reward
                progress_hue = (self.animation_frame % 360) / 360.0
                r, g, b = colorsys.hsv_to_rgb(progress_hue, 0.8, 0.9)
                color = (int(r * 255), int(g * 255), int(b * 255))
                
            pygame.draw.rect(
                self.screen,
                color,
                (progress_x, progress_y, fill_width, progress_height),
                border_radius=progress_height // 2
            )
                
        # Add shimmer effect on progress bar
        shimmer_pos = progress_x + int(math.sin(self.animation_frame * 0.05) * progress_width * 0.5 + progress_width * 0.5)
        if progress_x <= shimmer_pos <= progress_x + fill_width:
            # Only show shimmer on the filled portion
            shimmer_height = progress_height - 4
            shimmer_width = 10
            shimmer_y = progress_y + 2
            
            pygame.draw.rect(
                self.screen,
                (255, 255, 255, 150),  # Semi-transparent white
                (shimmer_pos - shimmer_width//2, shimmer_y, shimmer_width, shimmer_height),
                border_radius=shimmer_width // 2
            )
            
        # Draw streak counter if on a streak
        if self.game_state.score_in_row >= 2:
            streak_text = f"Streak: {self.game_state.score_in_row} 🔥"
            # Animate streak text for added excitement
            streak_scale = 1.0 + 0.1 * math.sin(self.animation_frame * 0.2)
            
            streak_font = pygame.font.SysFont("Arial", int(28 * streak_scale), bold=True)
            try:
                streak_surf = streak_font.render(streak_text, True, ORANGE)
                streak_rect = streak_surf.get_rect(center=(self.screen_width // 2, 85))
                self.screen.blit(streak_surf, streak_rect)
            except Exception as e:
                print(f"Error rendering streak text: {e}")
                draw_text(self.screen, streak_text, (self.screen_width // 2, 85), 
                         FONT_MEDIUM, ORANGE, center=True)
                         
        # Draw active surprise effect indicator
        if self.surprise_active:
            # Get the color based on surprise type
            if self.surprise_type == "rainbow_mode":
                # Rainbow cycling color
                hue = (self.animation_frame % 360) / 360.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                color = (int(r * 255), int(g * 255), int(b * 255))
                icon = "✨"
            elif self.surprise_type == "food_party":
                color = BRIGHT_GREEN
                icon = "🍎"
            elif self.surprise_type == "speed_boost":
                color = BRIGHT_CYAN
                icon = "⚡"
            elif self.surprise_type == "giant_snake":
                color = PURPLE
                icon = "🐍"
            else:
                color = WHITE
                icon = "?"
                
            # Draw surprise timer at top right
            timer_text = f"{icon} {int(self.surprise_duration)}s"
            draw_text(self.screen, timer_text, 
                     (self.screen_width - 20, 20), FONT_MEDIUM, color, center=False)
                     
            # Draw animated border around screen
            border_width = 6
            pulse = 0.7 + 0.3 * math.sin(self.animation_frame * 0.1)
            border_color = (
                min(255, int(color[0] * pulse)),
                min(255, int(color[1] * pulse)),
                min(255, int(color[2] * pulse))
            )
            
            # Top and bottom borders
            pygame.draw.rect(
                self.screen,
                border_color,
                (0, 0, self.screen_width, border_width)
            )
            pygame.draw.rect(
                self.screen,
                border_color,
                (0, self.screen_height - border_width, self.screen_width, border_width)
            )
            
            # Left and right borders
            pygame.draw.rect(
                self.screen,
                border_color,
                (0, 0, border_width, self.screen_height)
            )
            pygame.draw.rect(
                self.screen,
                border_color,
                (self.screen_width - border_width, 0, border_width, self.screen_height)
            )
