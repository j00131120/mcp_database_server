# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-01-14

### Added
- **Oracle Database Support**: Added `oracledb` driver for OceanBase Oracle compatibility mode
- **Enhanced Documentation**: Comprehensive README with installation, configuration, and troubleshooting
- **Multi-language Support**: Added Chinese documentation (README-zh.md)
- **Connection Pool Monitoring**: Enhanced logging and status tracking for connection pools
- **Test Data Generation Tool**: `generate_demo_data` for creating sample datasets

### Changed
- **Database Driver Architecture**: Dual-driver support for MySQL (`aiomysql`) and Oracle (`oracledb`) modes
- **Configuration System**: Enhanced validation and error handling for database configurations
- **Security Model**: Improved parameterized queries and transaction management
- **Logging System**: Enhanced structured logging with better error tracking
- **Package Metadata**: Updated keywords and classifiers for better PyPI discoverability

### Fixed
- **Configuration Path Resolution**: Fixed environment variable `config_file` handling
- **Connection Pool Stability**: Improved connection release and cleanup mechanisms
- **Error Handling**: Better exception handling across all database operations
- **Documentation Accuracy**: Corrected port numbers, package names, and configuration examples

### Technical Improvements
- **Async Architecture**: Fully asynchronous database operations with proper connection pooling
- **Type Safety**: Enhanced type annotations for better IDE support and code clarity
- **Resource Management**: Automatic connection cleanup and pool management
- **Error Recovery**: Robust error handling with automatic rollback mechanisms

### Dependencies
- Added `oracledb>=3.3.0` for Oracle database connectivity
- Updated `fastmcp>=2.11.3` for enhanced MCP server capabilities
- Maintained `aiomysql>=0.2.0` for MySQL compatibility
- All dependencies updated to latest stable versions

## [1.0.2] - 2025-01-10

### Added
- Enhanced logging configuration with file rotation and retention
- Improved database connection validation and error reporting
- Better support for multiple database instances configuration

### Changed
- Optimized connection pool performance and resource utilization
- Updated project URLs and repository references
- Improved error messages for configuration validation

### Fixed
- Fixed memory leaks in connection pool management
- Resolved timeout issues with long-running queries
- Corrected configuration loading edge cases

## [1.0.1] - 2025-01-08

### Added
- Enhanced type annotations for better code clarity and IDE support
- Improved error handling for configuration file validation
- Added comprehensive logging for configuration path resolution

### Changed
- **BREAKING**: Package name changed from `mysql-mcp-server` to `oceanbase-mcp-server3`
- **BREAKING**: Entry point command changed from `mysql-mcp-server` to `oceanbase-mcp-server3`
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

## [1.0.0] - 2025-01-05

### Added
- **Initial Release**: OceanBase MCP Server for Model Context Protocol integration
- **Database Support**: Full support for OceanBase (MySQL and Oracle modes)
- **MCP Protocol Implementation**: Complete MCP tools and resources
  - `sql_exec`: Universal SQL execution tool
  - `describe_table`: Table structure description tool
  - `generate_demo_data`: Test data generation tool
  - `database://tables`: Database table metadata resource
  - `database://config`: Database configuration resource
- **Async Database Operations**: High-performance async database connectivity
- **Connection Pooling**: Configurable connection pool with timeout and overflow settings
- **Configuration System**: JSON-based configuration with environment variable support
- **Logging System**: Comprehensive logging with configurable levels and file rotation
- **Security Features**: Parameterized queries, transaction management, and password masking

### Features
- **Multi-Database Support**: Support for multiple database instances with active/inactive states
- **FastMCP Integration**: Enhanced server capabilities with FastMCP framework
- **Environment Integration**: Flexible configuration file path management
- **Error Handling**: Robust error handling with detailed logging and recovery

### Technical Specifications
- **Python Version**: 3.12+
- **Async Support**: Full async/await support with aiomysql and oracledb
- **Logging**: Loguru-based logging with configurable output and rotation
- **Configuration**: JSON-based configuration with environment variable override
- **Packaging**: Modern Python packaging with pyproject.toml
- **Architecture**: Singleton pattern for connection pools and configuration management

