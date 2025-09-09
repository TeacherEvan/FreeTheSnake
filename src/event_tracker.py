"""
Event Tracking System for FreeTheSnake
Provides comprehensive event logging and analytics for debugging mobile adaptability
"""
import pygame
import json
import time
import os
from datetime import datetime
from config_manager import game_config
from logger_setup import get_logger

logger = get_logger(__name__)

class EventTracker:
    """Comprehensive event tracking and logging system"""
    
    def __init__(self):
        self.enabled = game_config.get_bool('EventTracking', 'enable_event_tracking', True)
        self.log_input_events = game_config.get_bool('EventTracking', 'log_input_events', True)
        self.log_performance = game_config.get_bool('EventTracking', 'log_performance_metrics', True)
        self.log_screen_events = game_config.get_bool('EventTracking', 'log_screen_events', True)
        
        # Event storage
        self.event_history = []
        self.performance_data = {
            'frame_times': [],
            'fps_samples': [],
            'memory_usage': [],
            'event_counts': {},
            'screen_transitions': [],
            'errors': []
        }
        
        # Session tracking
        self.session_start = time.time()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Mobile-specific tracking
        self.touch_gestures = []
        self.screen_orientations = []
        self.resize_events = []
        
        # Create tracking directory
        self.tracking_dir = "logs/event_tracking"
        os.makedirs(self.tracking_dir, exist_ok=True)
        
        if self.enabled:
            logger.info(f"EventTracker initialized for session {self.session_id}")
    
    def track_event(self, event_type, event_data=None, metadata=None):
        """Track a general event with optional data and metadata"""
        if not self.enabled:
            return
        
        timestamp = time.time()
        event_record = {
            'timestamp': timestamp,
            'session_time': timestamp - self.session_start,
            'type': event_type,
            'data': event_data or {},
            'metadata': metadata or {}
        }
        
        self.event_history.append(event_record)
        
        # Log significant events
        if event_type in ['ERROR', 'CRASH', 'PERFORMANCE_WARNING']:
            logger.warning(f"Event tracked: {event_type} - {event_data}")
        else:
            logger.debug(f"Event tracked: {event_type}")
        
        # Keep history manageable - using configurable values
        max_history = game_config.get_int('EventTracking', 'max_event_history', 1000)
        trim_size = game_config.get_int('EventTracking', 'event_history_trim_size', 500)
        if len(self.event_history) > max_history:
            self.event_history = self.event_history[-trim_size:]
    
    def track_pygame_event(self, pygame_event):
        """Track pygame events with detailed information"""
        if not self.enabled or not self.log_input_events:
            return
        
        event_name = pygame.event.event_name(pygame_event.type)
        
        # Count event types
        self.performance_data['event_counts'][event_name] = \
            self.performance_data['event_counts'].get(event_name, 0) + 1
        
        # Extract relevant event data
        event_data = {'event_type': event_name}
        
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            event_data.update({
                'button': pygame_event.button,
                'pos': pygame_event.pos
            })
        elif pygame_event.type == pygame.MOUSEBUTTONUP:
            event_data.update({
                'button': pygame_event.button,
                'pos': pygame_event.pos
            })
        elif pygame_event.type == pygame.MOUSEMOTION:
            event_data.update({
                'pos': pygame_event.pos,
                'rel': pygame_event.rel,
                'buttons': pygame_event.buttons
            })
        elif pygame_event.type == pygame.KEYDOWN:
            event_data.update({
                'key': pygame_event.key,
                'unicode': getattr(pygame_event, 'unicode', ''),
                'mod': pygame_event.mod
            })
        elif pygame_event.type == pygame.KEYUP:
            event_data.update({
                'key': pygame_event.key,
                'mod': pygame_event.mod
            })
        elif pygame_event.type == pygame.VIDEORESIZE:
            event_data.update({
                'size': pygame_event.size,
                'w': pygame_event.w,
                'h': pygame_event.h
            })
            self.resize_events.append({
                'timestamp': time.time(),
                'size': pygame_event.size
            })
        
        self.track_event('PYGAME_EVENT', event_data)
    
    def track_touch_gesture(self, gesture_type, start_pos, end_pos, duration=None):
        """Track touch gestures for mobile adaptability analysis"""
        if not self.enabled:
            return
        
        gesture_data = {
            'type': gesture_type,
            'start_pos': start_pos,
            'end_pos': end_pos,
            'duration': duration,
            'distance': self._calculate_distance(start_pos, end_pos) if end_pos else 0
        }
        
        self.touch_gestures.append({
            'timestamp': time.time(),
            **gesture_data
        })
        
        self.track_event('TOUCH_GESTURE', gesture_data)
    
    def track_screen_transition(self, from_state, to_state):
        """Track screen state transitions"""
        if not self.enabled or not self.log_screen_events:
            return
        
        transition_data = {
            'from_state': from_state,
            'to_state': to_state
        }
        
        self.performance_data['screen_transitions'].append({
            'timestamp': time.time(),
            **transition_data
        })
        
        self.track_event('SCREEN_TRANSITION', transition_data)
    
    def track_performance_metric(self, metric_name, value, unit=None):
        """Track performance metrics"""
        if not self.enabled or not self.log_performance:
            return
        
        timestamp = time.time()
        
        if metric_name == 'frame_time':
            self.performance_data['frame_times'].append({
                'timestamp': timestamp,
                'value': value
            })
        elif metric_name == 'fps':
            self.performance_data['fps_samples'].append({
                'timestamp': timestamp,
                'value': value
            })
        
        # Track significant performance issues
        if metric_name == 'fps' and value < 30:
            self.track_event('PERFORMANCE_WARNING', {
                'metric': metric_name,
                'value': value,
                'threshold': 30,
                'message': 'Low FPS detected'
            })
        elif metric_name == 'frame_time' and value > 33.33:  # > 30 FPS
            self.track_event('PERFORMANCE_WARNING', {
                'metric': metric_name,
                'value': value,
                'threshold': 33.33,
                'message': 'High frame time detected'
            })
    
    def track_error(self, error_type, error_message, stack_trace=None):
        """Track errors and exceptions"""
        if not self.enabled:
            return
        
        error_data = {
            'error_type': error_type,
            'message': error_message,
            'stack_trace': stack_trace
        }
        
        self.performance_data['errors'].append({
            'timestamp': time.time(),
            **error_data
        })
        
        self.track_event('ERROR', error_data)
        logger.error(f"Error tracked: {error_type} - {error_message}")
    
    def track_mobile_adaptation(self, screen_size, orientation, scale_factor):
        """Track mobile adaptation events"""
        if not self.enabled:
            return
        
        adaptation_data = {
            'screen_size': screen_size,
            'orientation': orientation,
            'scale_factor': scale_factor
        }
        
        self.screen_orientations.append({
            'timestamp': time.time(),
            **adaptation_data
        })
        
        self.track_event('MOBILE_ADAPTATION', adaptation_data)
    
    def get_session_summary(self):
        """Get a summary of the current tracking session"""
        current_time = time.time()
        session_duration = current_time - self.session_start
        
        # Calculate performance statistics
        fps_values = [sample['value'] for sample in self.performance_data['fps_samples']]
        frame_times = [sample['value'] for sample in self.performance_data['frame_times']]
        
        avg_fps = sum(fps_values) / len(fps_values) if fps_values else 0
        avg_frame_time = sum(frame_times) / len(frame_times) if frame_times else 0
        
        summary = {
            'session_id': self.session_id,
            'session_duration': session_duration,
            'total_events': len(self.event_history),
            'event_counts': self.performance_data['event_counts'].copy(),
            'performance': {
                'average_fps': avg_fps,
                'average_frame_time': avg_frame_time,
                'total_errors': len(self.performance_data['errors'])
            },
            'mobile_data': {
                'touch_gestures': len(self.touch_gestures),
                'screen_transitions': len(self.performance_data['screen_transitions']),
                'resize_events': len(self.resize_events),
                'orientation_changes': len(self.screen_orientations)
            }
        }
        
        return summary
    
    def export_session_data(self, filename=None):
        """Export session data to JSON file"""
        if not self.enabled:
            return None
        
        if filename is None:
            filename = f"session_{self.session_id}.json"
        
        filepath = os.path.join(self.tracking_dir, filename)
        
        export_data = {
            'session_info': {
                'session_id': self.session_id,
                'start_time': self.session_start,
                'export_time': time.time()
            },
            'summary': self.get_session_summary(),
            'events': self.event_history[-100:],  # Last 100 events
            'performance_data': {
                'event_counts': self.performance_data['event_counts'],
                'screen_transitions': self.performance_data['screen_transitions'],
                'errors': self.performance_data['errors']
            },
            'mobile_data': {
                'touch_gestures': self.touch_gestures[-50:],  # Last 50 gestures
                'resize_events': self.resize_events,
                'screen_orientations': self.screen_orientations
            }
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Session data exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to export session data: {e}")
            return None
    
    def log_mobile_compatibility_info(self, mobile_adapter):
        """Log mobile compatibility information"""
        if not self.enabled or not mobile_adapter:
            return
        
        compat_info = {
            'mobile_mode_enabled': mobile_adapter.mobile_mode,
            'touch_friendly_ui': mobile_adapter.touch_friendly,
            'adaptive_scaling': mobile_adapter.adaptive_scaling,
            'current_dimensions': f"{mobile_adapter.current_width}x{mobile_adapter.current_height}",
            'scale_factors': f"{mobile_adapter.scale_x:.2f}x{mobile_adapter.scale_y:.2f}",
            'ui_scale': mobile_adapter.ui_scale,
            'orientation': mobile_adapter.get_orientation(),
            'is_mobile_resolution': mobile_adapter.is_mobile_resolution()
        }
        
        self.track_event('MOBILE_COMPATIBILITY_INFO', compat_info)
        logger.info(f"Mobile compatibility: {compat_info}")
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate distance between two positions"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def cleanup(self):
        """Clean up and export final session data"""
        if self.enabled:
            self.export_session_data()
            logger.info(f"EventTracker session {self.session_id} ended")

# Global event tracker instance
event_tracker = None

def get_event_tracker():
    """Get the global event tracker instance"""
    return event_tracker

def initialize_event_tracker():
    """Initialize the global event tracker"""
    global event_tracker
    event_tracker = EventTracker()
    return event_tracker