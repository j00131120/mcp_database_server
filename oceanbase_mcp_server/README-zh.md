# OceanBase MCP 服务器

一个模型上下文协议（MCP）服务器，支持与 OceanBase 数据库进行安全交互。同时支持 MySQL 和 Oracle 兼容模式，具备高性能异步操作能力。

## 🚀 功能特性

- **MCP 协议支持**：基于 FastMCP 框架构建，提供标准 MCP 工具和资源
- **多数据库兼容性**：支持 OceanBase（MySQL/Oracle 模式）
- **异步架构**：使用 `aiomysql/oracledb` 实现高性能数据库操作
- **连接池管理**：高效的连接管理，支持可配置的连接池设置
- **安全特性**：查询类型限制、自动 LIMIT 强制执行和参数验证
- **综合工具**：SQL 执行、表结构查询和测试数据生成

## 📋 前置条件

- Python >= 3.12
- OceanBase 数据库实例（MySQL 或 Oracle 模式）
- 网络访问数据库服务器

## 🛠️ 安装

### 1. 从 PyPI 安装（推荐）
```bash
pip install oceanbase-mcp-server3
```

### 2. 配置数据库连接

使用您的数据库凭据编辑 `dbconfig.json`：

```json
{
    "dbPoolSize": 5,
    "dbMaxOverflow": 10,
    "dbPoolTimeout": 30,
    "dbType-Comment": "当前使用的数据库类型，如 OceanBase(Mysql/Oracle) 数据库",
    "dbList": [
        {   "dbInstanceId": "oceanbase_1",
            "dbHost": "localhost",
            "dbPort": 2881,
            "dbDatabase": "oceanbase_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "oracle",
            "dbVersion": "V4.0.0",
            "dbActive": true
        },
        {   "dbInstanceId": "oceanbase_2",
            "dbHost": "localhost",
            "dbPort": 2881,
            "dbDatabase": "oceanbase_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "mysql",
            "dbVersion": "V3.0.0",
            "dbActive": false
        }
    ],
    "logPath": "/path/to/logs",
    "logLevel": "info"
}
# dbType
OceanBase 实例处于 Oracle 模式或 MySQL 模式。
# dbActive
只有在 dbList 配置列表中将 dbActive 设置为 true 的数据库实例才可用。
# logPath
MCP 服务器日志存储在 /path/to/logs/mcp_server.log。
# logLevel
TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
```

### 3. 配置 MCP 客户端

添加到您的 MCP 客户端配置文件中：

```json
{
  "mcpServers": {
    "oceanbase-mcp-client": {
      "command": "oceanbase-mcp-server3",
      "env": {
        "config_file": "/path/to/your/dbconfig.json"
      },
      "disabled": false
    }
  }
}
```

**注意**：将 `/path/to/your/dbconfig.json` 替换为您的配置文件的实际路径。

### 4. 克隆仓库（开发模式）
```bash
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/oceanbase_mcp_server
# 将项目导入到您的 IDE 中
```

### 5. 配置开发模式的 MCP 客户端
```json
{
  "mcpServers": {
    "oceanbase-mcp-client": {
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
uv项目绝对路径
# cwd
项目绝对路径
# config_file
dbconfig.json配置文件存放位置
```

## 🚀 快速开始

### 启动 MCP 服务器
```bash
# 使用已安装的包
oceanbase-mcp-server3

# 使用 fastmcp CLI（开发模式）
fastmcp run src/server.py

# 使用 uv（开发模式）
uv run src/server.py

# 或直接使用 Python
python src/server.py

# 使用 fastmcp调试
fastmcp dev src/server.py
```

### 与 MCP 客户端一起使用
服务器提供以下 MCP 工具和资源：

#### 工具
- `sql_exec`：执行任何 SQL 语句
- `describe_table`：获取表结构信息
- `generate_demo_data`：为表生成测试数据

#### 资源
- `database://tables`：数据库表元数据
- `database://config`：数据库配置信息

## 📚 API 参考

### SQL 执行工具
```python
await sql_exec("SELECT * FROM users WHERE age > 18")
```

**参数：**
- `sql` (str)：要执行的 SQL 语句

