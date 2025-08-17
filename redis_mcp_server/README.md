# Redis MCP Server

A Model Context Protocol (MCP) server that enables secure interaction with Redis databases.

## 🚀 Features

- **MCP Protocol Support**: Built on FastMCP framework with standard MCP tools and resources
- **Multi-Database Compatibility**: Support for Redis
- **Asynchronous Architecture**: Built with `hiredis` for high-performance database operations
- **Connection Pooling**: Efficient connection management with configurable pool settings
- **Security Features**: Query type restrictions, automatic LIMIT enforcement, and parameter validation
- **Comprehensive Tools**: SQL execution, table structure queries, and test data generation

## 📋 Prerequisites

- Python >= 3.12
- MySQL/MariaDB/TiDB/OceanBase database instance
- Network access to database server

## 🛠️ Installation

### 1. Install from PyPI (Recommended)
```bash
pip install mysql-mcp-server3
```

### 2. Configure database connection

Edit `dbconfig.json` with your database credentials:

```bash
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
            "redisInstanceId": "redis-local-single",
            "redisType": "single",
            "redisHost": "localhost",
            "redisPort": 6379,
            "redisDatabase": 0,
            "redisPassword": 123456,
            "dbActive": false
        },
        {
            "redisInstanceId": "redis-local-single",
            "redisType": "single",
            "redisHost": "localhost",
            "redisPort": 6379,
            "redisDatabase": 0,
            "redisPassword": 123456,
            "dbActive": false
        }
    ],
    "logPath": "/Volumes/store/mysql_mcp_server",
    "logLevel": "info"
}
# dbActive
Only database instances with dbActive set to true in the dbList configuration list are available. 
# logPath
Mcp server log is stored in /Volumes/store/mysql_mcp_server/logs/mcp_server.log.
# logLevel
TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
```

### 3. Configure mcp json

```bash
{
  "mcpServers": {
    "redis-mcp-client": {
      "command": "redis-mcp-server3",
      "env": {
        "config_file": "/Users/frank/store/dbconfig.json"
      },
      "disabled": false
    }
  }
}

# config_file
dbconfig.json file path in your device
```

### 4. Clone the repository
```bash
git clone <repository-url>
cd mysql_mcp_server
import current project into your IDE Tool

```

### 5. Configure mcp json By IDE Tool
```bash
{
  "mcpServers": {
    "redis-mcp-client": {
      "command": "uv",
      "args": [
        "run",
        "src/server.py"
      ],
      "cwd": "/Volumes/store/redis_mcp_server",
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

## 🚀 Quick Start

### Start the MCP Server
```bash
# Using the installed package
redis-mcp-server

# Using fastmcp CLI
fastmcp run src/server.py

# Or directly with Python
python src/server.py
```

### Using with MCP Clients
The server provides the following MCP tools and resources:

#### Tools
- `sql_exec`: Execute any SQL statement
- `describe_table`: Get table structure information
- `generate_demo_data`: Generate test data for tables

#### Resources
- `database://tables`: Database table metadata
- `database://config`: Database configuration information

## 📚 API Reference

### SQL Execution Tool
```python
await sql_exec("SELECT * FROM users WHERE age > 18")
```

**Parameters:**
- `sql` (str): SQL statement to execute

**Returns:**
- `success` (bool): Execution status
- `result`: Query results or affected rows
- `message` (str): Status description

### Table Structure Tool
```python
await describe_table("users")
```

**Parameters:**
- `table_name` (str): Table name (supports `database.table` format)

**Returns:**
- Table structure information including columns, types, and constraints

### Test Data Generation
```python
await generate_demo_data("users", ["name", "email"], 50)
```

**Parameters:**
- `table_name` (str): Target table name
- `columns_name` (List[str]): Column names to populate
- `num` (int): Number of test records to generate

## ⚙️ Configuration

### Database Configuration
The `dbconfig.json` file supports multiple database instances:

```json
{
    "dbPoolSize": 5,           // Minimum connection pool size
    "dbMaxOverflow": 10,       // Maximum overflow connections
    "dbPoolTimeout": 30,       // Connection timeout in seconds
    "dbList": [
        {
            "dbInstanceId": "unique_id",
            "dbHost": "hostname",
            "dbPort": 3306,
            "dbDatabase": "database_name",
            "dbUsername": "username",
            "dbPassword": "password",
            "dbType": "MySQL",
            "dbVersion": "8.0",
            "dbActive": true    // Only one instance should be active
        },
        {
            "dbInstanceId": "unique_id",
            "dbHost": "hostname",
            "dbPort": 3306,
            "dbDatabase": "database_name",
            "dbUsername": "username",
            "dbPassword": "password",
            "dbType": "MySQL",
            "dbVersion": "5.7",
            "dbActive": false    // othre one instance should be unactive
        }
    ],
    "logPath": "/path/to/logs",
    "logLevel": "info"
}
```

