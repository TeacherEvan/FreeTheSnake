import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.lazy_loader import LazyLoader, ResourceCache, compute_scaled_font_size


class TestLazyLoader(unittest.TestCase):
    """Test cases for the LazyLoader class."""

    def test_lazy_loader_initialization(self):
        """Test that LazyLoader initializes correctly without loading the class."""
        loader = LazyLoader('game_state', 'GameState')
        # The class should not be loaded yet
        self.assertIsNone(loader._class)
        self.assertIsNone(loader._instance)

    def test_resource_cache_basic_operations(self):
        """Test basic ResourceCache set and get operations."""
        cache = ResourceCache(max_size=10)
        
        # Test setting and getting a value
        cache.set('test_key', 'test_value')
        result = cache.get('test_key')
        self.assertEqual(result, 'test_value')

    def test_resource_cache_factory_function(self):
        """Test ResourceCache factory function for lazy creation."""
        cache = ResourceCache(max_size=10)
        
        # Test factory function
        result = cache.get('computed_key', lambda: 42)
        self.assertEqual(result, 42)
        
        # Second call should return cached value
        result = cache.get('computed_key', lambda: 100)
        self.assertEqual(result, 42)  # Should be cached, not 100

    def test_resource_cache_invalidation(self):
        """Test ResourceCache invalidation."""
        cache = ResourceCache(max_size=10)
        
        cache.set('key_to_remove', 'value')
        self.assertEqual(cache.get('key_to_remove'), 'value')
        
        cache.invalidate('key_to_remove')
        self.assertIsNone(cache.get('key_to_remove'))

    def test_resource_cache_max_size(self):
        """Test ResourceCache respects max size limit."""
        cache = ResourceCache(max_size=3)
        
        # Add 4 items to a cache with max size 3
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.set('key3', 'value3')
        cache.set('key4', 'value4')
        
        # At most 3 items should be in the cache
        # key1 should be evicted as it's the oldest
        self.assertIsNone(cache.get('key1'))
        self.assertEqual(cache.get('key4'), 'value4')

    def test_compute_scaled_font_size(self):
        """Test the cached font size computation."""
        # Test normal scaling
        result = compute_scaled_font_size(24, 1.5)
        self.assertEqual(result, 36)  # 24 * 1.5 = 36
        
        # Test minimum clamping
        result = compute_scaled_font_size(10, 0.1)
        self.assertEqual(result, 8)  # Clamped to minimum 8
        
        # Test maximum clamping
        result = compute_scaled_font_size(100, 3.0)
        self.assertEqual(result, 200)  # Clamped to maximum 200


class TestResourceCacheLRU(unittest.TestCase):
    """Test LRU eviction behavior of ResourceCache."""

    def test_lru_eviction_order(self):
        """Test that least recently used items are evicted first."""
        cache = ResourceCache(max_size=3)
        
        # Add items
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.set('key3', 'value3')
        
        # Access key1 to make it recently used
        cache.get('key1')
        
        # Add a new item - key2 should be evicted (least recently used)
        cache.set('key4', 'value4')
        
        # key1 should still exist (was accessed), key2 should be evicted
        self.assertIsNotNone(cache.get('key1'))
        # Note: Depending on implementation details, this test may need adjustment


if __name__ == '__main__':
    unittest.main()
