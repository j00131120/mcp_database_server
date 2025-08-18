"""
数据库工具函数

提供SQL执行相关的数据库实用函数。
"""

import random
import string

from src.utils import execute_sql, logger


async def sql_exec(sql: str):
    """
    执行任意SQL语句（SELECT/INSERT/UPDATE/DELETE）
    """
    logger.info(f"执行SQL: {sql}")
    try:
        result = await execute_sql(sql)
        logger.info(f"SQL执行成功，返回 {len(result) if isinstance(result, list) else result} 行/影响行数")
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"SQL执行失败: {e}")
        return {"success": False, "error": str(e)}
