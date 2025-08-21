"""
Test mixins for adding specific functionality to test classes
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from typing import Any, Dict, List, Optional, Union
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import random
import string


class DatabaseMixin:
    """Mixin for database testing utilities"""
    
    @property
    def test_db(self):
        """Get test database instance"""
        if not hasattr(self, '_test_db'):
            self._test_db = self.create_test_db()
        return self._test_db
    
    def create_test_db(self):
        """Create a test database"""
        # Could be SQLite in-memory or test database
        return None
    
    def seed_test_data(self, table: str, data: List[Dict]):
        """Seed test data into database"""
        if self.test_db:
            # Insert data into table
            pass
    
    def clean_test_data(self, table: str = None):
        """Clean test data from database"""
        if self.test_db:
            if table:
                # Clean specific table
                pass
            else:
                # Clean all test data
                pass
    
    def assert_db_has(self, table: str, **conditions):
        """Assert database has record matching conditions"""
        # Query database and check if record exists
        pass
    
    def assert_db_missing(self, table: str, **conditions):
        """Assert database doesn't have record matching conditions"""
        # Query database and check record doesn't exist
        pass
    
    def get_db_count(self, table: str, **conditions) -> int:
        """Get count of records matching conditions"""
        return 0


class MockingMixin:
    """Mixin for advanced mocking helpers"""
    
    def create_mock_with_spec(self, spec_class: type, **attributes) -> Mock:
        """Create a mock with spec and attributes"""
        mock_obj = Mock(spec=spec_class)
        for attr, value in attributes.items():
            setattr(mock_obj, attr, value)
        return mock_obj
    
    def create_async_mock(self, return_value: Any = None) -> Mock:
        """Create an async mock"""
        mock_obj = MagicMock()
        mock_obj.__aenter__ = MagicMock(return_value=mock_obj)
        mock_obj.__aexit__ = MagicMock(return_value=None)
        if return_value is not None:
            mock_obj.return_value = return_value
        return mock_obj
    
    def mock_property(self, obj: Any, property_name: str, return_value: Any):
        """Mock a property on an object"""
        prop_mock = PropertyMock(return_value=return_value)
        setattr(type(obj), property_name, prop_mock)
        return prop_mock
    
    def create_mock_response(self, status_code: int = 200, json_data: Any = None, text: str = None):
        """Create a mock HTTP response"""
        response = Mock()
        response.status_code = status_code
        response.ok = 200 <= status_code < 300
        
        if json_data is not None:
            response.json.return_value = json_data
        if text is not None:
            response.text = text
        
        return response
    
    def create_mock_file(self, content: str = "", filename: str = "test.txt"):
        """Create a mock file object"""
        mock_file = MagicMock()
        mock_file.read.return_value = content
        mock_file.name = filename
        mock_file.__enter__.return_value = mock_file
        mock_file.__exit__.return_value = None
        return mock_file
    
    def assert_mock_called_once_with_partial(self, mock_obj: Mock, **expected_kwargs):
        """Assert mock called once with partial kwargs match"""
        assert mock_obj.call_count == 1, f"Expected 1 call, got {mock_obj.call_count}"
        actual_kwargs = mock_obj.call_args.kwargs if mock_obj.call_args else {}
        
        for key, value in expected_kwargs.items():
            assert key in actual_kwargs, f"Key '{key}' not in call arguments"
            assert actual_kwargs[key] == value, f"Expected {key}={value}, got {actual_kwargs[key]}"


class AssertionMixin:
    """Mixin for custom assertions"""
    
    def assert_dataframe_equal(self, df1: pd.DataFrame, df2: pd.DataFrame, check_dtype: bool = True):
        """Assert two dataframes are equal"""
        pd.testing.assert_frame_equal(df1, df2, check_dtype=check_dtype)
    
    def assert_dataframe_has_columns(self, df: pd.DataFrame, columns: List[str]):
        """Assert dataframe has specific columns"""
        missing_columns = set(columns) - set(df.columns)
        assert not missing_columns, f"Missing columns: {missing_columns}"
    
    def assert_in_range(self, value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]):
        """Assert value is in range"""
        assert min_val <= value <= max_val, f"Value {value} not in range [{min_val}, {max_val}]"
    
    def assert_list_equal_unordered(self, list1: List, list2: List):
        """Assert two lists are equal regardless of order"""
        assert sorted(list1) == sorted(list2), f"Lists not equal: {list1} != {list2}"
    
    def assert_dict_subset(self, subset: Dict, superset: Dict):
        """Assert dict is subset of another dict"""
        for key, value in subset.items():
            assert key in superset, f"Key '{key}' not in superset"
            assert superset[key] == value, f"Value mismatch for key '{key}': {superset[key]} != {value}"
    
    def assert_raises_with_message(self, exception_class: type, message: str, func, *args, **kwargs):
        """Assert function raises specific exception with message"""
        with pytest.raises(exception_class) as exc_info:
            func(*args, **kwargs)
        assert message in str(exc_info.value), f"Expected message '{message}' not in '{exc_info.value}'"
    
    def assert_json_equal(self, json1: Union[str, dict], json2: Union[str, dict]):
        """Assert two JSON objects are equal"""
        if isinstance(json1, str):
            json1 = json.loads(json1)
        if isinstance(json2, str):
            json2 = json.loads(json2)
        assert json1 == json2, f"JSON not equal: {json1} != {json2}"
    
    def assert_approximately_equal(self, value1: float, value2: float, tolerance: float = 0.01):
        """Assert two values are approximately equal"""
        diff = abs(value1 - value2)
        assert diff <= tolerance, f"Values differ by {diff}, exceeds tolerance {tolerance}"


