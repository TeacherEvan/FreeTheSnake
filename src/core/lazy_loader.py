# lazy_loader.py
# Implements lazy loading pattern for game screens and heavy components
# This improves initial load time and reduces memory footprint

import importlib
import threading
from typing import Any, Callable, Dict, Optional, Type
from functools import lru_cache


class LazyLoader:
    """
    Lazy loading utility for deferring module and class instantiation.
    
    This class implements the Proxy pattern to delay expensive imports
    and object creation until they are actually needed, improving
    application startup time and reducing memory usage.
    
    Usage:
        screen_loader = LazyLoader('screens.game_screen', 'GameScreen')
        game_screen = screen_loader.get_instance(screen, game_state)
    """
    
    def __init__(self, module_path: str, class_name: str):
        """
        Initialize the lazy loader with module and class information.
        
        Args:
            module_path: Dot-separated path to the module (e.g., 'screens.game_screen')
            class_name: Name of the class to instantiate from the module
        """
        self._module_path = module_path
        self._class_name = class_name
        self._instance: Optional[Any] = None
        self._class: Optional[Type] = None
        self._lock = threading.Lock()
        
    def _load_class(self) -> Type:
        """Load the class from the module. Thread-safe."""
        if self._class is None:
            with self._lock:
                if self._class is None:
                    module = importlib.import_module(self._module_path)
                    self._class = getattr(module, self._class_name)
        return self._class
    
    def get_instance(self, *args, **kwargs) -> Any:
        """
        Get or create an instance of the lazy-loaded class.
        
        Args:
            *args: Positional arguments to pass to the class constructor
            **kwargs: Keyword arguments to pass to the class constructor
            
        Returns:
            An instance of the lazy-loaded class
        """
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    cls = self._load_class()
                    self._instance = cls(*args, **kwargs)
        return self._instance
    
    def create_new_instance(self, *args, **kwargs) -> Any:
        """
        Create a new instance without caching.
        
        Args:
            *args: Positional arguments to pass to the class constructor
            **kwargs: Keyword arguments to pass to the class constructor
            
        Returns:
            A new instance of the lazy-loaded class
        """
        cls = self._load_class()
        return cls(*args, **kwargs)
    
    def reset_instance(self) -> None:
        """Reset the cached instance, forcing a new load on next access."""
        with self._lock:
            self._instance = None


class ScreenManager:
    """
    Centralized manager for lazy-loading game screens.
    
    This manager implements a screen registry pattern with lazy loading
    to optimize memory usage and startup time for the game.
    
    Attributes:
        SCREEN_REGISTRY: Dictionary mapping screen names to their module paths
    """
    
    # TODO: [OPTIMIZATION] Consider implementing screen preloading
    # based on predicted user navigation patterns
    SCREEN_REGISTRY: Dict[str, tuple] = {
        'welcome': ('screens.welcome_screen', 'WelcomeScreen'),
        'level_select': ('screens.level_select_screen', 'LevelSelectScreen'),
        'game': ('screens.game_screen', 'GameScreen'),
        'win_animation': ('screens.win_animation_screen', 'WinAnimationScreen'),
        'win_congrats': ('screens.win_congrats_screen', 'WinCongratsScreen'),
        'game_over': ('screens.game_over_screen', 'GameOverScreen'),
        'menu_select': ('screens.menu_select_screen', 'MenuSelectScreen'),
    }
    
    def __init__(self):
        """Initialize the screen manager with lazy loaders for each screen."""
        self._screen_loaders: Dict[str, LazyLoader] = {}
        self._screen_instances: Dict[str, Any] = {}
        self._preload_callbacks: Dict[str, Callable] = {}
        
        # Initialize lazy loaders for all registered screens
        for screen_name, (module_path, class_name) in self.SCREEN_REGISTRY.items():
            self._screen_loaders[screen_name] = LazyLoader(module_path, class_name)
    
    def get_screen(self, screen_name: str, screen_surface, game_state) -> Any:
        """
        Get a screen instance, creating it lazily if needed.
        
        Args:
            screen_name: Name of the screen (e.g., 'welcome', 'game')
            screen_surface: Pygame surface to render on
            game_state: Game state object to pass to the screen
            
        Returns:
            The screen instance
            
        Raises:
            KeyError: If the screen name is not registered
        """
        if screen_name not in self._screen_loaders:
            raise KeyError(f"Screen '{screen_name}' not registered in ScreenManager")
        
        if screen_name not in self._screen_instances:
            loader = self._screen_loaders[screen_name]
            self._screen_instances[screen_name] = loader.get_instance(
                screen_surface, game_state
            )
        
        return self._screen_instances[screen_name]
    
    def preload_screen(self, screen_name: str, screen_surface, game_state) -> None:
        """
        Preload a screen in the background for faster access later.
        
        Args:
            screen_name: Name of the screen to preload
            screen_surface: Pygame surface to render on
            game_state: Game state object to pass to the screen
        """
        def preload_worker():
            self.get_screen(screen_name, screen_surface, game_state)
        
        thread = threading.Thread(target=preload_worker, daemon=True)
        thread.start()
    
    def reload_screen(self, screen_name: str, screen_surface, game_state) -> Any:
        """
        Force reload a screen, creating a fresh instance.
        
        Args:
            screen_name: Name of the screen to reload
            screen_surface: Pygame surface to render on
            game_state: Game state object to pass to the screen
            
        Returns:
            The new screen instance
        """
        if screen_name in self._screen_instances:
            del self._screen_instances[screen_name]
        
        return self.get_screen(screen_name, screen_surface, game_state)
    
    def update_all_dimensions(self, width: int, height: int) -> None:
        """
        Update dimensions for all loaded screens.
        
        Args:
            width: New screen width
            height: New screen height
        """
        for screen in self._screen_instances.values():
            if hasattr(screen, 'update_dimensions'):
                screen.update_dimensions(width, height)
    
    def clear_cache(self) -> None:
        """Clear all cached screen instances."""
        self._screen_instances.clear()


