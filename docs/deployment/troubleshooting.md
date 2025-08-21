# Troubleshooting Guide

This comprehensive guide helps resolve common issues with the Personal Paraguay Fiber Comments Analysis System.

## 🚨 Common Issues and Solutions

### Installation Issues

#### Python Version Errors
**Problem**: `Python version 3.7 or lower detected`
```bash
python --version
# Shows: Python 3.7.x
```

**Solution**:
```bash
# Windows - Install Python 3.8+
# Download from python.org

# macOS
brew install python@3.9

# Linux
sudo apt update
sudo apt install python3.9
```

#### Dependency Installation Failures
**Problem**: `ERROR: Could not install packages due to an EnvironmentError`

**Solution**:
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt

# If still failing, install one by one
pip install streamlit==1.28.0
pip install openai==1.3.0
pip install pandas==2.0.0
```

### API Configuration Issues

#### Invalid API Key
**Problem**: `OpenAI API key is invalid`

**Solution**:
1. Verify API key format:
   ```bash
   cat .env
   # Should show: OPENAI_API_KEY=sk-proj-xxxxx
   ```
2. Check API key validity at platform.openai.com
3. Ensure no extra spaces or quotes in .env file
4. Restart application after changes

#### API Rate Limits
**Problem**: `Rate limit exceeded`

**Solution**:
```python
# Adjust configuration in .env
BATCH_SIZE=50  # Reduce from 100
MAX_CONCURRENT_REQUESTS=5  # Reduce from 10
API_RETRY_DELAY=60  # Add delay between retries
```

### Application Runtime Issues

#### Port Already in Use
**Problem**: `Port 8501 is already in use`

**Solution**:
```bash
# Option 1: Use different port
streamlit run src/main.py --server.port 8502

