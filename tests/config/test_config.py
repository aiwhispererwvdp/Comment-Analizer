"""
Test configuration management system
Provides centralized configuration for different test environments and scenarios
"""

import os
import json
import yaml
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from enum import Enum


class EnvironmentType(Enum):
    """Test environment types"""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    E2E = "e2e"
    LOAD = "load"
    SECURITY = "security"


class DataSize(Enum):
    """Test data size categories"""
    SMALL = "small"      # < 100 records
    MEDIUM = "medium"    # 100-1000 records
    LARGE = "large"      # 1000-10000 records
    XLARGE = "xlarge"    # > 10000 records


@dataclass
class DatabaseConfig:
    """Database configuration for tests"""
    url: str = "sqlite:///:memory:"
    driver: str = "sqlite"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    isolation_level: str = "READ_COMMITTED"


@dataclass
class APIConfig:
    """API configuration for tests"""
    base_url: str = "http://localhost:8000"
    timeout: int = 30
    retries: int = 3
    rate_limit: int = 100  # requests per minute
    api_key: Optional[str] = None
    use_mock: bool = True


@dataclass
class PerformanceConfig:
    """Performance testing configuration"""
    max_execution_time: float = 5.0
    max_memory_mb: float = 500.0
    min_throughput: float = 10.0
    max_cpu_percent: float = 80.0
    min_success_rate: float = 0.95
    stress_test_duration: int = 60
    max_concurrent_users: int = 50


@dataclass
class DataConfig:
    """Test data configuration"""
    sample_size: int = 100
    data_size: DataSize = DataSize.SMALL
    language: str = "es"
    include_noise: bool = False
    missing_data_ratio: float = 0.0
    duplicate_ratio: float = 0.0
    encoding: str = "utf-8"
    date_range_days: int = 30


@dataclass
class SecurityConfig:
    """Security testing configuration"""
    check_sql_injection: bool = True
    check_xss: bool = True
    check_csrf: bool = True
    check_auth: bool = True
    check_encryption: bool = True
    scan_secrets: bool = True
    allowed_vulnerabilities: List[str] = field(default_factory=list)


@dataclass
class MockConfig:
    """Mock configuration"""
    use_real_apis: bool = False
    openai_mock_delay: float = 0.1
    database_mock_delay: float = 0.01
    file_system_mock: bool = True
    network_mock: bool = True
    random_seed: int = 42


@dataclass
class ReportConfig:
    """Test reporting configuration"""
    output_dir: str = "test_reports"
    generate_html: bool = True
    generate_json: bool = True
    generate_plots: bool = True
    include_screenshots: bool = False
    verbose: bool = False
    save_artifacts: bool = True


