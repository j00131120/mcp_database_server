# 多数据库 MCP 客户端

一个基于模型上下文协议 (MCP) 的服务端，支持与多种数据库类型安全交互，包括 MySQL、MariaDB、TiDB、OceanBase 和 AWS RDS/Aurora MySQL。该服务将数据库操作作为 MCP 工具和资源公开，同时将实际的 SQL 执行代理到远程 HTTP 服务。

## 🚀 特性

- **通用 SQL 执行**: 通过单一工具执行任何 SQL 语句（SELECT、INSERT、UPDATE、DELETE、DDL）
- **多数据库支持**: 兼容 MySQL、MariaDB、TiDB、OceanBase 和兼容的云数据库
- **HTTP 代理架构**: 通过 HTTP 转发将 MCP 接口与数据库连接解耦
- **模式内省**: 获取表结构和数据库元数据作为 MCP 资源
- **测试数据生成**: 内置工具生成开发测试数据
- **灵活配置**: 支持多个数据库实例并可运行时切换
- **异步 I/O**: 使用 `aiohttp` 和 `asyncio` 完全异步操作
- **结构化日志**: 使用 `loguru` 提供全面的日志记录，同时输出到 stderr 和滚动文件

## 🏗️ 架构

系统遵循代理模式，其中 MCP 服务端充当客户端接口：

```
MCP 客户端 → FastMCP 工具/资源 → HTTP POST → 远程数据库服务 → 数据库
```

### 核心组件

- **`src/server.py`**: 基于 FastMCP 框架的 MCP 服务端，工具/资源定义
- **`src/utils/db_operate.py`**: HTTP 代理 SQL 执行引擎
- **`src/utils/db_config.py`**: 支持多实例的单例配置加载器
- **`src/resources/db_resources.py`**: 数据库元数据和配置资源构建器
- **`src/tools/db_tool.py`**: 测试数据生成工具
- **`src/utils/http_util.py`**: 异步 HTTP 客户端助手
- **`src/utils/logger_util.py`**: 日志设置和配置路径解析

## 📋 系统要求

- Python 3.12+
- 一个可通过配置的 `multiDBServer` 端点访问的远程数据库服务

## 🛠️ 安装

### 1. 从 PyPI 安装（推荐）
```bash
pip install multidb-mcp-client
```

### 2. 配置数据库连接

使用您的数据库凭据编辑 `dbconfig.json`：

```json
{
    "dbPoolSize": 5,
    "dbMaxOverflow": 10,
    "dbPoolTimeout": 30,
    "dbType-Comment": "当前使用的数据库类型，如 MySQL/MariaDB/TiDB OceanBase/RDS/Aurora MySQL 数据库",
    "dbList": [
        {   "dbInstanceId": "oceanbase_1",
            "dbHost": "localhost",
            "dbPort": 2281,
            "dbDatabase": "oceanbase_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "OceanBase",
            "dbVersion": "V4.0.0",
            "dbActive": true
        },
        {   "dbInstanceId": "mysql_2",
            "dbHost": "localhost",
            "dbPort": 3306,
            "dbDatabase": "mysql_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "MySQL",
            "dbVersion": "8.0",
            "dbActive": false
        },
        {   "dbInstanceId": "tidb_3",
            "dbHost": "localhost",
            "dbPort": 4000,
            "dbDatabase": "tidb_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "TiDB",
            "dbVersion": "8.5.3",
            "dbActive": false
        }
    ],
    "multiDBServer": "http://127.0.0.1:8080/mcp/executeQuery",
    "logPath": "/path/to/logs",
    "logLevel": "INFO"
}
```
### 配置属性

- **`dbList`**: 数据库实例配置数组
  - **`dbActive`**: 必须恰好有一个实例为 `true`（激活的数据库）
  - **`dbType`**: 支持的值包括 MySQL、OceanBase、TiDB 等