### Database Support
- **OceanBase MySQL Mode**: Full MySQL protocol compatibility
- **OceanBase Oracle Mode**: Oracle SQL syntax and feature support
- **Connection Types**: TCP/IP connections with SSL support
- **Transaction Management**: Automatic commit/rollback with connection pooling

### MCP Server Features
- **Transport**: stdio transport for MCP communication
- **Tools**: SQL execution and database management tools
- **Resources**: Schema introspection and configuration management
- **Security**: Safe SQL execution with parameter binding

### Development Features
- **Development Mode**: uv and fastmcp support for development
- **Code Quality**: Type hints, docstrings, and comprehensive error handling
- **Testing**: Test data generation and database connectivity validation
- **Documentation**: Comprehensive README and API documentation

---

## Migration Guide

### From 1.0.2 to 1.0.3

#### Oracle Database Support
```json
{
    "dbType": "oracle",  // New Oracle mode support
    "dbHost": "localhost",
    "dbPort": 2881,
    // ... other config
}
```

#### Docker Integration
```bash
# Start OceanBase with full monitoring stack
docker-compose up -d

# Or use simple development setup
docker-compose -f docker-compose.simple.yml up -d
```

### From 1.0.1 to 1.0.2

#### Enhanced Configuration
- Improved connection pool settings validation
- Better error messages for configuration issues
- Enhanced logging for troubleshooting

### From 1.0.0 to 1.0.1

#### Package Name Change
```bash
# Old
pip install mysql-mcp-server

# New  
pip install oceanbase-mcp-server3
```

#### Command Change
```bash
# Old
mysql-mcp-server

# New
oceanbase-mcp-server3
```

#### Configuration Update
```json
{
  "mcpServers": {
    "oceanbase-mcp-client": {
      "command": "oceanbase-mcp-server3",  // Updated command
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
oceanbase-mcp-server3
```

---

## Breaking Changes

### v1.0.1
- **Package Name**: Changed from `mysql-mcp-server` to `oceanbase-mcp-server3`
- **Command Name**: Entry point command updated
- **Configuration**: Updated MCP client configuration required

### v1.0.3
- **Database Drivers**: Added Oracle driver dependency
- **Configuration Schema**: Enhanced validation may reject previously accepted configs
- **Port Defaults**: Standard OceanBase port (2881) used in examples

---

## Deprecated Features

### v1.0.1
- Old package name `mysql-mcp-server` (removed)
- Legacy license classifiers (updated to SPDX format)

---

## Security Updates

### v1.0.3
- Enhanced parameter validation and SQL injection prevention
- Improved connection pool security and resource isolation
- Better error message sanitization to prevent information leakage

### v1.0.1
- Fixed configuration file path security issues
- Enhanced environment variable validation
- Improved error handling to prevent sensitive data exposure

---

## Performance Improvements

### v1.0.3
- Optimized connection pool management for better resource utilization
- Enhanced async operation performance with improved error handling
- Better memory management in long-running operations

### v1.0.2
- Reduced connection pool overhead
- Optimized query execution performance
- Improved memory usage patterns

---

## Known Issues

### v1.0.3
- Oracle mode requires proper OceanBase Oracle compatibility configuration
- Docker setup requires minimum 8GB RAM for optimal performance
- Some Oracle-specific SQL syntax may need validation

### Workarounds
- Use MySQL mode for maximum compatibility
- Refer to OceanBase documentation for Oracle mode setup
- Monitor Docker container resources during development

---

## Support

For issues and questions:
- **GitHub Issues**: [Report Issues](https://github.com/j00131120/mcp_database_server/issues)
- **Documentation**: [README.md](README.md) | [README-zh.md](README-zh.md)
- **Configuration**: See `dbconfig.json` examples in the repository
- **Docker Support**: See docker-compose documentation for container setup

---

## Contributors

- **Frank Jin** - *Project Author and Maintainer* - [j00131120@163.com](mailto:j00131120@163.com)

## Acknowledgments

- [OceanBase](https://www.oceanbase.com/) - Database platform
- [FastMCP](https://github.com/fastmcp/fastmcp) - MCP framework
- [aiomysql](https://github.com/aio-libs/aiomysql) - Async MySQL driver
- [oracledb](https://oracle.github.io/python-oracledb/) - Oracle Database driver
- [loguru](https://github.com/Delgan/loguru) - Logging library

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.