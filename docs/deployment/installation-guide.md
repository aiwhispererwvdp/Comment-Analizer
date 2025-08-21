# Installation Guide

This guide provides comprehensive instructions for installing and configuring the Personal Paraguay Fiber Comments Analysis System in production and development environments.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM, recommended 8GB+
- **Storage**: Minimum 2GB free disk space
- **Network**: Internet connection for API access

### Software Dependencies
- **Python Package Manager**: pip (latest version)
- **Git**: For version control and updates
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### External Services
- **OpenAI API Account** with active credits
- **Internet Connection** for real-time analysis

## 🚀 Quick Installation

### Option 1: Automated Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-repo/Personal_Paraguay_Fiber_Comments_Analysis.git
cd Personal_Paraguay_Fiber_Comments_Analysis

# Run the automated setup script
python setup.py install

# Configure environment variables
python configure.py
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/Personal_Paraguay_Fiber_Comments_Analysis.git
cd Personal_Paraguay_Fiber_Comments_Analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env file with your API keys
```

## 🔧 Detailed Installation Steps

### Step 1: Environment Setup
```bash
# Check Python version
python --version
# Should show Python 3.8 or higher

# Update pip to latest version
python -m pip install --upgrade pip

# Install virtualenv if not available
pip install virtualenv
```

### Step 2: Project Download
```bash
# Option A: Git clone (recommended)
git clone https://github.com/your-repo/Personal_Paraguay_Fiber_Comments_Analysis.git
cd Personal_Paraguay_Fiber_Comments_Analysis

# Option B: Download ZIP file
# Download from GitHub releases page
# Extract to desired directory
# Navigate to extracted folder
```

### Step 3: Virtual Environment
```bash
# Create virtual environment
python -m venv analysis_env

# Activate virtual environment
# Windows PowerShell:
analysis_env\Scripts\Activate.ps1
# Windows Command Prompt:
analysis_env\Scripts\activate.bat
# macOS/Linux:
source analysis_env/bin/activate

# Verify virtual environment is active
which python  # Should show path to virtual environment
```

### Step 4: Dependencies Installation
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
pip list | grep openai
pip list | grep pandas

# Install additional development tools (optional)
pip install -r requirements-dev.txt
```

### Step 5: Configuration Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration file
# Windows:
notepad .env
# macOS:
nano .env
# Linux:
vim .env
```

### Required Environment Variables
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
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

# File Upload Settings
MAX_FILE_SIZE_MB=200
ALLOWED_FILE_TYPES=xlsx,csv,json,txt

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=analysis.log
```

## 🧪 Installation Verification

### Step 1: Configuration Test
```bash
# Run configuration test
python test_config.py

# Expected output:
# ✓ OpenAI API key configured
# ✓ Environment variables loaded
# ✓ Required directories exist
# ✓ Dependencies installed
# Configuration test PASSED
```

### Step 2: Application Test
```bash
# Run application test
python test_app.py

# Expected output:
# Testing configuration... PASS
# Testing data processing... PASS
# Testing AI analysis... PASS
# Testing Streamlit app... PASS
# Overall status: ALL TESTS PASSED
```

### Step 3: Launch Application
```bash
# Start the application
streamlit run src/main.py

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

### Step 4: Browser Verification
1. Open web browser
2. Navigate to `http://localhost:8501`
3. Verify application loads correctly
4. Test file upload functionality
5. Run quick analysis test

## 🐳 Docker Installation

### Prerequisites
- Docker Desktop installed and running
- 4GB+ available memory allocated to Docker

### Docker Setup
```bash
# Build Docker image
docker build -t paraguay-analysis .

# Run Docker container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key paraguay-analysis

# Or use Docker Compose
docker-compose up -d
```

### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  analysis-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
```

## ☁️ Cloud Deployment

### AWS Deployment
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Deploy using AWS App Runner or EC2
# See deployment/aws-deployment.md for details
```

### Google Cloud Deployment
```bash
# Install Google Cloud SDK
# Follow Google Cloud documentation

# Deploy to Cloud Run
gcloud run deploy --source .

# See deployment/gcp-deployment.md for details
```