- **`multiDBServer`**: 接受 SQL 执行请求的 HTTP 端点
- **`logPath`**: 日志文件目录（如果不存在会自动创建）
- **`logLevel`**: TRACE、DEBUG、INFO、WARNING、ERROR、CRITICAL 之一

### 3. 配置 MCP 客户端

在您的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "multidb-mcp-client": {
      "command": "multidb-mcp-client",
      "env": {
        "config_file": "/path/to/your/dbconfig.json"
      },
      "disabled": false
    }
  }
}
```

**注意**: 将 `/path/to/your/dbconfig.json` 替换为您配置文件的实际路径。

### 4. 克隆仓库（开发模式）
```bash
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/multidb_mcp_client
# 将项目导入您的 IDE
```

### 5. 配置 MCP 客户端用于开发
```json
{
  "mcpServers": {
    "multidb-mcp-client": {
      "command": "/bin/uv",
      "args": ["run", "src/server.py"],
      "cwd": "/path/to/your/project",
      "env": {
        "config_file": "/path/to/your/dbconfig.json"
      },
      "disabled": false,
      "autoApprove": ["describe_table", "sql_exec", "generate_demo_data"]
    }
  }
}

# command
uv 的绝对路径
# cwd
项目的绝对路径
# config_file
dbconfig.json 文件路径
```

## 🚀 运行服务

### 命令行

安装后，使用提供的 CLI 命令：

```bash
multidb-mcp-client
```

这将启动 MCP 服务，通过 stdio 供 MCP 兼容客户端使用。

### FastMCP CLI（替代方式）

```bash
# 列出可用的 MCP 服务
fastmcp servers list

# 通过入口点运行（在 pyproject.toml 中定义）
fastmcp run mysql
```

### 环境变量

- **`config_file`**: 覆盖默认配置文件路径
- `loguru` 支持的标准日志环境变量

## 🛠️ MCP 工具

### `sql_exec(sql: str)`

执行任何 SQL 语句并自动处理事务。

**参数:**
- `sql`（字符串）: 要执行的 SQL 语句

**返回值:**
```json
{
  "success": true,
  "result": [...],  // 查询结果或受影响的行数
  "message": "SQL 执行成功"
}
```

**使用示例:**
```python
# 查询数据
await sql_exec("SELECT * FROM users WHERE age > 18")

# 插入数据
await sql_exec("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")

# 更新记录
await sql_exec("UPDATE users SET email = 'newemail@example.com' WHERE id = 1")

# DDL 操作
await sql_exec("CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100))")
```

### `describe_table(table_name: str)`

获取详细的表结构信息。

**参数:**
- `table_name`（字符串）: 表名（支持 `database.table` 格式）

**返回值:**
与 `sql_exec` 相同的格式，`result` 包含列元数据。

**使用示例:**
```python
await describe_table("users")
await describe_table("inventory.products")
```

### `generate_demo_data(table_name: str, columns_name: List[str], num: int)`

为开发和测试生成测试数据。

**参数:**
- `table_name`（字符串）: 目标表名
- `columns_name`（数组）: 要填充的列名列表
- `num`（整数）: 要生成的测试记录数

**使用示例:**
```python
# 生成 100 个测试用户
await generate_demo_data("users", ["name", "email", "phone"], 100)

# 生成 50 个测试产品
await generate_demo_data("products", ["product_name", "category", "description"], 50)
```

## 📊 MCP 资源

### `database://tables`

提供所有数据库表的全面元数据。

**返回值:**
```json
{
  "uri": "database://tables",
  "mimeType": "application/json",
  "text": "[{\"name\": \"users\", \"columns\": [...], \"record_count\": 1250}, ...]"
}
```

**使用场景:**
- 模式探索和文档化
- 数据库监控和统计
- 查询规划和优化

### `database://config`

提供当前数据库配置（敏感数据已掩码）。

**返回值:**
```json
{
  "uri": "database://config", 
  "mimeType": "application/json",
  "text": "{\"dbInstanceId\": \"primary_oceanbase\", \"dbHost\": \"localhost\", \"dbPassword\": \"***hidden***\", ...}"
}
```

