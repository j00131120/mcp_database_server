"""
Database Operations Module

Provides database operation functions with HTTP proxy support.
"""

from src.utils.db_pool import get_redis_pool
from src.utils.logger_util import logger
from typing import Any, Dict, List, Optional, Union, Tuple

async def get_redis_connection():
    """从Redis连接池获取连接"""
    try:
        pool = await get_redis_pool()
        redis_client = await pool.get_redis()
        return redis_client
    except Exception as e:
        logger.error(f"从Redis连接池获取连接失败: {e}")
        raise


async def get_redis_status():
    """从Redis连接池获取连接"""
    try:
        pool = await get_redis_pool()
        return pool.health_check()
    except Exception as e:
        logger.error(f"从Redis连接池获取连接失败: {e}")
        raise


async def execute_command(command: str, *args, **kwargs) -> Any:
    """
    执行任何Redis命令（异步版本，使用连接池）

    Args:
        command: Redis命令名称（如 'SET', 'GET', 'HSET' 等）
        *args: 命令参数
        **kwargs: 命令关键字参数

    Returns:
        Any: Redis命令执行结果

    Examples:
        # 字符串操作
        await execute_command('SET', 'key1', 'value1')
        await execute_command('GET', 'key1')
        await execute_command('SETEX', 'key2', 60, 'value2')

        # 哈希操作
        await execute_command('HSET', 'hash1', 'field1', 'value1')
        await execute_command('HGET', 'hash1', 'field1')
        await execute_command('HGETALL', 'hash1')

        # 列表操作
        await execute_command('LPUSH', 'list1', 'item1', 'item2')
        await execute_command('LRANGE', 'list1', 0, -1)

        # 集合操作
        await execute_command('SADD', 'set1', 'member1', 'member2')
        await execute_command('SMEMBERS', 'set1')

        # 有序集合操作
        await execute_command('ZADD', 'zset1', {'member1': 1.0, 'member2': 2.0})
        await execute_command('ZRANGE', 'zset1', 0, -1, withscores=True)

        # 通用操作
        await execute_command('KEYS', '*')
        await execute_command('EXISTS', 'key1')
        await execute_command('DEL', 'key1', 'key2')
        await execute_command('EXPIRE', 'key1', 60)
        await execute_command('TTL', 'key1')

        # 事务操作
        await execute_command('MULTI')
        await execute_command('EXEC')

        # 发布订阅
        await execute_command('PUBLISH', 'channel1', 'message')

        # 服务器信息
        await execute_command('INFO')
        await execute_command('PING')
    """
    logger.debug(f"准备执行Redis命令: {command} {args} {kwargs}")

    try:
        redis_client = await get_redis_connection()

        # 将命令名转换为小写
        command_lower = command.lower()

        # 检查Redis客户端是否有该命令方法
        if hasattr(redis_client, command_lower):
            cmd_method = getattr(redis_client, command_lower)

            # 执行命令
            if kwargs:
                # 如果有关键字参数，同时传递位置参数和关键字参数
                result = await cmd_method(*args, **kwargs)
            else:
                # 只有位置参数
                result = await cmd_method(*args)

            logger.debug(f"Redis命令执行成功，返回类型: {type(result)}")

            # 记录成功执行的命令（截断长参数以避免日志过长）
            args_str = str(args)[:200] + ('...' if len(str(args)) > 200 else '')
            kwargs_str = str(kwargs)[:200] + ('...' if len(str(kwargs)) > 200 else '')
            logger.info(f"Redis命令执行成功: {command} {args_str} {kwargs_str}")

            return result

        else:
            # 如果没有找到对应的方法，尝试使用execute_command方法
            try:
                # 使用Redis的原生execute_command方法
                result = await redis_client.execute_command(command.upper(), *args)
                logger.info(f"通过execute_command执行Redis命令成功: {command} {args}")
                return result
            except Exception as e:
                logger.error(f"不支持的Redis命令: {command}, 错误: {e}")
                raise AttributeError(f"不支持的Redis命令: {command}")

    except Exception as e:
        logger.error(f"Redis命令执行失败: {command} {args} {kwargs}, 错误: {e}")
        raise


async def execute_raw_command(command_string: str) -> Any:
    """
    执行原始Redis命令字符串

    Args:
        command_string: 完整的Redis命令字符串，如 "SET key1 value1"

    Returns:
        Any: Redis命令执行结果

    Examples:
        await execute_raw_command("SET key1 value1")
        await execute_raw_command("GET key1")
        await execute_raw_command("HSET hash1 field1 value1")
        await execute_raw_command("KEYS *")
    """
    logger.debug(f"准备执行原始Redis命令: {command_string}")

    try:
        # 简单的命令字符串解析（处理引号）
        import shlex
        parts = shlex.split(command_string.strip())
        if not parts:
            raise ValueError("命令字符串不能为空")

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        # 执行命令
        return await execute_command(command, *args)

    except Exception as e:
        logger.error(f"原始Redis命令执行失败: {command_string}, 错误: {e}")
        raise


async def execute_pipeline_commands(commands: List[Tuple[str, tuple, dict]]) -> List[Any]:
    """
    使用管道批量执行Redis命令

    Args:
        commands: 命令列表，每个元素为 (command, args, kwargs) 元组

    Returns:
        List[Any]: 所有命令的执行结果列表

    Examples:
        commands = [
            ('SET', ('key1', 'value1'), {}),
            ('SET', ('key2', 'value2'), {}),
            ('GET', ('key1',), {}),
            ('GET', ('key2',), {})
        ]
        results = await execute_pipeline_commands(commands)
    """
    logger.debug(f"准备执行管道命令，共 {len(commands)} 个命令")

    try:
        redis_client = await get_redis_connection()

        # 创建管道
        pipe = redis_client.pipeline()

        # 添加命令到管道
        for command, args, kwargs in commands:
            command_lower = command.lower()
            if hasattr(pipe, command_lower):
                cmd_method = getattr(pipe, command_lower)
                if kwargs:
                    cmd_method(*args, **kwargs)
                else:
                    cmd_method(*args)
            else:
                # 使用原生命令
                pipe.execute_command(command.upper(), *args)

        # 执行管道
        results = await pipe.execute()

        logger.info(f"管道命令执行成功，共 {len(commands)} 个命令")
        return results

    except Exception as e:
        logger.error(f"管道命令执行失败: {e}")
        raise


# 追加常用 Redis 操作的简易封装
async def redis_set(key, value):
    return await execute_command('SET', key, value)


async def redis_get(key):
    return await execute_command('GET', key)


async def redis_hset(name, key, value):
    return await execute_command('HSET', name, key, value)


async def redis_hgetall(name):
    result = await execute_command('HGETALL', name)
    # redis.asyncio 返回 dict，部分驱动可能返回 list/str，需兼容
    if isinstance(result, dict):
        return result
    elif isinstance(result, list):
        # 转换为 dict
        return dict(zip(result[::2], result[1::2]))
    elif isinstance(result, str):
        # 空 hash 时可能返回空字符串
        return {}
    else:
        raise TypeError(f"Unexpected HGETALL result type: {type(result)}")


if __name__ == "__main__":
    import asyncio


    async def main():
        """主测试函数"""


    # 运行测试
    asyncio.run(main())