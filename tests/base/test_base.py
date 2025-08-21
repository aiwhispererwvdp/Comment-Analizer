"""
Base classes for all test types
Provides common functionality and utilities for testing
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from unittest.mock import Mock, MagicMock, patch
import tempfile
import shutil
import json
import time
from datetime import datetime
from abc import ABC, abstractmethod


class BaseTest(ABC):
    """Abstract base class for all tests"""
    
    @classmethod
    def setup_class(cls):
        """Setup test class - runs once per class"""
        cls.test_start_time = time.time()
        cls.test_dir = Path(tempfile.mkdtemp(prefix='test_'))
        cls.setup_test_environment()
    
    @classmethod
    def teardown_class(cls):
        """Teardown test class - runs once per class"""
        cls.cleanup_test_environment()
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
        cls.test_duration = time.time() - cls.test_start_time
        cls.report_test_metrics()
    
    def setup_method(self, method):
        """Setup for each test method"""
        self.method_start_time = time.time()
        self.test_name = method.__name__
        self.setup_test_method()
    
    def teardown_method(self, method):
        """Teardown for each test method"""
        self.cleanup_test_method()
        self.method_duration = time.time() - self.method_start_time
        self.log_test_result()
    
    @classmethod
    def setup_test_environment(cls):
        """Setup test environment - override in subclasses"""
        pass
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup test environment - override in subclasses"""
        pass
    
    def setup_test_method(self):
        """Setup for individual test - override in subclasses"""
        pass
    
    def cleanup_test_method(self):
        """Cleanup for individual test - override in subclasses"""
        pass
    
    @classmethod
    def report_test_metrics(cls):
        """Report test metrics - override in subclasses"""
        if hasattr(cls, 'test_duration'):
            print(f"\n{cls.__name__} completed in {cls.test_duration:.2f} seconds")
    
    def log_test_result(self):
        """Log individual test result"""
        if hasattr(self, 'method_duration'):
            print(f"  {self.test_name}: {self.method_duration:.3f}s")
    
    # Utility methods
    @staticmethod
    def create_temp_file(content: str, suffix: str = '.txt') -> Path:
        """Create a temporary file with content"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
        temp_file.write(content)
        temp_file.close()
        return Path(temp_file.name)
    
    @staticmethod
    def load_fixture(fixture_name: str) -> Any:
        """Load a test fixture from fixtures directory"""
        fixture_path = Path(__file__).parent.parent / 'fixtures' / fixture_name
        if fixture_path.suffix == '.json':
            with open(fixture_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif fixture_path.suffix == '.csv':
            return pd.read_csv(fixture_path)
        elif fixture_path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(fixture_path)
        else:
            with open(fixture_path, 'r', encoding='utf-8') as f:
                return f.read()


class BaseUnitTest(BaseTest):
    """Base class for unit tests"""
    
    @classmethod
    def setup_test_environment(cls):
        """Setup unit test environment"""
        super().setup_test_environment()
        cls.mock_registry = {}
        cls.patch_registry = []
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup unit test environment"""
        # Stop all patches
        for patcher in cls.patch_registry:
            patcher.stop()
        cls.patch_registry.clear()
        cls.mock_registry.clear()
        super().cleanup_test_environment()
    
    @classmethod
    def create_mock(cls, name: str, spec: Optional[Any] = None, **kwargs) -> Mock:
        """Create and register a mock object"""
        mock_obj = Mock(spec=spec, **kwargs) if spec else Mock(**kwargs)
        cls.mock_registry[name] = mock_obj
        return mock_obj
    
    @classmethod
    def create_patch(cls, target: str, **kwargs) -> Any:
        """Create and register a patch"""
        patcher = patch(target, **kwargs)
        mock_obj = patcher.start()
        cls.patch_registry.append(patcher)
        return mock_obj
    
    def assert_called_with_subset(self, mock_obj: Mock, **expected_kwargs):
        """Assert mock was called with expected kwargs as subset"""
        actual_kwargs = mock_obj.call_args.kwargs if mock_obj.call_args else {}
        for key, value in expected_kwargs.items():
            assert key in actual_kwargs, f"Expected key '{key}' not in call arguments"
            assert actual_kwargs[key] == value, f"Expected {key}={value}, got {actual_kwargs[key]}"
    
    def assert_not_called(self, mock_obj: Mock):
        """Assert mock was not called"""
        assert mock_obj.call_count == 0, f"Expected no calls, but was called {mock_obj.call_count} times"


