"""
多数据源MCP服务器包

该包提供了一个模型上下文协议(MCP)服务器，支持多种数据库类型并提供统一的SQL执行功能。
"""

from pathlib import Path

__version__ = "0.1.0"
__author__ = "多数据源MCP团队"
__description__ = "多数据源模型上下文协议服务器"

# 项目路径配置
current_path = Path(__file__).parent
project_path = current_path.parent.resolve()

# 导出常用路径
__all__ = [
    "__version__",
    "__author__", 
    "__description__",
    "current_path",
    "project_path"
]

if __name__ == "__main__":
    print(f"当前路径: {current_path}")
    print(f"项目路径: {project_path}")
    print(f"版本: {__version__}")
