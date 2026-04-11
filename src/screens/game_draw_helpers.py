import colorsys
import math
import pygame

from constants import BLUE, BRIGHT_CYAN, BRIGHT_GREEN, DARK_GREY, GREEN, ORANGE, PURPLE, WHITE, BLACK
from core.lazy_loader import get_cached_resource
from ui.enhanced_graphics import draw_glow_circle
from utils import draw_text, get_cached_font, get_cached_text_surface


def get_food_sprite(value, color, size, glow_radius=8):
    label = str(value)
    font = get_cached_font("Consolas", 24) or pygame.font.Font(None, 24)
    cache_key = f"food-sprite:{label}:{color}:{size}:{glow_radius}"

    def _create():
        diameter = size * 2 + glow_radius * 2
        sprite = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (diameter // 2, diameter // 2)
        draw_glow_circle(sprite, center, size, color, glow_radius=glow_radius)
        text_surface = get_cached_text_surface(font, label, BLACK)
        if text_surface is None:
            text_surface = font.render(label, True, BLACK)
        sprite.blit(text_surface, text_surface.get_rect(center=center))
        return sprite

    return get_cached_resource(cache_key, _create)


def draw_food_sprite_item(surface, food):
    food_x, food_y = food["pos"]
    wiggle_amount = food.get("wiggle_amount", 3)
    animated_x = int(food_x + math.sin(food["wiggle_offset"]) * wiggle_amount)
    animated_y = int(food_y + math.cos(food["wiggle_offset"]) * wiggle_amount * 0.5)
    pulse_factor = 1.0 + food.get("pulse", 0) * 0.02
    animated_size = max(1, int(food.get("size", 15) * pulse_factor))
    sprite = get_food_sprite(food["value"], food["color"], animated_size)
    if sprite is None:
        return
    surface.blit(sprite, sprite.get_rect(center=(animated_x, animated_y)))


def _get_surprise_style(game, frame):
    if game.surprise_type == "rainbow_mode":
        hue = (frame % 360) / 360.0
        red, green, blue = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        return (int(red * 255), int(green * 255), int(blue * 255)), "✨"
    if game.surprise_type == "food_party":
        return BRIGHT_GREEN, "🍎"
    if game.surprise_type == "speed_boost":
        return BRIGHT_CYAN, "⚡"
    if game.surprise_type == "giant_snake":
        return PURPLE, "🐍"
    return WHITE, "?"


def draw_game_ui(game):
    screen = game.screen
    frame = getattr(game, "animation_frame", 0)
    score_font = get_cached_font("Consolas", 36) or pygame.font.Font(None, 36)
    hud_font = get_cached_font("Consolas", 36) or pygame.font.Font(None, 36)

    draw_text(screen, f"Score: {game.game_state.score}", (20, 20), score_font, WHITE)
    draw_text(screen, f"Level {game.game_state.current_level}", (game.screen_width // 2, 20), hud_font, WHITE, center=True)

    target_items = max(1, game.game_state.current_level * 3)
    progress_width, progress_height = 200, 20
    progress_x = (game.screen_width - progress_width) // 2
    progress_y = 50
    pygame.draw.rect(screen, DARK_GREY, (progress_x, progress_y, progress_width, progress_height), border_radius=10)

    progress_ratio = min(1.0, game.game_state.score_in_row / target_items)
    fill_width = int(progress_width * progress_ratio)
    if fill_width > 0:
        color = BLUE if progress_ratio < 0.5 else GREEN
        if progress_ratio >= 0.8:
            hue = (frame % 360) / 360.0
            red, green, blue = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            color = (int(red * 255), int(green * 255), int(blue * 255))
        pygame.draw.rect(screen, color, (progress_x, progress_y, fill_width, progress_height), border_radius=10)

    shimmer = progress_x + int(math.sin(frame * 0.05) * progress_width * 0.5 + progress_width * 0.5)
    if progress_x <= shimmer <= progress_x + fill_width:
        pygame.draw.rect(screen, (255, 255, 255, 150), (shimmer - 5, progress_y + 2, 10, progress_height - 4), border_radius=5)

    if game.game_state.score_in_row >= 2:
        streak_text = f"Streak: {game.game_state.score_in_row} 🔥"
        streak_scale = 1.0 + 0.1 * math.sin(frame * 0.2)
        streak_font = get_cached_font("Arial", int(28 * streak_scale), bold=True) or pygame.font.Font(None, int(28 * streak_scale))
        streak_surface = get_cached_text_surface(streak_font, streak_text, ORANGE)
        if streak_surface is None:
            streak_surface = streak_font.render(streak_text, True, ORANGE)
        screen.blit(streak_surface, streak_surface.get_rect(center=(game.screen_width // 2, 85)))

    if not game.surprise_active:
        return

    color, icon = _get_surprise_style(game, frame)
    timer_font = get_cached_font("Consolas", 36) or pygame.font.Font(None, 36)
    timer_text = f"{icon} {int(game.surprise_duration)}s"
    timer_surface = get_cached_text_surface(timer_font, timer_text, color)
    if timer_surface is None:
        timer_surface = timer_font.render(timer_text, True, color)
    screen.blit(timer_surface, timer_surface.get_rect(topright=(game.screen_width - 20, 20)))

    border_width = 6
    pulse = 0.7 + 0.3 * math.sin(frame * 0.1)
    border_color = tuple(min(255, int(component * pulse)) for component in color)
    pygame.draw.rect(screen, border_color, (0, 0, game.screen_width, border_width))
    pygame.draw.rect(screen, border_color, (0, game.screen_height - border_width, game.screen_width, border_width))
    pygame.draw.rect(screen, border_color, (0, 0, border_width, game.screen_height))
    pygame.draw.rect(screen, border_color, (game.screen_width - border_width, 0, border_width, game.screen_height))
