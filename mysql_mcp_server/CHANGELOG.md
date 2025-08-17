# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-08-17

### Added
- Enhanced type annotations for better code clarity and IDE support
- Improved error handling for configuration file validation
- Added comprehensive logging for configuration path resolution

### Changed
- **BREAKING**: Package name changed from `mysql-mcp-server` to `mysql-mcp-server3`
- **BREAKING**: Entry point command changed from `mysql-mcp-server` to `mysql-mcp-server3`
- Updated license configuration to use modern SPDX format (`license = "MIT"`)
- Removed deprecated license classifier `"License :: OSI Approved :: MIT License"`
- Fixed invalid PyPI classifier `"Topic :: Database :: Database Drivers"` → `"Topic :: Database"`

### Fixed
- **CRITICAL**: Fixed circular import issues between utility modules
- **CRITICAL**: Fixed environment variable `config_file` not being read in packaged version
- **CRITICAL**: Fixed configuration file path resolution in production builds
- Resolved import errors in `src.server` module
- Fixed `db_config_path` import issues in `logger_util.py`
- Corrected project path resolution in utility modules

### Technical Improvements
- Refactored `get_log_config()` function to return `tuple[str, str]`
- Enhanced `get_db_config_file()` function with file existence validation
- Improved error handling and logging for configuration loading
- Added warning logs for invalid environment variable paths
- Optimized module initialization to avoid runtime errors

### Dependencies
- Updated to use modern Python packaging standards
- Maintained compatibility with Python 3.12+
- All existing dependencies remain unchanged

## [1.0.0] - 2025-08-17

### Added
- Initial release of MySQL MCP Server
- Support for MySQL/MariaDB/TiDB/AWS OceanBase/RDS/Aurora MySQL databases
- Async database connection pooling
- Model Context Protocol (MCP) server implementation
- FastMCP integration for enhanced server capabilities
- Comprehensive logging system with configurable levels
- Database configuration management via JSON files
- Environment variable support for configuration paths

### Features
- **Database Operations**: Execute SQL queries with async support
- **Connection Pooling**: Configurable connection pool with timeout and overflow settings
- **Multi-Database Support**: Support for multiple database instances with active/inactive states
- **Logging**: Structured logging with file rotation and retention policies
- **Configuration**: Flexible configuration system with environment variable override
- **MCP Integration**: Full Model Context Protocol server implementation

### Technical Specifications
- **Python Version**: 3.12+
- **Async Support**: Full async/await support with aiomysql
- **Logging**: Loguru-based logging with configurable output
- **Configuration**: JSON-based configuration with environment variable support
- **Packaging**: Modern Python packaging with pyproject.toml

### Database Support
- **MySQL**: Full MySQL 8.0+ support
- **MariaDB**: MariaDB compatibility
- **TiDB**: TiDB database support
- **OceanBase**: AWS OceanBase integration
- **RDS/Aurora**: AWS RDS and Aurora MySQL support

### MCP Server Features
- **Tools**: SQL execution tool for database operations
- **Resources**: Database schema and configuration management
- **Transport**: stdio transport for MCP communication
- **FastMCP**: Enhanced server capabilities with FastMCP framework

---

## Migration Guide

### From 1.0.0 to 1.0.1

#### Package Name Change
```bash
# Old
pip install mysql-mcp-server

# New  
pip install mysql-mcp-server3
```

#### Command Change
```bash
# Old
mysql-mcp-server

# New
mysql-mcp-server3
```

#### Configuration Update
```json
{
  "mcpServers": {
    "xesql-mcp-client": {
      "command": "mysql-mcp-server3",  // Updated command
      "env": {
        "config_file": "/path/to/dbconfig.json"
      },
      "disabled": false
    }
  }
}
```

#### Environment Variable
```bash
# Set configuration file path
export config_file="/path/to/your/dbconfig.json"

# Run server
mysql-mcp-server3
```

---

## Support

For issues and questions:
- **GitHub Issues**: [Report Issues](https://github.com/j00131120/mcp_database_server/issues)
- **Documentation**: [README.md](README.md)
- **Configuration**: See `dbconfig.json` examples in the repository

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
