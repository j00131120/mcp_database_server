from src.utils.db_config import load_activate_redis_config
from src.utils.db_operate import execute_command
from src.utils.logger_util import logger


async def get_connection_status() -> dict:
    """测试Redis连接"""
    logger.info("=== 连接测试 ===")

    try:
        # 测试PING命令
        ping_result = await execute_command('PING')
        logger.info(f"PING测试: {ping_result}")

        # 测试简单的SET/GET操作
        await execute_command('SET', 'test:connection', 'ok')
        get_result = await execute_command('GET', 'test:connection')
        logger.info(f"SET/GET测试: {get_result}")

        # 清理测试键
        await execute_command('DEL', 'test:connection')

        return {"ping": ping_result, "set_get": get_result}
    except Exception as e:
        logger.error(f"连接测试失败: {e}")
        return {"error": str(e)}

async def generate_database_config():

    active_redis, redis_config = load_activate_redis_config()

    # 隐藏敏感信息
    safe_config = {
        "redisInstanceId": active_redis.redis_instance_id,
        "redisType": active_redis.redis_type,
        "host": active_redis.redis_host,
        "port": active_redis.redis_port,
        "database": active_redis.redis_database,
        "password": "***hidden***" if active_redis.redis_password else None,
        "ssl": active_redis.redis_ssl,
        "pool_size": redis_config.redis_pool_size,
        "max_connections": redis_config.redis_max_connections,
        "connection_timeout": redis_config.redis_connection_timeout,
    }
    logger.info("成功获取Redis配置信息")
    logger.info(f"Redis配置: {safe_config}")
    return safe_config