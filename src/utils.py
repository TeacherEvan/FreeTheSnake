# utils.py
import pygame
import math
import random
import traceback
from constants import *

def draw_text(surface, text, pos, font, color=WHITE, center=False, shadow=False, shadow_color=BLACK):
    try:
        # Defensive check for None font
        if font is None:
            print(f"Warning: Font is None for text '{text}'. Using default font.")
            font = pygame.font.Font(None, 36)
            
        text_surface = font.render(str(text), True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos

        if shadow:
            shadow_surface = font.render(str(text), True, shadow_color)
            shadow_rect = shadow_surface.get_rect()
            if center:
                shadow_rect.center = (pos[0] + 2, pos[1] + 2)
            else:
                shadow_rect.topleft = (text_rect.left + 2, text_rect.top + 2)
            surface.blit(shadow_surface, shadow_rect)

        surface.blit(text_surface, text_rect)
        return text_rect
    except Exception as e:
        print(f"Error rendering text '{text}': {e}")
        traceback.print_exc()
        try:
            error_font = pygame.font.Font(None, 20)
            err_surf = error_font.render("TxtErr", True, RED)
            err_rect = err_surf.get_rect()
            if center: err_rect.center = pos
            else: err_rect.topleft = pos
            surface.blit(err_surf, err_rect)
            return err_rect
        except:
            return pygame.Rect(pos[0], pos[1], 10, 10)

def get_cage_rect(screen_width, screen_height):
    min_dim = 50
    cage_h = max(min_dim, screen_height * 0.55)
    cage_w = max(min_dim, cage_h * 0.8)
    cage_w = min(cage_w, screen_width - 20)
    cage_h = min(cage_h, screen_height - 80)

    cage_x = max(10, (screen_width - cage_w) / 2)
    cage_y = max(60, screen_height * 0.18)

    return pygame.Rect(cage_x, cage_y, cage_w, cage_h)

def get_left_item_area_rect(screen_width, screen_height):
    try:
        cage_rect = get_cage_rect(screen_width, screen_height)
        area_width = max(1, (screen_width - cage_rect.width) / 2 - 30)
        area_x = 15
        area_y = cage_rect.top
        area_height = max(1, cage_rect.height)

        area_width = min(area_width, cage_rect.left - area_x - 15)
        area_width = max(1, area_width)

        return pygame.Rect(area_x, area_y, area_width, area_height)
    except Exception as e:
        print(f"Error in get_left_item_area_rect: {e}")
        traceback.print_exc()
        return pygame.Rect(10, 100, 50, 100)

def get_right_item_area_rect(screen_width, screen_height):
    try:
        cage_rect = get_cage_rect(screen_width, screen_height)
        area_width = max(1, (screen_width - cage_rect.width) / 2 - 30)
        area_x = cage_rect.right + 15
        area_y = cage_rect.top
        area_height = max(1, cage_rect.height)

        area_width = min(area_width, screen_width - area_x - 15)
        area_width = max(1, area_width)

        return pygame.Rect(area_x, area_y, area_width, area_height)
    except Exception as e:
        print(f"Error in get_right_item_area_rect: {e}")
        traceback.print_exc()
        return pygame.Rect(screen_width - 60, 100, 50, 100)

def get_item_type(item_text):
    if not isinstance(item_text, str): item_text = str(item_text)
    if item_text in SHAPE_NAMES:
        return "shape"
    elif item_text.isdigit():
        return "number"
    elif len(item_text) == 1 and 'A' <= item_text <= 'Z':
        return "uppercase"
    elif len(item_text) == 1 and 'a' <= item_text <= 'z':
        return "lowercase"
    else:
        return "word"

def draw_shape(surface, shape_name, rect, fill=True):
    outline_color = YELLOW
    fill_color = LIGHT_YELLOW
    center = rect.center
    size = min(rect.width, rect.height) * 0.65
    half_size = size / 2

    if size < 2:
        return

    try:
        center_int = (int(center[0]), int(center[1]))
        if shape_name == "Square":
            shape_rect = pygame.Rect(center_int[0] - half_size, center_int[1] - half_size, size, size)
            if fill: pygame.draw.rect(surface, fill_color, shape_rect)
            pygame.draw.rect(surface, outline_color, shape_rect, 2)
        elif shape_name == "Rectangle":
            rect_width = size
            rect_height = size * 0.6
            shape_rect = pygame.Rect(center_int[0] - rect_width / 2, center_int[1] - rect_height / 2, rect_width, rect_height)
            if fill: pygame.draw.rect(surface, fill_color, shape_rect)
            pygame.draw.rect(surface, outline_color, shape_rect, 2)
        elif shape_name == "Circle":
            radius = max(1, int(half_size))
            if fill: pygame.draw.circle(surface, fill_color, center_int, radius)
            pygame.draw.circle(surface, outline_color, center_int, radius, 2)
        elif shape_name == "Triangle":
            points = [
                (center_int[0], center_int[1] - half_size),
                (center_int[0] - half_size, center_int[1] + half_size),
                (center_int[0] + half_size, center_int[1] + half_size)]
            points_int = [(int(p[0]), int(p[1])) for p in points]
            if fill: pygame.draw.polygon(surface, fill_color, points_int)
            pygame.draw.polygon(surface, outline_color, points_int, 2)
        elif shape_name == "Pentagon":
            points = []
            for i in range(5):
                angle = math.pi / 2 - 2 * math.pi * i / 5
                x = center_int[0] + half_size * math.cos(angle)
                y = center_int[1] - half_size * math.sin(angle)
                points.append((int(x),int(y)))
            if fill: pygame.draw.polygon(surface, fill_color, points)
            pygame.draw.polygon(surface, outline_color, points, 2)
        else:
            draw_text(surface, shape_name, center_int, FONT_SMALL, WHITE, center=True)
    except Exception as e:
        print(f"Error drawing shape '{shape_name}' in rect {rect}: {e}")
        traceback.print_exc()
        pygame.draw.rect(surface, RED, rect, 1)

def trigger_flash(game_state, color, duration_frames=15):
    game_state.flash_color = color
    game_state.flash_timer = max(1, duration_frames)

def draw_flash(surface, game_state):
    if game_state.flash_timer > 0 and game_state.flash_color:
        try:
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            max_alpha = 100
            alpha_duration = 15
            alpha = int(max_alpha * max(0, min(1, game_state.flash_timer / alpha_duration)))
            alpha = max(0, min(255, alpha))

            flash_surface.fill((*game_state.flash_color, alpha))
            surface.blit(flash_surface, (0, 0))
            game_state.flash_timer -= 1
            if game_state.flash_timer <= 0:
                game_state.flash_color = None
        except Exception as e:
             print(f"Error drawing flash: {e}")
             traceback.print_exc()
             game_state.flash_timer = 0
             game_state.flash_color = None

# ----- MOTIVATION AND PSYCHOLOGY-BASED FUNCTIONS -----

def create_reward_burst(position, color=None, count=20, success=True):
    particles = []
    
    if color is None:
        color = (255, 215, 0) if success else (255, 100, 100)
        
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)
        size = random.uniform(2, 7)
        lifetime = random.randint(20, 60)
        
        particles.append({
            'pos': list(position),
            'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
            'size': size,
            'color': color,
            'lifetime': lifetime,
            'max_lifetime': lifetime,
        })
        
    return particles
    