class FixtureMixin:
    """Mixin for dynamic fixture generation"""
    
    def generate_test_dataframe(self, rows: int = 10, columns: List[str] = None) -> pd.DataFrame:
        """Generate a test dataframe"""
        if columns is None:
            columns = ['id', 'name', 'value', 'date']
        
        data = {}
        for col in columns:
            if col == 'id':
                data[col] = list(range(rows))
            elif col == 'name':
                data[col] = [f"Name_{i}" for i in range(rows)]
            elif col == 'value':
                data[col] = np.random.randn(rows)
            elif col == 'date':
                data[col] = pd.date_range(start='2024-01-01', periods=rows)
            else:
                data[col] = [f"{col}_{i}" for i in range(rows)]
        
        return pd.DataFrame(data)
    
    def generate_random_string(self, length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_test_comments(self, count: int = 10, language: str = 'es') -> List[str]:
        """Generate test comments"""
        positive_es = [
            "Excelente servicio",
            "Muy satisfecho",
            "Recomendado",
            "Perfecto",
            "Increíble"
        ]
        negative_es = [
            "Terrible servicio",
            "Muy malo",
            "No recomendado",
            "Pésimo",
            "Horrible"
        ]
        neutral_es = [
            "Normal",
            "Regular",
            "Aceptable",
            "Sin comentarios",
            "Estándar"
        ]
        
        comments = []
        for _ in range(count):
            sentiment = random.choice(['positive', 'negative', 'neutral'])
            if sentiment == 'positive':
                base = random.choice(positive_es)
            elif sentiment == 'negative':
                base = random.choice(negative_es)
            else:
                base = random.choice(neutral_es)
            
            comments.append(f"{base} - {self.generate_random_string(5)}")
        
        return comments
    
    def generate_test_file(self, file_type: str = 'csv', rows: int = 10) -> Path:
        """Generate a test file"""
        df = self.generate_test_dataframe(rows)
        
        temp_file = tempfile.NamedTemporaryFile(suffix=f'.{file_type}', delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()
        
        if file_type == 'csv':
            df.to_csv(temp_path, index=False)
        elif file_type in ['xlsx', 'xls']:
            df.to_excel(temp_path, index=False)
        elif file_type == 'json':
            df.to_json(temp_path, orient='records')
        
        return temp_path
    
    def generate_mock_api_response(self, success: bool = True, data: Any = None):
        """Generate mock API response"""
        if success:
            return {
                'status': 'success',
                'data': data or {'id': 1, 'result': 'test'},
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'error',
                'error': 'Test error message',
                'code': 'TEST_ERROR',
                'timestamp': datetime.now().isoformat()
            }


class TimeMixin:
    """Mixin for time-related testing utilities"""
    
    def freeze_time(self, target_time: datetime):
        """Freeze time for testing"""
        return patch('datetime.datetime.now', return_value=target_time)
    
    def advance_time(self, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
        """Advance time by specified amount"""
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        new_time = datetime.now() + delta
        return self.freeze_time(new_time)
    
    def assert_recent(self, timestamp: datetime, max_age_seconds: int = 60):
        """Assert timestamp is recent"""
        age = (datetime.now() - timestamp).total_seconds()
        assert age <= max_age_seconds, f"Timestamp is {age}s old, exceeds max age {max_age_seconds}s"
    
    def assert_datetime_equal(self, dt1: datetime, dt2: datetime, tolerance_seconds: int = 1):
        """Assert two datetimes are equal within tolerance"""
        diff = abs((dt1 - dt2).total_seconds())
        assert diff <= tolerance_seconds, f"Datetimes differ by {diff}s, exceeds tolerance {tolerance_seconds}s"


class FileMixin:
    """Mixin for file-related testing utilities"""
    
    def create_temp_directory(self, prefix: str = 'test_') -> Path:
        """Create temporary directory"""
        return Path(tempfile.mkdtemp(prefix=prefix))
    
    def create_temp_file(self, content: str = "", suffix: str = '.txt') -> Path:
        """Create temporary file with content"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
        temp_file.write(content)
        temp_file.close()
        return Path(temp_file.name)
    
    def assert_file_exists(self, file_path: Union[str, Path]):
        """Assert file exists"""
        path = Path(file_path)
        assert path.exists(), f"File does not exist: {path}"
    
    def assert_file_contains(self, file_path: Union[str, Path], text: str):
        """Assert file contains text"""
        path = Path(file_path)
        content = path.read_text()
        assert text in content, f"Text '{text}' not found in file {path}"
    
    def assert_file_size(self, file_path: Union[str, Path], min_size: int = None, max_size: int = None):
        """Assert file size is within bounds"""
        path = Path(file_path)
        size = path.stat().st_size
        
        if min_size is not None:
            assert size >= min_size, f"File size {size} is less than minimum {min_size}"
        if max_size is not None:
            assert size <= max_size, f"File size {size} exceeds maximum {max_size}"


class ValidationMixin:
    """Mixin for validation testing utilities"""
    
    def assert_valid_email(self, email: str):
        """Assert string is valid email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert re.match(pattern, email), f"Invalid email format: {email}"
    
    def assert_valid_url(self, url: str):
        """Assert string is valid URL"""
        import re
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        assert re.match(pattern, url), f"Invalid URL format: {url}"
    
    def assert_valid_json(self, json_string: str):
        """Assert string is valid JSON"""
        try:
            json.loads(json_string)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON: {e}")
    
    def assert_valid_dataframe(self, df: pd.DataFrame, min_rows: int = None, required_columns: List[str] = None):
        """Assert dataframe is valid"""
        assert isinstance(df, pd.DataFrame), "Not a DataFrame"
        
        if min_rows is not None:
            assert len(df) >= min_rows, f"DataFrame has {len(df)} rows, expected at least {min_rows}"
        
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            assert not missing, f"Missing required columns: {missing}"