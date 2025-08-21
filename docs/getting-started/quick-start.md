# Quick Start Guide

Get up and running with the Personal Paraguay Fiber Comments Analysis System in just 5 minutes!

## ⚡ Prerequisites Check

Before starting, ensure you have:
- **Python 3.8+** installed
- **Internet connection** for API access
- **OpenAI API key** (get one at [platform.openai.com](https://platform.openai.com))

## 🚀 5-Minute Setup

### Step 1: Get the Code (30 seconds)
```bash
# Download the system
git clone https://github.com/your-org/Personal_Paraguay_Fiber_Comments_Analysis.git
cd Personal_Paraguay_Fiber_Comments_Analysis
```

### Step 2: Install Dependencies (2 minutes)
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure API Key (30 seconds)
```bash
# Set up your OpenAI API key
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

### Step 4: Launch Application (30 seconds)
```bash
# Start the system
streamlit run src/main.py
```

### Step 5: Open in Browser (30 seconds)
1. Open your web browser
2. Go to `http://localhost:8501`
3. You should see the application interface!

## 🎯 First Analysis in 2 Minutes

### Quick Test with Sample Data
1. **Click "📁 Data Upload"** in the sidebar
2. **Click "Load Personal Paraguay Dataset"** 
3. **Go to "📊 Analysis Dashboard"**
4. **Set sample size to 50** (using the slider)
5. **Click "🔍 Analyze Comments"**
6. **Watch the results appear in real-time!**

### Upload Your Own Data
1. **Go back to "📁 Data Upload"**
2. **Click "Choose a file"** 
3. **Select your Excel/CSV file** with customer comments
4. **Review the data preview**
5. **Run analysis** from the dashboard

## 📊 Understanding Your Results

After analysis completes, you'll see:

### Summary Metrics
- **Overall Sentiment**: Percentage of positive vs negative feedback
- **Total Comments**: Number of comments analyzed
- **Top Theme**: Most frequently mentioned topic
- **Language Distribution**: Spanish vs Guaraní breakdown

### Key Insights
- **Sentiment Breakdown**: Visual pie chart of sentiment distribution
- **Top Themes**: Most important topics customers discuss
- **Pain Points**: Specific issues requiring attention
- **Recommendations**: AI-generated suggestions for improvement

### Export Your Results
1. **Scroll to "📥 Export Results"**
2. **Click "📊 Export Excel"** for comprehensive report
3. **Download the file** when ready
4. **Open in Excel** to explore detailed results

## 🔧 Common Quick Start Issues

### Issue: "Module not found" errors
```bash
# Solution: Update pip and reinstall
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Invalid API key" error  
```bash
# Solution: Check your .env file format
cat .env
# Should show: OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue: Port 8501 already in use
```bash
# Solution: Use a different port
streamlit run src/main.py --server.port 8502
```

### Issue: Browser doesn't open automatically
- **Manually open**: http://localhost:8501
- **Try different browser**: Chrome, Firefox, Safari, Edge
- **Check firewall**: Ensure port 8501 is not blocked

## 🎓 Next Steps

### Learn More
- **[📖 Complete User Manual](../user-guides/user-manual.md)** - Detailed usage guide
- **[🔧 Configuration Guide](configuration.md)** - Advanced settings
- **[❓ FAQ](../user-guides/faq.md)** - Common questions

### Advanced Features
- **Cost Optimization**: Set budgets and monitor API usage
- **Batch Processing**: Analyze large datasets efficiently  
- **Custom Analysis**: Configure analysis depth and parameters
- **Business Intelligence**: Generate executive reports

### Getting Help
- **[🔍 Troubleshooting Guide](../deployment/troubleshooting.md)** - Problem solutions
- **[📧 Support](mailto:support@personal.com.py)** - Technical assistance
- **[📋 User Manual](../user-guides/user-manual.md)** - Comprehensive documentation

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key configured in `.env` file
- [ ] Application launched (`streamlit run src/main.py`)
- [ ] Browser opened to http://localhost:8501
- [ ] Sample analysis completed
- [ ] Results exported to Excel

**Congratulations! You're ready to analyze customer feedback with AI! 🎉**

---

**Need help?** Check the [Complete User Manual](../user-guides/user-manual.md) or contact [support@personal.com.py](mailto:support@personal.com.py)