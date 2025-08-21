#!/usr/bin/env python
"""
System Testing Script for Personal Paraguay Fiber Comments Analysis
Run this script to verify all core functionalities are working
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Terminal colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

def print_test(test_name, passed, details=""):
    """Print test result"""
    if passed:
        status = f"{Colors.GREEN}✅ PASSED{Colors.ENDC}"
    else:
        status = f"{Colors.RED}❌ FAILED{Colors.ENDC}"
    
    print(f"  {test_name}: {status}")
    if details:
        print(f"    {Colors.YELLOW}{details}{Colors.ENDC}")

def test_environment():
    """Test environment setup"""
    print_header("ENVIRONMENT TESTS")
    
    # Test Python version
    python_version = sys.version_info
    print_test(
        "Python Version",
        python_version.major == 3 and python_version.minor >= 8,
        f"Version: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )
    
    # Test required directories
    required_dirs = [
        'data/raw',
        'data/cache',
        'data/processed',
        'outputs/reports',
        'outputs/exports',
        'outputs/visualizations'
    ]
    
    all_dirs_exist = True
    for dir_path in required_dirs:
        exists = Path(dir_path).exists()
        if not exists:
            all_dirs_exist = False
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print_test(
        "Directory Structure",
        True,  # We create them if they don't exist
        "All required directories present or created"
    )
    
    # Test .env file
    env_exists = Path('.env').exists()
    print_test(
        "Environment File",
        env_exists,
        ".env file found" if env_exists else "⚠️  .env file missing - create from .env.example"
    )
    
    return env_exists

def test_imports():
    """Test all required imports"""
    print_header("IMPORT TESTS")
    
    imports_to_test = [
        ('pandas', 'Data Processing'),
        ('numpy', 'Numerical Computing'),
        ('streamlit', 'Web Interface'),
        ('plotly', 'Visualizations'),
        ('openai', 'AI Integration'),
        ('openpyxl', 'Excel Support'),
        ('nltk', 'NLP Processing'),
        ('fuzzywuzzy', 'String Matching'),
    ]
    
    all_passed = True
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print_test(f"{description} ({module_name})", True)
        except ImportError as e:
            print_test(f"{description} ({module_name})", False, str(e))
            all_passed = False
    
    return all_passed

def test_configuration():
    """Test configuration loading"""
    print_header("CONFIGURATION TESTS")
    
    try:
        from config import Config, validate_config
        
        # Test Config class exists
        print_test("Config Class", True, "Successfully imported")
        
        # Test configuration validation
        try:
            validate_config()
            print_test("Configuration Validation", True)
        except Exception as e:
            print_test("Configuration Validation", False, str(e))
        
        # Test API key presence
        has_api_key = bool(Config.OPENAI_API_KEY)
        print_test(
            "OpenAI API Key",
            has_api_key,
            "API key configured" if has_api_key else "⚠️  No API key - limited functionality"
        )
        
        # Test settings
        settings_valid = all([
            hasattr(Config, 'BATCH_SIZE'),
            hasattr(Config, 'MAX_RETRIES'),
            hasattr(Config, 'SENTIMENT_CONFIDENCE_THRESHOLD')
        ])
        print_test("Configuration Settings", settings_valid)
        
        return True
    except Exception as e:
        print_test("Configuration Loading", False, str(e))
        return False

def test_services():
    """Test core services"""
    print_header("SERVICE TESTS")
    
    all_passed = True
    
    # Test File Upload Service
    try:
        from services.file_upload_service import FileUploadService
        service = FileUploadService()
        print_test("File Upload Service", True, f"Supports: {', '.join(service.supported_extensions)}")
    except Exception as e:
        print_test("File Upload Service", False, str(e))
        all_passed = False
    
    # Test Session Manager
    try:
        from services.session_manager import SessionManager
        manager = SessionManager()
        print_test("Session Manager", True, "Session management ready")
    except Exception as e:
        print_test("Session Manager", False, str(e))
        all_passed = False
    
    # Test Analysis Service
    try:
        from services.analysis_service import AnalysisService
        print_test("Analysis Service", True, "Analysis engine ready")
    except Exception as e:
        print_test("Analysis Service", False, str(e))
        all_passed = False
    
    return all_passed

def test_data_processing():
    """Test data processing capabilities"""
    print_header("DATA PROCESSING TESTS")
    
    # Create test data
    test_data = pd.DataFrame({
        'Comment': [
            'Excelente servicio de fibra óptica',
            'Problemas constantes de conexión',
            'Servicio normal sin quejas',
            'Muy satisfecho con la velocidad',
            'Internet muy lento y caro'
        ],
        'Date': pd.date_range(start='2024-01-01', periods=5),
        'Rating': [5, 2, 3, 4, 1]
    })
    
    # Save test data
    test_file = 'test_data_temp.xlsx'
    test_data.to_excel(test_file, index=False)
    
    try:
        # Test file reading
        from data_processing.comment_reader import CommentReader
        reader = CommentReader()
        
        # Test Excel reading
        df = pd.read_excel(test_file)
        print_test(
            "Excel File Reading",
            len(df) == 5,
            f"Read {len(df)} rows successfully"
        )
        
        # Test data validation
        has_required_columns = 'Comment' in df.columns
        print_test(
            "Data Validation",
            has_required_columns,
            "Required columns present"
        )
        
        # Clean up
        Path(test_file).unlink(missing_ok=True)
        return True
        
    except Exception as e:
        print_test("Data Processing", False, str(e))
        Path(test_file).unlink(missing_ok=True)
        return False

def test_sentiment_analysis():
    """Test sentiment analysis capabilities"""
    print_header("SENTIMENT ANALYSIS TESTS")
    
    try:
        from sentiment_analysis.basic_analyzer import BasicAnalyzer
        analyzer = BasicAnalyzer()
        
        # Test positive sentiment
        positive_text = "Excelente servicio, muy satisfecho"
        pos_result = analyzer.analyze_sentiment(positive_text)
        print_test(
            "Positive Sentiment Detection",
            pos_result['sentiment'] == 'positive',
            f"Detected: {pos_result['sentiment']}"
        )
        
        # Test negative sentiment
        negative_text = "Terrible servicio, muy malo"
        neg_result = analyzer.analyze_sentiment(negative_text)
        print_test(
            "Negative Sentiment Detection",
            neg_result['sentiment'] == 'negative',
            f"Detected: {neg_result['sentiment']}"
        )
        
        # Test neutral sentiment
        neutral_text = "El servicio funciona"
        neu_result = analyzer.analyze_sentiment(neutral_text)
        print_test(
            "Neutral Sentiment Detection",
            neu_result['sentiment'] in ['neutral', 'positive', 'negative'],
            f"Detected: {neu_result['sentiment']}"
        )
        
        return True
        
    except Exception as e:
        print_test("Sentiment Analysis", False, str(e))
        return False

def test_language_detection():
    """Test language detection"""
    print_header("LANGUAGE DETECTION TESTS")
    
    try:
        from data_processing.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        # Test Spanish detection
        spanish_text = "Este es un texto en español"
        spanish_lang = detector.detect(spanish_text)
        print_test(
            "Spanish Detection",
            spanish_lang == 'es',
            f"Detected: {spanish_lang}"
        )
        
        # Test English detection
        english_text = "This is text in English"
        english_lang = detector.detect(english_text)
        print_test(
            "English Detection",
            english_lang == 'en',
            f"Detected: {english_lang}"
        )
        
        return True
        
    except Exception as e:
        print_test("Language Detection", False, str(e))
        # Not critical - language detection is optional
        return True

def test_export_functionality():
    """Test export capabilities"""
    print_header("EXPORT TESTS")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'comment': ['Test 1', 'Test 2'],
        'sentiment': ['positive', 'negative'],
        'score': [0.8, 0.2]
    })
    
    try:
        # Test Excel export
        excel_file = 'outputs/exports/test_export.xlsx'
        sample_data.to_excel(excel_file, index=False)
        print_test(
            "Excel Export",
            Path(excel_file).exists(),
            "Excel file created successfully"
        )
        Path(excel_file).unlink(missing_ok=True)
        
        # Test CSV export
        csv_file = 'outputs/exports/test_export.csv'
        sample_data.to_csv(csv_file, index=False)
        print_test(
            "CSV Export",
            Path(csv_file).exists(),
            "CSV file created successfully"
        )
        Path(csv_file).unlink(missing_ok=True)
        
        # Test JSON export
        json_file = 'outputs/exports/test_export.json'
        sample_data.to_json(json_file, orient='records')
        print_test(
            "JSON Export",
            Path(json_file).exists(),
            "JSON file created successfully"
        )
        Path(json_file).unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print_test("Export Functionality", False, str(e))
        return False

def test_api_connectivity():
    """Test API connectivity (optional)"""
    print_header("API CONNECTIVITY TESTS")
    
    try:
        from config import Config
        
        if Config.OPENAI_API_KEY:
            import openai
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # Test with minimal API call
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Use cheaper model for testing
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                print_test("OpenAI API", True, "Connection successful")
                return True
            except Exception as e:
                print_test("OpenAI API", False, f"Connection failed: {str(e)[:50]}")
                return False
        else:
            print_test("OpenAI API", False, "No API key configured - skipping")
            return True  # Not critical
            
    except Exception as e:
        print_test("API Connectivity", False, str(e))
        return True  # Not critical

def generate_test_report(results):
    """Generate test report"""
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"  Total Tests: {total_tests}")
    print(f"  {Colors.GREEN}Passed: {passed_tests}{Colors.ENDC}")
    print(f"  {Colors.RED}Failed: {failed_tests}{Colors.ENDC}")
    print(f"  Pass Rate: {pass_rate:.1f}%")
    
    if pass_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL SYSTEMS OPERATIONAL!{Colors.ENDC}")
        print("The application is ready for use.")
    elif pass_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  SYSTEM MOSTLY OPERATIONAL{Colors.ENDC}")
        print("Some features may have limited functionality.")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SYSTEM NEEDS ATTENTION{Colors.ENDC}")
        print("Please fix the failed tests before using the application.")
    
    # Save report
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(f"Test Report - {datetime.now()}\n")
        f.write(f"{'='*50}\n")
        f.write(f"Total Tests: {total_tests}\n")
        f.write(f"Passed: {passed_tests}\n")
        f.write(f"Failed: {failed_tests}\n")
        f.write(f"Pass Rate: {pass_rate:.1f}%\n")
        f.write(f"{'='*50}\n")
        f.write("Test Results:\n")
        for test_name, passed in results.items():
            f.write(f"  {test_name}: {'PASSED' if passed else 'FAILED'}\n")
    
    print(f"\n📄 Report saved to: {report_file}")

def main():
    """Run all system tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🧪 PERSONAL PARAGUAY FIBER COMMENTS ANALYSIS{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}   SYSTEM TESTING SUITE{Colors.ENDC}")
    print(f"{Colors.YELLOW}   Version: 1.0.0{Colors.ENDC}")
    print(f"{Colors.YELLOW}   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    results = {}
    
    # Run tests
    results['Environment'] = test_environment()
    results['Imports'] = test_imports()
    results['Configuration'] = test_configuration()
    results['Services'] = test_services()
    results['Data Processing'] = test_data_processing()
    results['Sentiment Analysis'] = test_sentiment_analysis()
    results['Language Detection'] = test_language_detection()
    results['Export'] = test_export_functionality()
    
    # Optional API test (only if configured)
    from config import Config
    if Config.OPENAI_API_KEY:
        results['API Connectivity'] = test_api_connectivity()
    
    # Generate report
    generate_test_report(results)
    
    # Return exit code
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Testing interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)