class BaseIntegrationTest(BaseTest):
    """Base class for integration tests"""
    
    @classmethod
    def setup_test_environment(cls):
        """Setup integration test environment"""
        super().setup_test_environment()
        cls.test_database = cls.setup_test_database()
        cls.test_cache = cls.setup_test_cache()
        cls.test_services = cls.setup_test_services()
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup integration test environment"""
        cls.cleanup_test_services()
        cls.cleanup_test_cache()
        cls.cleanup_test_database()
        super().cleanup_test_environment()
    
    @classmethod
    def setup_test_database(cls) -> Optional[Any]:
        """Setup test database - override in subclasses"""
        return None
    
    @classmethod
    def cleanup_test_database(cls):
        """Cleanup test database - override in subclasses"""
        pass
    
    @classmethod
    def setup_test_cache(cls) -> Optional[Any]:
        """Setup test cache - override in subclasses"""
        return None
    
    @classmethod
    def cleanup_test_cache(cls):
        """Cleanup test cache - override in subclasses"""
        pass
    
    @classmethod
    def setup_test_services(cls) -> Dict[str, Any]:
        """Setup test services - override in subclasses"""
        return {}
    
    @classmethod
    def cleanup_test_services(cls):
        """Cleanup test services - override in subclasses"""
        pass
    
    def wait_for_condition(self, condition: Callable, timeout: float = 5.0, interval: float = 0.1) -> bool:
        """Wait for a condition to become true"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition():
                return True
            time.sleep(interval)
        return False


class BaseAPITest(BaseTest):
    """Base class for API tests"""
    
    @classmethod
    def setup_test_environment(cls):
        """Setup API test environment"""
        super().setup_test_environment()
        cls.api_client = cls.create_api_client()
        cls.api_mocks = {}
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup API test environment"""
        cls.api_client = None
        cls.api_mocks.clear()
        super().cleanup_test_environment()
    
    @classmethod
    def create_api_client(cls) -> Any:
        """Create API client - override in subclasses"""
        return None
    
    def mock_api_response(self, endpoint: str, response: Any, status_code: int = 200):
        """Mock an API response"""
        mock_response = Mock()
        mock_response.json.return_value = response
        mock_response.status_code = status_code
        mock_response.ok = 200 <= status_code < 300
        self.api_mocks[endpoint] = mock_response
        return mock_response
    
    def assert_api_called(self, endpoint: str, method: str = 'GET', **kwargs):
        """Assert API endpoint was called with expected parameters"""
        # Implementation depends on API client structure
        pass
    
    def create_mock_api_error(self, status_code: int, error_message: str):
        """Create a mock API error response"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.ok = False
        mock_response.json.return_value = {'error': error_message}
        mock_response.text = error_message
        return mock_response


