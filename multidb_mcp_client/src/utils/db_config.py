"""
数据库配置模块

使用单例模式处理数据库配置加载和管理。
"""

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from src import project_path

from .logger_util import logger


db_config_name = "dbconfig.json"
db_config_path = os.path.join(project_path, db_config_name)

logger.info(f"当前数据库配置路径: {db_config_path}")


@dataclass
class DatabaseInstance:
    """数据库实例配置"""
    db_instance_id: str
    db_host: str
    db_port: int
    db_database: str
    db_username: str
    db_password: str
    db_type: str
    db_active: bool


@dataclass
class DatabaseInstanceConfig:
    """数据库配置，包含连接池设置和数据库实例列表"""
    db_pool_size = 0
    db_max_overflow = 0
    db_pool_timeout = 0
    db_instances_list: List[DatabaseInstance]
    log_path: str
    multidb_server: str


class DatabaseInstanceConfigLoader:
    """数据库配置加载器，从JSON文件加载配置 - 单例模式"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        单例模式实现

        Returns:
            DatabaseInstanceConfigLoader: 单例实例
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化配置加载器（仅在第一次创建实例时执行）
        """
        if not self._initialized:
            self.config_json_file = db_config_path
            self._config: Optional[DatabaseInstanceConfig] = None
            self._initialized = True
            logger.info(f"数据库实例配置加载器已初始化，配置文件: {self.config_json_file}")

    def load_config(self) -> DatabaseInstanceConfig:
        """
        从JSON文件加载数据库配置

        Returns:
            DatabaseInstanceConfig: 加载的配置对象

        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: JSON格式无效
            KeyError: 缺少必需的配置键
        """
        if not os.path.exists(self.config_json_file):
            error_msg = f"配置文件未找到: {self.config_json_file}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(self.config_json_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            logger.info(f"成功读取配置文件: {self.config_json_file}")
        except json.JSONDecodeError as e:
            error_msg = f"配置文件JSON格式错误: {e}"
            logger.error(error_msg)
            raise json.JSONDecodeError(error_msg, e.doc, e.pos)

        # 验证必需的键
        required_keys = ['dbList']
        for key in required_keys:
            if key not in config_data:
                error_msg = f"缺少必需的配置键: {key}"
                logger.error(error_msg)
                raise KeyError(error_msg)

        # 解析数据库实例
        db_instances = []
        for db_data in config_data['dbList']:
            required_db_keys = [
                'dbInstanceId', 'dbHost', 'dbPort', 'dbDatabase',
                'dbUsername', 'dbPassword', 'dbType', 'dbActive'
            ]
            for key in required_db_keys:
                if key not in db_data:
                    error_msg = f"缺少必需的数据库配置键: {key}"
                    logger.error(error_msg)
                    raise KeyError(error_msg)

            db_instance = DatabaseInstance(
                db_instance_id=db_data['dbInstanceId'],
                db_host=db_data['dbHost'],
                db_port=db_data['dbPort'],
                db_database=db_data['dbDatabase'],
                db_username=db_data['dbUsername'],
                db_password=db_data['dbPassword'],
                db_type=db_data['dbType'],
                db_active=db_data['dbActive']
            )
            db_instances.append(db_instance)
            logger.info(f"解析数据库实例: {db_instance.db_instance_id} ({db_instance.db_host}:{db_instance.db_port})")

        # 创建配置对象
        self._config = DatabaseInstanceConfig(
            db_instances_list=db_instances,
            multidb_server=config_data['multiDBServer'],
            log_path=config_data['logPath']
        )

        logger.info(f"配置加载完成，共 {len(db_instances)} 个数据库实例")
        return self._config

    def get_config(self) -> DatabaseInstanceConfig:
        """
        获取加载的配置，如果未加载则自动加载

        Returns:
            DatabaseInstanceConfig: 配置对象
        """
        if self._config is None:
            return self.load_config()
        return self._config

    def get_active_database(self) -> Optional[DatabaseInstance]:
        """
        获取第一个活跃的数据库实例

        Returns:
            Optional[DatabaseInstance]: 第一个活跃的数据库实例，如果没有活跃实例则返回None
        """
        config = self.get_config()
        for db in config.db_instances_list:
            if db.db_active:
                logger.info(f"找到第一个活跃数据库: {db.db_instance_id}")
                return db
        logger.warning("没有找到活跃的数据库实例")
        return None


def load_db_config() -> DatabaseInstanceConfig:
    """
    加载数据库配置的便利函数

    Returns:
        DatabaseInstanceConfig: 加载的配置对象
    """
    loader = DatabaseInstanceConfigLoader()
    return loader.load_config()


def load_activate_db_config() -> tuple[DatabaseInstance, DatabaseInstanceConfig]:
    """
    加载数据库配置和活跃的数据库实例的便利函数

    Returns:
        tuple[DatabaseInstance, DatabaseInstanceConfig]: 活跃的数据库实例和配置对象的元组
    """
    loader = DatabaseInstanceConfigLoader()
    config = loader.get_config()
    active_database = loader.get_active_database()
    if active_database is None:
        raise ValueError("没有找到活跃的数据库实例")
    return active_database, config

# 示例用法
# if __name__ == "__main__":
#     # 加载配置
#     active_db, db_config = load_activate_db_config()
#     logger.info(f"数据库连接池大小: {db_config.db_pool_size}")
#     logger.info(f"数据库最大溢出连接数: {db_config.db_max_overflow}")
#     logger.info(f"数据库连接池超时时间: {db_config.db_pool_timeout}")
#     logger.info(f"数据库最大溢出连接数: {db_config.db_max_overflow}")
#     logger.info(f"数据库连接池超时时间: {db_config.db_pool_timeout}")
#     logger.info(f"多数据库服务器: {db_config.multidb_server}")
#     logger.info(f"日志路径: {db_config.log_path}")
#     logger.info(f"数据库实例数量: {len(db_config.db_instances_list)}")
#     # 显示活跃数据库信息
#     logger.info(f"\n活跃数据库: {active_db.db_instance_id}")
#     logger.info(f"  主机: {active_db.db_host}:{db_config.db_port}")
#     logger.info(f"  数据库: {active_db.db_database}")
#     logger.info(f"  用户名: {active_db.db_username}")
#     logger.info(f"  数据库类型: {active_db.db_type}")