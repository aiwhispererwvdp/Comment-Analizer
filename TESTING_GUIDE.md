# 🧪 Comprehensive Testing Guide
## Personal Paraguay Fiber Comments Analysis System

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Pre-Testing Setup](#pre-testing-setup)
3. [Core Functionalities](#core-functionalities)
4. [Testing Environments](#testing-environments)
5. [Test Data Preparation](#test-data-preparation)
6. [Functional Testing](#functional-testing)
7. [API Testing](#api-testing)
8. [Performance Testing](#performance-testing)
9. [Security Testing](#security-testing)
10. [Automated Testing](#automated-testing)
11. [User Acceptance Testing](#user-acceptance-testing)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## 🎯 System Overview

### Purpose
The Personal Paraguay Fiber Comments Analysis System is an AI-powered platform that analyzes customer feedback about fiber-to-the-home services, providing sentiment analysis, pattern detection, and actionable business intelligence.

### Key Components
- **Frontend**: Streamlit-based interactive dashboard
- **Backend**: Python services for data processing and analysis
- **AI Integration**: OpenAI GPT-4 for advanced analysis
- **Data Processing**: Pandas-based data manipulation
- **Export System**: Excel, CSV, and PDF report generation

---

## 🛠️ Pre-Testing Setup

### 1. Environment Verification
```bash
# Check Python version (requires 3.8+)
python --version

# Verify pip installation
pip --version

# Check git installation
git --version
```

### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "streamlit|pandas|openai|plotly"
```

### 3. Configure API Keys
```bash
# Create .env file if not exists
cp .env.example .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional: AZURE_TEXT_ANALYTICS_KEY, GOOGLE_APPLICATION_CREDENTIALS
```

### 4. Verify Directory Structure
```bash
# Check required directories exist
ls -la data/
ls -la outputs/
ls -la src/

# Create missing directories if needed
mkdir -p data/raw data/cache data/processed
mkdir -p outputs/reports outputs/exports outputs/visualizations
```

---

## 🔧 Core Functionalities

### 1. Data Input & Processing
- **File Upload**: Excel, CSV, JSON, TXT support
- **Data Validation**: Format checking, size limits
- **Language Detection**: Spanish and Guaraní support
- **Data Cleaning**: Duplicate removal, normalization

### 2. Analysis Capabilities
- **Sentiment Analysis**: Positive/Negative/Neutral classification
- **Emotion Detection**: Joy, Anger, Sadness, Fear, Surprise
- **Theme Extraction**: Automatic topic identification
- **Pattern Recognition**: Trend and anomaly detection
- **Language Processing**: Multilingual support

### 3. Visualization & Reporting
- **Interactive Dashboard**: Real-time charts and metrics
- **Export Formats**: Excel, CSV, PDF reports
- **Visualization Types**: Bar charts, pie charts, word clouds, heatmaps
- **Custom Reports**: Professional Excel workbooks with multiple sheets

### 4. API Integration
- **OpenAI GPT-4**: Advanced pattern detection
- **Azure Text Analytics**: Sentiment analysis
- **Google Cloud Translation**: Language support
- **Cost Monitoring**: API usage tracking

---

## 🌐 Testing Environments

### Application Entry Points

#### 1. Main Application
```bash
streamlit run src/main.py
# Full-featured interface with all capabilities
# URL: http://localhost:8501
```

#### 2. Professional Mode
```bash
streamlit run src/main_professional.py
# Enhanced features for business users
# Advanced analytics and reporting
```

#### 3. Simplified Interface
```bash
streamlit run src/simplified_main.py
# Clean, minimalist interface
# Best for quick analysis
```

#### 4. Spanish Interface
```bash
streamlit run src/simplified_main_es.py
# Spanish language interface
# Localized for Paraguay users
```

#### 5. Test Application
```bash
streamlit run src/test_app.py
# Development testing interface
# Debug features enabled
```

---

## 📊 Test Data Preparation

### 1. Sample Data Structure

Create test Excel file with following columns:

```excel
| Comment | Date | Category | Rating |
|---------|------|----------|--------|
| El servicio de fibra es excelente | 2024-01-15 | Service | 5 |
| Problemas constantes de conexión | 2024-01-16 | Technical | 2 |
| Muy satisfecho con la velocidad | 2024-01-17 | Performance | 4 |
```

### 2. Test Data Scenarios

#### Small Dataset (Quick Testing)
- **File**: `test_data_small.xlsx`
- **Rows**: 10-50 comments
- **Purpose**: Quick functionality verification
- **Languages**: Spanish only

#### Medium Dataset (Standard Testing)
- **File**: `test_data_medium.xlsx`
- **Rows**: 100-500 comments
- **Purpose**: Standard workflow testing
- **Languages**: Mixed Spanish/Guaraní

#### Large Dataset (Performance Testing)
- **File**: `test_data_large.xlsx`
- **Rows**: 1000-5000 comments
- **Purpose**: Performance and memory testing
- **Languages**: Multiple sheets, mixed languages

### 3. Test Data Generation Script
```python
# Create test_data_generator.py
import pandas as pd
import random
from datetime import datetime, timedelta

# Sample comments for testing
positive_comments = [
    "Excelente servicio de fibra óptica",
    "Muy contento con la velocidad",
    "Instalación rápida y profesional",
    "Mejor internet que he tenido"
]

negative_comments = [
    "Servicio interrumpido constantemente",
    "Velocidad más lenta que lo prometido",
    "Mal servicio al cliente",
    "Problemas técnicos frecuentes"
]

neutral_comments = [
    "El servicio funciona normalmente",
    "Sin problemas particulares",
    "Servicio estándar",
    "Cumple con lo básico"
]

# Generate test dataset
def generate_test_data(num_rows=100):
    data = []
    for i in range(num_rows):
        comment_type = random.choice(['positive', 'negative', 'neutral'])
        if comment_type == 'positive':
            comment = random.choice(positive_comments)
            rating = random.randint(4, 5)
        elif comment_type == 'negative':
            comment = random.choice(negative_comments)
            rating = random.randint(1, 2)
        else:
            comment = random.choice(neutral_comments)
            rating = 3
        
        data.append({
            'Comment': comment,
            'Date': datetime.now() - timedelta(days=random.randint(1, 90)),
            'Category': random.choice(['Service', 'Technical', 'Billing', 'Support']),
            'Rating': rating
        })
    
    df = pd.DataFrame(data)
    df.to_excel('test_data.xlsx', index=False)
    print(f"Generated {num_rows} test comments in test_data.xlsx")

# Run generator
generate_test_data(100)
```

---

## ✅ Functional Testing

### Test Case 1: File Upload
**Objective**: Verify file upload functionality

1. **Launch application**
   ```bash
   streamlit run src/main.py
   ```

2. **Test file formats**
   - ✅ Upload `.xlsx` file → Should accept
   - ✅ Upload `.csv` file → Should accept
   - ✅ Upload `.json` file → Should accept
   - ✅ Upload `.txt` file → Should accept
   - ❌ Upload `.pdf` file → Should reject
   - ❌ Upload `.doc` file → Should reject

3. **Test file size limits**
   - ✅ Upload <50MB file → Should accept
   - ❌ Upload >50MB file → Should show size error

4. **Test data validation**
   - ✅ Upload file with required columns → Should process
   - ❌ Upload empty file → Should show error
   - ❌ Upload corrupted file → Should handle gracefully

### Test Case 2: Sentiment Analysis
**Objective**: Verify sentiment detection accuracy

1. **Positive sentiment test**
   - Input: "Excelente servicio, muy satisfecho"
   - Expected: Positive sentiment (>0.7 confidence)
   - Emotion: Joy

2. **Negative sentiment test**
   - Input: "Terrible servicio, muy decepcionado"
   - Expected: Negative sentiment (>0.7 confidence)
   - Emotion: Anger/Sadness

3. **Neutral sentiment test**
   - Input: "El servicio funciona"
   - Expected: Neutral sentiment
   - Emotion: None/Low confidence

### Test Case 3: Language Detection
**Objective**: Verify multilingual support

1. **Spanish detection**
   - Input: "El internet funciona perfectamente"
   - Expected: Language = Spanish

2. **Guaraní detection**
   - Input: "Iporãite pe servicio"
   - Expected: Language = Guaraní

3. **Mixed language handling**
   - Input: "Che servicio iporã pero expensive"
   - Expected: Mixed language detection

### Test Case 4: Theme Extraction
**Objective**: Verify pattern detection

1. **Service quality themes**
   - Input multiple comments about speed
   - Expected: "Internet Speed" theme identified

2. **Technical issues themes**
   - Input multiple comments about disconnections
   - Expected: "Connection Problems" theme identified

3. **Customer service themes**
   - Input multiple comments about support
   - Expected: "Customer Support" theme identified

### Test Case 5: Export Functionality
**Objective**: Verify report generation

1. **Excel export**
   - Click "Export to Excel"
   - Verify file downloads
   - Check multiple sheets created
   - Verify charts included

2. **CSV export**
   - Click "Export to CSV"
   - Verify file downloads
   - Check data integrity

3. **PDF report**
   - Click "Generate PDF Report"
   - Verify file downloads
   - Check visualizations included

---

## 🔌 API Testing

### 1. OpenAI API Testing
```python
# Test OpenAI connection
import openai
from config import Config

def test_openai_api():
    try:
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print("✅ OpenAI API working")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

test_openai_api()
```

### 2. API Rate Limiting Test
```python
# Test rate limiting
import time
from api.monitoring import get_monitor

monitor = get_monitor()

def test_rate_limiting():
    for i in range(10):
        # Simulate API call
        monitor.track_api_call('openai', 0.01)
        time.sleep(0.1)
    
    stats = monitor.get_usage_stats()
    print(f"API calls made: {stats['total_calls']}")
    print(f"Total cost: ${stats['total_cost']}")

test_rate_limiting()
```

### 3. API Error Handling
```python
# Test error handling
def test_api_error_handling():
    # Test with invalid API key
    import os
    original_key = os.environ.get('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = 'invalid_key'
    
    try:
        # Try to run analysis
        # Should handle error gracefully
        pass
    finally:
        os.environ['OPENAI_API_KEY'] = original_key
```

---

## ⚡ Performance Testing

### 1. Load Testing
```bash
# Test with increasing data sizes
python -c "
import pandas as pd
import time
from src.services.file_upload_service import FileUploadService

service = FileUploadService()

for size in [100, 500, 1000, 5000]:
    df = pd.DataFrame({'comment': ['test'] * size})
    start = time.time()
    # Process data
    elapsed = time.time() - start
    print(f'{size} rows: {elapsed:.2f} seconds')
"
```

### 2. Memory Testing
```bash
# Monitor memory usage
python -c "
import psutil
import os

process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

### 3. Concurrent User Testing
```bash
# Test multiple simultaneous users
# Open multiple browser tabs
# Run analysis simultaneously
# Monitor for conflicts or errors
```

---

## 🔐 Security Testing

### 1. Input Validation
```python
# Test malicious inputs
test_inputs = [
    "<script>alert('XSS')</script>",  # XSS attempt
    "'; DROP TABLE comments; --",       # SQL injection
    "../../../etc/passwd",              # Path traversal
    "A" * 1000000                      # Buffer overflow
]

for input_text in test_inputs:
    # System should sanitize or reject
    print(f"Testing: {input_text[:50]}...")
```

### 2. API Key Security
```bash
# Verify API keys are not exposed
grep -r "sk-" src/ --include="*.py"
grep -r "OPENAI_API_KEY" src/ --include="*.log"

# Check git history for exposed keys
git log -p | grep -E "sk-[a-zA-Z0-9]{48}"
```

### 3. File Upload Security
- Test file type validation
- Test file size limits
- Test malformed files
- Test virus scanning (if implemented)

---

## 🤖 Automated Testing

### 1. Run Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_file_upload_service.py -v

# Run specific test
pytest tests/test_file_upload_service.py::TestFileUploadService::test_init -v
```

### 2. Test Categories

#### Unit Tests
- `test_file_upload_service.py` - File handling
- `test_session_manager.py` - Session management
- `test_config.py` - Configuration
- `test_validators.py` - Input validation
- `test_exceptions.py` - Error handling

#### Integration Tests
- `test_analysis_workflow.py` - End-to-end analysis
- `test_api_integration.py` - API connectivity
- `test_export_functionality.py` - Report generation

### 3. Continuous Testing Script
```bash
#!/bin/bash
# continuous_test.sh

echo "🧪 Starting Continuous Testing Suite"

# 1. Check environment
echo "✅ Checking environment..."
python --version
pip list | grep streamlit

# 2. Run unit tests
echo "✅ Running unit tests..."
pytest tests/unit/ -v

# 3. Run integration tests
echo "✅ Running integration tests..."
pytest tests/integration/ -v

# 4. Check code quality
echo "✅ Checking code quality..."
flake8 src/ --max-line-length=100
black src/ --check

# 5. Run security checks
echo "✅ Running security checks..."
bandit -r src/

# 6. Generate coverage report
echo "✅ Generating coverage report..."
pytest --cov=src --cov-report=html

echo "✅ Testing suite completed!"
```

---

## 👥 User Acceptance Testing (UAT)

### 1. Business User Scenarios

#### Scenario 1: Daily Analysis Workflow
1. **Login** to application
2. **Upload** daily comments file
3. **Review** sentiment analysis
4. **Identify** key themes
5. **Export** report for management
6. **Time**: Should complete in <5 minutes

#### Scenario 2: Weekly Reporting
1. **Upload** weekly data compilation
2. **Analyze** trend changes
3. **Compare** with previous week
4. **Generate** executive summary
5. **Export** professional Excel report

#### Scenario 3: Issue Investigation
1. **Upload** specific complaint data
2. **Filter** by negative sentiment
3. **Identify** root causes
4. **Extract** actionable insights
5. **Create** action plan report

### 2. UAT Checklist

#### Functionality
- [ ] File upload works for all formats
- [ ] Analysis completes without errors
- [ ] Results are accurate and meaningful
- [ ] Export functions work correctly
- [ ] UI is responsive and intuitive

#### Performance
- [ ] Page loads in <3 seconds
- [ ] Analysis completes in reasonable time
- [ ] No memory issues with large files
- [ ] Smooth scrolling and interactions

#### Usability
- [ ] Clear error messages
- [ ] Intuitive navigation
- [ ] Helpful tooltips and guides
- [ ] Consistent UI behavior
- [ ] Mobile-friendly (if applicable)

#### Business Requirements
- [ ] Sentiment analysis accuracy >80%
- [ ] Theme detection identifies main topics
- [ ] Reports contain required metrics
- [ ] Data security maintained
- [ ] API costs within budget

---

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Application Won't Start
```bash
# Error: streamlit: command not found
Solution: pip install streamlit

# Error: ModuleNotFoundError
Solution: pip install -r requirements.txt

# Error: Port already in use
Solution: streamlit run src/main.py --server.port 8502
```

#### 2. File Upload Issues
```python
# Error: File too large
Solution: Check file size < 50MB

# Error: Invalid file format
Solution: Use .xlsx, .csv, .json, or .txt

# Error: No data found
Solution: Ensure file has 'Comment' column
```

#### 3. API Errors
```bash
# Error: OpenAI API key invalid
Solution: 
1. Check .env file has correct key
2. Verify key at platform.openai.com
3. Ensure key has sufficient credits

# Error: Rate limit exceeded
Solution:
1. Wait 60 seconds
2. Reduce batch size in config
3. Implement retry logic
```

#### 4. Analysis Errors
```python
# Error: Memory error with large file
Solution:
1. Reduce file size
2. Increase MAX_MEMORY_MB in config
3. Use batch processing

# Error: Language not detected
Solution:
1. Check text is in Spanish/Guaraní
2. Ensure minimum text length (10 chars)
3. Clean special characters
```

#### 5. Export Issues
```bash
# Error: Export fails
Solution:
1. Check outputs/ directory exists
2. Ensure write permissions
3. Close Excel if file is open
4. Check disk space
```

### Debug Mode
```bash
# Enable debug mode for detailed logs
export DEBUG=True
export LOG_LEVEL=DEBUG
streamlit run src/main.py

# Check logs
tail -f logs/app.log
```

### Performance Optimization
```python
# config.py adjustments for performance

# Reduce batch size for slower systems
BATCH_SIZE = 50  # Default: 100

# Increase memory for large datasets
MAX_MEMORY_MB = 2048  # Default: 1024

# Reduce parallel workers if CPU limited
PARALLEL_WORKERS = 2  # Default: 4

# Disable cache if having issues
CACHE_ENABLED = False  # Default: True
```

---

## 📝 Test Report Template

### Test Execution Summary
```markdown
## Test Report - [Date]

### Environment
- Python Version: 3.x.x
- Streamlit Version: 1.x.x
- OS: Windows/Mac/Linux

### Test Results
| Test Category | Passed | Failed | Total | Pass Rate |
|---------------|--------|--------|-------|-----------|
| Unit Tests    | 55     | 6      | 61    | 90%       |
| Integration   | 10     | 0      | 10    | 100%      |
| Performance   | 5      | 1      | 6     | 83%       |
| Security      | 8      | 0      | 8     | 100%      |

### Issues Found
1. Issue #1: Description
   - Severity: High/Medium/Low
   - Status: Fixed/Pending

### Recommendations
- Recommendation 1
- Recommendation 2

### Sign-off
- Tester: [Name]
- Date: [Date]
- Status: Approved/Rejected
```

---

## 🚀 Quick Test Commands

```bash
# Quick health check
curl http://localhost:8501/healthz

# Test file upload via CLI
python -c "
from src.services.file_upload_service import FileUploadService
service = FileUploadService()
print('File upload service: OK')
"

# Test configuration
python -c "
from config import Config, validate_config
validate_config()
print('Configuration: OK')
"

# Test database connection
python -c "
import pandas as pd
df = pd.read_excel('data/raw/sample_data.xlsx')
print(f'Sample data loaded: {len(df)} rows')
"

# Full system test
python test_enhanced_features.py
```

---

## 📊 Testing Metrics

### Key Performance Indicators (KPIs)
- **Code Coverage**: Target >80%
- **Test Pass Rate**: Target >95%
- **Response Time**: <3 seconds for page load
- **Analysis Time**: <30 seconds for 1000 comments
- **Memory Usage**: <1GB for standard operation
- **API Success Rate**: >99%
- **Export Success Rate**: 100%

### Monitoring Commands
```bash
# Monitor real-time performance
python -m src.api.monitoring

# Check API usage
python -c "
from src.api.monitoring import get_monitor
monitor = get_monitor()
print(monitor.get_usage_stats())
"

# Memory profiling
python -m memory_profiler src/main.py
```

---

## 📚 Additional Resources

- [User Manual](documentation/USER_GUIDE.md)
- [API Documentation](docs/api-reference/)
- [Architecture Guide](docs/backend/infrastructure/architecture.md)
- [Deployment Guide](docs/deployment/)

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Maintained By**: Development Team