class ResourceCache:
    """
    Thread-safe cache for game resources with LRU eviction.
    
    This cache stores frequently accessed resources like fonts,
    surfaces, and computed values to avoid redundant calculations.
    """
    
    def __init__(self, max_size: int = 128):
        """
        Initialize the resource cache.
        
        Args:
            max_size: Maximum number of items to store in cache
        """
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._lock = threading.Lock()
        self._access_order: list = []
    
    def get(self, key: str, factory: Optional[Callable] = None) -> Optional[Any]:
        """
        Get a value from cache, optionally creating it if missing.
        
        Args:
            key: Cache key
            factory: Optional callable to create the value if not cached
            
        Returns:
            The cached value or None if not found and no factory provided
        """
        with self._lock:
            if key in self._cache:
                # Update access order for LRU
                if key in self._access_order:
                    self._access_order.remove(key)
                self._access_order.append(key)
                return self._cache[key]
            
            if factory is not None:
                value = factory()
                # Set value without acquiring lock again (we already hold it)
                self._set_internal(key, value)
                return value
            
            return None
    
    def _set_internal(self, key: str, value: Any) -> None:
        """Internal set method that assumes lock is already held."""
        # Evict oldest item if at capacity
        while len(self._cache) >= self._max_size and self._access_order:
            oldest_key = self._access_order.pop(0)
            self._cache.pop(oldest_key, None)
        
        self._cache[key] = value
        if key not in self._access_order:
            self._access_order.append(key)
    
    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to store
        """
        with self._lock:
            self._set_internal(key, value)
    
    def invalidate(self, key: str) -> None:
        """Remove a specific key from the cache."""
        with self._lock:
            self._cache.pop(key, None)
            if key in self._access_order:
                self._access_order.remove(key)
    
    def clear(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()


# Global cache instance for resource caching
# TODO: [OPTIMIZATION] Consider using Redis for distributed caching
# in multiplayer scenarios
_resource_cache = ResourceCache()


def get_cached_resource(key: str, factory: Optional[Callable] = None) -> Optional[Any]:
    """
    Get a resource from the global cache.
    
    Args:
        key: Cache key
        factory: Optional callable to create the value if not cached
        
    Returns:
        The cached resource or None
    """
    return _resource_cache.get(key, factory)


def cache_resource(key: str, value: Any) -> None:
    """
    Store a resource in the global cache.
    
    Args:
        key: Cache key
        value: Value to store
    """
    _resource_cache.set(key, value)


def clear_resource_cache() -> None:
    """Clear the global resource cache."""
    _resource_cache.clear()


@lru_cache(maxsize=64)
def compute_scaled_font_size(base_size: int, scale_factor: float) -> int:
    """
    Compute scaled font size with caching for performance.
    
    Args:
        base_size: Base font size in pixels
        scale_factor: Scale multiplier
        
    Returns:
        Scaled font size, clamped to reasonable bounds
    """
    scaled = int(base_size * scale_factor)
    return max(8, min(200, scaled))  # Clamp to reasonable range


@lru_cache(maxsize=32)
def compute_scaled_position(x: float, y: float, scale_x: float, scale_y: float) -> tuple:
    """
    Compute scaled position with caching.
    
    Args:
        x: Original x coordinate
        y: Original y coordinate
        scale_x: X scale factor
        scale_y: Y scale factor
        
    Returns:
        Tuple of scaled (x, y) coordinates
    """
    return (int(x * scale_x), int(y * scale_y))