@dataclass
class Config:
    """Main test configuration container"""
    environment: EnvironmentType = EnvironmentType.UNIT
    debug: bool = False
    parallel: bool = True
    max_workers: int = 4
    timeout: int = 300
    retry_failed: bool = True
    capture_logs: bool = True
    log_level: str = "INFO"
    
    # Sub-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    data: DataConfig = field(default_factory=DataConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    mock: MockConfig = field(default_factory=MockConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
    
    # Custom settings
    custom: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        result = asdict(self)
        # Convert enum values to strings
        result['environment'] = self.environment.value
        result['data']['data_size'] = self.data.data_size.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create configuration from dictionary"""
        # Handle enum conversions
        if 'environment' in data and isinstance(data['environment'], str):
            data['environment'] = EnvironmentType(data['environment'])
        
        if 'data' in data and 'data_size' in data['data'] and isinstance(data['data']['data_size'], str):
            data['data']['data_size'] = DataSize(data['data']['data_size'])
        
        # Create nested objects
        config = cls()
        
        # Update main fields
        for key, value in data.items():
            if hasattr(config, key) and key not in ['database', 'api', 'performance', 'data', 'security', 'mock', 'report']:
                setattr(config, key, value)
        
        # Update sub-configurations
        if 'database' in data:
            config.database = DatabaseConfig(**data['database'])
        if 'api' in data:
            config.api = APIConfig(**data['api'])
        if 'performance' in data:
            config.performance = PerformanceConfig(**data['performance'])
        if 'data' in data:
            config.data = DataConfig(**data['data'])
        if 'security' in data:
            config.security = SecurityConfig(**data['security'])
        if 'mock' in data:
            config.mock = MockConfig(**data['mock'])
        if 'report' in data:
            config.report = ReportConfig(**data['report'])
        
        return config


class ConfigManager:
    """Manages test configurations for different environments"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or "tests/config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self._configs = {}
        self._current_config = None
        
        # Load default configurations
        self._load_default_configs()
    
    def _load_default_configs(self):
        """Load default configurations for different environments"""
        
        # Unit test configuration
        unit_config = Config(
            environment=EnvironmentType.UNIT,
            parallel=True,
            max_workers=4,
            data=DataConfig(
                sample_size=50,
                data_size=DataSize.SMALL,
                include_noise=False
            ),
            mock=MockConfig(
                use_real_apis=False,
                openai_mock_delay=0.01,
                database_mock_delay=0.001
            ),
            performance=PerformanceConfig(
                max_execution_time=1.0,
                max_memory_mb=100.0
            )
        )
        
        # Integration test configuration
        integration_config = Config(
            environment=EnvironmentType.INTEGRATION,
            parallel=False,
            max_workers=2,
            data=DataConfig(
                sample_size=200,
                data_size=DataSize.MEDIUM,
                include_noise=True,
                missing_data_ratio=0.05
            ),
            mock=MockConfig(
                use_real_apis=False,
                file_system_mock=False,
                network_mock=True
            ),
            performance=PerformanceConfig(
                max_execution_time=10.0,
                max_memory_mb=200.0
            )
        )
        
        # Performance test configuration
        performance_config = Config(
            environment=EnvironmentType.PERFORMANCE,
            parallel=False,
            max_workers=1,
            timeout=600,
            data=DataConfig(
                sample_size=1000,
                data_size=DataSize.LARGE,
                include_noise=True
            ),
            mock=MockConfig(
                use_real_apis=False,
                openai_mock_delay=0.5
            ),
            performance=PerformanceConfig(
                max_execution_time=30.0,
                max_memory_mb=1000.0,
                stress_test_duration=120
            )
        )
        
        # End-to-end test configuration
        e2e_config = Config(
            environment=EnvironmentType.E2E,
            parallel=False,
            max_workers=1,
            timeout=900,
            data=DataConfig(
                sample_size=100,
                data_size=DataSize.MEDIUM,
                include_noise=True,
                missing_data_ratio=0.1
            ),
            mock=MockConfig(
                use_real_apis=True,
                file_system_mock=False,
                network_mock=False
            ),
            report=ReportConfig(
                generate_html=True,
                generate_plots=True,
                include_screenshots=True,
                save_artifacts=True
            )
        )
        
        # Load test configuration
        load_config = Config(
            environment=EnvironmentType.LOAD,
            parallel=True,
            max_workers=10,
            timeout=1800,
            data=DataConfig(
                sample_size=5000,
                data_size=DataSize.XLARGE
            ),
            performance=PerformanceConfig(
                stress_test_duration=300,
                max_concurrent_users=100
            )
        )
        
        # Security test configuration
        security_config = Config(
            environment=EnvironmentType.SECURITY,
            parallel=False,
            max_workers=1,
            data=DataConfig(
                sample_size=100,
                include_noise=True
            ),
            security=SecurityConfig(
                check_sql_injection=True,
                check_xss=True,
                check_csrf=True,
                check_auth=True,
                scan_secrets=True
            )
        )
        
        self._configs = {
            EnvironmentType.UNIT: unit_config,
            EnvironmentType.INTEGRATION: integration_config,
            EnvironmentType.PERFORMANCE: performance_config,
            EnvironmentType.E2E: e2e_config,
            EnvironmentType.LOAD: load_config,
            EnvironmentType.SECURITY: security_config
        }
        
        # Set default current config
        self._current_config = unit_config
    
    def get_config(self, environment: Optional[EnvironmentType] = None) -> Config:
        """Get configuration for specific environment"""
        if environment is None:
            return self._current_config
        
        return self._configs.get(environment, self._current_config)
    
    def set_current_environment(self, environment: EnvironmentType):
        """Set current test environment"""
        if environment in self._configs:
            self._current_config = self._configs[environment]
        else:
            raise ValueError(f"Unknown environment: {environment}")
    
    def update_config(self, environment: EnvironmentType, **kwargs):
        """Update configuration for specific environment"""
        if environment not in self._configs:
            raise ValueError(f"Unknown environment: {environment}")
        
        config = self._configs[environment]
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                config.custom[key] = value
    
    def save_config(self, environment: EnvironmentType, file_path: Optional[str] = None):
        """Save configuration to file"""
        if environment not in self._configs:
            raise ValueError(f"Unknown environment: {environment}")
        
        config = self._configs[environment]
        
        if file_path is None:
            file_path = self.config_dir / f"{environment.value}_config.json"
        
        config_dict = config.to_dict()
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
        
        print(f"Configuration saved to {file_path}")
    
    def load_config(self, file_path: str, environment: Optional[EnvironmentType] = None):
        """Load configuration from file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        if file_path.suffix.lower() in ['.yaml', '.yml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
        
        config = Config.from_dict(config_dict)
        
        if environment is None:
            environment = config.environment
        
        self._configs[environment] = config
        
        print(f"Configuration loaded from {file_path} for environment {environment.value}")
    
    def load_from_environment(self):
        """Load configuration from environment variables"""
        env_config = {}
        
        # Check for environment-specific configuration
        env_prefix = "TEST_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                
                # Try to parse as JSON for complex values
                try:
                    env_config[config_key] = json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    # Keep as string
                    env_config[config_key] = value
        
        # Update current configuration
        if env_config:
            for key, value in env_config.items():
                if hasattr(self._current_config, key):
                    setattr(self._current_config, key, value)
                else:
                    self._current_config.custom[key] = value
            
            print(f"Configuration updated from environment variables: {list(env_config.keys())}")
    
    def validate_config(self, environment: Optional[EnvironmentType] = None) -> List[str]:
        """Validate configuration and return list of issues"""
        config = self.get_config(environment)
        issues = []
        
        # Validate basic settings
        if config.max_workers <= 0:
            issues.append("max_workers must be positive")
        
        if config.timeout <= 0:
            issues.append("timeout must be positive")
        
        # Validate performance settings
        if config.performance.max_execution_time <= 0:
            issues.append("performance.max_execution_time must be positive")
        
        if config.performance.max_memory_mb <= 0:
            issues.append("performance.max_memory_mb must be positive")
        
        if not (0 <= config.performance.min_success_rate <= 1):
            issues.append("performance.min_success_rate must be between 0 and 1")
        
        # Validate data settings
        if config.data.sample_size <= 0:
            issues.append("data.sample_size must be positive")
        
        if not (0 <= config.data.missing_data_ratio <= 1):
            issues.append("data.missing_data_ratio must be between 0 and 1")
        
        if not (0 <= config.data.duplicate_ratio <= 1):
            issues.append("data.duplicate_ratio must be between 0 and 1")
        
        # Validate API settings
        if config.api.timeout <= 0:
            issues.append("api.timeout must be positive")
        
        if config.api.retries < 0:
            issues.append("api.retries must be non-negative")
        
        return issues
    
    def get_all_environments(self) -> List[EnvironmentType]:
        """Get list of all configured environments"""
        return list(self._configs.keys())
    
    def copy_config(self, source_env: EnvironmentType, target_env: EnvironmentType):
        """Copy configuration from one environment to another"""
        if source_env not in self._configs:
            raise ValueError(f"Source environment not found: {source_env}")
        
        # Deep copy the configuration
        source_config = self._configs[source_env]
        config_dict = source_config.to_dict()
        config_dict['environment'] = target_env.value
        
        target_config = Config.from_dict(config_dict)
        self._configs[target_env] = target_config
        
        print(f"Configuration copied from {source_env.value} to {target_env.value}")


# Global configuration manager instance
config_manager = ConfigManager()


# Convenience functions
def get_test_config(environment: Optional[EnvironmentType] = None) -> Config:
    """Get test configuration for current or specific environment"""
    return config_manager.get_config(environment)


def set_test_environment(environment: EnvironmentType):
    """Set current test environment"""
    config_manager.set_current_environment(environment)


def update_test_config(**kwargs):
    """Update current test configuration"""
    current_env = config_manager._current_config.environment
    config_manager.update_config(current_env, **kwargs)


# Context manager for temporary configuration changes
class ConfigContext:
    """Context manager for temporary configuration changes"""
    
    def __init__(self, environment: Optional[EnvironmentType] = None, **config_updates):
        self.environment = environment
        self.config_updates = config_updates
        self.original_config = None
        self.original_environment = None
    
    def __enter__(self):
        # Save original state
        self.original_environment = config_manager._current_config.environment
        self.original_config = config_manager.get_config()
        
        # Apply temporary changes
        if self.environment:
            config_manager.set_current_environment(self.environment)
        
        if self.config_updates:
            current_env = config_manager._current_config.environment
            config_manager.update_config(current_env, **self.config_updates)
        
        return config_manager.get_config()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original state
        config_manager._current_config = self.original_config
        config_manager.set_current_environment(self.original_environment)