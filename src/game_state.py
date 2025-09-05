# filepath: kindergarten-snake-game/kindergarten-snake-game/src/game_state.py
import random
from constants import *

class GameState:
    def __init__(self):
        self.current_state = STATE_WELCOME
        self.current_level = 1
        self.lives = 3
        self.score_in_row = 0
        self.request_timer = 0
        self.request_time_limit = 22
        self.snake_request = ""
        self.snake_size = 5
        self.snake_segments = []
        self.snake_pos = (0, 0)
        self.snake_direction = (1, 0)
        self.snake_speed = 3
        self.snake_target_pos = None
        self.snake_mouth_open = False
        self.snake_mouth_timer = 0
        self.snake_pulsing = False
        self.snake_pulse_hue = 0.0
        
        self.swallowed_items = []
        self.item_being_swallowed = None
        self.swallow_animation_timer = 0
        self.swallow_animation_duration = 30
        
        self.win_animation_timer = 0
        self.shake_intensity = 0
        self.shake_duration = 0
        self.flash_color = None
        self.flash_timer = 0
        self.cage_broken = False
        self.cage_bar_offsets = [0, 0, 0, 0]
        
        self.title_snake_segments = []
        self.title_snake_direction = (1, 0)
        self.title_snake_timer = 0
        self.title_snake_color_shift = 0
        
        self.food_items_available = []
        self.draggable_items = []
        self.dragging_item = None
        
        self.speech_bubble_rect = None
        self.dragging_bubble = False
        self.bubble_drag_offset_x = 0
        self.bubble_drag_offset_y = 0
        self.bubble_original_pos = (0, 0)
        
        self.menu_items = {}
        self.menu_confirm_button_rect = None
        
        self.loaded_resources = []
        
        self.background_snakes = []
        
        self.particles = []
        
        self.level_buttons = []
        
        self.available_powerups = []
        self.active_powerups = []
        self.powerup_timer = 0
        self.powerup_cooldown = 15.0
        self.max_powerups = 2
        
        self.total_correct_answers = 0
        self.total_wrong_answers = 0
        self.response_times = []
        self.skill_level = 0.5
        
    def reset_level(self, level, screen_width, screen_height, cage_rect):
        self.current_level = level
        self.lives = 3
        self.score_in_row = 0
        self.snake_size = 25  # Increased size for dramatic gameplay
        
        if cage_rect is not None:
            self.snake_pos = (cage_rect.centerx, cage_rect.centery)
        else:
            # Default position if cage_rect is None
            self.snake_pos = (screen_width // 2, screen_height // 2)
        self.snake_direction = (1, 0)
        self.snake_target_pos = None
        self.snake_pulsing = False
        self.cage_broken = False
        self.cage_bar_offsets = [0, 0, 0, 0]
        self.dragging_bubble = False
        self.dragging_item = None
        
        self.food_items_available = []
        self.draggable_items = []
        
        self.available_powerups = []
        self.active_powerups = []
        self.powerup_timer = 5.0
        
        self.response_times = []
        
        self.current_state = STATE_PLAYING
    
    def assign_new_request(self):
        self.snake_request = random.choice(ALL_FOOD_ITEMS)
    
    def check_win_condition(self):
        if self.score_in_row >= LEVELS[self.current_level]['target']:
            self.current_state = STATE_WIN_LEVEL_ANIMATING
            return True
        return False
    
    def update_powerups(self, dt):
        if len(self.available_powerups) < self.max_powerups:
            self.powerup_timer += dt
            if self.powerup_timer >= self.powerup_cooldown:
                self.generate_powerup()
                self.powerup_timer = 0
        
        active_powerups_remaining = []
        for powerup in self.active_powerups:
            powerup['duration'] -= dt
            if powerup['duration'] > 0:
                active_powerups_remaining.append(powerup)
        self.active_powerups = active_powerups_remaining
    
    def generate_powerup(self):
        possible_powerups = [
            {
                "id": "time_boost",
                "name": "Time Boost",
                "description": "Adds extra time to the current request",
                "icon": "⏰",
                "color": (50, 200, 50),
                "duration": 0,
                "effect_value": 5.0
            },
            {
                "id": "slow_timer",
                "name": "Slow Timer",
                "description": "Slows down the timer for a while",
                "icon": "⌛",
                "color": (50, 50, 200),
                "duration": 10.0,
                "effect_value": 0.5
            },
            {
                "id": "extra_life",
                "name": "Extra Life",
                "description": "Gives you an extra life",
                "icon": "❤️",
                "color": (200, 50, 50),
                "duration": 0,
                "effect_value": 1
            },
            {
                "id": "growth_boost",
                "name": "Growth Boost",
                "description": "Makes the snake grow faster on correct answers",
                "icon": "🔄",
                "color": (200, 150, 50),
                "duration": 20.0,
                "effect_value": 2.0
            }
        ]
        
        new_powerup = random.choice(possible_powerups).copy()
        cage_rect = get_cage_rect()
        edge_padding = 60
        positions = [
            (cage_rect.left - edge_padding, cage_rect.top + random.randint(0, cage_rect.height)),
            (cage_rect.right + edge_padding, cage_rect.top + random.randint(0, cage_rect.height)),
            (cage_rect.left + random.randint(0, cage_rect.width), cage_rect.top - edge_padding),
            (cage_rect.left + random.randint(0, cage_rect.width), cage_rect.bottom + edge_padding)
        ]
        new_powerup["position"] = random.choice(positions)
        self.available_powerups.append(new_powerup)
    
    def activate_powerup(self, powerup_id):
        for i, powerup in enumerate(self.available_powerups):
            if powerup['id'] == powerup_id:
                self.active_powerups.append(powerup)
                del self.available_powerups[i]
                return powerup
        return None
    
    def deactivate_powerup(self, powerup):
        pass
    
    def is_powerup_active(self, powerup_id):
        for powerup in self.active_powerups:
            if powerup['id'] == powerup_id:
                return True
        return False
    
    def get_timer_slowdown_factor(self):
        slowdown = 1.0
        for powerup in self.active_powerups:
            if powerup['id'] == "slow_timer":
                slowdown *= powerup['effect_value']
        return slowdown
    
    def get_growth_multiplier(self):
        multiplier = 1.0
        for powerup in self.active_powerups:
            if powerup['id'] == "growth_boost":
                multiplier *= powerup['effect_value']
        return multiplier
    
    def generate_variable_reward(self, reward_type="correct_answer"):
        pass
    
    def apply_reward(self, reward):
        pass
    
    def update_floating_texts(self):
        pass
    
    def draw_floating_texts(self, surface):
        pass