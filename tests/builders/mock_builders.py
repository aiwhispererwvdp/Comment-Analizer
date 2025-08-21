"""
Mock builders for creating consistent mock objects across tests
Provides fluent interface for building complex mock scenarios
"""

from unittest.mock import Mock, MagicMock, AsyncMock, patch, PropertyMock
from typing import Any, Dict, List, Optional, Union, Callable
import pandas as pd
import json
from datetime import datetime, timedelta
import random


class BaseMockBuilder:
    """Base class for all mock builders"""
    
    def __init__(self):
        self.mock = Mock()
        self._patches = []
        self._attributes = {}
        self._methods = {}
        self._properties = {}
    
    def with_attribute(self, name: str, value: Any):
        """Add an attribute to the mock"""
        self._attributes[name] = value
        return self
    
    def with_method(self, name: str, return_value: Any = None, side_effect: Any = None):
        """Add a method to the mock"""
        method_mock = Mock()
        if return_value is not None:
            method_mock.return_value = return_value
        if side_effect is not None:
            method_mock.side_effect = side_effect
        self._methods[name] = method_mock
        return self
    
    def with_property(self, name: str, value: Any):
        """Add a property to the mock"""
        self._properties[name] = value
        return self
    
    def build(self) -> Mock:
        """Build and return the configured mock"""
        # Set attributes
        for name, value in self._attributes.items():
            setattr(self.mock, name, value)
        
        # Set methods
        for name, method_mock in self._methods.items():
            setattr(self.mock, name, method_mock)
        
        # Set properties
        for name, value in self._properties.items():
            prop_mock = PropertyMock(return_value=value)
            setattr(type(self.mock), name, prop_mock)
        
        return self.mock


class SentimentAnalyzerMockBuilder(BaseMockBuilder):
    """Builder for sentiment analyzer mocks"""
    
    def __init__(self):
        super().__init__()
        self.mock = Mock()
        # Default behavior
        self.with_method('analyze', return_value={
            'sentiment': 'neutral',
            'confidence': 0.5
        })
    
    def with_sentiment_result(self, sentiment: str, confidence: float = 0.8, 
                            emotions: Optional[Dict[str, float]] = None):
        """Configure analyzer to return specific sentiment"""
        result = {
            'sentiment': sentiment,
            'confidence': confidence
        }
        if emotions:
            result['emotions'] = emotions
        
        self.with_method('analyze', return_value=result)
        return self
    
    def with_batch_analysis(self, results: List[Dict[str, Any]]):
        """Configure batch analysis results"""
        self.with_method('analyze_batch', return_value=results)
        return self
    
    def with_error(self, error_message: str = "Analysis failed"):
        """Configure analyzer to raise an error"""
        self.with_method('analyze', side_effect=Exception(error_message))
        return self
    
    def with_performance_tracking(self, processing_time: float = 0.1):
        """Configure performance tracking"""
        def analyze_with_timing(*args, **kwargs):
            import time
            time.sleep(processing_time)  # Simulate processing time
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'processing_time': processing_time
            }
        
        self.with_method('analyze', side_effect=analyze_with_timing)
        return self
    
    def with_language_detection(self, language: str = 'es'):
        """Configure language detection"""
        result = {
            'sentiment': 'neutral',
            'confidence': 0.5,
            'language': language
        }
        self.with_method('analyze', return_value=result)
        return self
    
    def with_random_results(self, seed: int = 42):
        """Configure random but consistent results"""
        random.seed(seed)
        
        def random_analyze(*args, **kwargs):
            sentiments = ['positive', 'negative', 'neutral']
            return {
                'sentiment': random.choice(sentiments),
                'confidence': random.uniform(0.3, 0.9),
                'emotions': {
                    'joy': random.uniform(0, 1),
                    'anger': random.uniform(0, 1),
                    'sadness': random.uniform(0, 1)
                }
            }
        
        self.with_method('analyze', side_effect=random_analyze)
        return self


