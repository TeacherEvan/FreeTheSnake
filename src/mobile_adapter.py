"""
Mobile Adaptability Module for FreeTheSnake
Provides responsive design, touch-friendly interfaces, and mobile-like functionality
"""
import pygame
import math
import time
from config_manager import game_config
from logger_setup import get_logger

logger = get_logger(__name__)

class MobileAdapter:
    """Handles mobile adaptability features including responsive scaling and touch events"""
    
    def __init__(self, initial_width=800, initial_height=600):
        self.base_width = initial_width
        self.base_height = initial_height
        self.current_width = initial_width
        self.current_height = initial_height
        
        # Mobile configuration
        self.mobile_mode = game_config.get_bool('Mobile', 'enable_mobile_mode', False)
        self.touch_friendly = game_config.get_bool('Mobile', 'touch_friendly_ui', True)
        self.adaptive_scaling = game_config.get_bool('Mobile', 'adaptive_scaling', True)
        self.min_touch_target = game_config.get_int('Mobile', 'minimum_touch_target_size', 44)
        
        # Scaling factors
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.ui_scale = 1.0
        
        # Touch state tracking
        self.touch_state = {
            'active_touches': {},
            'last_tap_time': 0,
            'tap_count': 0,
            'gesture_start': None
        }
        
        # Performance tracking
        self.performance_metrics = {
            'frame_times': [],
            'event_counts': {},
            'render_times': []
        }
        
        logger.info(f"MobileAdapter initialized - Mobile mode: {self.mobile_mode}, Touch friendly: {self.touch_friendly}")
    
    def update_dimensions(self, width, height):
        """Update screen dimensions and recalculate scaling factors"""
        self.current_width = width
        self.current_height = height
        
        if self.adaptive_scaling:
            self.scale_x = width / self.base_width
            self.scale_y = height / self.base_height
            # Use uniform scaling for UI elements
            self.ui_scale = min(self.scale_x, self.scale_y)
            
        logger.debug(f"Dimensions updated: {width}x{height}, Scale: {self.scale_x:.2f}x{self.scale_y:.2f}, UI Scale: {self.ui_scale:.2f}")
    
    def get_mobile_preset_dimensions(self, preset_type="mobile_portrait"):
        """Get predefined mobile screen dimensions"""
        presets = {
            "mobile_portrait": (
                game_config.get_int('Mobile', 'mobile_portrait_width', 390),
                game_config.get_int('Mobile', 'mobile_portrait_height', 844)
            ),
            "mobile_landscape": (
                game_config.get_int('Mobile', 'mobile_landscape_width', 844),
                game_config.get_int('Mobile', 'mobile_landscape_height', 390)
            ),
            "tablet_portrait": (
                game_config.get_int('Mobile', 'tablet_portrait_width', 768),
                game_config.get_int('Mobile', 'tablet_portrait_height', 1024)
            ),
            "tablet_landscape": (
                game_config.get_int('Mobile', 'tablet_landscape_width', 1024),
                game_config.get_int('Mobile', 'tablet_landscape_height', 768)
            )
        }
        return presets.get(preset_type, (800, 600))
    
    def scale_position(self, x, y):
        """Scale a position based on current scaling factors"""
        return int(x * self.scale_x), int(y * self.scale_y)
    
    def scale_size(self, width, height):
        """Scale dimensions based on current scaling factors"""
        return int(width * self.scale_x), int(height * self.scale_y)
    
    def scale_ui_element(self, size):
        """Scale UI element size for touch-friendly interface"""
        scaled_size = int(size * self.ui_scale)
        if self.touch_friendly:
            # Ensure minimum touch target size
            return max(scaled_size, self.min_touch_target)
        return scaled_size
    
    def get_adaptive_font_size(self, base_size):
        """Get adaptive font size based on screen scaling"""
        scaled_size = int(base_size * self.ui_scale)
        # Ensure readable font sizes
        return max(scaled_size, 12)
    
    def handle_touch_event(self, event):
        """Process touch events and convert them to appropriate game events"""
        event_tracking_enabled = game_config.get_bool('EventTracking', 'track_touch_gestures', True)
        
        if event_tracking_enabled:
            self._log_input_event(event)
        
        # Convert mouse events to touch-like events
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_touch_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._handle_touch_end(event)
        elif event.type == pygame.MOUSEMOTION:
            return self._handle_touch_move(event)
        
        return None
    
    def _handle_touch_start(self, event):
        """Handle touch start (mouse down) events"""
        touch_id = 0  # Simulate touch ID for mouse
        current_time = time.time()
        
        self.touch_state['active_touches'][touch_id] = {
            'start_pos': event.pos,
            'current_pos': event.pos,
            'start_time': current_time
        }
        
        # Detect double tap
        if current_time - self.touch_state['last_tap_time'] < 0.5:
            self.touch_state['tap_count'] += 1
        else:
            self.touch_state['tap_count'] = 1
        
        self.touch_state['last_tap_time'] = current_time
        
        logger.debug(f"Touch start at {event.pos}, tap count: {self.touch_state['tap_count']}")
        return event
    
    def _handle_touch_end(self, event):
        """Handle touch end (mouse up) events"""
        touch_id = 0
        
        if touch_id in self.touch_state['active_touches']:
            touch_info = self.touch_state['active_touches'][touch_id]
            duration = time.time() - touch_info['start_time']
            
            # Determine gesture type
            distance = self._calculate_distance(touch_info['start_pos'], event.pos)
            
            if distance < 10 and duration < 0.5:
                logger.debug(f"Tap gesture detected at {event.pos}")
            elif distance > 20:
                logger.debug(f"Swipe gesture detected from {touch_info['start_pos']} to {event.pos}")
            
            del self.touch_state['active_touches'][touch_id]
        
        return event
    
    def _handle_touch_move(self, event):
        """Handle touch move (mouse motion) events"""
        touch_id = 0
        
        if touch_id in self.touch_state['active_touches']:
            self.touch_state['active_touches'][touch_id]['current_pos'] = event.pos
        
        return event
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate distance between two positions"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _log_input_event(self, event):
        """Log input events for debugging"""
        if game_config.get_bool('EventTracking', 'log_input_events', True):
            event_type = pygame.event.event_name(event.type)
            self.performance_metrics['event_counts'][event_type] = \
                self.performance_metrics['event_counts'].get(event_type, 0) + 1
            
            if len(self.performance_metrics['event_counts']) % 100 == 0:
                logger.debug(f"Event counts: {self.performance_metrics['event_counts']}")
    
    def track_performance(self, frame_time):
        """Track performance metrics"""
        if game_config.get_bool('EventTracking', 'log_performance_metrics', True):
            self.performance_metrics['frame_times'].append(frame_time)
            
            # Keep only last 60 frames for analysis
            if len(self.performance_metrics['frame_times']) > 60:
                self.performance_metrics['frame_times'].pop(0)
            
            # Log performance every 5 seconds
            if len(self.performance_metrics['frame_times']) % 300 == 0:
                avg_frame_time = sum(self.performance_metrics['frame_times']) / len(self.performance_metrics['frame_times'])
                fps = 1000.0 / avg_frame_time if avg_frame_time > 0 else 0
                logger.debug(f"Performance: Avg FPS: {fps:.1f}, Frame time: {avg_frame_time:.2f}ms")
    
    def is_mobile_resolution(self):
        """Check if current resolution is mobile-like"""
        aspect_ratio = self.current_width / self.current_height
        
        # Portrait orientation (common for mobile)
        if aspect_ratio < 1.0:
            return True
        
        # Small landscape screens (mobile landscape)
        if self.current_width < 1000 and self.current_height < 700:
            return True
        
        return False
    
    def get_orientation(self):
        """Get current screen orientation"""
        if self.current_width > self.current_height:
            return "landscape"
        else:
            return "portrait"
    
    def create_touch_friendly_rect(self, base_rect):
        """Create a touch-friendly version of a rectangle"""
        if not self.touch_friendly:
            return base_rect
        
        # Ensure minimum touch target size
        min_size = self.min_touch_target
        width = max(base_rect.width, min_size)
        height = max(base_rect.height, min_size)
        
        # Center the enlarged rect on the original position
        x = base_rect.x - (width - base_rect.width) // 2
        y = base_rect.y - (height - base_rect.height) // 2
        
        return pygame.Rect(x, y, width, height)
    
    def get_mobile_ui_spacing(self):
        """Get appropriate UI spacing for mobile interfaces"""
        base_spacing = 10
        return self.scale_ui_element(base_spacing)
    
    def get_status_info(self):
        """Get current mobile adapter status for debugging"""
        return {
            'mobile_mode': self.mobile_mode,
            'dimensions': f"{self.current_width}x{self.current_height}",
            'scale': f"{self.scale_x:.2f}x{self.scale_y:.2f}",
            'ui_scale': f"{self.ui_scale:.2f}",
            'orientation': self.get_orientation(),
            'is_mobile_resolution': self.is_mobile_resolution(),
            'active_touches': len(self.touch_state['active_touches'])
        }

# Global mobile adapter instance
mobile_adapter = None

def get_mobile_adapter():
    """Get the global mobile adapter instance"""
    return mobile_adapter

def initialize_mobile_adapter(width=800, height=600):
    """Initialize the global mobile adapter"""
    global mobile_adapter
    mobile_adapter = MobileAdapter(width, height)
    return mobile_adapter