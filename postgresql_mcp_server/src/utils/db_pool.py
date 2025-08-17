"""
数据库连接池管理模块
提供异步PostgreSQL连接池功能
"""
import asyncio
import asyncpg
from src.utils.logger_util import logger
from src.utils.db_config import load_activate_db_config


class DatabasePool:
    """数据库连接池管理类"""

    _instance = None
    _pool = None
    _config = None

    @classmethod
    async def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = DatabasePool()
            await cls._instance._initialize()
        return cls._instance

    async def _initialize(self):
        """初始化连接池"""
        if self._pool is not None:
            return

        # 获取活跃的数据库实例和配置
        db_instance, db_config = load_activate_db_config()
        self._config = db_config

        try:
            pool_size = int(db_config.db_pool_size)
            max_overflow = int(db_config.db_max_overflow)
            pool_timeout = int(db_config.db_pool_timeout)
            max_size = pool_size + max_overflow
            self._pool = await asyncpg.create_pool(
                host=db_instance.db_host,
                port=int(db_instance.db_port),
                user=db_instance.db_username,
                password=db_instance.db_password,
                database=db_instance.db_database,
                min_size=pool_size,
                max_size=max_size,
                max_inactive_connection_lifetime=pool_timeout # Keep consistent with synchronous version
            )
            logger.info(
                f"Database connection pool initialized successfully, pool minsize: {pool_size}, maxsize: {max_size},  timeout:{pool_timeout}s")
            logger.info(
                f"Database connection pool Config: {db_instance}")
        except Exception as e:
            logger.error(f"Database connection pool initialization failed: {str(e)}")
            raise

    async def get_connection(self):
        """获取数据库连接"""
        if self._pool is None:
            await self._initialize()

        try:
            conn = await self._pool.acquire()
            logger.debug("从PostgreSQL连接池获取连接成功")
            return conn
        except Exception as e:
            logger.error(f"从PostgreSQL连接池获取连接失败: {str(e)}")
            raise

    async def release_connection(self, conn):
        """释放数据库连接回连接池"""
        if self._pool is None:
            logger.warning("PostgreSQL连接池不存在，无法释放连接")
            return

        try:
            self._pool.release(conn)
            logger.debug("释放连接回PostgreSQL连接池成功")
        except Exception as e:
            logger.error(f"释放连接回PostgreSQL连接池失败: {str(e)}")

    async def close_pool(self):
        """关闭连接池"""
        if self._pool is None:
            logger.warning("PostgreSQL连接池不存在，无需关闭")
            return

        try:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
            logger.info("PostgreSQL连接池已关闭")
        except Exception as e:
            logger.error(f"关闭PostgreSQL连接池失败: {str(e)}")


# 导出连接池获取函数
async def get_db_pool():
    """获取数据库连接池实例"""
    return await DatabasePool.get_instance()

if __name__ == "__main__":
    # 测试连接池
    async def test_pool():
        db_pool = await get_db_pool()
        conn = await db_pool.get_connection()
        await db_pool.release_connection(conn)
        await db_pool.close_pool()
        
    asyncio.run(test_pool())