**返回值：**
- `success` (bool)：执行状态
- `result`：查询结果或受影响的行数
- `message` (str)：状态描述

### 表结构工具
```python
await describe_table("users")
```

**参数：**
- `table_name` (str)：表名（支持 `database.table` 格式）

**返回值：**
- 包括列、类型和约束的表结构信息

### 测试数据生成
```python
await generate_demo_data("users", ["name", "email"], 50)
```

**参数：**
- `table_name` (str)：目标表名
- `columns_name` (List[str])：要填充的列名
- `num` (int)：要生成的测试记录数

## ⚙️ 配置

### 数据库配置
`dbconfig.json` 文件支持多个数据库实例：

```json
{
    "dbPoolSize": 5,
    "dbMaxOverflow": 10,
    "dbPoolTimeout": 30,
    "dbType-Comment": "当前使用的数据库类型，如 OceanBase(Mysql/Oracle) 数据库",
    "dbList": [
        {   "dbInstanceId": "oceanbase_1",
            "dbHost": "localhost",
            "dbPort": 2881,
            "dbDatabase": "oceanbase_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "oracle",
            "dbVersion": "V4.0.0",
            "dbActive": true   // 只有一个实例应该是活跃的
        },
        {   "dbInstanceId": "oceanbase_2",
            "dbHost": "localhost",
            "dbPort": 2881,
            "dbDatabase": "oceanbase_db",
            "dbUsername": "root",
            "dbPassword": "123456",
            "dbType": "mysql",
            "dbVersion": "V3.0.0",
            "dbActive": false   // 其他实例应该是非活跃的
        }
    ],
    "logPath": "/path/to/logs",
    "logLevel": "info"
}
```

### 日志配置
- **日志级别**：TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
- **日志轮转**：每个文件 10 MB，保留 7 天
- **输出**：stderr（用于 MCP）和文件日志

## 🔒 安全特性

### 查询限制
- **参数化查询**：所有 SQL 查询都使用参数绑定来防止 SQL 注入
- **事务管理**：自动提交/回滚以确保数据完整性
- **参数验证**：对所有参数进行输入验证

### 配置安全
- **密码隐藏**：响应中掩盖敏感信息
- **实例隔离**：仅暴露活跃的数据库配置
- **环境覆盖**：安全的配置文件路径管理

## 🏗️ 架构

### 项目结构
```
src/
├── server.py              # MCP 服务器主入口点
├── utils/                 # 工具模块
│   ├── db_config.py       # 数据库配置管理
│   ├── db_pool.py         # 连接池管理
│   ├── db_operate.py      # 数据库操作
│   ├── logger_util.py     # 日志管理
│   └── __init__.py        # 模块初始化
├── resources/             # MCP 资源
│   └── db_resources.py    # 数据库资源
└── tools/                 # MCP 工具
    └── db_tool.py         # 数据库工具
```

### 核心组件

#### 数据库连接池
- **单例模式**：确保单一连接池实例
- **异步管理**：非阻塞连接处理
- **自动清理**：连接释放和连接池管理

#### 配置管理
- **基于 JSON**：人类可读的配置格式
- **环境覆盖**：灵活的配置管理
- **验证**：必需字段验证和错误处理

#### 日志系统
- **统一接口**：跨模块的单一日志器实例
- **可配置输出**：文件和控制台日志
- **结构化格式**：时间戳、级别、模块、函数和行信息

## 🐳 Docker 支持

### 使用 Docker Compose

本项目包含了 OceanBase 的完整 Docker Compose 设置。详情请参见 docker-compose 文档。

```bash
# 启动带有监控堆栈的 OceanBase
docker-compose up -d

# 简单的 OceanBase 设置（用于开发）
docker-compose -f docker-compose.simple.yml up -d
```

### OceanBase 连接
启动 Docker 容器后，使用以下方式连接：
```bash
# MySQL 模式连接
mysql -h 127.0.0.1 -P 2881 -u root -p123456

# 更新您的 dbconfig.json 以指向 Docker 实例
{
    "dbHost": "localhost",
    "dbPort": 2881,
    "dbDatabase": "test",
    "dbUsername": "root",
    "dbPassword": "123456",
    "dbType": "mysql"
}
```

