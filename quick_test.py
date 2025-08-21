"""
Quick Test Script - Verify Core Functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("=" * 60)
print("QUICK SYSTEM TEST")
print("=" * 60)

# Test 1: Configuration
print("\n1. Testing Configuration...")
try:
    from config import Config, validate_config
    validate_config()
    print("   [PASS] Configuration loaded successfully")
except Exception as e:
    print(f"   [FAIL] Configuration error: {e}")

# Test 2: Services
print("\n2. Testing Services...")
try:
    from services.file_upload_service import FileUploadService
    service = FileUploadService()
    print("   [PASS] File Upload Service ready")
except Exception as e:
    print(f"   [FAIL] Service error: {e}")

# Test 3: Session Manager
print("\n3. Testing Session Manager...")
try:
    from services.session_manager import SessionManager
    manager = SessionManager()
    print("   [PASS] Session Manager ready")
except Exception as e:
    print(f"   [FAIL] Session Manager error: {e}")

# Test 4: Sentiment Analysis
print("\n4. Testing Sentiment Analysis...")
try:
    from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
    analyzer = EnhancedAnalyzer()
    print(f"   [PASS] Sentiment Analysis module loaded")
except Exception as e:
    print(f"   [FAIL] Sentiment Analysis error: {e}")

# Test 5: Data Processing
print("\n5. Testing Data Processing...")
try:
    import pandas as pd
    df = pd.DataFrame({'test': [1, 2, 3]})
    print(f"   [PASS] Data processing ready - Created DataFrame with {len(df)} rows")
except Exception as e:
    print(f"   [FAIL] Data processing error: {e}")

# Test 6: Check Streamlit
print("\n6. Testing Streamlit...")
try:
    import streamlit as st
    print("   [PASS] Streamlit is installed")
except Exception as e:
    print(f"   [FAIL] Streamlit error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE - System is ready if all tests passed")
print("=" * 60)
print("\nTo run the application:")
print("  streamlit run src/main.py")
print("  streamlit run src/simplified_main.py")
print("  streamlit run src/test_app.py")