### Azure Deployment
```bash
# Install Azure CLI
pip install azure-cli

# Deploy to Azure App Service
az webapp up --sku B1 --name paraguay-analysis

# See deployment/azure-deployment.md for details
```

## 🔧 Advanced Configuration

### Performance Optimization
```python
# config/performance.py
PERFORMANCE_CONFIG = {
    'max_workers': 4,
    'chunk_size': 1000,
    'cache_size': 1000,
    'timeout_seconds': 300
}
```

### Security Configuration
```python
# config/security.py
SECURITY_CONFIG = {
    'rate_limiting': True,
    'input_validation': True,
    'api_key_encryption': True,
    'secure_cookies': True
}
```

### Monitoring Setup
```python
# config/monitoring.py
MONITORING_CONFIG = {
    'metrics_enabled': True,
    'log_level': 'INFO',
    'performance_tracking': True,
    'error_reporting': True
}
```

## 🚨 Troubleshooting Installation Issues

### Common Issues and Solutions

#### Issue 1: Python Version Incompatibility
```bash
# Problem: Python version too old
python --version  # Shows Python 3.7 or older

# Solution: Install Python 3.8+
# Download from python.org or use package manager
# Windows: Download from python.org
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
```

#### Issue 2: Virtual Environment Creation Fails
```bash
# Problem: venv module not found
python -m venv analysis_env
# Error: No module named venv

# Solution: Install venv module
# Ubuntu/Debian:
sudo apt install python3-venv
# Other systems: reinstall Python with venv support
```

#### Issue 3: Package Installation Errors
```bash
# Problem: pip install fails with permission errors
pip install -r requirements.txt
# Error: Permission denied

# Solution 1: Use virtual environment
python -m venv analysis_env
source analysis_env/bin/activate  # or Windows equivalent
pip install -r requirements.txt

# Solution 2: User installation
pip install --user -r requirements.txt
```

#### Issue 4: OpenAI API Key Issues
```bash
# Problem: API key not recognized
# Error: Invalid API key

# Solution: Verify API key format and validity
# 1. Check OpenAI dashboard for correct key
# 2. Verify .env file format:
OPENAI_API_KEY=sk-your-actual-key-here
# 3. Restart application after changes
```

#### Issue 5: Port Already in Use
```bash
# Problem: Port 8501 already in use
streamlit run src/main.py
# Error: Port 8501 is already in use

# Solution: Use different port
streamlit run src/main.py --server.port 8502

# Or kill existing process
# Windows: netstat -ano | findstr :8501
# macOS/Linux: lsof -ti:8501 | xargs kill
```

#### Issue 6: Memory Issues
```bash
# Problem: Out of memory during analysis
# Error: MemoryError or system freeze

# Solution 1: Reduce batch size
# Edit config file: BATCH_SIZE=50 (instead of 100)

# Solution 2: Increase system memory
# Close other applications
# Consider upgrading RAM

# Solution 3: Use smaller datasets for testing
```

### Getting Help
If you encounter issues not covered here:

1. **Check the logs**: Look in `analysis.log` for error details
2. **Run diagnostics**: Use `python test_app.py` for system check
3. **Review configuration**: Verify all settings in `.env` file
4. **Check resources**: Ensure sufficient memory and disk space
5. **Update dependencies**: Run `pip install --upgrade -r requirements.txt`

## 📚 Next Steps

After successful installation:

1. **[Configuration Guide](configuration.md)** - Detailed configuration options
2. **[Quick Start Guide](../getting-started/quick-start.md)** - Get started with analysis
3. **[User Manual](../user-guides/user-manual.md)** - Complete usage instructions
4. **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run tests
python test_app.py

# Restart application
streamlit run src/main.py
```

### Backup and Recovery
```bash
# Backup configuration
cp .env .env.backup

# Backup data
cp -r data data_backup

# Recovery process (if needed)
cp .env.backup .env
cp -r data_backup data
```

## 📞 Support

For installation support:
- Check the [Troubleshooting Guide](troubleshooting.md)
- Review [FAQ](../user-guides/faq.md)
- Contact technical support team
- Submit issues on GitHub repository