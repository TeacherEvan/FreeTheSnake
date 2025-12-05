# optimized_renderer.py
# Provides optimized rendering utilities with caching and batching
# for improved visual performance in pygame applications

import pygame
import math
from typing import Dict, List, Optional, Tuple, Any
from functools import lru_cache
import threading


class SurfaceCache:
    """
    Intelligent surface caching system for pygame.
    
    Caches rendered surfaces to avoid redundant rendering operations,
    significantly improving performance for frequently drawn elements.
    """
    
    def __init__(self, max_cache_size: int = 256):
        """
        Initialize the surface cache.
        
        Args:
            max_cache_size: Maximum number of surfaces to cache
        """
        self._cache: Dict[str, pygame.Surface] = {}
        self._access_count: Dict[str, int] = {}
        self._max_size = max_cache_size
        self._lock = threading.Lock()
    
    def get_cached_surface(self, cache_key: str) -> Optional[pygame.Surface]:
        """
        Retrieve a cached surface by key.
        
        Args:
            cache_key: Unique identifier for the cached surface
            
        Returns:
            The cached surface or None if not found
        """
        with self._lock:
            if cache_key in self._cache:
                self._access_count[cache_key] = self._access_count.get(cache_key, 0) + 1
                return self._cache[cache_key]
        return None
    
    def cache_surface(self, cache_key: str, surface: pygame.Surface) -> None:
        """
        Store a surface in the cache.
        
        Args:
            cache_key: Unique identifier for the surface
            surface: The pygame surface to cache
        """
        with self._lock:
            # Evict least accessed surfaces if at capacity
            if len(self._cache) >= self._max_size:
                self._evict_least_used()
            
            self._cache[cache_key] = surface
            self._access_count[cache_key] = 1
    
    def _evict_least_used(self) -> None:
        """Remove the least frequently accessed surfaces."""
        if not self._access_count:
            return
        
        # Find the least accessed key
        min_key = min(self._access_count, key=self._access_count.get)
        self._cache.pop(min_key, None)
        self._access_count.pop(min_key, None)
    
    def clear(self) -> None:
        """Clear all cached surfaces."""
        with self._lock:
            self._cache.clear()
            self._access_count.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics for debugging.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            'cached_surfaces': len(self._cache),
            'max_size': self._max_size,
            'total_accesses': sum(self._access_count.values()),
        }


# Global surface cache instance
_surface_cache = SurfaceCache()


def get_cached_gradient_surface(
    width: int, 
    height: int, 
    start_color: Tuple[int, int, int],
    end_color: Tuple[int, int, int],
    direction: str = 'vertical'
) -> pygame.Surface:
    """
    Get or create a cached gradient surface.
    
    Args:
        width: Surface width in pixels
        height: Surface height in pixels
        start_color: RGB tuple for gradient start
        end_color: RGB tuple for gradient end
        direction: 'vertical', 'horizontal', or 'radial'
        
    Returns:
        A pygame surface with the gradient applied
    """
    cache_key = f"gradient_{width}_{height}_{start_color}_{end_color}_{direction}"
    
    cached = _surface_cache.get_cached_surface(cache_key)
    if cached is not None:
        return cached
    
    # Create new gradient surface
    surface = pygame.Surface((width, height))
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / max(1, height - 1)
            color = _interpolate_color(start_color, end_color, ratio)
            pygame.draw.line(surface, color, (0, y), (width, y))
    
    elif direction == 'horizontal':
        for x in range(width):
            ratio = x / max(1, width - 1)
            color = _interpolate_color(start_color, end_color, ratio)
            pygame.draw.line(surface, color, (x, 0), (x, height))
    
    elif direction == 'radial':
        # Optimized radial gradient using concentric circle drawing
        # This is much faster than pixel-by-pixel set_at() calls
        center_x, center_y = width // 2, height // 2
        max_distance = math.sqrt(center_x ** 2 + center_y ** 2)
        
        # Fill with end color first
        surface.fill(end_color)
        
        # Draw concentric circles from outside to inside
        # Use fewer steps for better performance (visual quality is still good)
        num_steps = min(100, int(max_distance))
        for i in range(num_steps, 0, -1):
            ratio = i / num_steps
            radius = int(max_distance * ratio)
            if radius > 0:
                color = _interpolate_color(start_color, end_color, ratio)
                pygame.draw.circle(surface, color, (center_x, center_y), radius)
    
    _surface_cache.cache_surface(cache_key, surface)
    return surface


def _interpolate_color(
    color1: Tuple[int, int, int], 
    color2: Tuple[int, int, int], 
    ratio: float
) -> Tuple[int, int, int]:
    """
    Interpolate between two colors.
    
    Args:
        color1: Start RGB color
        color2: End RGB color
        ratio: Interpolation ratio (0.0 to 1.0)
        
    Returns:
        Interpolated RGB color tuple
    """
    ratio = max(0.0, min(1.0, ratio))
    return (
        int(color1[0] + (color2[0] - color1[0]) * ratio),
        int(color1[1] + (color2[1] - color1[1]) * ratio),
        int(color1[2] + (color2[2] - color1[2]) * ratio),
    )


@lru_cache(maxsize=128)
def compute_glow_alpha_values(radius: int, base_alpha: int) -> Tuple[int, ...]:
    """
    Pre-compute alpha values for glow effects.
    
    Args:
        radius: Glow radius in pixels
        base_alpha: Base alpha value (0-255)
        
    Returns:
        Tuple of alpha values for each glow layer
    """
    return tuple(
        int(base_alpha * (1 - i / radius) * 0.3)
        for i in range(radius)
    )


