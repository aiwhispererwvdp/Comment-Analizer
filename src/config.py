"""
Configuration settings for Personal Paraguay Fiber Comments Analysis System
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Language Settings
    PRIMARY_LANGUAGE = "es"  # Spanish
    SECONDARY_LANGUAGE = "gn"  # Guarani
    TARGET_LANGUAGE = "es"  # Translate to Spanish
    
    # Analysis Settings
    SENTIMENT_CONFIDENCE_THRESHOLD = 0.7
    TRANSLATION_CONFIDENCE_THRESHOLD = 0.8
    BATCH_SIZE = 100
    MAX_RETRIES = 3
    
    # File Paths
    RAW_DATA_PATH = "data/raw/"
    PROCESSED_DATA_PATH = "data/processed/"
    OUTPUTS_PATH = "outputs/"
    
    # Dashboard Settings
    DASHBOARD_TITLE = "Personal Paraguay - Customer Comments Analysis"
    DASHBOARD_PORT = 8501
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation function
def validate_config():
    """Validate that required configuration is present"""
    required_keys = [
        "OPENAI_API_KEY"
    ]
    
    missing_keys = []
    for key in required_keys:
        if not getattr(Config, key):
            missing_keys.append(key)
    
    if missing_keys:
        import warnings
        warnings.warn(f"Missing environment variables: {missing_keys}. Some features may be limited.")
    
    return True