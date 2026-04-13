"""Root __init__.py for Naukri automation system."""

__version__ = "1.0.0"
__author__ = "Automation System"
__description__ = "Naukri Job Application Automation System"

from core import get_logger, get_config, get_driver_manager
from modules import (
    get_login_module,
    get_search_module,
    get_filter_module,
    get_apply_module,
    get_storage_module
)

__all__ = [
    'get_logger',
    'get_config',
    'get_driver_manager',
    'get_login_module',
    'get_search_module',
    'get_filter_module',
    'get_apply_module',
    'get_storage_module'
]
