"""
Utility Tools Module

This module contains utility functions and classes for:
- Database configuration management (JSON-based configuration with validation)
- Connection pooling (Async database connection pools for MySQL/Oracle)
- Database operations (SQL execution with transaction management)
- Logging utilities (Structured logging with file rotation)

All utilities support both MySQL and Oracle compatibility modes for OceanBase.
"""

from typing import TYPE_CHECKING, Any

# Core imports - always available
__all__ = [
    # Logging
    "logger",
    
    # Database configuration
    "DatabaseInstance",
    "DatabaseInstanceConfig", 
    "DatabaseInstanceConfigLoader",
    "load_activate_db_config",
    # Database operations
    "execute_sql",
]