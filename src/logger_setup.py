"""
Logging configuration for FreeTheSnake game.
Provides centralized logging setup with configurable levels.
"""

import logging
import os
import sys
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
    """
    Setup logging configuration for the game.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to also log to a file
    """
    # Convert string level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    if log_to_file:
        os.makedirs("logs", exist_ok=True)
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if requested
    if log_to_file:
        try:
            log_filename = f"logs/freethesnake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            logging.info(f"Logging to file: {log_filename}")
        except Exception as e:
            logging.warning(f"Failed to setup file logging: {e}")
    
    # Log startup information
    logging.info("=== FreeTheSnake Game Starting ===")
    logging.info(f"Log level set to: {log_level}")
    logging.info(f"Python version: {sys.version}")

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)