### Logging Configuration
- **Log Levels**: TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
- **Log Rotation**: 10 MB per file, 7 days retention
- **Output**: Both stderr (for MCP) and file logging

## 🔒 Security Features

### Query Restrictions
- **Read-only Queries**: `execute_query_with_limit` only allows SELECT statements
- **Automatic LIMIT**: Prevents excessive data retrieval (max 10,000 rows)
- **Parameter Validation**: Input validation for all parameters

### Configuration Security
- **Password Hiding**: Sensitive information is masked in responses
- **Instance Isolation**: Only active database configuration is exposed
- **Environment Override**: Secure configuration file path management

## 🏗️ Architecture

### Project Structure
```
src/
├── server.py              # MCP server main entry point
├── utils/                 # Utility modules
│   ├── db_config.py       # Database configuration management
│   ├── db_pool.py         # Connection pool management
│   ├── db_operate.py      # Database operations
│   ├── logger_util.py     # Logging management
│   └── __init__.py        # Module initialization
├── resources/             # MCP resources
│   └── db_resources.py    # Database resources
└── tools/                 # MCP tools
    └── db_tool.py         # Database tools
```

### Key Components

#### Database Connection Pool
- **Singleton Pattern**: Ensures single pool instance
- **Async Management**: Non-blocking connection handling
- **Automatic Cleanup**: Connection release and pool management

#### Configuration Management
- **JSON-based**: Human-readable configuration format
- **Environment Override**: Flexible configuration management
- **Validation**: Required field validation and error handling

#### Logging System
- **Unified Interface**: Single logger instance across modules
- **Configurable Output**: File and console logging
- **Structured Format**: Timestamp, level, module, function, and line information

## 🧪 Testing

### Generate Test Data
```python
# Generate 100 test records for users table
await generate_demo_data("users", ["name", "email", "phone"], 100)
```

### Test Database Connection
```python
# Test basic SQL execution
result = await sql_exec("SELECT 1 as test")
print(result)  # {'success': True, 'result': [{'test': 1}]}
```

## 📊 Monitoring

### Database Status
```python
# Get database configuration
config = await get_database_config()
print(f"Database: {config['dbType']} {config['dbVersion']}")

# Get table information
tables = await get_database_tables()
print(f"Total tables: {len(tables)}")
```

### Connection Pool Status
- Pool size and overflow configuration
- Connection timeout settings
- Active connection count

## 🚨 Troubleshooting

### Common Issues

#### Connection Errors
```bash
# Check database connectivity
mysql -h localhost -P 3306 -u username -p database_name

# Verify configuration
python -c "from src.utils.db_config import load_db_config; print(load_db_config())"
```

#### Permission Issues
- Ensure database user has necessary privileges
- Check firewall and network access
- Verify database server is running

#### Configuration Errors
- Validate JSON syntax in `dbconfig.json`
- Check file permissions
- Verify environment variables

### Debug Mode
Set log level to DEBUG in configuration:
```json
{
    "logLevel": "debug"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install in development mode with all dependencies
pip install -e ".[dev,test,docs]"

# Run with debug logging
export LOG_LEVEL=debug
python src/server.py
```

### Code Quality Tools
```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Frank Jin** - *Initial work* - [j00131120@163.com](mailto:j00131120@163.com)

## 🙏 Acknowledgments

- [FastMCP](https://github.com/fastmcp/fastmcp) - MCP framework
- [aiomysql](https://github.com/aio-libs/aiomysql) - Async MySQL driver
- [loguru](https://github.com/Delgan/loguru) - Logging library

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact: [j00131120@163.com](mailto:j00131120@163.com)

## 🔄 Changelog

### v1.0.0
- Initial release
- MCP protocol support
- Multi-database compatibility
- Async connection pooling
- Security features implementation

## 📦 Building and Distribution

### Build the Package
```bash
# Clean and build
python build.py build

# Build and check
python build.py check

# Build and test installation
python build.py test

# Complete build process
python build.py all
```

### Publish to PyPI
```bash
# Build, test, and publish
python build.py publish

# Or manually
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```

### Package Information
- **Package Name**: `mysql-server-mcp`
- **Entry Point**: `mysql-mcp-server`
- **MCP Server Entry Point**: `mysql`
- **Python Version**: >= 3.12
- **License**: MIT