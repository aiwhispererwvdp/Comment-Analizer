# Personal Paraguay Fiber To The Home Customer Comments Analysis System

**Client**: Personal Paraguay (Núcleo S.A.)  
**Project Type**: Customer Sentiment Analysis and Pattern Detection  
**Language Support**: Spanish + Guarani  

## Project Overview

AI-powered system to analyze customer comments about fiber-to-the-home services, providing sentiment analysis and pattern detection for business intelligence and customer experience improvement.

## Project Structure

```
Personal_Paraguay_Fiber_Comments_Analysis/
├── src/                           # Source code
│   ├── data_processing/          # Data ingestion and cleaning
│   ├── sentiment_analysis/       # Emotion and sentiment detection
│   ├── pattern_detection/        # Theme and pattern analysis
│   ├── visualization/            # Dashboard and reporting
│   └── api/                      # API integration layer
├── data/                         # Data storage
│   ├── raw/                      # Original datasets
│   ├── processed/                # Cleaned and processed data
│   └── sample/                   # Sample data for testing
├── outputs/                      # Generated results
│   ├── reports/                  # Analysis reports
│   ├── visualizations/           # Charts and graphs
│   └── exports/                  # Export files (PDF, Excel)
├── tests/                        # Testing suite
│   ├── unit_tests/              # Unit tests
│   └── integration_tests/       # Integration tests
└── documentation/               # Project documentation

```

## Key Features

- **Multilingual Support**: Spanish (Paraguayan dialect) + Guarani translation
- **Sentiment Analysis**: AI-powered emotion detection using Azure Text Analytics
- **Pattern Detection**: Theme identification using OpenAI GPT-4
- **Interactive Dashboard**: Streamlit-based visualization interface
- **Export Capabilities**: PDF reports and Excel exports

## Technology Stack

- **Python 3.8+**
- **Translation**: Google Cloud Translation API
- **Sentiment Analysis**: Azure Text Analytics API  
- **Pattern Recognition**: OpenAI GPT-4 API
- **Visualization**: Streamlit, Matplotlib, Plotly
- **Data Processing**: Pandas, NumPy

## Getting Started

1. Set up API credentials (Google Cloud, Azure, OpenAI)
2. Install Python dependencies
3. Configure environment variables
4. Load customer comment data
5. Run analysis pipeline

## Current Status

**Phase**: Initial Development  
**Progress**: Project structure created, ready for implementation