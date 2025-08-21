# Configuration Guide

This guide covers all configuration options for the Personal Paraguay Fiber Comments Analysis System, from basic API setup to advanced performance tuning.

## 🔧 Basic Configuration

### Environment Variables Setup

#### Required Configuration
Create a `.env` file in the project root directory:

```env
# OpenAI API Configuration (Required)
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# Application Settings
APP_NAME=Personal Paraguay Analysis
APP_VERSION=1.0.0
DEBUG_MODE=False

# Performance Settings
BATCH_SIZE=100
CACHE_TTL=3600
MAX_CONCURRENT_REQUESTS=10
```

#### Optional Configuration
```env
# Advanced OpenAI Settings
OPENAI_TEMPERATURE=0.1
OPENAI_TOP_P=0.95
OPENAI_FREQUENCY_PENALTY=0.0
OPENAI_PRESENCE_PENALTY=0.0

# File Upload Settings
MAX_FILE_SIZE_MB=200
ALLOWED_FILE_TYPES=xlsx,csv,json,txt
UPLOAD_TIMEOUT_SECONDS=300

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=analysis.log
LOG_MAX_SIZE_MB=50
LOG_BACKUP_COUNT=5

# Security Settings
RATE_LIMIT_ENABLED=True
INPUT_VALIDATION_ENABLED=True
SESSION_TIMEOUT_MINUTES=30
```

### API Key Configuration

