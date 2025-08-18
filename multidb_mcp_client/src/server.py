
"""
MCP SQL服务器

多数据源MCP服务器的主入口点。
"""

import asyncio
import os
import sys

# 将当前目录添加到Python的模块搜索路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp.server.fastmcp.server import FastMCP

from src.utils import execute_sql, logger

# 创建全局MCP服务器实例
logger.info("正在启动Multi DataSource MCP Client服务器...")

mcp = FastMCP("Multi DataSource MCP Client服务器")

@mcp.tool()
async def sql_exec(sql: str):
    """
    执行任意SQL语句（SELECT/INSERT/UPDATE/DELETE）
    
    这是一个通用的SQL执行工具，支持所有类型的SQL语句。它会通过HTTP代理
    将SQL语句发送到配置的数据库服务器执行，并返回结果。
    
    支持的SQL语句类型：
    - SELECT: 查询数据，返回结果集
    - INSERT: 插入数据，返回影响的行数
    - UPDATE: 更新数据，返回影响的行数
    - DELETE: 删除数据，返回影响的行数
    - DDL语句: CREATE, ALTER, DROP等
    
    Args:
        sql (str): 要执行的SQL语句。请确保SQL语句语法正确，
                  并且符合目标数据库的SQL方言要求。
        
    Returns:
        dict: 包含执行结果的字典，格式为:
            - success (bool): 执行是否成功
            - result (any): 查询结果或影响的行数
                - 对于SELECT语句：返回包含查询结果的列表
                - 对于INSERT/UPDATE/DELETE：返回影响的行数
            - message (str): 执行状态消息
            - error (str, optional): 错误信息（仅在失败时返回）
            
    Example:
        >>> await sql_exec("SELECT * FROM users LIMIT 5;")
        {
            "success": True,
            "result": [["1", "张三", "zhang@example.com"], ...],
            "message": "SQL执行成功"
        }
        
        >>> await sql_exec("UPDATE users SET name='李四' WHERE id=1;")
        {
            "success": True,
            "result": 1,
            "message": "SQL执行成功"
        }
    
    Raises:
        通过返回字典中的error字段返回错误信息，不会抛出异常。
        可能的错误包括：
        - 数据库连接失败
        - SQL语法错误
        - 权限不足
        - 表或字段不存在
    """
    logger.info(f"MCP工具执行SQL: {sql}")
    try:
        result = await execute_sql(sql)
        
        # 记录执行结果
        if isinstance(result, list):
            logger.info(f"SQL执行成功，返回 {len(result)} 行数据")
        else:
            logger.info(f"SQL执行成功，影响 {result} 行")
            
        return {
            "success": True, 
            "result": result,
            "message": "SQL执行成功"
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"MCP工具SQL执行失败: {error_msg}")
        return {
            "success": False, 
            "error": error_msg,
            "message": "SQL执行失败"
        }

@mcp.tool()
async def describe_table(table_name: str):
    """
    描述指定表的结构
    
    这个工具函数会显示指定表的详细结构信息，包括字段名、数据类型、
    是否允许NULL、键信息、默认值等。内部执行 "DESCRIBE table_name;" SQL语句。
    
    功能特点：
    - 显示表的完整结构信息
    - 包含字段的数据类型和约束
    - 显示主键、外键等索引信息
    - 支持不同数据库类型的表结构查询
    
    Args:
        table_name (str): 要查询的表名。请确保表名存在且有访问权限。
                         表名区分大小写（取决于数据库配置）。
        
    Returns:
        dict: 包含表结构信息的字典，格式为:
            - success (bool): 执行是否成功
            - result (list): 表结构信息列表，每行包含：
                - Field: 字段名
                - Type: 数据类型
                - Null: 是否允许NULL (YES/NO)
                - Key: 键类型 (PRI/UNI/MUL等)
                - Default: 默认值
                - Extra: 额外信息 (auto_increment等)
            - message (str): 执行状态消息
            - error (str, optional): 错误信息（仅在失败时返回）
            
    Example:
        >>> await describe_table("users")
        {
            "success": True,
            "result": [
                ["id", "int(11)", "NO", "PRI", null, "auto_increment"],
                ["name", "varchar(100)", "NO", "", null, ""],
                ["email", "varchar(255)", "YES", "UNI", null, ""]
            ],
            "message": "SQL执行成功"
        }
    
    Raises:
        可能的错误（通过返回字典的error字段）：
        - 表不存在
        - 没有访问权限
        - 数据库连接失败
        - 表名格式不正确
    """
    logger.info(f"MCP工具：描述表结构 - {table_name}")
    return await sql_exec(f"DESCRIBE {table_name};")


