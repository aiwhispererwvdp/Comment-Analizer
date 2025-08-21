"""
Centralized configuration management for the application.
All settings are loaded from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache
from dotenv import load_dotenv
import logging

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

logger = logging.getLogger(__name__)


class Settings:
    """Application configuration settings"""
    
    # Application Info
    APP_NAME: str = "Personal Paraguay Fiber Comments Analysis"
    APP_VERSION: str = "2.0.0"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    CACHE_DIR: Path = DATA_DIR / "cache"
    OUTPUTS_DIR: Path = BASE_DIR / "outputs"
    REPORTS_DIR: Path = OUTPUTS_DIR / "reports"
    EXPORTS_DIR: Path = OUTPUTS_DIR / "exports"
    VISUALIZATIONS_DIR: Path = OUTPUTS_DIR / "visualizations"
    
    # API Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    AZURE_TEXT_ANALYTICS_KEY: Optional[str] = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    AZURE_TEXT_ANALYTICS_ENDPOINT: Optional[str] = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Language Settings
    PRIMARY_LANGUAGE: str = os.getenv("PRIMARY_LANGUAGE", "es")
    SECONDARY_LANGUAGE: str = os.getenv("SECONDARY_LANGUAGE", "gn")
    TARGET_LANGUAGE: str = os.getenv("TARGET_LANGUAGE", "es")
    
    # Analysis Settings
    SENTIMENT_CONFIDENCE_THRESHOLD: float = float(os.getenv("SENTIMENT_CONFIDENCE_THRESHOLD", "0.7"))
    TRANSLATION_CONFIDENCE_THRESHOLD: float = float(os.getenv("TRANSLATION_CONFIDENCE_THRESHOLD", "0.8"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    DUPLICATE_SIMILARITY_THRESHOLD: float = float(os.getenv("DUPLICATE_SIMILARITY_THRESHOLD", "0.95"))
    
    # Performance Settings
    MAX_MEMORY_MB: int = int(os.getenv("MAX_MEMORY_MB", "1024"))
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    PARALLEL_WORKERS: int = int(os.getenv("PARALLEL_WORKERS", "4"))
    
    # Security Settings
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_ROWS: int = int(os.getenv("MAX_ROWS", "20000"))
    
    # Streamlit Settings
    DASHBOARD_TITLE: str = "Personal Paraguay - Customer Comments Analysis"
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", "8501"))
    LAYOUT: str = "wide"
    INITIAL_SIDEBAR_STATE: str = "expanded"
    
    # File Upload Settings
    SUPPORTED_EXTENSIONS: list = ['.xlsx', '.xls', '.csv', '.json', '.txt']
    
    # API Timeout Settings
    CONNECT_TIMEOUT: int = int(os.getenv("CONNECT_TIMEOUT", "10"))
    READ_TIMEOUT: int = int(os.getenv("READ_TIMEOUT", "60"))
    TOTAL_TIMEOUT: int = int(os.getenv("TOTAL_TIMEOUT", "120"))
    
    # Export Settings
    DEFAULT_EXPORT_FORMAT: str = os.getenv("DEFAULT_EXPORT_FORMAT", "xlsx")
    INCLUDE_VISUALIZATIONS: bool = os.getenv("INCLUDE_VISUALIZATIONS", "True").lower() == "true"
    COMPRESS_EXPORTS: bool = os.getenv("COMPRESS_EXPORTS", "True").lower() == "true"
    
    def __init__(self):
        """Initialize settings and create necessary directories"""
        self._create_directories()
        self._validate_settings()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        directories = [
            self.DATA_DIR,
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.CACHE_DIR,
            self.OUTPUTS_DIR,
            self.REPORTS_DIR,
            self.EXPORTS_DIR,
            self.VISUALIZATIONS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_settings(self) -> None:
        """Validate critical settings"""
        if not self.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. Some features may be limited.")
        
        if self.DEBUG:
            logger.warning("DEBUG mode is enabled. This should be disabled in production.")
        
        if self.MAX_MEMORY_MB < 512:
            logger.warning(f"MAX_MEMORY_MB is set to {self.MAX_MEMORY_MB}. This may be too low for large datasets.")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            key: getattr(self, key)
            for key in dir(self)
            if not key.startswith('_') and key.isupper()
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API-related configuration"""
        return {
            'openai_api_key': self.OPENAI_API_KEY,
            'azure_key': self.AZURE_TEXT_ANALYTICS_KEY,
            'azure_endpoint': self.AZURE_TEXT_ANALYTICS_ENDPOINT,
            'google_credentials': self.GOOGLE_APPLICATION_CREDENTIALS,
            'connect_timeout': self.CONNECT_TIMEOUT,
            'read_timeout': self.READ_TIMEOUT,
            'total_timeout': self.TOTAL_TIMEOUT,
            'max_retries': self.MAX_RETRIES
        }
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis-related configuration"""
        return {
            'primary_language': self.PRIMARY_LANGUAGE,
            'secondary_language': self.SECONDARY_LANGUAGE,
            'sentiment_threshold': self.SENTIMENT_CONFIDENCE_THRESHOLD,
            'translation_threshold': self.TRANSLATION_CONFIDENCE_THRESHOLD,
            'batch_size': self.BATCH_SIZE,
            'duplicate_threshold': self.DUPLICATE_SIMILARITY_THRESHOLD,
            'parallel_workers': self.PARALLEL_WORKERS
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security-related configuration"""
        return {
            'rate_limit_enabled': self.RATE_LIMIT_ENABLED,
            'max_requests_per_minute': self.MAX_REQUESTS_PER_MINUTE,
            'session_timeout_minutes': self.SESSION_TIMEOUT_MINUTES,
            'max_file_size_mb': self.MAX_FILE_SIZE_MB,
            'max_rows': self.MAX_ROWS
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# For backwards compatibility with existing code
Config = Settings
validate_config = lambda: get_settings()._validate_settings()