#### Getting an OpenAI API Key
1. **Visit OpenAI Platform**: Go to [platform.openai.com](https://platform.openai.com)
2. **Create Account**: Sign up or log in to your account
3. **Navigate to API Keys**: Go to "API Keys" in the left sidebar
4. **Create New Key**: Click "Create new secret key"
5. **Copy Key**: Copy the key (starts with "sk-")
6. **Add to .env**: Paste into your `.env` file

#### API Key Security Best Practices
```env
# ✅ Correct format
OPENAI_API_KEY=sk-your-actual-key-here

# ❌ Don't include quotes
OPENAI_API_KEY="sk-your-key"

# ❌ Don't add spaces
OPENAI_API_KEY= sk-your-key

# ❌ Don't commit to version control
# Add .env to .gitignore file
```

### Model Configuration

#### OpenAI Model Options
```env
# GPT-4 (Recommended)
OPENAI_MODEL=gpt-4
# Best accuracy, higher cost

# GPT-3.5 Turbo (Budget-friendly)
OPENAI_MODEL=gpt-3.5-turbo
# Good accuracy, lower cost

# GPT-4 Turbo (Latest)
OPENAI_MODEL=gpt-4-turbo-preview
# Latest features, variable cost
```

## ⚙️ Application Configuration

### Performance Settings

#### Batch Processing Configuration
```env
# Batch Size (comments per batch)
BATCH_SIZE=100          # Conservative (stable)
BATCH_SIZE=200          # Aggressive (faster)
BATCH_SIZE=50           # Safe (slower)

# Concurrent Processing
MAX_CONCURRENT_REQUESTS=10     # Default
MAX_CONCURRENT_REQUESTS=5      # Conservative
MAX_CONCURRENT_REQUESTS=15     # Aggressive

# Timeout Settings
API_TIMEOUT_SECONDS=30         # API request timeout
BATCH_TIMEOUT_SECONDS=300      # Batch processing timeout
```

#### Memory Management
```env
# Cache Settings
CACHE_ENABLED=True
CACHE_TTL=3600                 # 1 hour cache
CACHE_MAX_SIZE=1000            # Max cached items

# Memory Limits
MAX_MEMORY_MB=2048             # 2GB memory limit
GARBAGE_COLLECTION_INTERVAL=100 # Clean up every 100 batches
```

### User Interface Configuration

#### Streamlit Settings
```env
# Server Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_SERVER_HEADLESS=False

# Theme Settings
STREAMLIT_THEME_PRIMARY_COLOR=#FF6B6B
STREAMLIT_THEME_BACKGROUND_COLOR=#FFFFFF
STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#F0F2F6
STREAMLIT_THEME_TEXT_COLOR=#262730
```

#### Interface Customization
```env
# Application Branding
COMPANY_NAME=Personal Paraguay
COMPANY_LOGO_URL=assets/logo.png
BRAND_COLOR=#FF6B6B

# Feature Toggles
ENABLE_DARK_MODE=True
ENABLE_MOBILE_RESPONSIVE=True
ENABLE_COST_MONITORING=True
ENABLE_ADVANCED_ANALYTICS=True
```

## 🔒 Security Configuration

### Input Validation Settings
```env
# File Upload Security
MAX_FILE_SIZE_MB=200
ALLOWED_MIME_TYPES=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv,application/json,text/plain
SCAN_UPLOADS_FOR_MALWARE=True

# Content Validation
MIN_COMMENT_LENGTH=10
MAX_COMMENT_LENGTH=5000
ALLOW_HTML_CONTENT=False
STRIP_PERSONAL_INFO=True
```

### Rate Limiting
```env
# API Rate Limiting
RATE_LIMIT_ENABLED=True
REQUESTS_PER_MINUTE=60
REQUESTS_PER_HOUR=1000
RATE_LIMIT_STORAGE=memory

# User Session Limits
MAX_SESSIONS_PER_USER=3
SESSION_TIMEOUT_MINUTES=30
CONCURRENT_ANALYSES_LIMIT=2
```

## 📊 Analysis Configuration

### Sentiment Analysis Settings
```env
# Analysis Depth
DEFAULT_ANALYSIS_DEPTH=standard    # basic, standard, comprehensive
ENABLE_EMOTION_ANALYSIS=True
ENABLE_THEME_DETECTION=True
ENABLE_LANGUAGE_DETECTION=True

# Confidence Thresholds
MIN_SENTIMENT_CONFIDENCE=0.7
MIN_THEME_CONFIDENCE=0.6
MIN_LANGUAGE_CONFIDENCE=0.8

# Cultural Context
CULTURAL_CONTEXT=paraguayan
DIALECT_ADAPTATION=True
REGIONAL_LANGUAGE_SUPPORT=guarani,spanish
```

### Language Processing
```env
# Language Settings
PRIMARY_LANGUAGE=spanish
SECONDARY_LANGUAGE=guarani
ENABLE_TRANSLATION=True
TRANSLATION_QUALITY_THRESHOLD=0.8

# Text Processing
ENABLE_TEXT_CLEANING=True
REMOVE_STOPWORDS=True
NORMALIZE_UNICODE=True
HANDLE_MIXED_LANGUAGES=True
```

## 💰 Cost Management Configuration

### Budget Controls
```env
# Budget Settings
ENABLE_COST_TRACKING=True
DEFAULT_DAILY_BUDGET=50.00
DEFAULT_MONTHLY_BUDGET=1000.00
BUDGET_CURRENCY=USD

# Alert Thresholds
BUDGET_ALERT_75_PERCENT=True
BUDGET_ALERT_90_PERCENT=True
BUDGET_ALERT_100_PERCENT=True
AUTO_STOP_AT_BUDGET=True

# Cost Optimization
ENABLE_DUPLICATE_DETECTION=True
ENABLE_SMART_SAMPLING=True
CACHE_SIMILAR_REQUESTS=True
```

### Usage Analytics
```env
# Usage Tracking
TRACK_API_USAGE=True
TRACK_USER_BEHAVIOR=True
TRACK_PERFORMANCE_METRICS=True
ANALYTICS_RETENTION_DAYS=90

# Cost Reporting
GENERATE_COST_REPORTS=True
COST_REPORT_FREQUENCY=weekly
EMAIL_COST_REPORTS=False
```

## 📝 Logging and Monitoring

### Logging Configuration
```env
# Log Levels
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE=True
LOG_TO_CONSOLE=True

# Log File Settings
LOG_FILE=logs/analysis.log
LOG_MAX_SIZE_MB=50
LOG_BACKUP_COUNT=5
LOG_ROTATION_INTERVAL=daily

# Component Logging
LOG_API_REQUESTS=True
LOG_USER_ACTIONS=True
LOG_PERFORMANCE_METRICS=True
LOG_ERROR_STACK_TRACES=True
```

### Performance Monitoring
```env
# Metrics Collection
ENABLE_METRICS=True
METRICS_RETENTION_DAYS=30
TRACK_RESPONSE_TIMES=True
TRACK_ERROR_RATES=True

# Health Checks
ENABLE_HEALTH_CHECKS=True
HEALTH_CHECK_INTERVAL=60
ALERT_ON_HEALTH_ISSUES=True
```

## 🔧 Advanced Configuration

### Database Configuration
```env
# Database Settings (if using database storage)
DATABASE_URL=sqlite:///data/analysis.db
DATABASE_POOL_SIZE=10
DATABASE_TIMEOUT=30

# Data Retention
ANALYSIS_DATA_RETENTION_DAYS=90
LOG_DATA_RETENTION_DAYS=30
CACHE_DATA_RETENTION_HOURS=24
```

### Export Configuration
```env
# Export Settings
DEFAULT_EXPORT_FORMAT=excel
EXCEL_INCLUDE_CHARTS=True
EXCEL_INCLUDE_PIVOT_TABLES=True
CSV_ENCODING=utf-8

# Report Customization
COMPANY_LOGO_IN_REPORTS=True
CUSTOM_REPORT_HEADER=Personal Paraguay Analysis Report
REPORT_FOOTER_TEXT=Generated by AI Analysis System
```

### Integration Settings
```env
# External Integrations
ENABLE_WEBHOOK_NOTIFICATIONS=False
WEBHOOK_URL=https://your-webhook-url.com
WEBHOOK_SECRET=your-webhook-secret

# API Endpoints
ENABLE_REST_API=False
API_BASE_URL=/api/v1
API_AUTHENTICATION=api_key
```

## 🚀 Environment-Specific Configuration

### Development Environment
```env
# Development Settings
DEBUG_MODE=True
LOG_LEVEL=DEBUG
ENABLE_PROFILING=True
MOCK_API_CALLS=False

# Development Features
ENABLE_DEBUG_TOOLBAR=True
AUTO_RELOAD_CODE=True
SHOW_SQL_QUERIES=True
```

### Production Environment
```env
# Production Settings
DEBUG_MODE=False
LOG_LEVEL=INFO
ENABLE_PROFILING=False
SECURE_COOKIES=True

# Production Optimizations
ENABLE_COMPRESSION=True
ENABLE_CACHING=True
MINIFY_RESPONSES=True
USE_CDN=True
```

### Testing Environment
```env
# Testing Settings
TESTING_MODE=True
USE_TEST_DATABASE=True
MOCK_EXTERNAL_APIS=True
DISABLE_RATE_LIMITING=True

# Test Data
TEST_DATA_PATH=tests/data
GENERATE_TEST_REPORTS=True
```

## 🔍 Configuration Validation

### Validation Script
Run the configuration validation script to check your setup:

```bash
# Validate configuration
python scripts/validate_config.py

# Expected output:
# ✅ OpenAI API key configured correctly
# ✅ Environment variables loaded
# ✅ File permissions correct
# ✅ Required directories exist
# ✅ Dependencies installed
# Configuration validation PASSED
```

### Common Configuration Issues

#### Issue: Invalid API Key Format
```env
# ❌ Wrong
OPENAI_API_KEY=invalid-key-format

# ✅ Correct
OPENAI_API_KEY=sk-proj-1234567890abcdef...
```

#### Issue: Missing Required Variables
```bash
# Check for missing variables
python -c "import os; print('Missing:' if not os.getenv('OPENAI_API_KEY') else 'OK')"
```

#### Issue: Invalid File Paths
```env
# ❌ Wrong (backslashes on Windows)
LOG_FILE=logs\analysis.log

# ✅ Correct (forward slashes work everywhere)
LOG_FILE=logs/analysis.log
```

## 📚 Configuration Templates

### Minimal Configuration (.env.minimal)
```env
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4
BATCH_SIZE=100
LOG_LEVEL=INFO
```

### Production Configuration (.env.production)
```env
# Production optimized settings
OPENAI_API_KEY=your-production-key
OPENAI_MODEL=gpt-4
BATCH_SIZE=200
MAX_CONCURRENT_REQUESTS=15
CACHE_ENABLED=True
CACHE_TTL=7200
DEBUG_MODE=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
AUTO_STOP_AT_BUDGET=True
```

### Development Configuration (.env.development)
```env
# Development friendly settings
OPENAI_API_KEY=your-development-key
OPENAI_MODEL=gpt-3.5-turbo
BATCH_SIZE=50
MAX_CONCURRENT_REQUESTS=5
DEBUG_MODE=True
LOG_LEVEL=DEBUG
CACHE_ENABLED=False
RATE_LIMIT_ENABLED=False
```

---

## 🆘 Need Help?

For configuration assistance:
- **[Installation Guide](../deployment/installation-guide.md)** - Setup instructions
- **[Troubleshooting](../deployment/troubleshooting.md)** - Common issues
- **[Support](mailto:support@personal.com.py)** - Technical assistance