def update_particles(particles):
    remaining = []
    
    for p in particles:
        p['lifetime'] -= 1
        if p['lifetime'] <= 0:
            continue
            
        p['pos'][0] += p['vel'][0]
        p['pos'][1] += p['vel'][1]
        p['vel'][1] += 0.05
        
        age_ratio = p['lifetime'] / p['max_lifetime']
        p['size'] = p['size'] * 0.95 + p['size'] * 0.05 * age_ratio
        
        remaining.append(p)
        
    return remaining
    
def draw_particles(surface, particles):
    for p in particles:
        age_ratio = p['lifetime'] / p['max_lifetime']
        
        r, g, b = p['color']
        pulse = 0.7 + 0.3 * math.sin(age_ratio * math.pi * 3)
        
        color = (
            min(255, int(r * pulse)),
            min(255, int(g * pulse)),
            min(255, int(b * pulse))
        )
        
        size = int(p['size'])
        if size < 1:
            size = 1
            
        pygame.draw.circle(
            surface,
            color,
            (int(p['pos'][0]), int(p['pos'][1])),
            size
        )

def get_motivational_message(correct_count=0, score_streak=0, level=1):
    general_messages = [
        "Good job!",
        "Way to go!",
        "Amazing!",
        "You're doing great!",
        "Wonderful!",
        "Super!",
        "Fantastic!",
        "You're a star!"
    ]
    
    streak_messages = [
        "Keep going!",
        "You're on a roll!",
        "Don't stop now!",
        "Wow, look at you go!",
        "You're unstoppable!"
    ]
    
    milestone_messages = [
        "You're learning so fast!",
        "You're getting so smart!",
        "Your brain is growing!",
        "You're becoming a master!",
        "You're a learning superstar!"
    ]
    
    if score_streak >= 3:
        return random.choice(streak_messages)
    elif correct_count > 0 and correct_count % 5 == 0:
        return random.choice(milestone_messages)
    else:
        return random.choice(general_messages)

