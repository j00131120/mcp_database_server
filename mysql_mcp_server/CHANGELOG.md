# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive packaging configuration
- Build automation scripts
- Development tools integration
- Code quality tools (black, isort, flake8, mypy)
- Pre-commit hooks
- Makefile for common tasks
- Test coverage reporting
- Documentation build system

### Changed
- Enhanced pyproject.toml with complete packaging metadata
- Improved project structure and organization
- Added optional dependencies for development, testing, and documentation

## [1.0.0] - 2025-01-XX

### Added
- Initial release of MySQL MCP Server
- Model Context Protocol (MCP) support
- Multi-database compatibility (MySQL, MariaDB, TiDB, OceanBase, AWS RDS, Aurora MySQL)
- Asynchronous database operations with aiomysql
- Connection pooling with configurable settings
- Comprehensive MCP tools:
  - `sql_exec`: Universal SQL execution tool
  - `describe_table`: Table structure description tool
  - `execute_query_with_limit`: Limited query execution with security features
  - `generate_demo_data`: Test data generation tool
- MCP resources:
  - `database://tables`: Database table metadata
  - `database://config`: Database configuration information
- Security features:
  - Query type restrictions
  - Automatic LIMIT enforcement
  - Parameter validation
  - Sensitive information hiding
- Configuration management:
  - JSON-based configuration
  - Environment variable support
  - Multi-instance database support
- Logging system:
  - Unified logging interface
  - Configurable log levels
  - File and console output
  - Log rotation and retention

### Technical Features
- Python 3.12+ support
- Async/await architecture
- Singleton pattern for configuration and connection pool
- Comprehensive error handling and logging
- Type hints and documentation
- Modular and extensible design

### Dependencies
- fastmcp >= 2.11.3
- aiomysql >= 0.2.0
- mcp[cli] >= 1.12.4
- loguru >= 0.7.3

---

## Version History

- **1.0.0**: Initial release with full MCP protocol support and multi-database compatibility

## Release Process

1. Update version in `pyproject.toml`
2. Update version in `src/__init__.py`
3. Update version in `README.md`
4. Create git tag
5. Build and test package
6. Publish to PyPI
7. Update CHANGELOG.md

## Contributing

When contributing to this project, please:

1. Add your changes to the appropriate section in the [Unreleased] section
2. Use the following categories:
   - **Added**: for new features
   - **Changed**: for changes in existing functionality
   - **Deprecated**: for soon-to-be removed features
   - **Removed**: for now removed features
   - **Fixed**: for any bug fixes
   - **Security**: for security vulnerability fixes
3. Follow the existing format and style
4. Include relevant issue numbers or pull request references
