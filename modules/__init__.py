"""Modules for Naukri automation system."""

from modules.login import get_login_module
from modules.search import get_search_module
from modules.filter import get_filter_module
from modules.apply import get_apply_module
from modules.storage import get_storage_module

__all__ = [
    'get_login_module',
    'get_search_module',
    'get_filter_module',
    'get_apply_module',
    'get_storage_module'
]
