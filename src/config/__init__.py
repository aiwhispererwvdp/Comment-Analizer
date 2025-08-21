"""Configuration module for Personal Paraguay Fiber Comments Analysis System"""

from .settings import Settings, get_settings

# Create Config alias for backwards compatibility
Config = Settings

# Create validate_config function for backwards compatibility  
def validate_config():
    """Validate configuration settings"""
    settings = get_settings()
    settings._validate_settings()
    return True

__all__ = ['Settings', 'get_settings', 'Config', 'validate_config']