"""
Configuration management for FreeTheSnake game.
Provides centralized configuration loading and default values.
"""

import configparser
import os
import logging
from typing import Union

class GameConfig:
    """Manages game configuration from config.ini file with fallback defaults."""
    
    def __init__(self, config_path: str = "config.ini"):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file with default fallbacks."""
        # Set default values
        self.config.read_dict({
            'Game': {
                'screen_width': '800',
                'screen_height': '600',
                'fps': '60',
                'initial_lives': '3',
                'snake_initial_size': '5'
            },
            'Graphics': {
                'enable_custom_fonts': 'true',
                'fallback_to_default_fonts': 'true',
                'enable_animations': 'true',
                'enable_particles': 'true',
                'enable_mouse_trail': 'true'
            },
            'Audio': {
                'enable_sound': 'false',
                'music_volume': '0.7',
                'sound_effects_volume': '0.8'
            },
            'Development': {
                'debug_mode': 'false',
                'show_fps': 'false',
                'log_level': 'INFO'
            },
            'Education': {
                'include_numbers': 'true',
                'include_letters': 'true',
                'include_shapes': 'true',
                'difficulty_progression': 'true'
            }
        })
        
        # Try to load from file, but don't fail if file doesn't exist
        if os.path.exists(self.config_path):
            try:
                self.config.read(self.config_path)
                logging.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logging.warning(f"Failed to load config from {self.config_path}: {e}")
                logging.info("Using default configuration values")
        else:
            logging.info(f"Config file {self.config_path} not found, using defaults")
    
    def get_int(self, section: str, option: str, fallback: int = 0) -> int:
        """Get integer value from config."""
        try:
            return self.config.getint(section, option)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_float(self, section: str, option: str, fallback: float = 0.0) -> float:
        """Get float value from config."""
        try:
            return self.config.getfloat(section, option)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_bool(self, section: str, option: str, fallback: bool = False) -> bool:
        """Get boolean value from config."""
        try:
            return self.config.getboolean(section, option)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_str(self, section: str, option: str, fallback: str = "") -> str:
        """Get string value from config."""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

# Global configuration instance
game_config = GameConfig()