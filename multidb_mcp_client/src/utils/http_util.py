"""
HTTP工具模块

提供异步HTTP GET和POST请求函数。
"""

import asyncio
from typing import Dict, Optional

import aiohttp

from .logger_util import logger

async def http_get(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Dict:
    """
    异步执行HTTP GET请求
    """
    logger.info(f"执行GET请求到 {url}，参数: {params}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error(f"GET请求失败: {e}")
        raise

async def http_post(url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict] = None) -> Dict:
    """
    异步执行HTTP POST请求
    """
    logger.info(f"执行POST请求到 {url}，数据: {data}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error(f"POST请求失败: {e}")
        raise