class BasePerformanceTest(BaseTest):
    """Base class for performance tests"""
    
    # Performance thresholds
    MAX_RESPONSE_TIME = 1.0  # seconds
    MAX_MEMORY_USAGE = 100  # MB
    MIN_THROUGHPUT = 10  # operations per second
    
    @classmethod
    def setup_test_environment(cls):
        """Setup performance test environment"""
        super().setup_test_environment()
        cls.performance_metrics = {
            'response_times': [],
            'memory_usage': [],
            'throughput': [],
            'errors': []
        }
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup performance test environment"""
        cls.generate_performance_report()
        super().cleanup_test_environment()
    
    @classmethod
    def generate_performance_report(cls):
        """Generate performance test report"""
        if cls.performance_metrics['response_times']:
            avg_response = np.mean(cls.performance_metrics['response_times'])
            p95_response = np.percentile(cls.performance_metrics['response_times'], 95)
            p99_response = np.percentile(cls.performance_metrics['response_times'], 99)
            
            print(f"\n{'='*60}")
            print(f"Performance Test Report: {cls.__name__}")
            print(f"{'='*60}")
            print(f"Average Response Time: {avg_response:.3f}s")
            print(f"P95 Response Time: {p95_response:.3f}s")
            print(f"P99 Response Time: {p99_response:.3f}s")
            
            if cls.performance_metrics['memory_usage']:
                avg_memory = np.mean(cls.performance_metrics['memory_usage'])
                max_memory = np.max(cls.performance_metrics['memory_usage'])
                print(f"Average Memory Usage: {avg_memory:.2f} MB")
                print(f"Peak Memory Usage: {max_memory:.2f} MB")
            
            if cls.performance_metrics['throughput']:
                avg_throughput = np.mean(cls.performance_metrics['throughput'])
                print(f"Average Throughput: {avg_throughput:.2f} ops/sec")
            
            if cls.performance_metrics['errors']:
                error_rate = len(cls.performance_metrics['errors']) / len(cls.performance_metrics['response_times'])
                print(f"Error Rate: {error_rate:.2%}")
            print(f"{'='*60}\n")
    
    def measure_performance(self, func: Callable, *args, **kwargs) -> tuple:
        """Measure performance of a function"""
        import psutil
        import os
        
        # Measure memory before
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Measure execution time
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            self.performance_metrics['errors'].append(str(e))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Measure memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        # Record metrics
        self.performance_metrics['response_times'].append(execution_time)
        self.performance_metrics['memory_usage'].append(memory_used)
        
        # Calculate throughput
        if execution_time > 0:
            throughput = 1.0 / execution_time
            self.performance_metrics['throughput'].append(throughput)
        
        return result, execution_time, memory_used, success
    
    def assert_performance(self, execution_time: float, memory_used: float = None):
        """Assert performance meets thresholds"""
        assert execution_time < self.MAX_RESPONSE_TIME, \
            f"Response time {execution_time:.3f}s exceeds threshold {self.MAX_RESPONSE_TIME}s"
        
        if memory_used is not None:
            assert memory_used < self.MAX_MEMORY_USAGE, \
                f"Memory usage {memory_used:.2f}MB exceeds threshold {self.MAX_MEMORY_USAGE}MB"
    
    def run_load_test(self, func: Callable, num_requests: int = 100, concurrent: int = 10):
        """Run a load test with concurrent requests"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            futures = [executor.submit(self.measure_performance, func) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.performance_metrics['errors'].append(str(e))
        
        return results


class BaseEndToEndTest(BaseTest):
    """Base class for end-to-end tests"""
    
    @classmethod
    def setup_test_environment(cls):
        """Setup E2E test environment"""
        super().setup_test_environment()
        cls.browser = cls.setup_browser()
        cls.test_users = cls.create_test_users()
    
    @classmethod
    def cleanup_test_environment(cls):
        """Cleanup E2E test environment"""
        cls.cleanup_test_users()
        cls.cleanup_browser()
        super().cleanup_test_environment()
    
    @classmethod
    def setup_browser(cls) -> Optional[Any]:
        """Setup browser for E2E testing - override in subclasses"""
        return None
    
    @classmethod
    def cleanup_browser(cls):
        """Cleanup browser - override in subclasses"""
        if hasattr(cls, 'browser') and cls.browser:
            cls.browser.quit()
    
    @classmethod
    def create_test_users(cls) -> List[Dict[str, Any]]:
        """Create test users - override in subclasses"""
        return []
    
    @classmethod
    def cleanup_test_users(cls):
        """Cleanup test users - override in subclasses"""
        pass
    
    def login_as_user(self, user: Dict[str, Any]):
        """Login as a test user - override in subclasses"""
        pass
    
    def navigate_to(self, url: str):
        """Navigate to a URL - override in subclasses"""
        if self.browser:
            self.browser.get(url)
    
    def wait_for_element(self, selector: str, timeout: int = 10):
        """Wait for an element to be present - override in subclasses"""
        pass
    
    def click_element(self, selector: str):
        """Click an element - override in subclasses"""
        pass
    
    def input_text(self, selector: str, text: str):
        """Input text into an element - override in subclasses"""
        pass
    
    def assert_text_present(self, text: str):
        """Assert text is present on page - override in subclasses"""
        pass