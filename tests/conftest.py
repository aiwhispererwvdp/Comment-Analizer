"""
Pytest configuration and shared fixtures for all tests
Enhanced with comprehensive testing framework integration
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import os
import sys
from datetime import datetime, timedelta
import json
import warnings

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root))

# Import framework components
from tests.config import TestEnvironment, config_manager, set_test_environment
from tests.factories.test_factories import CommentFactory, UserFactory, AnalysisResultFactory
from tests.builders.mock_builders import (
    SentimentAnalyzerMockBuilder, 
    OpenAIMockBuilder, 
    DataFrameMockBuilder,
    mock_sentiment_analyzer,
    mock_openai_client
)

# Set test environment variables
os.environ['TESTING'] = 'True'
os.environ['DEBUG'] = 'False'
os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'
os.environ['LOG_LEVEL'] = 'ERROR'  # Reduce log noise during testing

# Suppress warnings during testing
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'Comentario': [
            'Excelente servicio, muy satisfecho',
            'El internet es muy lento',
            'Buen precio pero mala atención',
            'No funciona desde ayer',
            'Perfecto, sin problemas'
        ],
        'Fecha': pd.date_range('2024-01-01', periods=5),
        'Nota': [5, 2, 3, 1, 5],
        'Ciudad': ['Asunción', 'Ciudad del Este', 'Asunción', 'Luque', 'San Lorenzo']
    })


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_streamlit():
    """Mock streamlit for testing"""
    mock_st = MagicMock()
    mock_st.session_state = {}
    mock_st.sidebar = MagicMock()
    mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
    mock_st.tabs = MagicMock(return_value=[MagicMock() for _ in range(5)])
    return mock_st


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"sentiment": "positive", "score": 0.9}'))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def sample_excel_file(temp_dir, sample_dataframe):
    """Create a sample Excel file for testing"""
    file_path = temp_dir / 'test_data.xlsx'
    sample_dataframe.to_excel(file_path, index=False)
    return file_path


@pytest.fixture
def sample_csv_file(temp_dir, sample_dataframe):
    """Create a sample CSV file for testing"""
    file_path = temp_dir / 'test_data.csv'
    sample_dataframe.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    mock_cfg = MagicMock()
    mock_cfg.OPENAI_API_KEY = 'test-key'
    mock_cfg.MAX_FILE_SIZE_MB = 50
    mock_cfg.MAX_ROWS = 20000
    mock_cfg.BATCH_SIZE = 100
    mock_cfg.SUPPORTED_EXTENSIONS = ['.xlsx', '.csv', '.json', '.txt']
    return mock_cfg


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    # Reset any global singletons here
    yield
    # Cleanup after test


@pytest.fixture
def sample_comments():
    """Sample comments for testing sentiment analysis"""
    return {
        'positive': [
            'Excelente servicio de fibra óptica, muy satisfecho',
            'La velocidad es increíble, lo mejor que he tenido',
            'Instalación perfecta y rápida, muy profesionales'
        ],
        'negative': [
            'Terrible servicio, siempre se corta',
            'Muy lento y caro, no lo recomiendo',
            'Pésima atención al cliente, muy malo'
        ],
        'neutral': [
            'El servicio funciona normalmente',
            'Sin comentarios particulares',
            'Es un servicio de internet estándar'
        ]
    }


@pytest.fixture
def multi_language_comments():
    """Comments in multiple languages for testing"""
    return {
        'spanish': 'Excelente servicio de internet',
        'guarani': 'Iporãite pe servicio',
        'mixed': 'Che servicio iporã pero un poco expensive',
        'english': 'Great internet service'
    }


@pytest.fixture
def mock_analysis_result():
    """Mock analysis result for testing"""
    return {
        'sentiment': 'positive',
        'confidence': 0.85,
        'emotions': {
            'joy': 0.7,
            'anger': 0.1,
            'sadness': 0.1,
            'fear': 0.05,
            'surprise': 0.05
        },
        'themes': ['service_quality', 'speed', 'reliability'],
        'language': 'es'
    }


@pytest.fixture
def large_dataframe():
    """Create a large dataframe for performance testing"""
    num_rows = 1000
    comments = [
        'Excelente servicio' if i % 3 == 0 
        else 'Mal servicio' if i % 3 == 1 
        else 'Servicio normal'
        for i in range(num_rows)
    ]
    return pd.DataFrame({
        'Comentario': comments,
        'Fecha': pd.date_range('2024-01-01', periods=num_rows, freq='H'),
        'Nota': np.random.randint(1, 6, num_rows),
        'Ciudad': np.random.choice(['Asunción', 'Ciudad del Este', 'Luque'], num_rows)
    })


@pytest.fixture
def mock_uploaded_file(sample_excel_file):
    """Mock uploaded file object for Streamlit"""
    mock_file = MagicMock()
    mock_file.name = 'test_data.xlsx'
    mock_file.size = 1024 * 10  # 10KB
    mock_file.type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    # Read actual file content
    with open(sample_excel_file, 'rb') as f:
        content = f.read()
    mock_file.read.return_value = content
    mock_file.getvalue.return_value = content
    
    return mock_file


@pytest.fixture
def test_output_dir(temp_dir):
    """Create test output directory structure"""
    output_dir = temp_dir / 'outputs'
    (output_dir / 'reports').mkdir(parents=True)
    (output_dir / 'exports').mkdir(parents=True)
    (output_dir / 'visualizations').mkdir(parents=True)
    return output_dir


# Framework-integrated fixtures

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment for the session"""
    # Set default test environment
    set_test_environment(TestEnvironment.UNIT)
    
    # Load environment-specific configuration
    config_manager.load_from_environment()
    
    yield
    
    # Cleanup after session


