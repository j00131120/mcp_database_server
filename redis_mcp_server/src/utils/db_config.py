"""
Database Configuration Module

Uses singleton pattern to handle database configuration loading and management.
"""

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from .logger_util import logger, db_config_path


@dataclass
class RedisInstance:
    """Redis实例配置"""
    redis_instance_id: str
    redis_type: str
    redis_host: str
    redis_port: int
    redis_database: int
    redis_password: Optional[str]
    redis_active: bool
    redis_ssl: bool = False
    redis_decode_responses: bool = True


@dataclass
class DatabaseConfig:
    """数据库配置，包含连接池设置和Redis实例列表"""
    redis_encoding: str
    redis_pool_size: int
    redis_max_connections: int
    redis_connection_timeout: int
    socket_timeout: int
    retry_on_timeout: bool
    health_check_interval: int
    redis_instances_list: List[RedisInstance]


class DatabaseConfigLoader:
    """数据库配置加载器，从JSON文件加载配置 - 单例模式"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        单例模式实现

        Returns:
            DatabaseConfigLoader: 单例实例
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
            self._config: Optional[DatabaseConfig] = None
            self._initialized = True
            logger.info(f"数据库配置加载器已初始化，配置文件: {self.config_json_file}")

    def load_config(self) -> DatabaseConfig:
        """
        从JSON文件加载数据库配置

        Returns:
            DatabaseConfig: 加载的配置对象

        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: JSON格式无效
            KeyError: 缺少必需的配置键
        """
        if not os.path.exists(self.config_json_file):
            error_msg = f"数据库配置文件未找到: {self.config_json_file}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(self.config_json_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            logger.info(f"成功读取数据库配置文件: {self.config_json_file}")
        except json.JSONDecodeError as e:
            error_msg = f"数据库配置文件JSON格式错误: {e}"
            logger.error(error_msg)
            raise json.JSONDecodeError(error_msg, e.doc, e.pos)

        # 验证必需的键
        required_keys = ['redisPoolSize', 'redisMaxConnections', 'redisConnectionTimeout', 'redisList']
        for key in required_keys:
            if key not in config_data:
                error_msg = f"缺少必需的数据库配置键: {key}"
                logger.error(error_msg)
                raise KeyError(error_msg)

        # 解析Redis实例
        redis_instances = []
        for redis_data in config_data['redisList']:
            required_redis_keys = [
                'redisInstanceId', 'redisType', 'redisHost', 'redisPort',
                'redisDatabase', 'dbActive'
            ]
            for key in required_redis_keys:
                if key not in redis_data:
                    error_msg = f"缺少必需的Redis实例配置键: {key}"
                    logger.error(error_msg)
                    raise KeyError(error_msg)

            redis_instance = RedisInstance(
                redis_instance_id=redis_data['redisInstanceId'],
                redis_type=redis_data['redisType'],
                redis_host=redis_data['redisHost'],
                redis_port=redis_data['redisPort'],
                redis_database=redis_data['redisDatabase'],
                redis_password=redis_data.get('redisPassword'),
                redis_active=redis_data['dbActive'],  # 使用dbActive字段
                redis_ssl=redis_data.get('redisSsl', False),
                redis_decode_responses=redis_data.get('redisDecodeResponses', True)
            )
            redis_instances.append(redis_instance)
            logger.info(
                f"解析Redis实例: {redis_instance.redis_instance_id} ({redis_instance.redis_host}:{redis_instance.redis_port})")

        # 创建配置对象
        self._config = DatabaseConfig(
            redis_encoding=config_data.get('redisEncoding', 'utf-8'),
            redis_pool_size=config_data['redisPoolSize'],
            redis_max_connections=config_data['redisMaxConnections'],
            redis_connection_timeout=config_data['redisConnectionTimeout'],
            socket_timeout=config_data.get('socketTimeout', 30),
            retry_on_timeout=config_data.get('retryOnTimeout', True),
            health_check_interval=config_data.get('healthCheckInterval', 30),
            redis_instances_list=redis_instances
        )

        logger.info(f"数据库配置加载完成，共 {len(redis_instances)} 个Redis实例")
        return self._config

    def get_config(self) -> DatabaseConfig:
        """
        获取加载的配置，如果未加载则自动加载

        Returns:
            DatabaseConfig: 配置对象
        """
        if self._config is None:
            return self.load_config()
        return self._config

    def get_active_redis(self) -> Optional[RedisInstance]:
        """
        获取第一个活跃的Redis实例

        Returns:
            Optional[RedisInstance]: 第一个活跃的Redis实例，如果没有活跃实例则返回None
        """
        config = self.get_config()
        for redis in config.redis_instances_list:
            if redis.redis_active:
                logger.info(f"找到第一个活跃Redis实例: {redis.redis_instance_id}")
                return redis
        logger.warning("没有找到活跃的Redis实例")
        return None


def load_db_config() -> DatabaseConfig:
    """
    加载数据库配置的便利函数

    Returns:
        DatabaseConfig: 加载的配置对象
    """
    loader = DatabaseConfigLoader()
    return loader.load_config()


def load_active_redis_config() -> tuple[RedisInstance, DatabaseConfig]:
    """
    加载数据库配置和活跃的Redis实例的便利函数

    Returns:
        tuple[RedisInstance, DatabaseConfig]: 活跃的Redis实例和配置对象的元组
    """
    loader = DatabaseConfigLoader()
    config = loader.get_config()
    active_redis = loader.get_active_redis()
    if active_redis is None:
        raise ValueError("没有找到活跃的Redis实例")
    return active_redis, config


# 为了向后兼容，保留原有的函数名
def load_redis_config() -> DatabaseConfig:
    """
    加载Redis配置的便利函数（向后兼容）

    Returns:
        DatabaseConfig: 加载的配置对象
    """
    return load_db_config()


def load_activate_redis_config() -> tuple[RedisInstance, DatabaseConfig]:
    """
    加载Redis配置和活跃的Redis实例的便利函数（向后兼容）

    Returns:
        tuple[RedisInstance, DatabaseConfig]: 活跃的Redis实例和配置对象的元组
    """
    return load_active_redis_config()


# 示例用法
if __name__ == "__main__":
    # 加载配置
    active_redis, db_config = load_active_redis_config()
    logger.info(f"Redis编码: {db_config.redis_encoding}")
    logger.info(f"Redis连接池大小: {db_config.redis_pool_size}")
    logger.info(f"Redis最大连接数: {db_config.redis_max_connections}")
    logger.info(f"Redis连接超时时间: {db_config.redis_connection_timeout}")
    logger.info(f"Socket超时时间: {db_config.socket_timeout}")
    logger.info(f"超时重试: {db_config.retry_on_timeout}")
    logger.info(f"健康检查间隔: {db_config.health_check_interval}")

    # 显示活跃Redis信息
    logger.info(f"\n活跃Redis实例: {active_redis.redis_instance_id}")
    logger.info(f"  主机: {active_redis.redis_host}:{active_redis.redis_port}")
    logger.info(f"  数据库: {active_redis.redis_database}")
    logger.info(f"  类型: {active_redis.redis_type}")
    logger.info(f"  密码: {'已设置' if active_redis.redis_password else '未设置'}")
