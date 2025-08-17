# PostgreSQL MCP 服务器

<div align="center">

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.6-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-2.11.3+-orange.svg)

**面向PostgreSQL数据库的高性能模型上下文协议(MCP)服务器**

[功能特色](#-功能特色) • [安装说明](#️-安装说明) • [快速开始](#-快速开始) • [API参考](#-api参考) • [配置说明](#️-配置说明)

</div>

---

## 📖 目录

- [概述](#-概述)
- [功能特色](#-功能特色)
- [系统要求](#-系统要求)
- [安装说明](#️-安装说明)
- [快速开始](#-快速开始)
- [API参考](#-api参考)
- [配置说明](#️-配置说明)
- [系统架构](#️-系统架构)
- [安全性](#-安全性)
- [测试](#-测试)
- [问题排查](#-问题排查)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## 🔍 概述

PostgreSQL MCP服务器是一个健壮、生产就绪的模型上下文协议服务器，提供与PostgreSQL数据库的安全高效交互。采用现代Python异步/等待模式构建，针对高性能数据库操作进行了优化。

### 什么是MCP？

模型上下文协议（MCP）是一个开放标准，使AI模型能够安全连接到外部数据源和工具。本服务器实现了MCP协议，为AI模型提供对PostgreSQL数据库的直接、受控访问。

## ✨ 功能特色

### 🚀 **核心能力**
- **MCP协议支持**：使用FastMCP框架完全符合MCP规范
- **PostgreSQL优化**：使用`asyncpg`驱动原生支持PostgreSQL
- **异步架构**：高性能异步/等待实现
- **连接池管理**：智能连接管理，支持可配置的池设置

### 🔧 **数据库操作**
- **通用SQL执行**：支持SELECT、INSERT、UPDATE、DELETE、DDL操作
- **表结构查询**：详细的模式信息检索
- **测试数据生成**：内置的示例数据生成工具
- **参数化查询**：安全的参数绑定，防止SQL注入

### 🛡️ **安全与保护**
- **查询类型限制**：可配置的查询执行控制
- **参数验证**：全面的输入验证
- **密码保护**：安全的凭据处理
- **连接隔离**：基于实例的访问控制

### 📊 **监控与日志**
- **结构化日志**：详细的操作日志，支持可配置级别
- **连接池监控**：实时池状态跟踪
- **错误处理**：全面的错误报告和恢复

## 📋 系统要求

- **Python**：3.12或更高版本
- **PostgreSQL**：12.0或更高版本（已在17.6版本测试）
- **网络访问**：能够连接到PostgreSQL服务器
- **内存**：建议最少512MB RAM

## 🛠️ 安装说明

### 方式一：从PyPI安装（推荐）

```bash
pip install postgresql-mcp-server3
```

### 方式二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/postgresql_mcp_server

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

### 方式三：使用UV（快速Python包管理器）

```bash
uv add postgresql-mcp-server3
```

## 🚀 快速开始

### 1. 配置数据库连接

创建一个包含PostgreSQL数据库凭据的`dbconfig.json`文件：

```json
{
    "dbPoolSize": 5,
    "dbMaxOverflow": 10,
    "dbPoolTimeout": 30,
    "dbList": [
        {
            "dbInstanceId": "postgresql_main",
            "dbHost": "localhost",
            "dbPort": 5432,
            "dbDatabase": "pg_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "PostgreSQL",
            "dbVersion": "17.6",
            "dbActive": true
        },
        {   "dbInstanceId": "rasesql_2",
            "dbHost": "localhost",
            "dbPort": 5432,
            "dbDatabase": "rasesql_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "RaseSQL",
            "dbVersion": "2.0",
            "dbActive": false
        }
    ],
    "logPath": "/path/to/logs",
    "logLevel": "info"
}
# dbActive
只有在dbList配置列表中dbActive设置为true的数据库实例才可用。
# logPath
MCP服务器日志存储在 /path/to/logs/mcp_server.log。
# logLevel
TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
# dbActive
只有在dbList配置列表中dbActive设置为true的数据库实例才可用。
# logPath
MCP服务器日志存储在 /Volumes/store/mysql_mcp_server/logs/mcp_server.log。
# logLevel
TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
```

### 3. 配置MCP JSON

```bash
{
  "mcpServers": {
    "postgresql-mcp-client": {
      "command": "postgresql-mcp-server3",
      "env": {
        "config_file": "/Users/frank/store/dbconfig.json"
      },
      "disabled": false
    }
  }
}

# config_file
设备中dbconfig.json文件的路径
```

### 4. 克隆仓库
```bash
git clone <repository-url>
cd mysql_mcp_server
将当前项目导入到你的IDE工具中

```

### 5. 通过IDE工具配置MCP JSON
```bash
{
  "mcpServers": {
    "postgresql-mcp-client": {
      "command": "uv",
      "args": [
        "run",
        "src/server.py"
      ],
      "cwd": "/Volumes/store/postgresql_mcp_server",
      "env": {
        "config_file": "/Volumes/store/dbconfig.json"
      },
      "disabled": false,
      "autoApprove": [
        "describe_table",
        "sql_exec",
        "generate_demo_data"
      ]
    }
  }
}
```

### 3. 启动服务器

#### 使用已安装的包
```bash
postgresql-mcp-server3
```

#### 使用FastMCP CLI
```bash
fastmcp run src/server.py
```

#### 直接Python执行
```bash
python src/server.py
```

#### 使用UV的开发模式
```bash
uv run src/server.py
```

### 4. 验证安装

```bash
# 测试连接
python -c "
import asyncio
from src.utils.db_config import load_activate_db_config
try:
    active_db, config = load_activate_db_config()
    print('✅ 配置加载成功')
    print(f'数据库: {active_db.db_type} {active_db.db_version}')
except Exception as e:
    print(f'❌ 配置错误: {e}')
"
```

## 📚 API参考

### MCP工具

#### `sql_exec(sql: str)`

执行任何SQL语句，自动格式化结果。

**参数：**
- `sql` (str): 要执行的SQL语句

**返回：**
```json
{
    "success": true,
    "result": [...],  // 查询结果或受影响的行数
    "message": "SQL执行成功"
}
```

**示例：**
```sql
-- 查询数据
SELECT * FROM users WHERE age > 18 LIMIT 10;

-- 插入数据
INSERT INTO users (name, email) VALUES ('张三', 'zhangsan@example.com');

-- 更新数据
UPDATE users SET last_login = NOW() WHERE id = 1;

-- DDL操作
CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255));
```

#### `describe_table(table_name: str)`

获取详细的表结构信息。

**参数：**
- `table_name` (str): 表名（支持`schema.table`格式）

**返回：**
- 详细的列信息，包括类型、约束和默认值

**示例：**
```python
# 描述public模式中的表
describe_table("users")

# 描述特定模式中的表
describe_table("inventory.products")
```

#### `generate_demo_data(table_name: str, columns_name: List[str], num: int)`

为开发和测试生成测试数据。

**参数：**
- `table_name` (str): 目标表名
- `columns_name` (List[str]): 要填充的列名
- `num` (int): 要生成的测试记录数

**示例：**
```python
generate_demo_data("users", ["name", "email", "phone"], 100)
```

### MCP资源

#### `database://tables`

提供所有数据库表的元数据，包括：
- 表名和模式
- 列定义和类型
- 主键和约束
- 行数

#### `database://config`

返回当前数据库配置（敏感数据已屏蔽）：
- 连接参数
- 池设置
- 数据库版本信息

## ⚙️ 配置说明

### 数据库配置（`dbconfig.json`）

```json
{
    "dbPoolSize": 5,              // 最小连接池大小
    "dbMaxOverflow": 10,          // 最大额外连接数
    "dbPoolTimeout": 30,          // 连接超时时间（秒）
    "dbList": [
        {
            "dbInstanceId": "unique_identifier",
            "dbHost": "localhost",
            "dbPort": 5432,
            "dbDatabase": "database_name",
            "dbUsername": "username",
            "dbPassword": "password",
            "dbType": "PostgreSQL",
            "dbVersion": "17.6",
            "dbActive": true          // 只有一个实例应该处于活动状态
        }
    ],
    "logPath": "/path/to/logs",   // 日志文件目录
    "logLevel": "info"            // TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
}
```

### 环境变量

- `config_file`: 覆盖默认配置文件路径
- `LOG_LEVEL`: 从配置中覆盖日志级别

### MCP客户端配置示例

#### Claude Desktop
```json
{
  "mcpServers": {
    "postgresql": {
      "command": "postgresql-mcp-server3",
      "env": {
        "config_file": "/Users/yourusername/dbconfig.json"
      }
    }
  }
}
```

#### 使用UV的开发配置
```json
{
  "mcpServers": {
    "postgresql-dev": {
      "command": "uv",
      "args": ["run", "src/server.py"],
      "cwd": "/path/to/postgresql_mcp_server",
      "env": {
        "config_file": "/path/to/dbconfig.json"
      }
    }
  }
}
```

## 🏗️ 系统架构

### 项目结构
```
postgresql_mcp_server/
├── src/
│   ├── server.py              # MCP服务器入口点
│   ├── utils/                 # 核心工具
│   │   ├── db_config.py      # 配置管理
│   │   ├── db_pool.py        # 连接池
│   │   ├── db_operate.py     # 数据库操作
│   │   ├── logger_util.py    # 日志工具
│   │   └── __init__.py       # 模块导出
│   ├── resources/            # MCP资源
│   │   └── db_resources.py   # 数据库元数据资源
│   └── tools/                # MCP工具
│       └── db_tool.py        # 数据库操作工具
├── dbconfig.json             # 数据库配置
├── pyproject.toml           # 包配置
├── requirements.txt         # 依赖
└── README.md               # 文档
```

### 关键组件

#### 🔗 **连接池管理**
- **单例模式**：每个应用程序一个池实例
- **异步操作**：非阻塞连接处理
- **健康监控**：自动连接验证
- **资源清理**：适当的连接生命周期管理

#### ⚙️ **配置系统**
- **基于JSON**：人类可读的配置
- **环境覆盖**：灵活的部署选项
- **验证**：全面的配置验证
- **热重载**：无需重启的配置更新

#### 📝 **日志框架**
- **结构化日志**：JSON格式的日志条目
- **多重输出**：控制台和文件日志
- **日志轮转**：自动日志文件管理
- **调试支持**：详细的操作跟踪

## 🛡️ 安全性

### 连接安全
- **参数化查询**：自动防止SQL注入
- **连接加密**：支持数据库连接的SSL/TLS
- **凭据保护**：安全的密码处理和屏蔽
- **访问控制**：基于实例的权限管理

### 查询安全
- **SQL验证**：查询类型验证
- **结果限制**：自动行数限制
- **参数清理**：输入验证和清理
- **错误处理**：安全的错误消息格式化

### 配置安全
- **环境变量**：安全的凭据管理
- **文件权限**：适当的配置文件保护
- **网络安全**：防火墙和访问控制建议

## 🧪 测试

### 连接测试
```bash
# 测试数据库连通性
python -c "
import asyncio
from src.utils.db_pool import get_db_pool

async def test():
    pool = await get_db_pool()
    conn = await pool.get_connection()
    result = await conn.fetchval('SELECT version()')
    print(f'已连接到: {result[:50]}...')
    await pool.release_connection(conn)

asyncio.run(test())
"
```

### SQL执行测试
```python
# 测试SQL执行
from src.tools.db_tool import sql_exec

result = await sql_exec("SELECT current_timestamp as now")
print(result)
```

### 负载测试
```python
# 测试并发连接
import asyncio
from src.utils.db_operate import execute_sql

async def load_test():
    tasks = []
    for i in range(10):
        task = execute_sql(f"SELECT {i} as test_id, pg_sleep(0.1)")
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    print(f"完成了 {len(results)} 个并发查询")

asyncio.run(load_test())
```

## 🚨 问题排查

### 常见问题

#### 连接错误
```bash
# 检查PostgreSQL连通性
psql -h localhost -p 5432 -U username -d database_name

# 测试配置
python -c "
from src.utils.db_config import load_activate_db_config
try:
    db, config = load_activate_db_config()
    print('✅ 配置有效')
except Exception as e:
    print(f'❌ 配置错误: {e}')
"
```

#### 权限问题
- 确保PostgreSQL用户具有必要权限：
  ```sql
  GRANT CONNECT ON DATABASE your_db TO your_user;
  GRANT USAGE ON SCHEMA public TO your_user;
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_user;
  ```
- 检查防火墙设置和网络连通性
- 验证PostgreSQL服务器正在运行并接受连接

#### 配置问题
- 验证`dbconfig.json`中的JSON语法
- 检查文件权限和路径
- 验证环境变量
- 查看日志文件获取详细错误信息

### 调试模式

启用详细日志：
```json
{
    "logLevel": "debug"
}
```

或设置环境变量：
```bash
export LOG_LEVEL=debug
python src/server.py
```

### 日志分析
```bash
# 查看最近的日志
tail -f /path/to/logs/mcp_server.log

# 搜索错误
grep -i error /path/to/logs/mcp_server.log

# 监控连接池
grep -i "connection pool" /path/to/logs/mcp_server.log
```

## 🤝 贡献指南

我们欢迎贡献！请遵循以下指南：

### 开始贡献
1. Fork仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 进行修改
4. 为新功能添加测试
5. 运行测试套件
6. 提交拉取请求

### 开发环境设置
```bash
# 克隆和设置
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/postgresql_mcp_server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev,test]"

# 安装pre-commit hooks
pre-commit install
```

### 代码质量
```bash
# 格式化代码
black src/
isort src/

# 代码检查
flake8 src/
mypy src/

# 运行测试
pytest tests/ -v

# 运行覆盖率测试
pytest --cov=src --cov-report=html
```

### 拉取请求指南
- 编写清晰、描述性的提交信息
- 为新功能包含测试
- 根据需要更新文档
- 确保所有测试通过
- 遵循现有的代码风格和约定

## 📄 许可证

本项目基于MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 👥 作者与贡献者

- **Frank Jin** - *初始开发* - [j00131120@163.com](mailto:j00131120@163.com)

## 🙏 致谢

- [FastMCP](https://github.com/fastmcp/fastmcp) - MCP框架基础
- [asyncpg](https://github.com/MagicStack/asyncpg) - 高性能PostgreSQL驱动
- [loguru](https://github.com/Delgan/loguru) - 现代日志库
- [PostgreSQL](https://www.postgresql.org/) - 世界上最先进的开源数据库

## 📞 支持

### 获取帮助
- 📖 **文档**：查看此README和内联代码文档
- 🐛 **错误报告**：[创建问题](https://github.com/j00131120/mcp_database_server/issues)
- 💬 **问题咨询**：联系[j00131120@163.com](mailto:j00131120@163.com)
- 💡 **功能请求**：[提交增强请求](https://github.com/j00131120/mcp_database_server/issues)

### 社区
- 如果觉得有用，请为此仓库加星 ⭐
- 与使用PostgreSQL和AI的同事分享
- 贡献改进和错误修复

---

<div align="center">

**用 ❤️ 为PostgreSQL和AI社区制作**

[⬆ 返回顶部](#postgresql-mcp-服务器)

</div>