@pytest.fixture
def test_config():
    """Get current test configuration"""
    from tests.config import get_test_config
    return get_test_config()


@pytest.fixture
def comment_factory():
    """Comment factory for generating test data"""
    return CommentFactory


@pytest.fixture
def user_factory():
    """User factory for generating test data"""
    return UserFactory


@pytest.fixture
def analysis_result_factory():
    """Analysis result factory for generating test data"""
    return AnalysisResultFactory


@pytest.fixture
def sentiment_analyzer_mock():
    """Pre-configured sentiment analyzer mock"""
    return mock_sentiment_analyzer("positive", 0.8)


@pytest.fixture
def openai_client_mock():
    """Pre-configured OpenAI client mock"""
    return mock_openai_client("positive")


@pytest.fixture
def enhanced_sentiment_analyzer_mock():
    """Enhanced sentiment analyzer mock with multiple features"""
    return (SentimentAnalyzerMockBuilder()
           .with_sentiment_result("positive", 0.85)
           .with_language_detection("es")
           .with_performance_tracking(0.1)
           .build())


@pytest.fixture
def openai_mock_with_costs():
    """OpenAI mock with cost tracking"""
    return (OpenAIMockBuilder()
           .with_successful_response("positive")
           .with_cost_tracking(0.0001)
           .build())


@pytest.fixture
def large_test_dataframe():
    """Large DataFrame using factory for performance testing"""
    builder = DataFrameMockBuilder()
    comments = CommentFactory.create_batch(1000)
    return (builder
           .with_comments_column(comments)
           .with_dates_column()
           .with_ids_column()
           .with_sentiment_results()
           .build())


@pytest.fixture
def small_test_dataframe():
    """Small DataFrame using factory for unit testing"""
    builder = DataFrameMockBuilder()
    comments = CommentFactory.create_batch(10)
    return (builder
           .with_comments_column(comments)
           .with_dates_column()
           .with_ids_column()
           .build())


@pytest.fixture
def performance_test_data():
    """Performance test data with various sizes"""
    return {
        'small': CommentFactory.create_batch(10),
        'medium': CommentFactory.create_batch(100),
        'large': CommentFactory.create_batch(1000),
        'xlarge': CommentFactory.create_batch(5000)
    }


@pytest.fixture
def multilingual_test_comments():
    """Multilingual comments for testing language detection"""
    return {
        'spanish': CommentFactory.create(content="Excelente servicio de internet"),
        'guarani': CommentFactory.create(content="Iporãite pe servicio"),
        'mixed': CommentFactory.create(content="Che servicio iporã pero expensive"),
        'english': CommentFactory.create(content="Great internet service")
    }


@pytest.fixture
def test_analysis_results():
    """Collection of test analysis results"""
    return [
        AnalysisResultFactory.create(sentiment="positive", confidence=0.9),
        AnalysisResultFactory.create(sentiment="negative", confidence=0.8),
        AnalysisResultFactory.create(sentiment="neutral", confidence=0.6),
        AnalysisResultFactory.create(sentiment="positive", confidence=0.75),
        AnalysisResultFactory.create(sentiment="negative", confidence=0.85)
    ]


@pytest.fixture
def mock_file_processor():
    """Mock file processor for testing file operations"""
    from tests.builders.mock_builders import FileMockBuilder
    
    processor_mock = Mock()
    
    # Mock CSV processing
    csv_mock = (FileMockBuilder()
               .with_csv_content(DataFrameMockBuilder()
                               .with_comments_column(CommentFactory.create_batch(5))
                               .with_dates_column()
                               .build())
               .build())
    
    processor_mock.process_csv.return_value = csv_mock
    return processor_mock


@pytest.fixture
def performance_thresholds():
    """Performance thresholds for testing"""
    from tests.performance import PerformanceThresholds
    return PerformanceThresholds(
        max_execution_time=2.0,
        max_memory_usage_mb=200.0,
        min_throughput_ops_per_sec=5.0,
        max_cpu_percent=70.0,
        min_success_rate=0.90
    )


@pytest.fixture
def performance_benchmark():
    """Performance benchmark instance for testing"""
    from tests.performance import PerformanceBenchmark
    return PerformanceBenchmark()


@pytest.fixture
def api_response_mock():
    """Mock API response for testing"""
    from tests.builders.mock_builders import APIResponseMockBuilder
    return (APIResponseMockBuilder()
           .with_success_response({"result": "analysis completed"})
           .build())


@pytest.fixture(autouse=True)
def reset_framework_state():
    """Reset framework state between tests"""
    # Reset factory sequences
    CommentFactory.reset_sequence()
    UserFactory.reset_sequence()
    AnalysisResultFactory.reset_sequence()
    
    yield
    
    # Cleanup after test
    CommentFactory.reset_sequence()
    UserFactory.reset_sequence()
    AnalysisResultFactory.reset_sequence()


@pytest.fixture
def database_mock():
    """Mock database for testing"""
    from tests.builders.mock_builders import DatabaseMockBuilder
    
    test_data = [
        {'id': 1, 'comment': 'Test comment 1', 'sentiment': 'positive'},
        {'id': 2, 'comment': 'Test comment 2', 'sentiment': 'negative'}
    ]
    
    return (DatabaseMockBuilder()
           .with_table_data('comments', test_data)
           .with_transaction_support()
           .build())


# Pytest configuration

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")
    config.addinivalue_line("markers", "security: marks tests as security tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on path"""
    for item in items:
        # Add markers based on test file path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
        elif "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="session")
def test_session_info():
    """Information about the test session"""
    return {
        'start_time': datetime.now(),
        'python_version': sys.version,
        'platform': sys.platform,
        'test_framework_version': '1.0.0'
    }