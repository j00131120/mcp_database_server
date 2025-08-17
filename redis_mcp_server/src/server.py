
"""
MCP NoSQL Server

Main entry point for Redis MCP Client server.
"""
import os
import sys
from mcp.server.fastmcp.server import FastMCP
from src.resources.db_resources import generate_database_config, get_connection_status
from src.tools.db_tool import generate_test_data, get_redis_server_info, get_redis_memory_info, get_redis_clients_info, \
    get_redis_stats_info, get_database_info, get_keys_sample, get_key_types_distribution, get_config_info
from src.utils.db_operate import execute_command

project_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add current directory to Python module search path
sys.path.insert(0,project_path)
from src.utils.logger_util import logger, db_config_path
from src.utils import load_activate_redis_config
# Create global MCP server instance
mcp = FastMCP("Redis MCP Client Server")


@mcp.tool()
async def redis_exec(command: str, args: list = None):
    """
    执行Redis命令

    Args:
        command: Redis命令名称，如 'GET', 'SET', 'HGET' 等
        args: 命令参数列表，如 ['key'] 或 ['key', 'value']

    Examples:
        redis_exec('GET', ['mykey'])
        redis_exec('SET', ['mykey', 'myvalue'])
        redis_exec('HGET', ['myhash', 'field'])

    Returns:
        dict: 包含执行结果的字典
    """
    if args is None:
        args = []

    logger.info(f"执行Redis命令: {command} {args}")
    try:
        result = await execute_command(command, *args)
        logger.info(f"Redis命令执行成功")
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Redis命令执行失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def gen_test_data(table: str, columns: list, num: int = 10):
    """
    自动生成测试数据

    Args:
        table: 表名
        columns: 列名列表
        num: 生成的记录数量，默认10条

    Returns:
        dict: 包含成功状态和消息的字典
    """
    logger.info(f"正在为表 {table} 生成 {num} 条测试数据，字段: {columns}")

    try:
        await generate_test_data(table, columns, num)
        logger.info(f"成功为 {table} 生成 {num} 条数据")
        return {"success": True, "msg": f"Generated {num} rows for {table}"}
    except Exception as e:
        logger.error(f"生成测试数据失败: {e}")
        return {"success": False, "error": str(e)}


# ==================== Redis 获取resource信息 ====================

@mcp.resource("database://config")
async def get_database_config_resource():
    """
    获取数据库配置信息（隐藏敏感信息）
    """
    logger.info("获取数据库配置信息")

    try:
        safe_config = await generate_database_config()
        return {
            "uri": "database://config",
            "mimeType": "application/json",
            "text": str(safe_config)
        }
    except Exception as e:
        logger.error(f"获取数据库配置失败: {e}")
        return {
            "uri": "database://config",
            "mimeType": "application/json",
            "text": f'{{"error": "{str(e)}"}}'
        }


@mcp.resource("database://status")
async def get_database_status_resource():
    """
    获取数据库连接状态
    """
    logger.info("获取数据库状态")

    try:
        connection_status = get_connection_status()
        return {
            "uri": "database://status",
            "mimeType": "application/json",
            "text": str(connection_status)
        }
    except Exception as e:
        logger.error(f"获取数据库状态失败: {e}")
        return {
            "uri": "database://status",
            "mimeType": "application/json",
            "text": f'{{"error": "{str(e)}"}}'
        }


# ==================== Redis信息获取工具 ====================

@mcp.tool()
async def get_server_info():
    """
    获取Redis服务器基本信息

    Returns:
        dict: 包含Redis服务器信息的字典
    """
    logger.info("获取Redis服务器信息")

    try:
        info = await get_redis_server_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取服务器信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_memory_info():
    """
    获取Redis内存使用信息

    Returns:
        dict: 包含Redis内存使用信息的字典
    """
    logger.info("获取Redis内存信息")

    try:
        info = await get_redis_memory_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取内存信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_clients_info():
    """
    获取Redis客户端连接信息

    Returns:
        dict: 包含Redis客户端连接信息的字典
    """
    logger.info("获取Redis客户端信息")

    try:
        info = await get_redis_clients_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取客户端信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_stats_info():
    """
    获取Redis统计信息

    Returns:
        dict: 包含Redis统计信息的字典
    """
    logger.info("获取Redis统计信息")

    try:
        info = await get_redis_stats_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_db_info():
    """
    获取Redis数据库信息

    Returns:
        dict: 包含Redis数据库信息的字典
    """
    logger.info("获取Redis数据库信息")

    try:
        info = await get_database_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_keys_info():
    """
    获取Redis键样本信息

    Returns:
        dict: 包含Redis键样本信息的字典
    """
    logger.info("获取Redis键样本信息")

    try:
        info = await get_keys_sample()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取键信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_key_types():
    """
    获取Redis键类型分布统计

    Returns:
        dict: 包含Redis键类型分布的字典
    """
    logger.info("获取Redis键类型分布")

    try:
        info = await get_key_types_distribution()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取键类型分布失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_redis_config():
    """
    获取Redis配置信息

    Returns:
        dict: 包含Redis配置信息的字典
    """
    logger.info("获取Redis配置信息")

    try:
        info = await get_config_info()
        return {"success": True, "data": info}
    except Exception as e:
        logger.error(f"获取配置信息失败: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_redis_overview():
    """
    获取Redis完整概览信息（包含所有监控信息）

    Returns:
        dict: 包含Redis完整概览信息的字典
    """
    logger.info("获取Redis完整概览信息")

    try:
        overview = {}

        # 获取所有信息
        overview['server'] = await get_redis_server_info()
        overview['memory'] = await get_redis_memory_info()
        overview['clients'] = await get_redis_clients_info()
        overview['stats'] = await get_redis_stats_info()
        overview['database'] = await get_database_info()
        overview['keys_sample'] = await get_keys_sample()
        overview['key_types'] = await get_key_types_distribution()
        overview['config'] = await get_config_info()

        return {"success": True, "data": overview}
    except Exception as e:
        logger.error(f"获取Redis概览信息失败: {e}")
        return {"success": False, "error": str(e)}

# ==================== Server Startup Related ====================

# When using fastmcp run, FastMCP CLI automatically handles server startup
# No need to manually call mcp.run() or handle stdio

def main():
    """Main function: Start MCP server"""
    logger.info(f"Database configuration file path:{db_config_path}")
    logger.info(f"Current project path:{project_path}")
    logger.info("Xesql/Mysql/Ubisql DataSource MCP Client server is ready to accept connections")

    active_db, _ = load_activate_redis_config()
    logger.info(f"Current database instance configuration: {active_db}")
    # When using fastmcp run, just call mcp.run() directly
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