def draw_optimized_glow_circle(
    surface: pygame.Surface,
    center: Tuple[int, int],
    radius: int,
    color: Tuple[int, int, int],
    glow_radius: int = 10,
    base_alpha: int = 128
) -> None:
    """
    Draw a circle with an optimized glow effect using cached computations.
    
    Args:
        surface: Target pygame surface
        center: Center point (x, y)
        radius: Circle radius
        color: RGB color tuple
        glow_radius: Size of the glow effect
        base_alpha: Base alpha for the glow
    """
    # Use cached alpha values
    alpha_values = compute_glow_alpha_values(glow_radius, base_alpha)
    
    # Draw glow layers from outer to inner
    for i, alpha in enumerate(reversed(alpha_values)):
        if alpha > 5:
            glow_size = radius + glow_radius - i
            try:
                glow_surface = pygame.Surface(
                    (glow_size * 2, glow_size * 2), 
                    pygame.SRCALPHA
                )
                pygame.draw.circle(
                    glow_surface, 
                    (*color, alpha),
                    (glow_size, glow_size), 
                    glow_size
                )
                surface.blit(
                    glow_surface, 
                    (center[0] - glow_size, center[1] - glow_size)
                )
            except pygame.error:
                continue
    
    # Draw the main circle
    pygame.draw.circle(surface, color, center, radius)


class BatchRenderer:
    """
    Batched rendering system for drawing multiple similar elements efficiently.
    
    Collects draw calls and executes them in optimized batches to reduce
    state changes and improve rendering performance.
    """
    
    def __init__(self, surface: pygame.Surface):
        """
        Initialize the batch renderer.
        
        Args:
            surface: Target pygame surface for rendering
        """
        self._surface = surface
        self._circle_batch: List[Tuple[Tuple[int, int, int], Tuple[int, int], int]] = []
        self._rect_batch: List[Tuple[Tuple[int, int, int], pygame.Rect]] = []
        self._line_batch: List[Tuple[Tuple[int, int, int], Tuple[int, int], Tuple[int, int], int]] = []
    
    def add_circle(
        self, 
        color: Tuple[int, int, int], 
        center: Tuple[int, int], 
        radius: int
    ) -> None:
        """Add a circle to the batch queue."""
        self._circle_batch.append((color, center, radius))
    
    def add_rect(
        self, 
        color: Tuple[int, int, int], 
        rect: pygame.Rect
    ) -> None:
        """Add a rectangle to the batch queue."""
        self._rect_batch.append((color, rect))
    
    def add_line(
        self, 
        color: Tuple[int, int, int], 
        start: Tuple[int, int], 
        end: Tuple[int, int], 
        width: int = 1
    ) -> None:
        """Add a line to the batch queue."""
        self._line_batch.append((color, start, end, width))
    
    def flush(self) -> None:
        """
        Execute all batched draw calls.
        
        This should be called once per frame after all elements
        have been added to their respective batches.
        """
        # Draw all circles
        for color, center, radius in self._circle_batch:
            pygame.draw.circle(self._surface, color, center, radius)
        
        # Draw all rectangles
        for color, rect in self._rect_batch:
            pygame.draw.rect(self._surface, color, rect)
        
        # Draw all lines
        for color, start, end, width in self._line_batch:
            pygame.draw.line(self._surface, color, start, end, width)
        
        # Clear batches
        self._circle_batch.clear()
        self._rect_batch.clear()
        self._line_batch.clear()
    
    def clear_batches(self) -> None:
        """Clear all pending draw calls without executing them."""
        self._circle_batch.clear()
        self._rect_batch.clear()
        self._line_batch.clear()


class AnimatedSpriteRenderer:
    """
    Optimized renderer for animated sprites with frame caching.
    
    Caches animation frames and provides smooth interpolation
    between keyframes for fluid animations.
    """
    
    def __init__(self):
        """Initialize the animated sprite renderer."""
        self._frame_cache: Dict[str, List[pygame.Surface]] = {}
        self._current_frames: Dict[str, int] = {}
        self._animation_speeds: Dict[str, float] = {}
    
    def register_animation(
        self, 
        animation_id: str, 
        frames: List[pygame.Surface],
        speed: float = 1.0
    ) -> None:
        """
        Register an animation sequence.
        
        Args:
            animation_id: Unique identifier for the animation
            frames: List of pygame surfaces for each frame
            speed: Animation playback speed multiplier
        """
        self._frame_cache[animation_id] = frames
        self._current_frames[animation_id] = 0
        self._animation_speeds[animation_id] = speed
    
    def get_current_frame(
        self, 
        animation_id: str, 
        delta_time: float
    ) -> Optional[pygame.Surface]:
        """
        Get the current frame of an animation, advancing based on delta time.
        
        Args:
            animation_id: Animation identifier
            delta_time: Time since last frame in seconds
            
        Returns:
            Current animation frame surface or None if animation not found
        """
        if animation_id not in self._frame_cache:
            return None
        
        frames = self._frame_cache[animation_id]
        if not frames:
            return None
        
        # Update frame index
        speed = self._animation_speeds.get(animation_id, 1.0)
        self._current_frames[animation_id] += speed * delta_time * 60  # Assume 60 FPS base
        
        # Loop animation
        frame_index = int(self._current_frames[animation_id]) % len(frames)
        return frames[frame_index]
    
    def reset_animation(self, animation_id: str) -> None:
        """Reset an animation to its first frame."""
        if animation_id in self._current_frames:
            self._current_frames[animation_id] = 0


def clear_all_caches() -> None:
    """Clear all rendering caches. Call when screen size changes."""
    _surface_cache.clear()
    compute_glow_alpha_values.cache_clear()
