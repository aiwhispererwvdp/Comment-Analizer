# User Manual - Personal Paraguay Fiber Comments Analysis System

## 📖 Table of Contents
1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Data Upload and Management](#data-upload-and-management)
4. [Analysis Configuration](#analysis-configuration)
5. [Running Analysis](#running-analysis)
6. [Understanding Results](#understanding-results)
7. [Export and Reporting](#export-and-reporting)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## 🎯 System Overview

### What is the Personal Paraguay Fiber Comments Analysis System?
A sophisticated AI-powered platform designed to analyze customer feedback for Personal Paraguay's fiber-to-the-home services. The system provides comprehensive sentiment analysis, theme detection, and business intelligence insights from customer comments.

### Key Capabilities
- **Multilingual Analysis**: Supports Spanish and Guaraní languages
- **Sentiment Detection**: Identifies positive, negative, and neutral sentiments
- **Theme Recognition**: Automatically categorizes feedback by topic
- **Emotion Analysis**: Detects joy, anger, sadness, fear, and surprise
- **Business Intelligence**: Generates actionable insights and recommendations
- **Professional Reporting**: Creates comprehensive reports in multiple formats

### Who Should Use This System?
- **Customer Service Managers**: Analyze customer satisfaction trends
- **Product Managers**: Understand feature requests and pain points
- **Business Analysts**: Generate data-driven insights
- **Quality Assurance Teams**: Monitor service quality trends
- **Executive Leadership**: Review high-level business metrics

## 🚀 Getting Started

### Accessing the System
1. **Open your web browser** (Chrome, Firefox, Safari, or Edge)
2. **Navigate to the application URL** (typically `http://localhost:8501`)
3. **Wait for the application to load** (may take 30-60 seconds on first launch)
4. **Verify the interface appears** with the sidebar navigation

### First-Time Setup
When you first access the system:

1. **Check API Configuration**
   - Navigate to **⚙️ Settings** in the sidebar
   - Verify OpenAI API key is configured
   - Test the connection with the "Test API Connection" button

2. **Review System Status**
   - Go to **ℹ️ About** section
   - Check that all system components show "✓ Ready"
   - Note any warnings or configuration issues

3. **Load Sample Data** (Optional)
   - Go to **📁 Data Upload**
   - Click "Load Personal Paraguay Dataset"
   - This loads sample data for testing

## 📊 Data Upload and Management

### Supported File Formats
The system accepts multiple file formats for maximum flexibility:

#### Excel Files (.xlsx)
- **Recommended format** for most users
- **Automatic column detection** - system identifies comment columns
- **Multiple sheet support** - choose which sheet to analyze
- **Date recognition** - automatically detects date columns for trend analysis

#### CSV Files (.csv)
- **Universal compatibility** with most systems
- **Encoding detection** - handles various character encodings
- **Delimiter detection** - automatic comma, semicolon, or tab detection
- **Large file support** - efficient handling of large datasets

#### JSON Files (.json)
- **Structured data support** for API integrations
- **Nested object handling** - extracts comments from complex structures
- **Array processing** - handles multiple comment arrays
- **Metadata preservation** - maintains additional data fields

#### Text Files (.txt)
- **Simple format** for basic comment lists
- **One comment per line** format
- **UTF-8 encoding** support
- **Batch processing** ready

### Upload Process

#### Step 1: Access Upload Interface
1. Click **📁 Data Upload** in the sidebar
2. Choose your upload method:
   - **Upload New File**: For your own data
   - **Load Sample Dataset**: For testing purposes

#### Step 2: File Selection and Upload
```
For New File Upload:
1. Click "Choose a file" button or drag-and-drop
2. Select your file from the file browser
3. Wait for upload progress to complete
4. Review upload status messages
```

#### Step 3: Data Validation and Preview
After upload, the system will:
- **Validate file format** and structure
- **Detect comment columns** automatically
- **Show data preview** (first 100 rows)
- **Display statistics** (total comments, languages detected)
- **Identify quality issues** (empty rows, encoding problems)

#### Step 4: Column Configuration
If automatic detection needs adjustment:
1. **Review detected columns** in the preview section
2. **Manually select comment column** if needed
3. **Choose date column** for temporal analysis (optional)
4. **Select additional fields** for context (optional)

### Data Quality Guidelines

#### Preparing Your Data
For best results, prepare your data as follows:

**Excel/CSV Format:**
```
Comment                          | Date       | Category
Great internet speed!           | 2024-01-15 | Service
Muy lento el internet           | 2024-01-16 | Technical
Excelente atención al cliente   | 2024-01-17 | Support
```

**Data Quality Checklist:**
- ✅ Comments are in a single column
- ✅ Each row contains one comment
- ✅ Minimum 10 characters per comment
- ✅ No excessive special characters
- ✅ Consistent language (Spanish/Guaraní)
- ✅ Remove personal information (names, phone numbers)

#### Common Data Issues and Solutions

**Issue: Empty or very short comments**
```
Solution: Filter out comments shorter than 10 characters
Example: Remove entries like "ok", "si", "no"
```

**Issue: Mixed languages in single comments**
```
Solution: These are handled automatically by the system
Example: "El internet está good pero expensive"
```

**Issue: Special formatting characters**
```
Solution: System automatically cleans most issues
Manual cleanup recommended for: excessive punctuation, HTML tags
```

## ⚙️ Analysis Configuration

### Configuration Overview
Before running analysis, configure the system to match your needs and budget.

### Analysis Parameters

#### Sample Size Selection
```
Quick Analysis (1-200 comments):
- Purpose: Testing and validation
- Time: 1-5 minutes
- Cost: $0.20 - $4.00
- Use for: Initial data exploration

Batch Processing (Full Dataset):
- Purpose: Complete analysis
- Time: 10-60 minutes
- Cost: Varies by dataset size
- Use for: Production analysis
```

#### Analysis Depth Options
1. **Basic Analysis**
   - Sentiment classification only
   - Fastest processing
   - Lowest cost
   - Good for quick insights

2. **Standard Analysis** (Recommended)
   - Sentiment + basic themes
   - Balanced speed and detail
   - Moderate cost
   - Suitable for most use cases

3. **Comprehensive Analysis**
   - Full sentiment, themes, emotions
   - Detailed insights
   - Higher cost
   - Best for detailed reporting

#### Language Processing Settings
- **Auto-detect**: System determines language automatically
- **Spanish Only**: Process only Spanish comments
- **Guaraní Translation**: Translate Guaraní to Spanish first
- **Mixed Language**: Handle code-switching appropriately

### Cost Management

#### Understanding Costs
The system uses OpenAI's GPT-4 API, which charges based on:
- **Number of comments analyzed**
- **Analysis depth selected**
- **Language processing complexity**

Typical costs:
- **$0.002 per comment** for standard analysis
- **$0.001 per comment** for basic analysis
- **$0.004 per comment** for comprehensive analysis

#### Budget Controls
1. **Set Daily Budget Limit**
   ```
   Navigate to: ⚙️ Settings → Budget Management
   Set limit: $50.00 (example)
   Enable alerts: ✅ Alert at 75% usage
   ```

2. **Monitor Real-time Costs**
   - Live cost tracking during analysis
   - Estimated total cost before starting
   - Budget remaining display
   - Historical usage analytics

3. **Optimization Features**
   - Smart sampling for large datasets
   - Batch size optimization
   - Duplicate detection and removal
   - Similar comment grouping

## 🎯 Running Analysis

### Quick Analysis Workflow

#### Step 1: Start Analysis
1. Go to **📊 Analysis Dashboard**
2. Verify your data is loaded (shows dataset statistics)
3. Select sample size with the slider (start with 50-100 comments)
4. Review estimated cost display
5. Click **🔍 Analyze Comments**

#### Step 2: Monitor Progress
During analysis, you'll see:
- **Progress bar** showing completion percentage
- **Current status** (e.g., "Analyzing sentiment...")
- **Comments processed** count
- **Estimated time remaining**
- **Real-time cost tracking**

#### Step 3: Review Preliminary Results
As analysis progresses:
- **Sentiment distribution** updates in real-time
- **Key themes** appear as they're identified
- **Language breakdown** shows detected languages
- **Quality metrics** indicate analysis confidence

### Batch Processing Workflow

#### Step 1: Configure Batch Settings
1. Select **"Process All"** mode
2. Choose batch size:
   - **50 comments/batch**: Conservative, slower but stable
   - **100 comments/batch**: Balanced (recommended)
   - **200 comments/batch**: Aggressive, faster but higher memory usage

#### Step 2: Review Cost Estimate
Before starting:
- Review **total estimated cost**
- Check **budget remaining**
- Confirm **analysis settings**
- Set **stop conditions** if needed

#### Step 3: Execute and Monitor
1. Click **🚀 Process All**
2. Monitor batch progress:
   - **Batch X of Y** completion
   - **Overall progress** percentage
   - **Error rate** tracking
   - **Performance metrics**

#### Step 4: Quality Checkpoints
The system includes automatic quality checks:
- **Pause for review** if error rate exceeds 5%
- **Quality validation** at 25%, 50%, 75% completion
- **Confidence monitoring** throughout process
- **Option to adjust settings** mid-process

### Handling Interruptions
If analysis is interrupted:
1. **Resume Option**: Continue from last completed batch
2. **Partial Results**: Access already processed data
3. **Reprocess Option**: Start over with different settings
4. **Save Progress**: Export partial results before continuing

## 📈 Understanding Results

### Results Dashboard Overview
After analysis completion, the results dashboard displays:

#### Summary Metrics (Top Section)
```
┌─────────────────────────────────────────────────────────┐
│ 📊 Analysis Summary                                     │
├─────────────────────────────────────────────────────────┤
│ Total Comments: 1,247        Overall Sentiment: 72% +  │
│ Languages: 85% Spanish       Top Theme: Internet Speed │
│ Confidence: 89%              Quality Score: A          │
└─────────────────────────────────────────────────────────┘
```

#### Sentiment Analysis Results
**Sentiment Distribution Pie Chart:**
- **Positive**: Green sections (satisfaction, praise)
- **Negative**: Red sections (complaints, issues)
- **Neutral**: Gray sections (factual, informational)

**Emotion Breakdown Bar Chart:**
- **Joy**: Customer satisfaction and happiness
- **Anger**: Frustration and complaints
- **Sadness**: Disappointment and regret
- **Fear**: Concerns and anxiety
- **Surprise**: Unexpected experiences

**Confidence Metrics:**
- **High Confidence (>80%)**: Reliable results
- **Medium Confidence (60-80%)**: Generally reliable
- **Low Confidence (<60%)**: Review manually

#### Theme Analysis Results
**Top Themes Table:**
```
Theme                 | Count | Sentiment | Priority
Internet Speed        | 234   | 45% Neg   | High
Customer Service      | 187   | 67% Pos   | Medium
Pricing              | 156   | 38% Neg   | High
Installation         | 143   | 78% Pos   | Low
Technical Issues     | 89    | 23% Pos   | High
```

**Theme Categories:**
- **Service Quality**: Speed, reliability, uptime
- **Customer Experience**: Support, installation, billing
- **Technical Issues**: Connection problems, equipment
- **Business Aspects**: Pricing, contracts, promotions

### Detailed Results Table
Access comprehensive results in the detailed table:

#### Column Explanations
- **Original Comment**: The customer's original feedback
- **Language**: Detected language (Spanish/Guaraní/Mixed)
- **Sentiment**: Classification (Positive/Negative/Neutral)
- **Confidence**: Analysis certainty (0-100%)
- **Primary Theme**: Main topic identified
- **Emotions**: Detected emotional content
- **Business Impact**: Potential impact level (High/Medium/Low)

#### Filtering and Sorting
Use the interactive table features:
1. **Filter by Sentiment**: Show only positive/negative comments
2. **Filter by Theme**: Focus on specific topics
3. **Sort by Confidence**: Review uncertain classifications
4. **Search Text**: Find specific comments or keywords

### Business Intelligence Insights

#### Executive Summary
The system generates automatic insights:
```
🎯 Key Findings:
• Customer satisfaction is 72% positive, above industry average
• Internet speed is the primary concern (23% of negative feedback)  
• Customer service receives high praise (78% positive mentions)
• Technical issues affect 15% of customers, requiring attention

🚀 Recommendations:
• Investigate speed issues in high-complaint areas
• Leverage positive service feedback in marketing
• Implement proactive technical support outreach
• Monitor speed improvements impact on satisfaction
```

#### Performance Benchmarks
- **Industry Comparison**: How you compare to telecom industry standards
- **Historical Trends**: Changes from previous analysis periods
- **Regional Variations**: Geographic satisfaction differences
- **Service Category Performance**: Breakdown by service type

#### Risk Indicators
- **Churn Risk Score**: Customers likely to cancel service
- **Escalation Potential**: Issues that may escalate
- **Competitive Threats**: Mentions of competitor services
- **Service Degradation**: Quality decline indicators

### Language Analysis Results

#### Language Distribution
```
📊 Language Breakdown:
• Spanish: 85.3% (1,064 comments)
• Guaraní: 12.1% (151 comments)  
• Mixed: 2.6% (32 comments)
```

#### Translation Quality
For Guaraní content:
- **Translation Confidence**: Average quality score
- **Cultural Context**: Preservation of meaning
- **Regional Variations**: Dialect handling accuracy

#### Language-Specific Insights
- **Spanish Comments**: Direct analysis results
- **Guaraní Comments**: Translated analysis with original context
- **Mixed Language**: Code-switching analysis and interpretation

## 📤 Export and Reporting

### Export Options Overview
The system provides multiple export formats for different use cases:

#### Excel Workbook Export (Recommended)
**What's Included:**
- **Summary Sheet**: Key metrics and insights
- **Detailed Results**: Complete analysis for each comment
- **Charts and Graphs**: Visual representations
- **Pivot Tables**: Interactive data exploration
- **Recommendations**: Business action items

**File Structure:**
```
Personal_Paraguay_Analysis_[Date].xlsx
├── Executive Summary
├── Detailed Analysis  
├── Sentiment Breakdown
├── Theme Analysis
├── Language Report
├── Recommendations
└── Raw Data
```

#### CSV Data Export
**Use Cases:**
- Import into other analytics tools
- Database integration
- Further statistical analysis
- Custom visualization creation

**Data Included:**
- All comment-level analysis results
- Metadata and processing information
- Quality scores and confidence metrics
- Timestamp and processing details

#### Summary Report (Text)
**Business-Focused Report:**
- Executive summary in plain text
- Key findings and recommendations
- Printable format for meetings
- Email-friendly formatting

#### JSON Data Export
**Technical Integration:**
- Machine-readable format
- API-compatible structure
- Complete analysis metadata
- Custom application integration

### Export Process

#### Step 1: Complete Analysis
Ensure analysis is finished before exporting:
- ✅ Analysis status shows "Complete"
- ✅ All batches processed successfully
- ✅ Quality validation passed
- ✅ Results displayed in dashboard

#### Step 2: Choose Export Format
1. Scroll to **📥 Export Results** section
2. Select desired format(s):
   - Click **📊 Export Excel** for comprehensive report
   - Click **📄 Export CSV** for raw data
   - Click **📝 Export Summary** for executive report
   - Click **🔧 Export JSON** for technical integration

#### Step 3: Download Files
1. Wait for export processing (30-60 seconds)
2. Files appear in **📂 Download Files** section
3. Click file names to download
4. Files are saved to your browser's download folder

### Excel Report Guide

#### Executive Summary Sheet
```
┌─────────────────────────────────────────────────────┐
│ PERSONAL PARAGUAY - CUSTOMER FEEDBACK ANALYSIS      │
│ Analysis Date: January 26, 2024                    │
│ Dataset: 1,247 customer comments                   │
└─────────────────────────────────────────────────────┘

Key Metrics:
• Overall Satisfaction: 72% Positive
• Primary Languages: Spanish (85%), Guaraní (12%)
• Top Issue: Internet Speed (234 mentions)
• Service Excellence: Customer Support (78% positive)

Recommendations:
1. Investigate speed issues in Metro Area
2. Expand technical support team
3. Implement proactive speed monitoring
4. Develop Guaraní customer service materials
```

#### Detailed Analysis Sheet
**Interactive Features:**
- **Filter dropdowns** for each column
- **Conditional formatting** highlighting key issues
- **Sortable columns** for custom analysis
- **Comments section** for notes and observations

#### Charts and Visualizations
**Included Charts:**
- Sentiment distribution pie chart
- Theme frequency bar chart  
- Emotion analysis radar chart
- Language distribution chart
- Temporal trend analysis (if dates available)

#### Pivot Tables
**Pre-configured Analysis:**
- Sentiment by theme breakdown
- Monthly/weekly trends
- Language-specific sentiment analysis
- Geographic analysis (if location data available)

### Report Customization

#### Custom Branding
Configure reports with company branding:
1. Go to **⚙️ Settings → Report Configuration**
2. Upload company logo
3. Set brand colors
4. Configure report header/footer
5. Add custom disclaimers

#### Selective Export
Choose specific data to include:
- **Confidence Threshold**: Export only high-confidence results
- **Date Range**: Export specific time periods
- **Theme Filter**: Export specific topic areas
- **Language Filter**: Export single language results

## 🔧 Advanced Features

### Batch Processing Optimization

#### Smart Sampling
For very large datasets (>5,000 comments):
1. **Statistical Sampling**: Analyze representative subset
2. **Stratified Sampling**: Ensure demographic representation
3. **Quality Sampling**: Focus on high-quality comments
4. **Temporal Sampling**: Distribute across time periods

#### Processing Strategies
```
Dataset Size    | Recommended Strategy
< 500 comments  | Full analysis, single batch
500-2000        | Batch processing, 100/batch
2000-5000       | Batch processing, 200/batch  
> 5000          | Smart sampling + batch processing
```

### Quality Control Features

#### Manual Review Interface
Access individual comment review:
1. Go to detailed results table
2. Click **"Review"** on low-confidence results
3. Manually verify or correct classifications
4. System learns from corrections

#### Quality Metrics Dashboard
Monitor analysis quality:
- **Confidence Distribution**: Histogram of confidence scores
- **Inter-rater Reliability**: Consistency across batches
- **Error Rate Tracking**: Failed analysis attempts
- **Manual Override Rate**: Human correction frequency

### Advanced Analytics

#### Trend Analysis
When date information is available:
- **Sentiment Trends**: Track satisfaction over time
- **Theme Evolution**: How topics change over time
- **Seasonal Patterns**: Identify recurring issues
- **Event Correlation**: Link events to sentiment changes

#### Comparative Analysis
Compare different data segments:
- **Period Comparison**: Month-over-month changes
- **Segment Comparison**: Different customer groups
- **Channel Comparison**: Different feedback sources
- **Product Comparison**: Different service offerings

### Integration Features

#### API Access
For technical teams:
```python
# Example API usage
import requests

response = requests.post('/api/analyze', {
    'comments': comment_list,
    'config': analysis_config
})
results = response.json()
```

#### Automated Reporting
Set up automated analysis:
1. **Scheduled Analysis**: Weekly/monthly automatic runs
2. **Email Reports**: Automatic report distribution
3. **Alert System**: Notification for significant changes
4. **Dashboard Integration**: Real-time business intelligence

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Analysis Issues

**Issue: Low Confidence Scores**
```
Symptoms: Many results show <70% confidence
Causes: Unclear comments, mixed languages, technical jargon
Solutions:
• Review comment quality and clarity
• Enable translation for Guaraní content
• Use "comprehensive analysis" mode
• Filter out very short comments
```

**Issue: Unexpected Sentiment Results**
```
Symptoms: Results don't match manual review
Causes: Cultural context, sarcasm, domain-specific language
Solutions:
• Review detailed emotion analysis
• Check individual comment classifications
• Consider cultural context settings
• Use manual review feature for corrections
```

**Issue: Slow Processing**
```
Symptoms: Analysis takes much longer than estimated
Causes: Large batch sizes, API rate limits, network issues
Solutions:
• Reduce batch size to 50-100 comments
• Check internet connection stability
• Monitor API usage limits
• Try during off-peak hours
```

#### Data Issues

**Issue: File Upload Failures**
```
Common Causes:
• File too large (>200MB)
• Unsupported file format
• Corrupted file
• Special characters in filename

Solutions:
• Split large files into smaller chunks
• Convert to supported format (Excel/CSV)
• Re-save file to fix corruption
• Rename file removing special characters
```

**Issue: Column Detection Problems**
```
Symptoms: System doesn't find comment columns
Causes: Non-standard column names, merged cells, formatting
Solutions:
• Rename columns to include "comment" or "feedback"
• Remove merged cells and special formatting
• Use first row as headers
• Manually select columns in interface
```

#### Performance Issues

**Issue: System Running Slowly**
```
Symptoms: Interface lag, slow responses
Causes: Large datasets, insufficient memory, browser issues
Solutions:
• Close other browser tabs
• Restart the application
• Use smaller sample sizes for testing
• Clear browser cache
```

**Issue: Export Failures**
```
Symptoms: Export buttons don't work or files are empty
Causes: Analysis not complete, browser restrictions, file size
Solutions:
• Ensure analysis is 100% complete
• Check browser download settings
• Try different export format
• Clear browser downloads folder
```

### Getting Help

#### Self-Service Resources
1. **Check System Status**: ℹ️ About section
2. **Review Logs**: Look for error messages
3. **Test Configuration**: Run system diagnostics
4. **Check FAQ**: Common questions and answers

#### Diagnostic Information
When contacting support, provide:
- **Error messages**: Exact text of any errors
- **Browser information**: Chrome/Firefox version
- **Dataset size**: Number of comments being processed
- **Analysis configuration**: Settings used
- **System specifications**: Operating system, memory

#### Contact Support
- **Technical Issues**: Contact IT support team
- **Analysis Questions**: Contact business analyst team
- **Feature Requests**: Submit through feedback form
- **Training Needs**: Contact user training coordinator

## 💡 Best Practices

### Data Preparation Best Practices

#### Optimal Data Quality
```
✅ DO:
• Include 50+ comments for meaningful analysis
• Ensure comments are substantive (>20 characters)
• Remove personal information before upload
• Use consistent date formats
• Keep original language intact

❌ DON'T:
• Include test data or placeholder text
• Mix different data sources without context
• Include duplicate comments
• Use excessive abbreviations or acronyms
• Include comments in unsupported languages
```

#### File Organization
```
Recommended File Structure:
• One comment per row
• Clear column headers
• Consistent data formatting
• Include metadata (dates, categories)
• Use descriptive filenames

Example Good Filename:
"Personal_Paraguay_Customer_Comments_Jan2024.xlsx"

Example Poor Filename:
"data123.csv"
```

### Analysis Strategy Best Practices

#### Progressive Analysis Approach
1. **Start Small**: Begin with 100-200 comments
2. **Validate Results**: Review quality and accuracy
3. **Optimize Settings**: Adjust based on initial results
4. **Scale Up**: Process full dataset with optimized settings
5. **Monitor Quality**: Check confidence scores throughout

#### Budget Management
```
Cost Optimization Strategy:
1. Use sample analysis for initial insights ($2-5)
2. Implement duplicate detection (-20% cost)
3. Choose appropriate analysis depth
4. Monitor usage with daily budgets
5. Schedule large analyses during off-peak hours
```

### Results Interpretation Best Practices

#### Confidence Score Guidelines
```
Confidence Level | Interpretation | Action Required
90-100%         | Highly reliable | Use directly
80-89%          | Very reliable   | Minimal review needed
70-79%          | Generally reliable | Spot check key results  
60-69%          | Needs review    | Manual validation
<60%            | Uncertain       | Detailed review required
```

#### Business Decision Framework
```
Priority Matrix for Issues:
High Impact + High Frequency = Immediate Action
High Impact + Low Frequency = Monitor Closely  
Low Impact + High Frequency = Process Improvement
Low Impact + Low Frequency = Note for Reference
```

### Reporting Best Practices

#### Executive Reporting
```
Effective Executive Summary Structure:
1. Key Metric (Overall satisfaction: 72%)
2. Primary Insight (Speed is main concern)
3. Business Impact (15% of customers affected)
4. Recommended Action (Investigate Metro Area speeds)
5. Success Metric (Target: 80% satisfaction next quarter)
```

#### Stakeholder Communication
- **Customer Service**: Focus on specific complaint themes
- **Technical Teams**: Highlight technical issue patterns
- **Management**: Emphasize business impact and ROI
- **Marketing**: Identify positive themes for promotion

### Continuous Improvement

#### Regular Analysis Schedule
```
Recommended Schedule:
• Weekly: High-level metrics monitoring
• Monthly: Detailed theme analysis  
• Quarterly: Comprehensive trend analysis
• Annually: Full system review and optimization
```

#### Quality Monitoring
- Track confidence score trends over time
- Monitor manual override rates
- Review customer satisfaction correlation
- Validate insights with business outcomes

#### System Optimization
- Regularly update analysis configurations
- Optimize batch sizes based on performance
- Review and update business rules
- Train team on new features and capabilities

---

## 📞 Support and Resources

### Quick Reference
- **Application URL**: http://localhost:8501
- **Support Email**: support@personal.com.py
- **Documentation**: /docs folder
- **FAQ**: See user-guides/faq.md

### Training Resources
- **Video Tutorials**: Available in training portal
- **User Training Sessions**: Monthly group sessions
- **One-on-one Support**: Available upon request
- **Best Practices Workshop**: Quarterly sessions

For additional help, refer to the [FAQ](faq.md) or contact your system administrator.