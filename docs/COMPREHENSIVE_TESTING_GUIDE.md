# Comprehensive Testing Framework Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Test Types](#test-types)
5. [Framework Components](#framework-components)
6. [Usage Examples](#usage-examples)
7. [Best Practices](#best-practices)
8. [Configuration](#configuration)
9. [Performance Testing](#performance-testing)
10. [Troubleshooting](#troubleshooting)

## Overview

This comprehensive testing framework provides a modular, scalable, and maintainable approach to testing the Personal Paraguay Fiber Comments Analysis System. The framework supports multiple testing paradigms including unit tests, integration tests, performance tests, and end-to-end tests.

### Key Features

- **Modular Architecture**: Base classes, mixins, and factories for reusable components
- **Parameterized Testing**: Extensive use of pytest.mark.parametrize for comprehensive coverage
- **Custom Assertions**: Domain-specific assertions for sentiment analysis and data processing
- **Mock Builders**: Fluent interface for creating consistent mock objects
- **Performance Framework**: Built-in performance monitoring and benchmarking
- **Configuration Management**: Environment-specific test configurations
- **Automated Reporting**: HTML, JSON, and visual reports

## Architecture

### Directory Structure
```
tests/
├── base/                    # Base test classes
│   └── test_base.py
├── mixins/                  # Reusable test functionality
│   └── test_mixins.py
├── factories/               # Test data factories
│   └── test_factories.py
├── builders/                # Mock builders
│   └── mock_builders.py
├── assertions/              # Custom assertions
│   └── custom_assertions.py
├── performance/             # Performance testing
│   └── performance_framework.py
├── config/                  # Test configuration
│   └── test_config.py
├── unit/                    # Unit tests
├── integration/             # Integration tests
├── fixtures/                # Test fixtures and data
└── conftest.py             # Pytest configuration
```

### Core Components

1. **Base Classes**: `BaseTest`, `BaseUnitTest`, `BaseIntegrationTest`, etc.
2. **Mixins**: `DatabaseMixin`, `MockingMixin`, `AssertionMixin`, etc.
3. **Factories**: `CommentFactory`, `UserFactory`, `AnalysisResultFactory`
4. **Builders**: `SentimentAnalyzerMockBuilder`, `OpenAIMockBuilder`, etc.
5. **Assertions**: `SentimentAssertions`, `DataAssertions`, `PerformanceAssertions`

## Quick Start

### 1. Basic Test Example

```python
from tests.base.test_base import BaseUnitTest
from tests.mixins.test_mixins import AssertionMixin
from tests.assertions import SentimentAssertions

class TestSentimentAnalysis(BaseUnitTest, AssertionMixin):
    def test_basic_sentiment(self):
        from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
        
        analyzer = EnhancedAnalyzer()
        result = analyzer.analyze("Excelente servicio")
        
        # Use custom assertions
        SentimentAssertions.assert_valid_sentiment_result(result)
        SentimentAssertions.assert_sentiment_consistency("Excelente servicio", result)
```

### 2. Parameterized Test Example

```python
import pytest
from tests.unit.test_sentiment_parameterized import TestSentimentParameterized

class TestMyModule(TestSentimentParameterized):
    @pytest.mark.parametrize("comment,expected", [
        ("Excelente servicio", "positive"),
        ("Terrible servicio", "negative"),
        ("Servicio normal", "neutral"),
    ])
    def test_sentiment_classification(self, comment, expected):
        # Test implementation using inherited methods
        pass
```

### 3. Using Mock Builders

```python
from tests.builders import SentimentAnalyzerMockBuilder, mock_openai_client

def test_with_mock_analyzer():
    # Fluent mock building
    mock_analyzer = (SentimentAnalyzerMockBuilder()
                    .with_sentiment_result("positive", 0.9)
                    .with_language_detection("es")
                    .build())
    
    # Use mock in test
    result = mock_analyzer.analyze("Test comment")
    assert result['sentiment'] == "positive"
    assert result['confidence'] == 0.9
```

### 4. Performance Testing

```python
from tests.performance import PerformanceBenchmark, PerformanceThresholds

def test_performance():
    thresholds = PerformanceThresholds(
        max_execution_time=2.0,
        max_memory_usage_mb=100.0
    )
    
    benchmark = PerformanceBenchmark(thresholds)
    
    def function_to_test():
        # Your function implementation
        pass
    
    metrics = benchmark.measure_execution(function_to_test)
    
    # Validate against thresholds
    validation = benchmark.validate_thresholds(metrics)
    assert all(validation.values())
```

## Test Types

### Unit Tests
- **Location**: `tests/unit/`
- **Purpose**: Test individual components in isolation
- **Base Class**: `BaseUnitTest`
- **Characteristics**: Fast, isolated, use mocks extensively

```python
from tests.base.test_base import BaseUnitTest

class TestSentimentAnalyzer(BaseUnitTest):
    def test_analyze_positive_comment(self):
        # Test implementation
        pass
```

### Integration Tests
- **Location**: `tests/integration/`
- **Purpose**: Test component interactions
- **Base Class**: `BaseIntegrationTest`
- **Characteristics**: Test real integrations, slower than unit tests

```python
from tests.base.test_base import BaseIntegrationTest

class TestAnalysisWorkflow(BaseIntegrationTest):
    def test_end_to_end_analysis(self):
        # Test complete workflow
        pass
```

### Performance Tests
- **Location**: `tests/performance/`
- **Purpose**: Measure and validate performance
- **Base Class**: `BasePerformanceTest`
- **Tools**: Built-in performance framework

```python
from tests.base.test_base import BasePerformanceTest

class TestAnalysisPerformance(BasePerformanceTest):
    def test_large_dataset_processing(self):
        # Performance test implementation
        pass
```

### API Tests
- **Location**: `tests/api/`
- **Purpose**: Test API endpoints
- **Base Class**: `BaseAPITest`
- **Tools**: Built-in API mock builders

```python
from tests.base.test_base import BaseAPITest

class TestSentimentAPI(BaseAPITest):
    def test_analyze_endpoint(self):
        # API test implementation
        pass
```

## Framework Components

### Base Classes

#### BaseTest
Abstract base providing common functionality:
- Temporary directory management
- Test timing and metrics
- Fixture loading utilities
- Setup and teardown hooks

#### BaseUnitTest
Extends BaseTest with:
- Mock registry and management
- Patch registry with automatic cleanup
- Assertion helpers for unit tests

#### BaseIntegrationTest
Extends BaseTest with:
- Test database setup
- Test cache management
- Service integration utilities
- Condition waiting helpers

#### BasePerformanceTest
Extends BaseTest with:
- Performance measurement tools
- Threshold validation
- Load testing capabilities
- Performance reporting

### Mixins

#### DatabaseMixin
```python
class DatabaseMixin:
    def seed_test_data(self, table: str, data: List[Dict]):
        # Seed data implementation
        pass
    
    def assert_db_has(self, table: str, **conditions):
        # Database assertion implementation
        pass
```

#### MockingMixin
```python
class MockingMixin:
    def create_mock_with_spec(self, spec_class: type, **attributes) -> Mock:
        # Mock creation with spec
        pass
    
    def create_async_mock(self, return_value: Any = None) -> Mock:
        # Async mock creation
        pass
```

#### AssertionMixin
```python
class AssertionMixin:
    def assert_dataframe_equal(self, df1: pd.DataFrame, df2: pd.DataFrame):
        # DataFrame comparison
        pass
    
    def assert_in_range(self, value: float, min_val: float, max_val: float):
        # Range assertion
        pass
```

### Factories

#### CommentFactory
```python
from tests.factories import CommentFactory

# Create single comment
comment = CommentFactory.create()

# Create batch of comments
comments = CommentFactory.create_batch(50)

# Create with specific attributes
positive_comment = CommentFactory.create(sentiment="positive")
```

#### AnalysisResultFactory
```python
from tests.factories import AnalysisResultFactory

# Create analysis result
result = AnalysisResultFactory.create(
    sentiment="positive",
    confidence=0.95
)
```

### Mock Builders

#### SentimentAnalyzerMockBuilder
```python
from tests.builders import SentimentAnalyzerMockBuilder

mock_analyzer = (SentimentAnalyzerMockBuilder()
                .with_sentiment_result("positive", 0.9)
                .with_batch_analysis([...])
                .with_performance_tracking(0.1)
                .build())
```

#### OpenAIMockBuilder
```python
from tests.builders import OpenAIMockBuilder

mock_client = (OpenAIMockBuilder()
              .with_successful_response("positive")
              .with_cost_tracking(0.0001)
              .build())
```

### Custom Assertions

#### SentimentAssertions
```python
from tests.assertions import SentimentAssertions

# Validate sentiment result structure
SentimentAssertions.assert_valid_sentiment_result(result)

# Check sentiment distribution
SentimentAssertions.assert_sentiment_distribution(results, 
                                                 expected_positive_ratio=0.3)

# Validate confidence quality
SentimentAssertions.assert_confidence_quality(results, min_avg_confidence=0.7)
```

#### DataAssertions
```python
from tests.assertions import DataAssertions

# Validate DataFrame structure
DataAssertions.assert_valid_dataframe(df, 
                                     required_columns=['Comentario', 'Fecha'])

# Check data quality
DataAssertions.assert_data_quality(df, 
                                  max_missing_ratio=0.1)
```

## Configuration

### Environment-based Configuration

```python
from tests.config import TestEnvironment, set_test_environment, get_test_config

# Set test environment
set_test_environment(TestEnvironment.PERFORMANCE)

# Get current configuration
config = get_test_config()

# Access specific settings
max_memory = config.performance.max_memory_mb
sample_size = config.data.sample_size
```

### Custom Configuration

```python
from tests.config import TestConfigContext, TestEnvironment

# Temporary configuration changes
with TestConfigContext(TestEnvironment.UNIT, max_workers=2) as config:
    # Run tests with modified configuration
    pass
```

### Configuration Files

Save and load configurations:

```python
from tests.config import config_manager, TestEnvironment

# Save configuration
config_manager.save_config(TestEnvironment.UNIT, "my_config.json")

# Load configuration
config_manager.load_config("my_config.json", TestEnvironment.CUSTOM)
```

## Performance Testing

### Basic Performance Measurement

```python
from tests.performance import PerformanceBenchmark

benchmark = PerformanceBenchmark()

def my_function():
    # Function to test
    pass

metrics = benchmark.measure_execution(my_function)
print(f"Execution time: {metrics.execution_time:.3f}s")
print(f"Memory used: {metrics.memory_used_mb:.2f}MB")
```

### Batch Performance Testing

```python
# Test different batch sizes
batch_results = benchmark.benchmark_batch_processing(
    analyze_comments,
    data_batches=[comments],
    batch_sizes=[10, 50, 100, 500]
)

for batch_size, metrics in batch_results.items():
    print(f"Batch {batch_size}: {metrics.throughput_ops_per_sec:.2f} ops/sec")
```

### Load Testing

```python
# Test with varying concurrent users
load_results = benchmark.load_test(
    analyze_comment,
    test_data=sample_comments,
    concurrent_users=[1, 5, 10, 20]
)

for users, result in load_results.items():
    print(f"{users} users: {result['throughput_ops_per_sec']:.2f} ops/sec")
```

### Stress Testing

```python
# Run stress test
stress_results = benchmark.stress_test(
    analyze_comment,
    test_data="Test comment",
    duration_seconds=60,
    max_concurrent=10
)

print(f"Operations/sec: {stress_results['operations_per_second']:.2f}")
print(f"Success rate: {stress_results['success_rate']:.2%}")
```

### Performance Reporting

```python
# Generate performance report
report = benchmark.generate_report("performance_report.txt")

# Generate performance plots
benchmark.plot_performance_trends("performance_plots.png")
```

## Best Practices

### 1. Test Organization

- Use inheritance hierarchies for shared functionality
- Group related tests in classes
- Use descriptive test names
- Keep tests focused and atomic

### 2. Mock Strategy

- Mock external dependencies
- Use builders for consistent mock creation
- Verify mock interactions
- Reset mocks between tests

### 3. Data Management

- Use factories for test data generation
- Keep test data small and focused
- Clean up test data after tests
- Use different data sets for different scenarios

### 4. Assertions

- Use custom assertions for domain-specific checks
- Make assertions specific and meaningful
- Include helpful error messages
- Assert both positive and negative cases

### 5. Performance Testing

- Set realistic performance thresholds
- Test with realistic data sizes
- Monitor resource usage
- Document performance expectations

### 6. Configuration

- Use environment-specific configurations
- Keep sensitive data out of test configs
- Document configuration options
- Validate configurations

## Running Tests

### Command Line Options

```bash
# Run all tests
python -m pytest

# Run specific test type
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/performance/

# Run with specific configuration
TEST_ENVIRONMENT=performance python -m pytest tests/performance/

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run in parallel
python -m pytest -n auto

# Run with specific markers
python -m pytest -m "not slow"
python -m pytest -m performance
```

### Automated Test Runner

```bash
# Run comprehensive test suite
python scripts/run_all_tests.py

# Run with specific options
python scripts/run_all_tests.py --verbose --no-coverage

# Quick test run
python scripts/run_all_tests.py --quick
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure project root is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Mock Issues
```python
# Reset mocks between tests
def teardown_method(self):
    # Reset all mocks
    for mock_obj in self.mock_registry.values():
        mock_obj.reset_mock()
```

#### Performance Test Failures
```python
# Adjust thresholds for CI environment
if os.getenv('CI'):
    thresholds.max_execution_time *= 2
    thresholds.max_memory_usage_mb *= 1.5
```

#### Configuration Issues
```python
# Validate configuration before running tests
issues = config_manager.validate_config()
if issues:
    pytest.fail(f"Configuration issues: {issues}")
```

### Debugging Tests

#### Verbose Output
```bash
python -m pytest -v -s
```

#### Debug Mode
```python
# Enable debug mode in test configuration
config = get_test_config()
config.debug = True
```

#### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### CI/CD Integration

#### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    - name: Run tests
      run: python scripts/run_all_tests.py
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Framework Extension

### Adding New Test Types

1. Create new base class extending `BaseTest`
2. Add specific mixins for the test type
3. Create builders for test-specific mocks
4. Add custom assertions
5. Update configuration for new environment

### Custom Assertions

```python
class MyCustomAssertions:
    @staticmethod
    def assert_my_condition(data, expected):
        # Custom assertion implementation
        assert condition, f"Custom assertion failed: {data} != {expected}"
```

### New Mock Builders

```python
class MyServiceMockBuilder(BaseMockBuilder):
    def with_specific_behavior(self, behavior):
        # Configure specific mock behavior
        return self
    
    def build(self):
        # Build and return mock
        return self.mock
```

This comprehensive testing framework provides a solid foundation for ensuring the quality, performance, and reliability of the Personal Paraguay Fiber Comments Analysis System. The modular design allows for easy extension and customization while maintaining consistency across different test types.