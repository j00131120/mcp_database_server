"""
日志工具模块

统一的日志配置模块。所有其他模块都应该从这里导入logger。
"""

import json
import os
import sys

from loguru import logger

from src import project_path

def get_log_path_from_config():
    """从配置文件获取日志路径"""
    config_file = os.path.join(project_path, "dbconfig.json")
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('logPath', os.path.join(project_path, "logs"))
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # 如果配置文件不存在或解析失败，使用默认路径
        return os.path.join(project_path, "logs")

log_path = get_log_path_from_config()
log_file = os.path.join(log_path, "mcp_server.log")

def setup_logger():
    """配置日志输出"""
    # 移除默认的logger配置
    logger.remove()

    # 输出到stderr，这样MCP可以看到日志
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )

    # 同时输出到文件
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )

    logger.info(f"日志配置完成，日志文件路径: {log_file}")
    return logger


# 初始化日志配置
setup_logger()

# 导出logger供其他模块使用
__all__ = ['logger']