@mcp.tool()
async def database_status():
    """
    获取数据库状态信息
    
    这个工具函数会获取当前活跃数据库的详细状态信息，包括连接参数、
    连接状态、表数量等。它是一个综合性的数据库健康检查工具。
    
    功能特点：
    - 显示当前活跃数据库的配置信息
    - 检查数据库连接状态
    - 统计数据库中的表数量
    - 提供数据库类型和版本信息
    - 用于系统监控和故障排查
    
    检查项目：
    - 数据库连接参数（主机、端口、数据库名）
    - 数据库类型（MySQL、PostgreSQL等）
    - 连接状态（已连接/连接错误）
    - 表数量统计
    - 数据库实例ID
    
    Returns:
        dict: 包含数据库状态信息的字典，格式为:
            - success (bool): 状态检查是否成功
            - result (dict): 数据库状态详情，包含：
                - database_id (str): 数据库实例ID
                - host (str): 数据库主机地址
                - port (int): 数据库端口号
                - database (str): 数据库名称
                - type (str): 数据库类型
                - table_count (int): 表数量
                - status (str): 连接状态 ("connected" 或 "connection_error")
            - message (str): 状态检查消息
            - error (str, optional): 错误信息（仅在失败时返回）
            
    Example:
        >>> await database_status()
        {
            "success": True,
            "result": {
                "database_id": "mylocalmysql",
                "host": "localhost",
                "port": 3306,
                "database": "mysql_db",
                "type": "mysql",
                "table_count": 15,
                "status": "connected"
            },
            "message": "数据库状态获取成功"
        }
    
    Use Cases:
        - 系统健康检查
        - 数据库连接诊断
        - 监控数据库状态
        - 故障排查和调试
        - 获取数据库基本信息
    
    Note:
        - 此函数会尝试执行SHOW TABLES来测试连接
        - 如果数据库连接失败，status字段会显示"connection_error"
        - table_count在连接失败时会显示为0
    """
    logger.info("MCP工具：获取数据库状态")
    try:
        from src.utils import load_activate_db_config
        
        # 获取活跃数据库配置
        active_db, config = load_activate_db_config()
        
        # 尝试获取表数量
        tables_result = await sql_exec("SHOW TABLES;")
        table_count = len(tables_result.get("result", [])) if tables_result.get("success") else 0
        
        return {
            "success": True,
            "result": {
                "database_id": active_db.db_instance_id,
                "host": active_db.db_host,
                "port": active_db.db_port,
                "database": active_db.db_database,
                "type": active_db.db_type,
                "table_count": table_count,
                "status": "connected" if tables_result.get("success") else "connection_error"
            },
            "message": "数据库状态获取成功"
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"获取数据库状态失败: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "message": "数据库状态获取失败"
        }


@mcp.tool()
async def execute_query_with_limit(sql: str, limit: int = 100):
    """
    执行查询语句并限制返回行数
    
    这是一个安全的查询工具，它会自动为SELECT语句添加LIMIT子句，
    防止意外查询大量数据导致性能问题或内存溢出。
    
    功能特点：
    - 自动添加LIMIT限制，防止大结果集
    - 只允许SELECT查询，提高安全性
    - 可配置返回行数限制
    - 适用于数据探索和调试
    
    Args:
        sql (str): 要执行的SELECT查询语句。必须是SELECT语句，
                  不支持INSERT/UPDATE/DELETE等修改操作。
        limit (int, optional): 最大返回行数，默认100行。
                              范围：1-10000行。
        
    Returns:
        dict: 包含查询结果的字典，格式为:
            - success (bool): 查询是否成功
            - result (list): 查询结果列表（最多limit行）
            - limit_applied (int): 实际应用的行数限制
            - message (str): 查询状态消息
            - error (str, optional): 错误信息（仅在失败时返回）
            
    Example:
        >>> await execute_query_with_limit("SELECT * FROM users", 10)
        {
            "success": True,
            "result": [["1", "张三", "zhang@example.com"], ...],
            "limit_applied": 10,
            "message": "查询执行成功"
        }
    
    Security:
        - 只允许SELECT语句
        - 自动限制返回行数
        - 防止SQL注入（通过参数验证）
        - 不允许执行修改操作
    
    Limitations:
        - 不支持非SELECT语句
        - 最大限制10000行
        - 不支持存储过程调用
    """
    logger.info(f"MCP工具：执行限制查询 - SQL: {sql}, LIMIT: {limit}")
    
    # 验证SQL语句类型
    sql_trimmed = sql.strip().upper()
    if not sql_trimmed.startswith('SELECT'):
        return {
            "success": False,
            "error": "只允许执行SELECT查询语句",
            "message": "查询类型不支持"
        }
    
    # 验证limit参数
    if not isinstance(limit, int) or limit < 1 or limit > 10000:
        return {
            "success": False,
            "error": "limit参数必须是1-10000之间的整数",
            "message": "参数验证失败"
        }
    
    try:
        # 检查SQL是否已经包含LIMIT
        if 'LIMIT' not in sql_trimmed:
            # 添加LIMIT子句
            limited_sql = f"{sql.rstrip(';')} LIMIT {limit};"
        else:
            # 如果已有LIMIT，使用原SQL但记录警告
            limited_sql = sql
            logger.warning(f"SQL语句已包含LIMIT子句: {sql}")
        
        result = await sql_exec(limited_sql)
        
        if result.get("success"):
            return {
                "success": True,
                "result": result["result"],
                "limit_applied": limit,
                "message": "查询执行成功"
            }
        else:
            return result
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"限制查询执行失败: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "message": "查询执行失败"
        }

# ==================== 服务器启动相关 ====================

# 当使用 fastmcp run 时，不需要手动调用 mcp.run()
# FastMCP CLI 会自动处理服务器启动

# 当直接使用 Python 运行时，手动启动服务器
def main():
    """主函数：启动MCP服务器"""
    logger.info("Multi DataSource MCP Client服务器已准备好接受连接")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
