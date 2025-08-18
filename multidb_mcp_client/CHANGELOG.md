# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive English and Chinese documentation (README.md, README_CN.md)
- Development mode configuration examples for MCP clients
- Enhanced installation instructions with PyPI and development options

### Changed
- Improved MCP client configuration examples with autoApprove settings
- Updated database configuration format with connection pool settings

## [0.1.0] - 2024-12-19

### Added
- **Core MCP Server**: FastMCP-based server with stdio transport
- **Universal SQL Tool**: `sql_exec(sql: str)` for executing any SQL statement
- **Table Introspection**: `describe_table(table_name: str)` for schema exploration
- **Test Data Generator**: `generate_demo_data()` for development testing
- **Database Resources**: 
  - `database://tables` - comprehensive table metadata
  - `database://config` - masked database configuration
- **Multi-Database Support**: MySQL, MariaDB, TiDB, OceanBase, AWS RDS/Aurora MySQL
- **HTTP Proxy Architecture**: Decoupled database access via remote HTTP service
- **Flexible Configuration**: Multi-instance database configuration with runtime switching
- **Async I/O**: Full asynchronous operation using aiohttp and asyncio
- **Structured Logging**: Comprehensive logging with loguru (stderr + rotating files)
- **Configuration Management**: 
  - Singleton pattern configuration loader
  - Environment variable override support (`config_file`)
  - Automatic log path normalization
- **CLI Integration**: 
  - Command-line entry point (`multidb-mcp-client`)
  - FastMCP CLI integration (`fastmcp run mysql`)

### Security
- **Password Masking**: Sensitive data hidden in resource responses
- **Configuration Isolation**: Only active database config exposed to resources
- **HTTP Client Security**: Support for custom headers and authentication

### Technical Details
- **Python 3.12+** requirement
- **Key Dependencies**:
  - `fastmcp>=2.11.2` - MCP framework
  - `aiohttp>=3.12.15` - Async HTTP client
  - `loguru>=0.7.3` - Structured logging
  - `mcp[cli]>=1.12.4` - MCP CLI tools
- **Project Structure**: Modular architecture with clear separation of concerns
- **Error Handling**: Comprehensive exception handling throughout the codebase

### Fixed
- **Async Operations**: Fixed missing `await` calls in `generate_database_tables()`
- **Resource Format**: Corrected resource return format to avoid double-wrapping
- **Code Quality**: 
  - Unified English comments and log messages
  - Fixed linter warnings
  - Improved type annotations

### Documentation
- **English README**: Comprehensive installation, configuration, and usage guide
- **Chinese README**: Complete localization with technical term translations
- **API Documentation**: Detailed tool and resource specifications
- **Security Guide**: Production deployment and security recommendations
- **Development Guide**: Project structure, code style, and contribution guidelines

### Configuration
- **Database Instances**: Support for multiple database configurations
- **Active Database Selection**: Single active instance via `dbActive: true`
- **Remote Service Integration**: HTTP POST to `multiDBServer` endpoint
- **Logging Configuration**: Configurable levels and output paths
- **Example Configuration**: Complete `dbconfig.json` template provided

### Remote Service Contract
- **Request Format**: Standardized JSON payload with SQL, params, and database instance
- **Response Format**: Consistent result structure for queries and modifications
- **Error Handling**: Proper error propagation from remote service

## [0.0.1] - 2024-12-15

### Added
- Initial project structure and basic MCP framework integration
- Core database configuration loading mechanism
- Basic HTTP client utilities
- Logging infrastructure setup

---

## Version Naming Convention

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version when making incompatible API changes
- **MINOR** version when adding functionality in a backwards compatible manner
- **PATCH** version when making backwards compatible bug fixes

## Release Notes

### v0.1.0 - Production Ready Release
This release marks the first production-ready version of the Multi-Database MCP Client. The system provides a robust, secure, and scalable solution for database access through the Model Context Protocol, with comprehensive documentation and security features suitable for production environments.

**Key Highlights:**
- ✅ Complete MCP tool and resource implementation
- ✅ Production-ready security features
- ✅ Comprehensive documentation in English and Chinese
- ✅ Flexible multi-database configuration
- ✅ Robust error handling and logging
- ✅ HTTP proxy architecture for scalability

**Migration Notes:**
- This is the initial stable release
- No breaking changes from previous development versions
- Configuration file format is stable and backward compatible

**Known Limitations:**
- Requires external `multiDBServer` service for SQL execution
- Database credentials stored in local configuration file
- Single active database instance at runtime

**Future Roadmap:**
- Direct database connection mode (bypass HTTP proxy)
- Enhanced security with credential vault integration
- Multiple active database instances
- Performance monitoring and metrics
- Connection pooling optimizations

## Support

For questions about releases or upgrade paths:
- **GitHub Issues**: [Report bugs or request features](https://github.com/j00131120/mcp_database_server/issues)
- **Documentation**: [Project Wiki](https://github.com/j00131120/mcp_database_server/wiki)
- **Email**: j00131120@163.com
