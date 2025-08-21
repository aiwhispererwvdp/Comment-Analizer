"""
Test configuration management package
"""

from .test_config import (
    EnvironmentType,
    DataSize,
    Config,
    DatabaseConfig,
    APIConfig,
    PerformanceConfig,
    DataConfig,
    SecurityConfig,
    MockConfig,
    ReportConfig,
    ConfigManager,
    ConfigContext,
    config_manager,
    get_test_config,
    set_test_environment,
    update_test_config,
)

# Backward compatibility aliases
TestEnvironment = EnvironmentType
TestConfig = Config
TestConfigManager = ConfigManager
TestConfigContext = ConfigContext

__all__ = [
    'TestEnvironment',
    'DataSize',
    'TestConfig',
    'DatabaseConfig',
    'APIConfig',
    'PerformanceConfig',
    'DataConfig',
    'SecurityConfig',
    'MockConfig',
    'ReportConfig',
    'TestConfigManager',
    'TestConfigContext',
    'config_manager',
    'get_test_config',
    'set_test_environment',
    'update_test_config',
]