# Option 2: Kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8501 | xargs kill -9
```

#### Memory Errors
**Problem**: `MemoryError` or application freezing

**Solution**:
1. Reduce batch size in configuration
2. Process smaller datasets
3. Clear cache:
   ```bash
   rm -rf data/cache/*
   streamlit cache clear
   ```
4. Increase available memory or use machine with more RAM

### Data Processing Issues

#### File Upload Failures
**Problem**: `File upload failed` or `Unsupported file format`

**Solutions by file type:

**Excel Files**:
- Remove merged cells
- Ensure first row contains headers
- Save as .xlsx (not .xls)
- Remove special formatting

**CSV Files**:
- Check encoding (use UTF-8)
- Verify delimiter (comma, semicolon, tab)
- Remove special characters from headers

**Large Files**:
- Split into smaller chunks (<200MB)
- Use batch processing
- Consider sampling for testing

#### Column Detection Problems
**Problem**: `Cannot find comment column`

**Solution**:
1. Rename column to include "comment" or "feedback"
2. Ensure column has text data
3. Remove empty rows at the beginning
4. Use manual column selection in UI

### Analysis Issues

#### Low Confidence Scores
**Problem**: Many results show confidence <70%

**Causes and Solutions**:
- **Short comments**: Filter out comments <20 characters
- **Mixed languages**: Enable translation in settings
- **Technical jargon**: Use comprehensive analysis mode
- **Unclear text**: Review and clean source data

#### Unexpected Results
**Problem**: Analysis results don't match expectations

**Debugging Steps**:
1. Check individual comment analysis
2. Verify language detection is correct
3. Review sentiment distribution
4. Enable debug mode for detailed logs

### Performance Issues

#### Slow Processing
**Problem**: Analysis takes much longer than estimated

**Solutions**:
```bash
# Optimize configuration
BATCH_SIZE=50  # Smaller batches
CACHE_ENABLED=True  # Enable caching
PARALLEL_PROCESSING=True  # Enable parallel processing

# Check system resources
# Windows: Task Manager
# macOS: Activity Monitor
# Linux: htop or top
```

#### High API Costs
**Problem**: Unexpectedly high OpenAI API costs

**Cost Reduction Strategies**:
1. Enable duplicate detection
2. Use caching aggressively
3. Sample large datasets
4. Use basic analysis for initial testing
5. Set daily budget limits

### Export Issues

#### Export Button Not Working
**Problem**: Export buttons don't respond or downloads fail

**Solutions**:
1. Ensure analysis is 100% complete
2. Check browser download settings
3. Try different export format
4. Clear browser cache
5. Check disk space availability

#### Corrupted Export Files
**Problem**: Excel/CSV files won't open

**Solutions**:
- Try different application (LibreOffice vs Excel)
- Check file isn't still being written
- Verify sufficient disk space
- Re-export with different format

## 🔍 Diagnostic Commands

### System Information
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "streamlit|openai|pandas"

# Check environment variables
python -c "import os; print(os.getenv('OPENAI_API_KEY')[:10] + '...')"

# Check available memory
# Windows
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory

# macOS/Linux
free -h
```

### Application Diagnostics
```bash
# Run diagnostic script
python src/test_app.py

# Check Streamlit version
streamlit version

# Validate configuration
python scripts/validate_config.py

# Test API connection
python scripts/test_openai.py
```

## 📝 Log Files

### Accessing Logs
```bash
# Application logs
tail -f logs/analysis.log

# Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log

# Error logs
grep ERROR logs/analysis.log
```

### Log Levels
```python
# Set in .env file
LOG_LEVEL=DEBUG  # For detailed debugging
LOG_LEVEL=INFO   # Normal operation
LOG_LEVEL=ERROR  # Only errors
```

## 🆘 Getting Help

### Before Contacting Support
1. Check this troubleshooting guide
2. Review the [FAQ](../user-guides/faq.md)
3. Search error messages in documentation
4. Try with sample data first
5. Collect diagnostic information

### Information to Provide
When contacting support, include:
- Error messages (exact text)
- Screenshots of the issue
- System information (OS, Python version)
- Configuration settings
- Sample data that reproduces issue
- Log files (last 100 lines)

### Support Channels
- Email: support@personal.com.py
- GitHub Issues: [Create issue](https://github.com/your-repo/issues)
- Documentation: [User Manual](../user-guides/user-manual.md)

## 🔄 Recovery Procedures

### Reset Application
```bash
# Stop application
Ctrl+C

# Clear cache
rm -rf data/cache/*

# Reset configuration
cp .env.example .env
# Edit .env with your API key

# Restart
streamlit run src/main.py
```

### Database Reset
```bash
# Clear usage database
rm data/monitoring/usage_metrics.db

# Clear session data
rm -rf ~/.streamlit/cache/
```

### Complete Reinstall
```bash
# Backup your data
cp -r data data_backup
cp .env .env.backup

# Remove and reinstall
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Restore configuration
cp .env.backup .env
```

## 🚀 Performance Optimization

### Recommended Settings for Large Datasets
```env
# .env configuration
BATCH_SIZE=200
MAX_CONCURRENT_REQUESTS=15
CACHE_ENABLED=True
CACHE_TTL=7200
MEMORY_LIMIT_MB=4096
```

### Recommended Settings for Limited Resources
```env
# .env configuration
BATCH_SIZE=50
MAX_CONCURRENT_REQUESTS=5
CACHE_ENABLED=True
MEMORY_LIMIT_MB=2048
ENABLE_COMPRESSION=True
```

## 📊 Known Issues

### Current Limitations
- Maximum file size: 200MB
- Maximum comments per batch: 500
- Guaraní translation accuracy: ~85%
- Mixed language detection: ~80% accuracy

### Workarounds
- **Large files**: Split into multiple files
- **Memory issues**: Use smaller batch sizes
- **Translation issues**: Pre-translate Guaraní text
- **Detection issues**: Separate mixed language comments

## 🔗 Related Documentation
- [Installation Guide](installation-guide.md)
- [Configuration Guide](../getting-started/configuration.md)
- [User Manual](../user-guides/user-manual.md)
- [FAQ](../user-guides/faq.md)