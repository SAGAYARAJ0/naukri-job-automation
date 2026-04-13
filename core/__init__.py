"""Core module for Naukri automation system."""

from core.exceptions import *
from core.logger import get_logger
from core.config_manager import get_config
from core.driver_manager import get_driver_manager

__all__ = [
    'get_logger',
    'get_config',
    'get_driver_manager'
]
