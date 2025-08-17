# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-08-17

### 🎉 **Major Release: PostgreSQL Migration & Complete Internationalization**

This is a **BREAKING CHANGE** release that transforms the MySQL MCP Server into a PostgreSQL-focused solution with complete English internationalization.

### 🔄 **Database Migration: MySQL → PostgreSQL**

#### Added
- **PostgreSQL Native Support**: Complete migration from MySQL to PostgreSQL using `asyncpg` driver
- **PostgreSQL Information Schema**: Native PostgreSQL schema queries using `information_schema` tables
- **PostgreSQL-Specific Features**: Support for PostgreSQL data types, functions, and syntax
- **RaseSQL Compatibility**: Added support for RaseSQL database alongside PostgreSQL
- **Multi-Database Configuration**: Support for multiple PostgreSQL/RaseSQL instances with active/inactive states

#### Changed
- **BREAKING**: Primary database support changed from MySQL to PostgreSQL
- **BREAKING**: Database driver changed from `aiomysql` to `asyncpg` 
- **BREAKING**: SQL syntax updated for PostgreSQL compatibility
- **BREAKING**: Parameter placeholders changed from `%s` to `$1, $2, $3...` format
- **BREAKING**: Connection pool configuration adapted for `asyncpg.create_pool()`

#### Removed
- **BREAKING**: MySQL/MariaDB/TiDB/OceanBase support discontinued
- **BREAKING**: `aiomysql` dependency removed
- **BREAKING**: MySQL-specific SQL commands and syntax

### 🌍 **Complete Internationalization**

#### Added
- **English-Only Codebase**: All Chinese comments, docstrings, and messages translated to English
- **Professional Documentation**: Class and method documentation in English
- **Standardized Logging**: All log messages converted to English
- **International Standards**: Code comments follow international development standards

#### Changed
- **Code Comments**: 100% Chinese → English translation across all Python files
- **Function Documentation**: Professional English docstrings for all methods and classes
- **Error Messages**: User-facing messages in English for global compatibility
- **Log Output**: Runtime logging unified in English language

### 📖 **Documentation Overhaul**

#### Added
- **Professional README**: Completely rewritten 600+ line README with:
  - Professional badges and visual enhancements
  - Comprehensive Table of Contents with anchor navigation
  - Detailed installation guides for multiple package managers
  - Complete API reference with examples
  - Security best practices and architecture documentation
  - Troubleshooting guide and contributing guidelines
- **Enhanced Code Examples**: PostgreSQL-specific configuration and usage examples
- **Multi-Installation Methods**: PyPI, source, and UV package manager support
- **Production Deployment**: Enterprise-ready configuration templates

#### Changed
- **README Structure**: Reorganized from 446 to 601 lines (+35% content)
- **Configuration Examples**: Updated all examples for PostgreSQL compatibility
- **API Documentation**: Detailed parameter descriptions and return value specifications
- **Quick Start Guide**: Streamlined 4-step deployment process

### 🔧 **Core System Improvements**

#### Connection Pool Enhancements
```python
# Before (MySQL/aiomysql)
max_inactive_connection_lifetime=pool_timeout

# After (PostgreSQL/asyncpg)
command_timeout=pool_timeout
```

#### SQL Operations Optimization
- **Query Execution**: Optimized for PostgreSQL syntax and performance
- **Parameter Binding**: Safe parameter binding using PostgreSQL placeholders
- **Result Processing**: Enhanced result formatting and type conversion
- **Error Handling**: PostgreSQL-specific error handling and reporting

#### Configuration System
- **Database Configuration**: Updated for PostgreSQL connection parameters
- **Multi-Instance Support**: Enhanced support for PostgreSQL and RaseSQL instances
- **Environment Variables**: Improved configuration override capabilities
- **Validation**: Comprehensive configuration validation for PostgreSQL

### 🛡️ **Security & Safety**

#### Added
- **PostgreSQL Security**: Database-specific security configurations
- **Query Validation**: Enhanced SQL query validation for PostgreSQL
- **Parameter Sanitization**: Improved input validation and sanitization
- **Connection Security**: SSL/TLS support for PostgreSQL connections

#### Enhanced
- **Password Protection**: Improved credential masking in logs and responses
- **Access Control**: Enhanced instance-based access management
- **Error Handling**: Secure error message formatting without information disclosure

### 🏗️ **Architecture Updates**

#### File Structure Changes
```
src/
├── server.py              # MCP server with PostgreSQL integration
├── utils/                 # Enhanced utilities
│   ├── db_config.py       # PostgreSQL configuration management
│   ├── db_pool.py         # asyncpg connection pool
│   ├── db_operate.py      # PostgreSQL operations
│   └── logger_util.py     # Internationalized logging
├── resources/             # PostgreSQL resources
│   └── db_resources.py    # PostgreSQL metadata resources
└── tools/                 # PostgreSQL tools
    └── db_tool.py         # PostgreSQL-specific tools
```