def draw_animated_text(surface, text, pos, font, color, frame_counter, center=True):
    x, y = pos
    
    # Defensive check for None font
    if font is None:
        print(f"Warning: Font is None for animated text '{text}'. Using default font.")
        font = pygame.font.Font(None, 36)
    
    y_offset = math.sin(frame_counter * 0.1) * 5
    
    scale = 1.0 + math.sin(frame_counter * 0.15) * 0.05
    
    hue_shift = math.sin(frame_counter * 0.2) * 15
    r = min(255, max(0, color[0] + hue_shift))
    g = min(255, max(0, color[1] + hue_shift))
    b = min(255, max(0, color[2] + hue_shift))
    dynamic_color = (r, g, b)
    
    text_surface = font.render(str(text), True, dynamic_color)
    
    if scale != 1.0:
        new_width = int(text_surface.get_width() * scale)
        new_height = int(text_surface.get_height() * scale)
        text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
    
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y + y_offset)
    else:
        text_rect.topleft = (x, y + y_offset)
    
    shadow_surface = font.render(str(text), True, (0, 0, 0))
    shadow_rect = shadow_surface.get_rect()
    if center:
        shadow_rect.center = (x + 2, y + y_offset + 2)
    else:
        shadow_rect.topleft = (x + 2, y + y_offset + 2)
    
    surface.blit(shadow_surface, shadow_rect)
    surface.blit(text_surface, text_rect)
    
    return text_rect

def get_achievement_emoji(achievement_type):
    emoji_map = {
        "correct_answer": "✓",
        "level_complete": "🏆",
        "streak": "🔥",
        "speed": "⚡",
        "life_gained": "❤️",
        "perfect_score": "⭐",
        "first_try": "🎯",
        "comeback": "🚀"
    }
    return emoji_map.get(achievement_type, "✓")

