# Comment Analyzer - Customer Feedback Analysis System

A sophisticated multilingual sentiment analysis and pattern detection system designed for analyzing customer comments about fiber-to-the-home services. Built specifically for Personal Paraguay (Núcleo S.A.) to provide actionable business intelligence from customer feedback.

## 🚀 Features

### Core Capabilities
- **Multilingual Support**: Full support for Spanish (Paraguayan dialect) and Guaraní
- **Advanced Sentiment Analysis**: AI-powered emotion detection and sentiment scoring
- **Pattern Recognition**: Automatic theme identification and trend analysis
- **Interactive Dashboard**: Real-time visualization with Streamlit
- **Professional Reporting**: Excel exports with detailed analytics and visualizations

### Technical Features
- **API Integration**: OpenAI GPT-4, Azure Text Analytics, Google Cloud Translation
- **Performance Optimization**: Intelligent caching, batch processing, memory management
- **Cost Control**: Built-in API usage monitoring and optimization
- **Responsive Design**: Mobile-friendly interface with dark mode support
- **Security**: Input validation, rate limiting, secure API handling

## 📁 Project Structure

```
Comment-Analyzer/
├── src/                          # Source code
│   ├── analysis_service/        # Core analysis logic
│   ├── api/                     # API clients and monitoring
│   ├── components/              # UI components
│   ├── data_processing/         # Data ingestion and cleaning
│   ├── sentiment_analysis/      # Sentiment detection modules
│   ├── pattern_detection/       # Theme and pattern analysis
│   ├── services/                # Business logic services
│   ├── theme/                   # UI theming and styles
│   ├── utils/                   # Utility functions
│   └── visualization/           # Charts and exports
├── data/                        # Data storage
│   ├── raw/                     # Original datasets
│   ├── cache/                   # API response cache
│   └── monitoring/              # Usage metrics
├── outputs/                     # Generated results
│   ├── reports/                 # Analysis reports
│   ├── exports/                 # Excel/CSV exports
│   └── visualizations/          # Generated charts
├── tests/                       # Test suite
└── documentation/               # User guides and docs
```

## 🛠️ Technology Stack

- **Framework**: Python 3.8+ with Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **AI/ML APIs**: 
  - OpenAI GPT-4 (pattern detection)
  - Azure Text Analytics (sentiment analysis)
  - Google Cloud Translation (language support)
- **Export**: XlsxWriter, ReportLab
- **Testing**: Pytest, unittest

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aiwhispererwvdp/Comment-Analizer.git
   cd Comment-Analizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file with your API credentials:
   ```env
   OPENAI_API_KEY=your_openai_key
   AZURE_TEXT_ANALYTICS_KEY=your_azure_key
   AZURE_TEXT_ANALYTICS_ENDPOINT=your_azure_endpoint
   GOOGLE_APPLICATION_CREDENTIALS=path_to_google_credentials.json
   ```

## 🚀 Usage

### Quick Start
```bash
streamlit run src/main.py
```

### Alternative Entry Points
- **Simplified Interface**: `streamlit run src/simplified_main.py`
- **Spanish Interface**: `streamlit run src/simplified_main_es.py`
- **Responsive Mode**: `streamlit run src/responsive_main.py`
- **Optimized Version**: `streamlit run src/optimized_main.py`

### Data Input
1. Navigate to http://localhost:8501
2. Upload Excel file with customer comments
3. Select analysis parameters
4. View real-time results and export reports

## 📊 Input Data Format

The system expects Excel files with the following structure:
- **Comment Column**: Text feedback from customers
- **Date Column** (optional): Timestamp of feedback
- **Category Column** (optional): Pre-existing categories
- **Rating Column** (optional): Numerical ratings

## 📈 Output Capabilities

### Analysis Results
- Sentiment scores and classifications
- Emotion detection (joy, anger, sadness, fear, surprise)
- Key themes and patterns
- Trend analysis over time
- Customer satisfaction metrics

### Export Formats
- **Excel**: Comprehensive workbook with multiple sheets
  - Summary statistics
  - Detailed analysis per comment
  - Visualizations and charts
  - Pivot tables for exploration
- **CSV**: Raw data export for further processing
- **PDF**: Professional reports with visualizations
- **JSON**: Structured data for API integration

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_file_upload_service.py

# Run with coverage
pytest --cov=src tests/
```

## 📖 Documentation

- [User Guide](documentation/USER_GUIDE.md) - Complete usage instructions
- [API Documentation](src/api/README.md) - API integration details
- [Theme Customization](src/theme/README.md) - UI theming guide

## 🔒 Security & Privacy

- All data processing is performed locally
- API calls use encrypted connections
- No customer data is stored permanently
- Configurable data retention policies
- Input validation and sanitization

## 🎯 Use Cases

- **Customer Service**: Identify common complaints and issues
- **Product Development**: Understand feature requests and needs
- **Marketing**: Gauge campaign effectiveness and brand sentiment
- **Quality Assurance**: Track service quality trends
- **Business Intelligence**: Data-driven decision making

## 📝 License

Proprietary - Personal Paraguay (Núcleo S.A.)

## 🤝 Support

For support, feature requests, or bug reports, please contact the development team or create an issue in this repository.

## 🏗️ Development Status

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: July 2025

---

Built with ❤️ for Personal Paraguay to enhance customer experience through data-driven insights.