#### Component Updates
- **Database Pool**: Redesigned for asyncpg compatibility
- **Resource Management**: PostgreSQL information_schema integration
- **Tool Implementation**: PostgreSQL-specific SQL generation
- **Logging System**: English-only structured logging

### 📦 **Package & Deployment**

#### Changed
- **Package Description**: Updated to reflect PostgreSQL focus
- **Keywords**: Updated package keywords for PostgreSQL ecosystem
- **Dependencies**: Replaced `aiomysql` with `asyncpg>=0.30.0`
- **Entry Points**: Maintained `postgresql-mcp-server3` command consistency

#### Installation Options
```bash
# PyPI Installation
pip install postgresql-mcp-server3

# Source Installation
git clone https://github.com/j00131120/mcp_database_server.git
cd mcp_database_server/postgresql_mcp_server
pip install -e .

# UV Package Manager
uv add postgresql-mcp-server3
```

### 🧪 **Testing & Quality**

#### Added
- **PostgreSQL Testing**: Comprehensive test coverage for PostgreSQL operations
- **Connection Pool Testing**: Advanced pool testing with concurrent operations
- **Configuration Testing**: Validation testing for PostgreSQL configurations
- **Integration Testing**: End-to-end testing with PostgreSQL databases

#### Quality Improvements
- **Code Linting**: Fixed linting warnings and improved code quality
- **Type Annotations**: Enhanced type hints throughout codebase
- **Error Handling**: Robust error handling for PostgreSQL-specific scenarios

### 🔧 **Configuration Migration**

#### Database Configuration Format
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
        {
            "dbInstanceId": "rasesql_2",
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
```

#### MCP Client Configuration
```json
{
  "mcpServers": {
    "postgresql-mcp-client": {
      "command": "postgresql-mcp-server3",
      "env": {
        "config_file": "/path/to/dbconfig.json"
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

### 🚨 **Breaking Changes Summary**

| Component | v1.x (MySQL) | v2.0 (PostgreSQL) |
|-----------|--------------|-------------------|
| **Database** | MySQL/MariaDB/TiDB | PostgreSQL/RaseSQL |
| **Driver** | aiomysql | asyncpg |
| **Placeholders** | `%s` | `$1, $2, $3...` |
| **Schema Queries** | `SHOW TABLES`, `DESCRIBE` | `information_schema` |
| **Language** | Mixed Chinese/English | English Only |
| **Port** | 3306 | 5432 |

### 📋 **Migration Guide: v1.x → v2.0**

#### 1. Update Database
```bash
# Migrate from MySQL to PostgreSQL
# 1. Export MySQL data
mysqldump -u username -p database_name > backup.sql

# 2. Convert to PostgreSQL format (manual process)
# 3. Import to PostgreSQL
psql -U username -d database_name -f converted_backup.sql
```

#### 2. Update Configuration
```bash
# Update dbconfig.json
# Change dbType: "MySQL" → "PostgreSQL"
# Change dbPort: 3306 → 5432
# Update connection parameters
```

#### 3. Update Dependencies
```bash
# Uninstall old version
pip uninstall mysql-mcp-server3

# Install new version
pip install postgresql-mcp-server3
```

#### 4. Update Queries
```sql
-- OLD (MySQL)
SHOW TABLES;
DESCRIBE table_name;

-- NEW (PostgreSQL)
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'table_name';
```

---

## [1.0.0] - 2025-08-17 (Legacy MySQL Version)

### Added
- Initial MySQL MCP Server implementation
- Support for MySQL/MariaDB/TiDB/AWS OceanBase/RDS/Aurora MySQL
- Async database connection pooling with aiomysql
- Model Context Protocol (MCP) server implementation
- FastMCP framework integration
- Comprehensive logging system
- JSON-based configuration management

### Features
- **Database Operations**: MySQL-specific SQL execution
- **Connection Pooling**: aiomysql-based connection management
- **Multi-Database Support**: MySQL ecosystem compatibility
- **MCP Integration**: Full Model Context Protocol implementation
- **Logging**: Structured logging with Chinese/English mixed content

---

## 🆘 **Support & Resources**

### Documentation
- **Main Documentation**: [README.md](README.md) - Comprehensive guide
- **API Reference**: Detailed in README.md with examples
- **Configuration Guide**: Complete configuration documentation

### Community & Support
- **GitHub Issues**: [Report Issues](https://github.com/j00131120/mcp_database_server/issues)
- **Email Support**: [j00131120@163.com](mailto:j00131120@163.com)
- **Contributing**: See contributing guidelines in README.md

### Resources
- **PostgreSQL Documentation**: [postgresql.org](https://www.postgresql.org/docs/)
- **AsyncPG Guide**: [MagicStack/asyncpg](https://github.com/MagicStack/asyncpg)
- **FastMCP Framework**: [FastMCP Documentation](https://github.com/fastmcp/fastmcp)
- **Model Context Protocol**: [MCP Specification](https://github.com/modelcontextprotocol/specification)

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2025 Frank Jin**