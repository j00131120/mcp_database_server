# Redis MCP 服务器

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org)
[![Redis Version](https://img.shields.io/badge/redis-5.0%2B-red.svg)](https://redis.io)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.11.3%2B-green.svg)](https://github.com/fastmcp/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

一个模型上下文协议（MCP）服务器，通过AI助手和应用程序实现与Redis数据库的安全、高效交互。

## 🚀 功能特性

- **🔌 MCP协议支持**：基于FastMCP框架构建，支持标准MCP工具和资源
- **🗄️ Redis兼容性**：支持Redis单机、主从和集群部署
- **⚡ 异步架构**：使用`redis.asyncio`和`hiredis`构建高性能操作
- **🔗 连接池**：高效的连接管理，支持可配置的池设置
- **🔒 安全特性**：密码保护、SSL支持和连接验证
- **🛠️ 综合工具**：Redis命令执行、监控和数据管理
- **📊 监控和分析**：服务器信息、内存使用、客户端连接和键统计
- **🔧 灵活配置**：基于JSON的配置，支持多实例
- **📝 详细日志**：结构化日志，支持可配置级别和文件轮转
- **🐳 生产就绪**：健康检查、错误处理和优雅连接管理

## 📋 系统要求

- **Python**：>= 3.12
- **Redis**：>= 5.0.0
- **网络访问**：到Redis服务器实例的网络连接

## 🛠️ 安装

### 1. 从PyPI安装（推荐）

```bash
pip install redis-mcp-server3
```

### 2. 配置数据库连接

使用您的数据库凭据编辑`dbconfig.json`：

```json
{
  "redisEncoding": "utf-8",
  "redisPoolSize": 5,
  "redisMaxConnections": 10,
  "redisConnectionTimeout": 30,
  "socketTimeout": 30,
  "retryOnTimeout": true,
  "healthCheckInterval": 30,
  "redisType-Comment": "single 单机模式、masterslave 主从模式、cluster 集群模式",
  "redisList": [
    {
      "redisInstanceId": "redis-local-single",
      "redisType": "single",
      "redisHost": "localhost",
      "redisPort": 6379,
      "redisDatabase": 0,
      "redisPassword": 123456,
      "dbActive": true
    },
    {
      "redisInstanceId": "redis-ms-single",
      "redisType": "masterslave",
      "redisHost": "localhost",
      "redisPort": 6379,
      "redisDatabase": 0,
      "redisPassword": 123456,
      "dbActive": false
    },
    {
      "redisInstanceId": "redis-cluster-single",
      "redisType": "cluster",
      "redisHost": "localhost",
      "redisPort": 6379,
      "redisDatabase": 0,
      "redisPassword": 123456,
      "dbActive": false
    }
  ],
  "logPath": "/path/to/logs",
  "logLevel": "info"
}
# redisType
Redis实例支持单机、主从、集群模式
# dbActive
只有在dbList配置列表中将dbActive设置为true的数据库实例才可用
# logPath
MCP服务器日志存储在/path/to/logs/mcp_server.log
# logLevel
TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
```

#### 配置参数说明

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `redisEncoding` | Redis操作的字符编码 | `utf-8` |
| `redisPoolSize` | 最小连接池大小 | `5` |
| `redisMaxConnections` | 最大连接数 | `10` |
| `redisConnectionTimeout` | 连接超时时间（秒） | `30` |
| `socketTimeout` | Socket超时时间（秒） | `30` |
| `retryOnTimeout` | 是否在超时时重试 | `true` |
| `healthCheckInterval` | 健康检查间隔（秒） | `30` |
| `dbActive` | 此实例是否激活 | `false` |
| `redisSsl` | 启用SSL连接 | `false` |
| `redisDecodeResponses` | 将响应解码为字符串 | `true` |

### 3. 配置MCP客户端

添加到您的MCP客户端配置文件：

```json
{
  "mcpServers": {
    "redis-mcp-client": {
      "command": "redis-mcp-server3",
      "env": {
        "config_file": "/path/to/your/dbconfig.json"
      },
      "disabled": false
    }
  }
}
```

**注意**：将`/path/to/your/dbconfig.json`替换为您配置文件的实际路径。

### 4. 克隆仓库（开发模式）

```bash
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/redis_mcp_server
# 将项目导入到您的IDE中
```

### 5. 开发环境的MCP客户端配置

```json
{
  "mcpServers": {
    "redis-mcp-client": {
      "command": "/bin/uv",
      "args": ["run", "src/server.py"],
      "cwd": "/path/to/your/project",
      "env": {
        "config_file": "/path/to/your/dbconfig.json"
      },
      "disabled": false
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

### 1. 启动MCP服务器

```bash
# 使用已安装的包
redis-mcp-server3

# 使用FastMCP CLI
fastmcp run src/server.py

# 直接使用Python执行
python src/server.py

# 使用 fastmcp调试
fastmcp dev src/server.py
```

### 2. 基本使用示例

```python
# 执行Redis命令
await redis_exec("SET", ["user:1001", "John Doe"])
await redis_exec("GET", ["user:1001"])

# 哈希操作
await redis_exec("HSET", ["user:1001:profile", "name", "John", "age", "30"])
await redis_exec("HGETALL", ["user:1001:profile"])

# 列表操作
await redis_exec("LPUSH", ["tasks", "task1", "task2"])
await redis_exec("LRANGE", ["tasks", "0", "-1"])

# 获取服务器信息
server_info = await get_server_info()
memory_info = await get_memory_info()
```

## 📚 API参考

### MCP工具

#### `redis_exec(command: str, args: list = None)`
执行任何Redis命令及其参数。

**参数：**
- `command` (str)：Redis命令名称（如'GET'、'SET'、'HGET'）
- `args` (list, 可选)：命令参数

**返回：**
- `dict`：包含成功状态和数据的执行结果

**示例：**
```python
# 字符串操作
await redis_exec("SET", ["key1", "value1"])
await redis_exec("GET", ["key1"])
await redis_exec("SETEX", ["key2", "60", "temp_value"])

# 哈希操作
await redis_exec("HSET", ["hash1", "field1", "value1"])
await redis_exec("HGETALL", ["hash1"])

# 列表操作
await redis_exec("LPUSH", ["list1", "item1", "item2"])
await redis_exec("LRANGE", ["list1", "0", "-1"])

# 集合操作
await redis_exec("SADD", ["set1", "member1", "member2"])
await redis_exec("SMEMBERS", ["set1"])
```

#### `gen_test_data(table: str, columns: list, num: int = 10)`
为Redis哈希结构生成测试数据。

**参数：**
- `table` (str)：键的表/前缀名称
- `columns` (list)：要填充的字段名称
- `num` (int)：要生成的测试记录数

#### `get_server_info()`
获取Redis服务器基本信息。

**返回：**
- 服务器版本、模式、操作系统、架构、运行时间

#### `get_memory_info()`
获取Redis内存使用统计。

**返回：**
- 内存使用量、峰值使用量、RSS内存、最大内存设置

#### `get_clients_info()`
获取Redis客户端连接信息。

**返回：**
- 连接的客户端数量、输入/输出缓冲区大小

#### `get_stats_info()`
获取Redis操作统计。

**返回：**
- 总连接数、处理的命令数、键空间命中/未命中

#### `get_db_info()`
获取Redis数据库信息。

**返回：**
- 数据库大小、键空间信息

#### `get_keys_info()`
获取键样本信息（前10个键）。

**返回：**
- 总键数、带类型和TTL的样本键

#### `get_key_types()`
获取键类型分布统计。

**返回：**
- 不同键类型的分布（string、hash、list、set、zset）

#### `get_redis_config()`
获取Redis配置信息。

**返回：**
- 重要的Redis配置参数

#### `get_redis_overview()`
获取综合Redis概览（所有监控信息）。

**返回：**
- 包含上述所有信息的完整系统概览

### MCP资源

#### `database://config`
数据库配置信息（隐藏敏感数据）。

**返回：**
- 不包含密码的安全配置详情

#### `database://status`
数据库连接状态和健康检查结果。

**返回：**
- 连接状态、ping结果、基本操作测试

## 🏗️ 架构

### 项目结构
```
redis_mcp_server/
├── src/
│   ├── __init__.py              # 包元数据和API
│   ├── server.py                # 主MCP服务器入口点
│   ├── utils/                   # 工具模块
│   │   ├── __init__.py          # 工具导出
│   │   ├── db_config.py         # 配置管理
│   │   ├── db_pool.py           # 连接池管理
│   │   ├── db_operate.py        # Redis操作包装器
│   │   └── logger_util.py       # 日志配置
│   ├── resources/               # MCP资源
│   │   └── db_resources.py      # 数据库资源提供者
│   └── tools/                   # MCP工具
│       └── db_tool.py           # Redis管理工具
├── dbconfig.json               # 数据库配置
├── pyproject.toml              # 项目配置
├── requirements.txt            # Python依赖
└── README.md                   # 项目文档
```

### 核心组件

#### 连接池管理器
- **单例模式**：每个应用程序一个池实例
- **异步管理**：非阻塞连接处理
- **健康监控**：自动连接验证
- **资源清理**：正确的连接释放

#### 配置系统
- **基于JSON**：人类可读的配置
- **环境覆盖**：灵活的部署选项
- **多实例**：支持多个Redis实例
- **验证**：全面的错误检查

#### 日志系统
- **结构化日志**：JSON格式的日志条目
- **文件轮转**：自动日志文件管理
- **可配置级别**：从TRACE到CRITICAL
- **性能优化**：异步日志记录

## 🔧 高级配置

### SSL/TLS配置

对于安全连接，在您的`dbconfig.json`中配置SSL：

```json
{
  "redisList": [
    {
      "redisInstanceId": "secure-redis",
      "redisHost": "secure.redis.example.com",
      "redisPort": 6380,
      "redisSsl": true,
      "redisPassword": "secure_password",
      "dbActive": true
    }
  ]
}
```

### 集群配置

对于Redis集群部署：

```json
{
  "redisList": [
    {
      "redisInstanceId": "redis-cluster",
      "redisType": "cluster",
      "redisHost": "cluster-node1.example.com",
      "redisPort": 7000,
      "redisPassword": "cluster_password",
      "dbActive": true
    }
  ]
}
```

### 性能调优

针对高吞吐量场景的优化：

```json
{
  "redisPoolSize": 20,
  "redisMaxConnections": 50,
  "redisConnectionTimeout": 10,
  "socketTimeout": 5,
  "healthCheckInterval": 60
}
```

## 🧪 测试

### 基本连接测试

```python
# 测试Redis连接
status = await get_connection_status()
print(status)  # {'ping': True, 'set_get': 'ok'}
```

### 性能测试

```python
# 生成测试数据
await gen_test_data("users", ["name", "email", "age"], 1000)

# 检查数据库大小
db_info = await get_db_info()
print(f"总键数: {db_info['dbsize']}")
```

## 📊 监控

### 健康检查

服务器提供内置健康监控：

```python
# 获取综合概览
overview = await get_redis_overview()

# 检查特定指标
memory = await get_memory_info()
if memory['used_memory'] > threshold:
    # 处理高内存使用
    pass
```

### 日志分析

监控服务器日志以了解性能和错误：

```bash
# 查看实时日志
tail -f /var/log/redis_mcp_server/logs/mcp_server.log

# 搜索错误
grep "ERROR" /var/log/redis_mcp_server/logs/mcp_server.log
```

## 🚨 故障排除

### 常见问题

#### 连接错误

**问题**：`ConnectionError: Connection refused`

**解决方案**：
```bash
# 检查Redis服务器状态
redis-cli ping

# 验证Redis是否运行
systemctl status redis

# 检查网络连接
telnet localhost 6379
```

#### 认证错误

**问题**：`AuthenticationError: Auth failed`

**解决方案**：
- 验证`dbconfig.json`中的密码
- 检查Redis AUTH配置
- 确保用户有适当的权限

#### 内存问题

**问题**：高内存使用或OOM错误

**解决方案**：
- 使用`get_memory_info()`监控
- 调整`maxmemory`策略
- 实施键过期
- 使用Redis内存优化技术

#### 性能问题

**问题**：响应时间慢

**解决方案**：
- 增加连接池大小
- 减少连接超时
- 使用`get_stats_info()`监控
- 检查网络延迟

### 调试模式

启用调试日志：

```json
{
  "logLevel": "debug"
}
```

### 诊断命令

```python
# 检查服务器健康
server_info = await get_server_info()
clients_info = await get_clients_info()
stats_info = await get_stats_info()

# 分析键分布
key_types = await get_key_types()
keys_sample = await get_keys_info()
```

## 🤝 贡献

我们欢迎贡献！请遵循以下指南：

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/redis_mcp_server

# 安装开发依赖
pip install -e ".[dev,test,docs]"

# 安装pre-commit钩子
pre-commit install
```

### 代码质量

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
```

### 提交更改

1. Fork仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 进行更改
4. 为新功能添加测试
5. 确保所有测试通过
6. 提交更改（`git commit -m 'Add amazing feature'`）
7. 推送到分支（`git push origin feature/amazing-feature`）
8. 打开Pull Request

### 代码风格

- 遵循PEP 8指南
- 为所有函数使用类型提示
- 为公共方法添加文档字符串
- 编写全面的测试
- 更新文档

## 📄 许可证

本项目根据MIT许可证授权 - 有关详细信息，请参阅[LICENSE](LICENSE)文件。

## 👥 作者

- **Frank Jin** - *初始工作* - [j00131120@163.com](mailto:j00131120@163.com)

## 🙏 致谢

- [FastMCP](https://github.com/fastmcp/fastmcp) - MCP框架基础
- [redis-py](https://github.com/redis/redis-py) - Python Redis客户端
- [Loguru](https://github.com/Delgan/loguru) - 结构化日志库
- [Redis](https://redis.io/) - 内存数据结构存储

## 📞 支持

- **问题**：[GitHub Issues](https://github.com/j00131120/mcp_database_server/issues)
- **讨论**：[GitHub Discussions](https://github.com/j00131120/mcp_database_server/discussions)
- **邮件**：[j00131120@163.com](mailto:j00131120@163.com)

## 🔄 版本历史

### v1.0.0
- 初始版本
- 完整的MCP协议支持
- Redis连接池
- 综合监控工具
- 安全特性实现
- 生产就绪部署

---

<p align="center">
  <strong>为Redis和MCP社区用❤️构建</strong>
</p>