## 📝 日志记录

系统提供全面的日志记录：

- **控制台输出**: 输出到 stderr 以便 MCP 客户端可见
- **文件日志**: 滚动日志文件（最大 10MB，保留 7 天）
- **结构化格式**: 时间戳、级别、函数、行号和消息
- **可配置级别**: 从 TRACE 到 CRITICAL

日志文件存储在：
- 配置的 `logPath` 目录
- 默认: `<项目根目录>/logs/mcp_server.log`

## 🔒 安全考虑

### 当前安全特性

- **密码掩码**: 敏感数据在资源响应中隐藏
- **HTTP 客户端**: 支持自定义头部进行身份验证
- **配置隔离**: 仅暴露激活的数据库配置

### 安全建议

1. **凭据管理**: 将数据库密码存储在环境变量或安全保险库中
2. **网络安全**: 对 `multiDBServer` 端点使用 HTTPS 并进行适当的身份验证
3. **访问控制**: 将 `sql_exec` 工具的使用限制在可信环境中
4. **文件权限**: 使用适当的文件系统权限保护 `dbconfig.json`
5. **网络隔离**: 将 `multiDBServer` 部署在安全的网络段中

### 生产部署

```bash
# 使用环境变量处理敏感数据
export DB_PASSWORD="your_secure_password"
export MULTIDB_SERVER_URL="https://secure-db-proxy.internal.com/api/v1/execute"

# 限制配置文件权限
chmod 600 dbconfig.json

# 使用非 root 用户运行
useradd -r mcp-client
sudo -u mcp-client multidb-mcp-client
```

## 🧪 开发

### 项目结构

```
multidb_mcp_client/
├── src/
│   ├── server.py              # MCP 服务端和工具定义
│   ├── resources/
│   │   └── db_resources.py    # 资源数据构建器
│   ├── tools/
│   │   └── db_tool.py         # 工具实现
│   └── utils/
│       ├── db_config.py       # 配置管理
│       ├── db_operate.py      # 通过 HTTP 执行 SQL
│       ├── http_util.py       # HTTP 客户端工具
│       └── logger_util.py     # 日志配置
├── dbconfig.json              # 数据库配置
├── pyproject.toml             # 项目元数据和依赖
└── logs/                      # 日志输出目录
```

### 代码风格

- **明确命名**: 清晰、描述性的函数和变量名
- **早期返回**: 使用保护子句减少嵌套
- **类型注解**: 公共 API 包含类型提示
- **错误处理**: 全面的异常处理并记录日志
- **异步/等待**: 全程使用适当的异步模式

### 关键依赖

- **`fastmcp`**: MCP 框架和协议实现
- **`aiohttp`**: 用于数据库代理调用的异步 HTTP 客户端
- **`loguru`**: 带有滚动和格式化的结构化日志
- **`mcp[cli]`**: MCP 命令行工具

## 📄 许可证

MIT 许可证 - 详见 LICENSE 文件。

## 🔗 链接

- **主页**: https://github.com/j00131120/mcp_database_server/tree/main/multidb_mcp_client
- **文档**: https://github.com/j00131120/mcp_database_server/blob/main/multidb_mcp_client/README.md
- **源代码**: https://github.com/j00131120/mcp_database_server.git
- **问题跟踪**: https://github.com/j00131120/mcp_database_server/issues
- **更新日志**: https://github.com/j00131120/mcp_database_server/blob/main/multidb_mcp_client/CHANGELOG.md

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 开启 Pull Request

## 📞 支持

如有问题、疑问或贡献：

- **作者**: Frank Jin (j00131120@163.com)
- **GitHub Issues**: 使用问题跟踪器报告错误和功能请求
- **文档**: 查看仓库 wiki 获取更多文档

---

**注意**: 此 MCP 服务需要在配置的 `multiDBServer` 端点运行兼容的远程数据库服务。在运行客户端之前，请确保您的远程服务实现了预期的 HTTP API 契约。
