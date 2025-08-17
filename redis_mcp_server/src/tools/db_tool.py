"""
Database Utility Functions

Provides database utility functions related to SQL execution.
"""
from src.utils.db_operate import execute_command
from src.utils.logger_util import logger
import random, string


async def generate_test_data(table, columns, num):
    """生成Redis测试数据"""
    logger.info(f"Starting to generate {num} test records for Redis table '{table}'")
    logger.debug(f"Target {table} columns: {columns}")

    for i in range(num):
        # 生成记录ID
        record_id = str(i + 1)
        key = f"table:{table}:{record_id}"

        # 生成字段数据
        record_data = {}
        for col in columns:
            # 简单示例：全部用8位随机字符串
            random_value = ''.join(random.choices(string.ascii_letters, k=8))
            record_data[col] = random_value

        # 使用Redis HSET命令存储记录
        await execute_command("HSET", key, mapping=record_data)

        logger.debug(f"Inserting row {i + 1}/{num}: {record_data}")

    logger.info(f"Successfully generated {num} test records for Redis table '{table}'")


async def get_redis_server_info():
    """获取Redis服务器基本信息"""
    logger.info("=== Redis服务器信息 ===")

    try:
        # 获取服务器信息
        info = await execute_command('INFO', 'server')
        logger.info("服务器信息:")
        for key, value in info.items():
            if key in ['redis_version', 'redis_mode', 'os', 'arch_bits', 'uptime_in_seconds', 'uptime_in_days']:
                logger.info(f"  {key}: {value}")

        return info
    except Exception as e:
        logger.error(f"获取服务器信息失败: {e}")
        return {}


async def get_redis_memory_info():
    """获取Redis内存使用信息"""
    logger.info("=== Redis内存信息 ===")

    try:
        info = await execute_command('INFO', 'memory')
        logger.info("内存使用情况:")
        for key, value in info.items():
            if key in ['used_memory_human', 'used_memory_peak_human', 'used_memory_rss_human', 'maxmemory_human']:
                logger.info(f"  {key}: {value}")

        return info
    except Exception as e:
        logger.error(f"获取内存信息失败: {e}")
        return {}


async def get_redis_clients_info():
    """获取Redis客户端连接信息"""
    logger.info("=== Redis客户端信息 ===")

    try:
        info = await execute_command('INFO', 'clients')
        logger.info("客户端连接情况:")
        for key, value in info.items():
            if key in ['connected_clients', 'client_recent_max_input_buffer', 'client_recent_max_output_buffer']:
                logger.info(f"  {key}: {value}")

        return info
    except Exception as e:
        logger.error(f"获取客户端信息失败: {e}")
        return {}


async def get_redis_stats_info():
    """获取Redis统计信息"""
    logger.info("=== Redis统计信息 ===")

    try:
        info = await execute_command('INFO', 'stats')
        logger.info("操作统计:")
        for key, value in info.items():
            if key in ['total_connections_received', 'total_commands_processed', 'instantaneous_ops_per_sec',
                       'keyspace_hits', 'keyspace_misses']:
                logger.info(f"  {key}: {value}")

        return info
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return {}


async def get_database_info():
    """获取数据库信息"""
    logger.info("=== 数据库信息 ===")

    try:
        # 获取当前数据库大小
        dbsize = await execute_command('DBSIZE')
        logger.info(f"当前数据库键数量: {dbsize}")

        # 获取数据库键空间信息
        info = await execute_command('INFO', 'keyspace')
        logger.info("键空间信息:")
        for key, value in info.items():
            if key.startswith('db'):
                logger.info(f"  {key}: {value}")

        return {"dbsize": dbsize, "keyspace": info}
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        return {}


async def get_keys_sample():
    """获取键样本信息"""
    logger.info("=== 键样本信息 ===")

    try:
        # 获取所有键（注意：在生产环境中要小心使用KEYS *）
        all_keys = await execute_command('KEYS', '*')
        total_keys = len(all_keys)
        logger.info(f"总键数: {total_keys}")

        if total_keys > 0:
            # 显示前10个键作为样本
            sample_keys = all_keys[:10]
            logger.info("键样本（前10个）:")
            for i, key in enumerate(sample_keys, 1):
                key_type = await execute_command('TYPE', key)
                ttl = await execute_command('TTL', key)
                ttl_info = f"TTL: {ttl}s" if ttl > 0 else "无过期时间" if ttl == -1 else "已过期"
                logger.info(f"  {i}. {key} (类型: {key_type}, {ttl_info})")

        return {"total_keys": total_keys, "sample_keys": all_keys[:10]}
    except Exception as e:
        logger.error(f"获取键信息失败: {e}")
        return {}


async def get_key_types_distribution():
    """获取键类型分布"""
    logger.info("=== 键类型分布 ===")

    try:
        all_keys = await execute_command('KEYS', '*')
        type_count = {}

        for key in all_keys:
            key_type = await execute_command('TYPE', key)
            type_count[key_type] = type_count.get(key_type, 0) + 1

        logger.info("键类型分布:")
        for key_type, count in type_count.items():
            logger.info(f"  {key_type}: {count}")

        return type_count
    except Exception as e:
        logger.error(f"获取键类型分布失败: {e}")
        return {}


async def get_config_info():
    """获取Redis配置信息"""
    logger.info("=== Redis配置信息 ===")

    try:
        # 获取一些重要的配置项
        important_configs = [
            'maxmemory', 'maxmemory-policy', 'timeout', 'databases',
            'save', 'appendonly', 'appendfsync'
        ]

        config_info = {}
        for config_key in important_configs:
            try:
                config_value = await execute_command('CONFIG', 'GET', config_key)
                if config_value and len(config_value) >= 2:
                    config_info[config_key] = config_value[1]
                    logger.info(f"  {config_key}: {config_value[1]}")
            except Exception as e:
                logger.debug(f"获取配置 {config_key} 失败: {e}")

        return config_info
    except Exception as e:
        logger.error(f"获取配置信息失败: {e}")
        return {}