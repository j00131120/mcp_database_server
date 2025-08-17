from src.utils.db_pool import get_db_pool
from src.utils.logger_util import logger
import asyncpg

async def get_pooled_connection():
    """从连接池获取数据库连接"""
    try:
        pool = await get_db_pool()
        conn = await pool.get_connection()
        return conn
    except Exception as e:
        logger.error(f"从PostgreSQL连接池获取连接失败: {e}")
        raise
async def execute_sql(sql, params=None):
    """执行SQL语句（异步版本，使用连接池）"""
    conn = None
    logger.debug(f"准备执行异步SQL: {sql}")
    try:
        logger.debug("正在获取PostgreSQL连接池连接...")
        conn = await get_pooled_connection()

        # 执行SQL
        logger.debug("正在执行异步SQL查询...")

        # 处理不同类型的SQL语句
        sql_lower = sql.strip().lower()
        if sql_lower.startswith(("select", "show", "describe", "desc")):
            # 对于查询语句，返回结果集
            if params:
                result = await conn.fetch(sql, *params)
            else:
                result = await conn.fetch(sql)
            # 将 asyncpg.Record 转换为字典列表以保持兼容性
            result = [dict(row) for row in result]
            logger.debug(f"异步查询返回 {len(result)} 行数据")
        elif sql_lower.startswith(("insert", "update", "delete")):
            # 对于修改语句，返回影响的行数
            if params:
                result = await conn.execute(sql, *params)
            else:
                result = await conn.execute(sql)
            # 从返回的状态字符串中提取行数（如 "UPDATE 5"）
            if isinstance(result, str) and ' ' in result:
                try:
                    result = int(result.split()[-1])
                except (ValueError, IndexError):
                    result = 0
            logger.debug(f"异步查询影响了 {result} 行数据")
        else:
            # 对于其他语句（如CREATE, DROP等）
            if params:
                await conn.execute(sql, *params)
            else:
                await conn.execute(sql)
            result = "Query executed successfully"
            logger.debug("异步DDL查询执行成功")

        logger.info(f"异步SQL执行成功: {sql[:200]}{'...' if len(sql) > 50 else ''}")
        return result

    except Exception as e:
        logger.error(f"异步SQL执行失败: {e}")
        logger.debug(f"失败的异步SQL: {sql}")
        raise
    finally:
        if conn:
            pool = await get_db_pool()
            await pool.release_connection(conn)
            logger.debug("异步连接已释放回连接池")