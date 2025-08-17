"""
Database Connection Pool Management Module
Provides asynchronous MySQL connection pool functionality
"""
import asyncio

import redis.asyncio as redis
from src.utils.logger_util import logger
from src.utils.db_config import load_activate_redis_config


class RedisPool:
    """Redis连接池管理类"""

    _instance = None
    _pool = None
    _redis = None
    _config = None

    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = RedisPool()
            await cls._instance._initialize()
        return cls._instance

    async def _initialize(self):
        """初始化连接池"""
        if self._pool is not None:
            return

        # 获取活跃的Redis实例和配置
        redis_instance, redis_config = load_activate_redis_config()
        self._config = redis_config

        try:
            # 准备连接池参数
            pool_kwargs = {
                'host': redis_instance.redis_host,
                'port': redis_instance.redis_port,
                'db': redis_instance.redis_database,
                'max_connections': redis_config.redis_max_connections,
                'socket_connect_timeout': redis_config.redis_connection_timeout,
                'socket_timeout': redis_config.socket_timeout,
                'decode_responses': redis_instance.redis_decode_responses,
                'health_check_interval': redis_config.health_check_interval,
                'retry_on_timeout': redis_config.retry_on_timeout
            }

            # 只有在密码存在时才添加密码参数
            if redis_instance.redis_password:
                pool_kwargs['password'] = redis_instance.redis_password

            # 只有在启用SSL时才添加SSL参数
            if redis_instance.redis_ssl:
                pool_kwargs['ssl'] = True
                pool_kwargs['ssl_check_hostname'] = False
                pool_kwargs['ssl_cert_reqs'] = None

            # 创建连接池
            self._pool = redis.ConnectionPool(**pool_kwargs)

            # 创建Redis客户端
            self._redis = redis.Redis(connection_pool=self._pool)

            # 测试连接
            await self._redis.ping()

            logger.info(f"Redis连接池初始化成功")
            logger.info(f"  实例: {redis_instance.redis_instance_id}")
            logger.info(f"  地址: {redis_instance.redis_host}:{redis_instance.redis_port}")
            logger.info(f"  数据库: {redis_instance.redis_database}")
            logger.info(f"  最大连接数: {redis_config.redis_max_connections}")

        except Exception as e:
            logger.error(f"Redis连接池初始化失败: {str(e)}")
            raise

    async def get_redis(self) -> redis.Redis:
        """
        获取Redis客户端实例

        Returns:
            redis.Redis: Redis客户端实例
        """
        if self._redis is None:
            await self._initialize()
        return self._redis

    async def health_check(self) -> bool:
        """
        执行健康检查

        Returns:
            bool: 连接是否健康
        """
        try:
            if self._redis is None:
                return False

            # 执行ping命令检查连接
            result = await self._redis.ping()
            if result:
                logger.debug("Redis健康检查通过")
                return True
            else:
                logger.warning("Redis健康检查失败: ping返回False")
                return False

        except Exception as e:
            logger.error(f"Redis健康检查失败: {str(e)}")
            return False

    async def close_pool(self):
        """关闭连接池"""
        if self._pool is None:
            logger.warning("Redis连接池不存在，无需关闭")
            return

        try:
            # 关闭Redis客户端
            if self._redis:
                await self._redis.aclose()
                self._redis = None

            # 断开连接池
            await self._pool.aclose()
            self._pool = None

            logger.info("Redis连接池已关闭")

        except Exception as e:
            logger.error(f"关闭Redis连接池失败: {str(e)}")


# 导出连接池获取函数
async def get_redis_pool():
    """获取Redis连接池实例"""
    return await RedisPool.get_instance()


if __name__ == "__main__":
    # 测试连接池
    async def test_pool():
        redis_pool = await get_redis_pool()
        redis_client = await redis_pool.get_redis()

        # 测试基本操作
        await redis_client.set("test_key", "test_value")
        value = await redis_client.get("test_key")
        logger.info(f"测试结果: {value}")

        # 清理测试数据
        await redis_client.delete("test_key")

        # 关闭连接池
        await redis_pool.close_pool()


    asyncio.run(test_pool())