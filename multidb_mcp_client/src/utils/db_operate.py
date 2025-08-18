"""
数据库操作模块

提供支持HTTP代理的数据库操作函数。
"""

import json
from typing import Any, Dict, Optional

from .db_config import load_activate_db_config
from .http_util import http_post
from .logger_util import logger

async def execute_sql(sql: str, params: Optional[Dict] = None) -> Any:
    """执行SQL语句（异步版本，使用远程HTTP调用）"""

    # 加载活跃数据库配置
    active_db, config = load_activate_db_config()

    # 远程服务器的API端点
    url = config.multidb_server

    # 准备请求数据，将数据库实例转换为字典
    active_db_dict = {
        "dbInstanceId": active_db.db_instance_id,
        "dbHost": active_db.db_host,
        "dbPort": active_db.db_port,
        "dbDatabase": active_db.db_database,
        "dbUsername": active_db.db_username,
        "dbPassword": active_db.db_password,
        "dbType": active_db.db_type,
        "dbActive": active_db.db_active
    }

    data = {
        "sql": sql,
        "params": params,
        "databaseInstance": active_db_dict
    }

    json_str=json.dumps(data, indent=4)
    logger.debug(f"准备通过HTTP POST执行远程SQL到 {url}，数据: {json_str}")

    try:
        response = await http_post(url, data=data)
        logger.info(f"远程SQL执行成功，结果: {response}")
        return response.get("result", [])
    except Exception as e:
        logger.error(f"远程SQL执行失败: {e}")
        raise