class OpenAIMockBuilder(BaseMockBuilder):
    """Builder for OpenAI API mocks"""
    
    def __init__(self):
        super().__init__()
        self.client_mock = Mock()
        self.completion_mock = Mock()
        self.chat_mock = Mock()
        
        # Set up default structure
        self.client_mock.chat = self.chat_mock
        self.chat_mock.completions = self.completion_mock
    
    def with_successful_response(self, content: str = "positive", 
                                usage_tokens: int = 50,
                                model: str = "gpt-3.5-turbo"):
        """Configure successful API response"""
        response = Mock()
        response.choices = [Mock()]
        response.choices[0].message = Mock()
        response.choices[0].message.content = content
        response.usage = Mock()
        response.usage.total_tokens = usage_tokens
        response.model = model
        
        self.completion_mock.create.return_value = response
        return self
    
    def with_rate_limit_error(self, retry_after: int = 60):
        """Configure rate limit error"""
        from openai import RateLimitError
        
        error = RateLimitError(
            message="Rate limit exceeded",
            response=Mock(status_code=429),
            body={"error": {"message": "Rate limit exceeded"}}
        )
        error.response.headers = {"retry-after": str(retry_after)}
        
        self.completion_mock.create.side_effect = error
        return self
    
    def with_api_error(self, status_code: int = 500, message: str = "API Error"):
        """Configure API error"""
        from openai import APIError
        
        error = APIError(
            message=message,
            request=Mock(),
            body={"error": {"message": message}}
        )
        
        self.completion_mock.create.side_effect = error
        return self
    
    def with_timeout_error(self):
        """Configure timeout error"""
        import requests
        
        self.completion_mock.create.side_effect = requests.Timeout("Request timed out")
        return self
    
    def with_cost_tracking(self, cost_per_token: float = 0.0001):
        """Configure cost tracking"""
        def track_cost(*args, **kwargs):
            response = Mock()
            response.choices = [Mock()]
            response.choices[0].message = Mock()
            response.choices[0].message.content = "positive"
            response.usage = Mock()
            response.usage.total_tokens = 50
            response.cost = 50 * cost_per_token
            return response
        
        self.completion_mock.create.side_effect = track_cost
        return self
    
    def with_streaming_response(self, chunks: List[str]):
        """Configure streaming response"""
        def create_stream(*args, **kwargs):
            for chunk in chunks:
                mock_chunk = Mock()
                mock_chunk.choices = [Mock()]
                mock_chunk.choices[0].delta = Mock()
                mock_chunk.choices[0].delta.content = chunk
                yield mock_chunk
        
        self.completion_mock.create.return_value = create_stream()
        return self
    
    def build(self) -> Mock:
        """Build OpenAI client mock"""
        return self.client_mock