## 🧪 测试

### 生成测试数据
```python
# 为 users 表生成 100 条测试记录
await generate_demo_data("users", ["name", "email", "phone"], 100)
```

### 测试数据库连接
```python
# 测试基本 SQL 执行
result = await sql_exec("SELECT 1 as test")
print(result)  # {'success': True, 'result': [{'test': 1}]}
```

## 📊 监控

### 数据库状态
```python
# 获取数据库配置（通过 MCP 资源）
# 这将显示当前活跃的数据库实例配置

# 获取表信息（通过 MCP 资源）
# 这将显示所有表及其结构和记录数

# 使用 MCP 客户端时的示例输出：
# 数据库：oracle V4.0.0（或 mysql V3.0.0）
# 表：users, products, orders 等。
```

### 连接池状态
- 连接池大小和溢出配置
- 连接超时设置
- 活跃连接数

## 🚨 故障排除

### 常见问题

#### 连接错误
```bash
# 检查 OceanBase 连接性（MySQL 模式）
mysql -h localhost -P 2881 -u username -p database_name

# 检查 OceanBase 连接性（Oracle 模式）
sqlplus username/password@localhost:2881/database_name

# 验证配置
python -c "from src.utils.db_config import load_db_config; print(load_db_config())"
```

#### 权限问题
- 确保数据库用户具有必要的权限
- 检查防火墙和网络访问
- 验证数据库服务器正在运行

#### 配置错误
- 验证 `dbconfig.json` 中的 JSON 语法
- 检查文件权限
- 验证环境变量

### 调试模式
在配置中将日志级别设置为 DEBUG：
```json
{
    "logLevel": "debug"
}
```

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 如果适用，添加测试
5. 提交拉取请求

### 开发环境设置
```bash
# 使用 uv 安装依赖
uv sync

# 使用调试日志运行
export config_file="/path/to/your/dbconfig.json"
uv run src/server.py

# 或使用 fastmcp 进行开发
fastmcp run src/server.py
```

### 代码质量工具
```bash
# 格式化代码
black src/
isort src/

# 检查代码
flake8 src/
mypy src/

# 运行测试
pytest

# 运行带覆盖率的测试
pytest --cov=src --cov-report=html

# 预提交钩子
pre-commit install
pre-commit run --all-files
```

## 📄 许可证

本项目在 MIT 许可证下授权 - 详情请参见 [LICENSE](LICENSE) 文件。

## 👥 作者

- **Frank Jin** - *初始工作* - [j00131120@163.com](mailto:j00131120@163.com)

## 🙏 致谢

- [FastMCP](https://github.com/fastmcp/fastmcp) - MCP 框架
- [aiomysql](https://github.com/aio-libs/aiomysql) - 异步 MySQL 驱动
- [oracledb](https://oracle.github.io/python-oracledb/) - Oracle 数据库驱动
- [loguru](https://github.com/Delgan/loguru) - 日志库

## 📞 支持

获得支持和问题咨询：
- 在仓库中创建问题
- 联系：[j00131120@163.com](mailto:j00131120@163.com)

## 🔄 变更日志

### v1.0.3（当前版本）
- 添加了 Oracle 数据库驱动支持（`oracledb`）
- 增强了多数据库兼容性
- 改进了配置管理
- 错误修复和性能优化

### v1.0.1
- 增强了类型注解和错误处理
- 修复了配置文件路径解析
- 包名更改为 `oceanbase-mcp-server3`

### v1.0.0
- 初始发布
- MCP 协议支持
- 多数据库兼容性
- 异步连接池
- 安全特性实现

## 📦 构建和分发

### 构建包
```bash
# 使用 uv（推荐）
uv build

# 或使用传统工具
python -m build
```

### 发布到 PyPI
```bash
# 检查包
python -m twine check dist/*

# 上传到 PyPI
python -m twine upload dist/*
```

### 包信息
- **包名**：`oceanbase-mcp-server3`
- **入口点**：`oceanbase-mcp-server3`
- **MCP 服务器入口点**：`main`
- **Python 版本**：>= 3.12
- **许可证**：MIT
