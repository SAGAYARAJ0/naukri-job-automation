"""
Centralized logging system for Naukri automation.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """Centralized logger with file and console output."""
    
    _instance = None
    _loggers = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logging configuration."""
        self.log_dir = Path(__file__).parent.parent / "data" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log file paths
        self.app_log = self.log_dir / "app.log"
        self.error_log = self.log_dir / "error.log"
        self.debug_log = self.log_dir / "debug.log"
    
    def get_logger(self, name):
        """Get or create logger for module."""
        if name in self._loggers:
            return self._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        # File handler (app log)
        file_handler = logging.FileHandler(self.app_log)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        # Error handler
        error_handler = logging.FileHandler(self.error_log)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        
        # Debug handler
        debug_handler = logging.FileHandler(self.debug_log)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(file_format)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)
        logger.addHandler(debug_handler)
        
        self._loggers[name] = logger
        return logger
    
    def log_execution_start(self, module_name):
        """Log execution start."""
        logger = self.get_logger(module_name)
        logger.info("=" * 80)
        logger.info(f"{module_name.upper()} EXECUTION STARTED")
        logger.info("=" * 80)
    
    def log_execution_end(self, module_name, status="Success"):
        """Log execution end."""
        logger = self.get_logger(module_name)
        logger.info("=" * 80)
        logger.info(f"{module_name.upper()} EXECUTION ENDED - Status: {status}")
        logger.info("=" * 80)


# Singleton instance
logger_instance = Logger()

def get_logger(name):
    """Get logger for a module."""
    return logger_instance.get_logger(name)
