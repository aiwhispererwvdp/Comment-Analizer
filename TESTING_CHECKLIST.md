# ✅ Testing Checklist
## Personal Paraguay Fiber Comments Analysis System

---

## 🚀 Quick Start Testing

### ⚡ Immediate Verification (2 minutes)
```bash
# 1. Run quick test
python quick_test.py

# 2. Launch main application  
streamlit run src/main.py

# 3. Launch simplified interface
streamlit run src/simplified_main.py
```

If all three commands work, the system is operational!

---

## 📋 Complete Testing Checklist

### 1️⃣ Initial Setup Verification
- [ ] Python 3.8+ installed (`python --version`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured with API keys
- [ ] Application launches without errors

### 2️⃣ File Upload Testing
- [ ] **Excel Upload** (.xlsx)
  - [ ] Small file (<10 rows) 
  - [ ] Medium file (100-500 rows)
  - [ ] Large file (1000+ rows)
  - [ ] Multi-sheet Excel file
- [ ] **CSV Upload** (.csv)
  - [ ] UTF-8 encoding
  - [ ] Different delimiters (comma, semicolon)
- [ ] **JSON Upload** (.json)
- [ ] **Text Upload** (.txt)
- [ ] **Error Handling**
  - [ ] Reject invalid formats (.pdf, .doc)
  - [ ] Handle empty files gracefully
  - [ ] Show error for files >50MB

### 3️⃣ Data Validation Testing
- [ ] **Required Columns**
  - [ ] File with 'Comment' column only
  - [ ] File with all columns (Comment, Date, Category, Rating)
  - [ ] File missing 'Comment' column (should error)
- [ ] **Data Types**
  - [ ] Text comments
  - [ ] Numeric ratings
  - [ ] Date formats
- [ ] **Special Characters**
  - [ ] Spanish characters (ñ, á, é, í, ó, ú)
  - [ ] Guaraní characters
  - [ ] Emojis and symbols

### 4️⃣ Analysis Features Testing

#### Sentiment Analysis
- [ ] **Positive Detection**
  - Input: "Excelente servicio, muy satisfecho"
  - Expected: Positive (>0.7 confidence)
- [ ] **Negative Detection**  
  - Input: "Terrible, muy malo"
  - Expected: Negative (>0.7 confidence)
- [ ] **Neutral Detection**
  - Input: "El servicio funciona"
  - Expected: Neutral

#### Emotion Detection
- [ ] Joy detection ("Estoy muy feliz")
- [ ] Anger detection ("Estoy furioso")
- [ ] Sadness detection ("Muy triste")
- [ ] Fear detection ("Tengo miedo")
- [ ] Surprise detection ("Increíble!")

#### Language Processing
- [ ] Spanish text recognition
- [ ] Guaraní text recognition
- [ ] Mixed language handling
- [ ] English text handling

#### Theme Extraction
- [ ] Service quality themes
- [ ] Technical issue themes
- [ ] Billing themes
- [ ] Customer support themes

### 5️⃣ Visualization Testing
- [ ] **Charts Display**
  - [ ] Sentiment distribution pie chart
  - [ ] Emotion radar chart
  - [ ] Timeline trends
  - [ ] Word cloud generation
  - [ ] Theme frequency bars
- [ ] **Interactivity**
  - [ ] Hover tooltips work
  - [ ] Charts are responsive
  - [ ] Filters apply correctly

### 6️⃣ Export Functionality Testing
- [ ] **Excel Export**
  - [ ] Creates .xlsx file
  - [ ] Multiple sheets included
  - [ ] Charts embedded
  - [ ] Formatting preserved
- [ ] **CSV Export**
  - [ ] Creates .csv file
  - [ ] Data integrity maintained
  - [ ] Special characters handled
- [ ] **PDF Report**
  - [ ] Generates PDF
  - [ ] Includes visualizations
  - [ ] Professional formatting

### 7️⃣ Performance Testing
- [ ] **Response Times**
  - [ ] Page load <3 seconds
  - [ ] File upload <5 seconds
  - [ ] Analysis <30 seconds for 1000 rows
  - [ ] Export generation <10 seconds
- [ ] **Resource Usage**
  - [ ] Memory usage <1GB normal operation
  - [ ] CPU usage reasonable
  - [ ] No memory leaks
- [ ] **Concurrent Usage**
  - [ ] Multiple browser tabs work
  - [ ] No session conflicts

### 8️⃣ API Integration Testing
- [ ] **OpenAI API**
  - [ ] Connection successful
  - [ ] API key valid
  - [ ] Error handling for rate limits
  - [ ] Cost tracking works
- [ ] **Fallback Mechanisms**
  - [ ] Works without API key (limited)
  - [ ] Switches to basic analysis
  - [ ] Shows appropriate warnings

### 9️⃣ User Interface Testing
- [ ] **Navigation**
  - [ ] All buttons clickable
  - [ ] Forms submit correctly
  - [ ] Navigation intuitive
- [ ] **Responsive Design**
  - [ ] Works on desktop (1920x1080)
  - [ ] Works on laptop (1366x768)
  - [ ] Sidebar collapsible
- [ ] **Error Messages**
  - [ ] Clear error descriptions
  - [ ] Helpful suggestions
  - [ ] No technical jargon

### 🔟 Security Testing
- [ ] **Input Validation**
  - [ ] SQL injection prevention
  - [ ] XSS attack prevention
  - [ ] Path traversal prevention
- [ ] **API Security**
  - [ ] API keys not exposed in logs
  - [ ] Keys not in git history
  - [ ] Secure storage in .env
- [ ] **Data Privacy**
  - [ ] No data permanently stored
  - [ ] Session data cleared
  - [ ] Export files secure

---

## 🧪 Automated Test Execution

### Run Unit Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_file_upload_service.py -v

# With coverage report
pytest tests/ --cov=src --cov-report=html
```

### Run System Tests
```bash
# Quick verification
python quick_test.py

# Comprehensive testing
python run_system_tests.py

# Enhanced features test
python test_enhanced_features.py
```

---

## 📊 Test Scenarios by User Role

### 🏢 Business Analyst
1. Upload daily comments file
2. Review sentiment dashboard
3. Identify negative trends
4. Export Excel report
5. Share with management

### 👷 Technical Support
1. Upload problem tickets
2. Categorize by issue type
3. Identify common problems
4. Generate action items
5. Track resolution

### 📈 Marketing Team
1. Upload campaign feedback
2. Measure sentiment change
3. Identify positive drivers
4. Export visualizations
5. Create presentation

### 🎯 Product Manager
1. Upload feature requests
2. Extract themes
3. Prioritize by frequency
4. Generate roadmap input
5. Track satisfaction

---

## 🔍 Troubleshooting Tests

### If Application Won't Start
```bash
# Check Python
python --version

# Check Streamlit
streamlit --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Try different port
streamlit run src/main.py --server.port 8502
```

### If Analysis Fails
```bash
# Check API key
python -c "from config import Config; print(Config.OPENAI_API_KEY[:10] if Config.OPENAI_API_KEY else 'No key')"

# Test basic analysis
python -c "from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer; print('OK')"

# Check memory
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

### If Export Fails
```bash
# Check directories
ls -la outputs/exports/

# Check permissions
touch outputs/exports/test.txt

# Check disk space
df -h
```

---

## 📝 Test Recording Template

### Test Session: [Date/Time]
**Tester**: [Name]
**Version**: 1.0.0
**Environment**: [Windows/Mac/Linux]

### Results Summary
| Feature | Status | Notes |
|---------|--------|-------|
| File Upload | ✅ Pass | All formats work |
| Sentiment Analysis | ✅ Pass | 90% accuracy |
| Export | ⚠️ Warning | PDF slow for large files |
| API Integration | ❌ Fail | Rate limit hit |

### Issues Found
1. **Issue**: [Description]
   - **Severity**: High/Medium/Low
   - **Steps to Reproduce**: [Steps]
   - **Expected**: [Expected behavior]
   - **Actual**: [Actual behavior]

### Recommendations
- [Recommendation 1]
- [Recommendation 2]

---

## ✨ Final Verification

### System is Ready When:
- ✅ All quick tests pass (`python quick_test.py`)
- ✅ Main application launches
- ✅ Can upload and analyze a file
- ✅ Can export results
- ✅ No critical errors in console

### Sign-off
- [ ] Development Testing Complete
- [ ] User Acceptance Testing Complete
- [ ] Performance Testing Complete
- [ ] Security Testing Complete
- [ ] Documentation Updated

---

**Last Updated**: January 2025
**Next Review**: Monthly