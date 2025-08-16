"""
Logging Utility Module

Unified logging configuration module. All other modules should import logger from here.
"""

import json
import os
import sys
from loguru import logger

from src.server import project_path
from src.utils.db_config import get_db_config_file

loglevel_array = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
db_config_path = get_db_config_file()
def get_log_path_from_config():
    """Get log path from configuration file"""
    config_file = db_config_path
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            log_path = config.get('logPath')
        if log_path is None or 0 == len(log_path.strip()):
            log_path = os.path.join(project_path, "logs")
        else:
            log_path = os.path.join(log_path, "logs")
        return log_path
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # If configuration file doesn't exist or parsing fails, use default path
        return os.path.join(project_path, "logs")

log_path = get_log_path_from_config()
log_file = os.path.join(log_path, "mcp_server.log")

def get_log_level_from_config():
    """Get log level from configuration file"""
    config_file = db_config_path
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            log_level = config.get('logLevel')
            if log_level is None or 0 == len(log_level.strip()):
                log_level = "INFO"
            else:
                log_level=log_level.upper()
                if log_level not in loglevel_array:
                 log_level = "INFO"
        return log_level
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # If configuration file doesn't exist or parsing fails, default to INFO level
        return "INFO"

log_level = get_log_level_from_config()

def setup_logger(log_file: str, log_level:str):
    """Configure logging output"""
    # Remove default logger configuration
    logger.remove()

    # Output to stderr so MCP can see logs
    logger.add(
        sys.stderr,
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )

    # Also output to file
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )

    logger.info(f"Logging configuration completed, log level: {log_level}, log file path: {log_file}")
    return logger


# Initialize logging configuration
setup_logger(log_file, log_level)

# Export logger for use by other modules
__all__ = ['logger']