def create_progress_indicator(current, total, width=200, height=20, color_full=GREEN, color_empty=GREY):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    pygame.draw.rect(surface, color_empty, (0, 0, width, height), border_radius=height//2)
    
    if total > 0:
        fill_width = int(width * (current / total))
        if fill_width > 0:
            pygame.draw.rect(surface, color_full, (0, 0, fill_width, height), border_radius=height//2)
    
    highlight_height = height // 4
    pygame.draw.rect(surface, (255, 255, 255, 100), (0, 0, width, highlight_height), 
                     border_top_left_radius=height//2, border_top_right_radius=height//2)
    
    return surface

def play_sound_effect(sound_type):
    sound_types = {
        "correct": "Positive reinforcement sound",
        "wrong": "Gentle wrong answer sound",
        "level_up": "Celebratory sound",
        "crash": "Gentle collision sound", 
        "countdown": "Timer warning sound"
    }
    print(f"Sound effect: {sound_types.get(sound_type, 'unknown')}")

def display_instructor_feedback(surface, feedback_type, position=(100, 100)):
    expressions = {
        "hint": "Hint: Try looking at the shape!",
        "encouragement": "You can do it!",
        "celebration": "Great job, I knew you could do it!",
        "correction": "That's not quite right, but you're learning!"
    }
    
    message = expressions.get(feedback_type, "Keep trying!")
    
    bubble_rect = pygame.Rect(position[0], position[1], 200, 50)
    pygame.draw.rect(surface, WHITE, bubble_rect, border_radius=15)
    pygame.draw.rect(surface, BLACK, bubble_rect, width=2, border_radius=15)
    
    points = [(position[0] + 20, position[1] + 50), 
              (position[0] - 10, position[1] + 70), 
              (position[0] + 40, position[1] + 50)]
    pygame.draw.polygon(surface, WHITE, points)
    pygame.draw.polygon(surface, BLACK, points, width=2)
    
    try:
        font = pygame.font.SysFont("Arial", 16)
        text_surf = font.render(message, True, BLACK)
        text_rect = text_surf.get_rect(center=(bubble_rect.centerx, bubble_rect.centery))
        surface.blit(text_surf, text_rect)
    except Exception as e:
        print(f"Error rendering instructor feedback: {e}")

def create_completion_star(progress_ratio):
    size = 50
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi * 2 / 10
        radius = size / 2 if i % 2 == 0 else size / 4
        x = size / 2 + radius * math.cos(angle)
        y = size / 2 + radius * math.sin(angle)
        points.append((x, y))
    
    pygame.draw.polygon(surface, BLACK, points, width=2)
    
    clip_height = int(size * (1 - progress_ratio))
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    mask.fill((255, 255, 255, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, clip_height, size, size - clip_height))
    
    fill_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(fill_surface, YELLOW, points)
    
    fill_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(fill_surface, (0, 0))
    
    return surface

def apply_growth_mindset_message(game_state, success=True):
    if success:
        messages = [
            "Your brain is growing!",
            "You learned something new!",
            "Your practice is paying off!",
            "Your effort made you succeed!",
            "You didn't give up and won!"
        ]
    else:
        messages = [
            "Mistakes help us learn!",
            "You'll get better with practice!",
            "Let's try a different way!",
            "You're not there YET, but you will be!",
            "Every try makes your brain stronger!"
        ]
    
    if not hasattr(game_state, 'floating_messages'):
        game_state.floating_messages = []
    
    game_state.floating_messages.append({
        "text": random.choice(messages),
        "pos": (game_state.screen_width // 2, game_state.screen_height // 2 - 100),
        "color": GREEN if success else BLUE,
        "size": 24,
        "lifetime": 120,
        "velocity": (0, -0.5),
        "frame": 0
    })

def show_variable_reward(game_state, position, value, reward_type="standard"):
    variance = random.uniform(-0.2, 0.2)
    adjusted_value = int(value * (1 + variance))
    
    bonus_chance = 0.2
    if random.random() < bonus_chance:
        adjusted_value = int(adjusted_value * 2)
        message = f"BONUS x2! +{adjusted_value}"
        color = (255, 215, 0)
    else:
        message = f"+{adjusted_value}"
        color = (50, 200, 50)
    
    if not hasattr(game_state, 'floating_messages'):
        game_state.floating_messages = []
        
    game_state.floating_messages.append({
        "text": message,
        "pos": position,
        "color": color,
        "size": 30,
        "lifetime": 60,
        "velocity": (random.uniform(-0.3, 0.3), -2),
        "frame": 0
    })
    
    return adjusted_value

def update_difficulty(game_state):
    recent_correct_ratio = 0.0
    if game_state.total_correct_answers + game_state.total_wrong_answers > 0:
        recent_correct_ratio = game_state.total_correct_answers / (game_state.total_correct_answers + game_state.total_wrong_answers)
    
    avg_response_time = 0
    if game_state.response_times:
        avg_response_time = sum(game_state.response_times) / len(game_state.response_times)
    
    target_success_ratio = 0.7
    
    if recent_correct_ratio > 0.85:
        game_state.request_time_limit = max(5, game_state.request_time_limit * 0.9)
        
    elif recent_correct_ratio < 0.5:
        game_state.request_time_limit = min(30, game_state.request_time_limit * 1.1)
    
    game_state.skill_level = max(0, min(1, recent_correct_ratio))
    
    return game_state

def avoid_learned_helplessness(game_state, consecutive_failures):
    if consecutive_failures >= 3:
        game_state.request_time_limit += 5
        game_state.show_hint = True
        apply_growth_mindset_message(game_state, False)
    
    if consecutive_failures >= 5:
        game_state.guaranteed_success = True
        return 0
        
    return consecutive_failures

# ----- RESPONSIVE SCALING FUNCTIONS -----

def get_scale_factors(screen_width, screen_height, base_width=800, base_height=600):
    """Calculate scaling factors based on current screen dimensions versus base design dimensions.
    This helps all UI elements and gameplay mechanics scale properly across different resolutions."""
    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    # Use the smaller scale factor to ensure everything fits on screen
    uniform_scale = min(scale_x, scale_y)
    return {
        'x': scale_x,
        'y': scale_y,
        'uniform': uniform_scale,
        'font': max(0.5, min(2.0, uniform_scale)),  # Limit font scaling between 0.5x and 2x
    }

def scale_position(pos, scale_factors):
    """Scale a position based on current screen dimensions."""
    return (pos[0] * scale_factors['x'], pos[1] * scale_factors['y'])

def scale_rect(rect, scale_factors):
    """Scale a rectangle based on current screen dimensions."""
    x = rect.x * scale_factors['x']
    y = rect.y * scale_factors['y']
    width = rect.width * scale_factors['x']
    height = rect.height * scale_factors['y']
    return pygame.Rect(x, y, width, height)

def scale_size(size, scale_factor):
    """Scale a size value uniformly."""
    return max(1, int(size * scale_factor))

def get_scaled_font(base_font, scale_factor):
    """Get a font scaled appropriately for the current screen size."""
    base_size = base_font.get_height()
    new_size = max(10, int(base_size * scale_factor))
    
    try:
        # Try to create a font with the same name but scaled size
        font_name = base_font.get_name()
        if font_name:
            return pygame.font.SysFont(font_name, new_size, 
                                      bold=pygame.font.Font.get_bold(base_font),
                                      italic=pygame.font.Font.get_italic(base_font))
        else:
            # If we can't get the name, fall back to default font
            return pygame.font.Font(None, new_size)
    except:
        # Fallback if anything goes wrong
        return pygame.font.Font(None, new_size)