class DataFrameMockBuilder(BaseMockBuilder):
    """Builder for DataFrame mocks"""
    
    def __init__(self):
        super().__init__()
        self.data = {}
        self.index = None
        self.columns = []
    
    def with_comments_column(self, comments: List[str]):
        """Add comments column"""
        self.data['Comentario'] = comments
        self.columns.append('Comentario')
        return self
    
    def with_dates_column(self, start_date: str = "2024-01-01", count: Optional[int] = None):
        """Add dates column"""
        if count is None:
            count = len(next(iter(self.data.values()))) if self.data else 10
        
        dates = pd.date_range(start=start_date, periods=count, freq='D')
        self.data['Fecha'] = dates.strftime('%Y-%m-%d').tolist()
        self.columns.append('Fecha')
        return self
    
    def with_ids_column(self, start_id: int = 1):
        """Add ID column"""
        count = len(next(iter(self.data.values()))) if self.data else 10
        self.data['ID'] = list(range(start_id, start_id + count))
        self.columns.append('ID')
        return self
    
    def with_sentiment_results(self, sentiments: Optional[List[str]] = None):
        """Add sentiment analysis results"""
        count = len(next(iter(self.data.values()))) if self.data else 10
        
        if sentiments is None:
            sentiments = ['positive', 'negative', 'neutral'] * (count // 3 + 1)
            sentiments = sentiments[:count]
        
        self.data['Sentiment'] = sentiments
        self.data['Confidence'] = [random.uniform(0.5, 0.9) for _ in range(count)]
        self.columns.extend(['Sentiment', 'Confidence'])
        return self
    
    def with_metadata_columns(self, **metadata):
        """Add metadata columns"""
        for col_name, values in metadata.items():
            self.data[col_name] = values
            self.columns.append(col_name)
        return self
    
    def with_missing_values(self, missing_ratio: float = 0.1):
        """Add missing values to data"""
        for col_name, values in self.data.items():
            if isinstance(values, list):
                missing_count = int(len(values) * missing_ratio)
                missing_indices = random.sample(range(len(values)), missing_count)
                for idx in missing_indices:
                    values[idx] = None
        return self
    
    def build(self) -> pd.DataFrame:
        """Build DataFrame"""
        return pd.DataFrame(self.data)


class FileMockBuilder(BaseMockBuilder):
    """Builder for file operation mocks"""
    
    def __init__(self):
        super().__init__()
        self.file_mock = Mock()
        self.content = ""
        self.file_type = "txt"
    
    def with_content(self, content: str):
        """Set file content"""
        self.content = content
        return self
    
    def with_csv_content(self, df: pd.DataFrame):
        """Set CSV content from DataFrame"""
        self.content = df.to_csv(index=False)
        self.file_type = "csv"
        return self
    
    def with_json_content(self, data: Any):
        """Set JSON content"""
        self.content = json.dumps(data, indent=2, ensure_ascii=False)
        self.file_type = "json"
        return self
    
    def with_read_error(self, error_type: type = FileNotFoundError, 
                       message: str = "File not found"):
        """Configure read error"""
        self.file_mock.read.side_effect = error_type(message)
        return self
    
    def with_write_error(self, error_type: type = PermissionError,
                        message: str = "Permission denied"):
        """Configure write error"""
        self.file_mock.write.side_effect = error_type(message)
        return self
    
    def build(self) -> Mock:
        """Build file mock"""
        self.file_mock.read.return_value = self.content
        self.file_mock.name = f"test_file.{self.file_type}"
        self.file_mock.__enter__.return_value = self.file_mock
        self.file_mock.__exit__.return_value = None
        return self.file_mock


class APIResponseMockBuilder(BaseMockBuilder):
    """Builder for API response mocks"""
    
    def __init__(self):
        super().__init__()
        self.response_mock = Mock()
        self.status_code = 200
        self.headers = {}
        self.json_data = {}
        self.text_data = ""
    
    def with_status_code(self, status_code: int):
        """Set response status code"""
        self.status_code = status_code
        return self
    
    def with_json_data(self, data: Any):
        """Set JSON response data"""
        self.json_data = data
        return self
    
    def with_text_data(self, text: str):
        """Set text response data"""
        self.text_data = text
        return self
    
    def with_headers(self, headers: Dict[str, str]):
        """Set response headers"""
        self.headers.update(headers)
        return self
    
    def with_success_response(self, data: Any = None):
        """Configure successful response"""
        self.status_code = 200
        if data is not None:
            self.json_data = {"status": "success", "data": data}
        return self
    
    def with_error_response(self, error_message: str, status_code: int = 400):
        """Configure error response"""
        self.status_code = status_code
        self.json_data = {"status": "error", "message": error_message}
        return self
    
    def with_timeout(self):
        """Configure timeout"""
        import requests
        self.response_mock.raise_for_status.side_effect = requests.Timeout()
        return self
    
    def build(self) -> Mock:
        """Build response mock"""
        self.response_mock.status_code = self.status_code
        self.response_mock.ok = 200 <= self.status_code < 300
        self.response_mock.headers = self.headers
        self.response_mock.json.return_value = self.json_data
        self.response_mock.text = self.text_data
        
        return self.response_mock


class DatabaseMockBuilder(BaseMockBuilder):
    """Builder for database mocks"""
    
    def __init__(self):
        super().__init__()
        self.connection_mock = Mock()
        self.cursor_mock = Mock()
        self.data_store = {}
    
    def with_table_data(self, table_name: str, data: List[Dict]):
        """Add data for a table"""
        self.data_store[table_name] = data
        return self
    
    def with_query_result(self, result: List[tuple]):
        """Set query result"""
        self.cursor_mock.fetchall.return_value = result
        self.cursor_mock.fetchone.return_value = result[0] if result else None
        return self
    
    def with_connection_error(self, error_message: str = "Connection failed"):
        """Configure connection error"""
        self.connection_mock.connect.side_effect = Exception(error_message)
        return self
    
    def with_query_error(self, error_message: str = "Query failed"):
        """Configure query error"""
        self.cursor_mock.execute.side_effect = Exception(error_message)
        return self
    
    def with_transaction_support(self):
        """Add transaction support"""
        self.connection_mock.commit.return_value = None
        self.connection_mock.rollback.return_value = None
        self.connection_mock.autocommit = False
        return self
    
    def build(self) -> Mock:
        """Build database mock"""
        self.connection_mock.cursor.return_value = self.cursor_mock
        return self.connection_mock


# Convenience functions for quick mock creation
def mock_sentiment_analyzer(sentiment: str = 'neutral', confidence: float = 0.5) -> Mock:
    """Quick sentiment analyzer mock"""
    return SentimentAnalyzerMockBuilder().with_sentiment_result(sentiment, confidence).build()


def mock_openai_client(response_content: str = "positive") -> Mock:
    """Quick OpenAI client mock"""
    return OpenAIMockBuilder().with_successful_response(response_content).build()


def mock_dataframe(comments: List[str]) -> pd.DataFrame:
    """Quick DataFrame mock"""
    return (DataFrameMockBuilder()
            .with_comments_column(comments)
            .with_dates_column()
            .with_ids_column()
            .build())


def mock_api_response(status_code: int = 200, data: Any = None) -> Mock:
    """Quick API response mock"""
    builder = APIResponseMockBuilder().with_status_code(status_code)
    if data is not None:
        builder.with_json_data(data)
    return builder.build()


# Export all builders
__all__ = [
    'BaseMockBuilder',
    'SentimentAnalyzerMockBuilder',
    'OpenAIMockBuilder',
    'DataFrameMockBuilder',
    'FileMockBuilder',
    'APIResponseMockBuilder',
    'DatabaseMockBuilder',
    'mock_sentiment_analyzer',
    'mock_openai_client',
    'mock_dataframe',
    'mock_api_response',
]