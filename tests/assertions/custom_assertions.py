"""
Custom assertion helpers for the testing framework
Provides domain-specific assertions for sentiment analysis and data processing
"""

import pytest
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union
import json
import re
from pathlib import Path


class SentimentAssertions:
    """Custom assertions for sentiment analysis results"""
    
    @staticmethod
    def assert_valid_sentiment_result(result: Dict[str, Any], 
                                    require_confidence: bool = True,
                                    require_emotions: bool = False):
        """Assert that a sentiment analysis result has valid structure"""
        assert isinstance(result, dict), f"Result should be dict, got {type(result)}"
        
        # Required fields
        assert 'sentiment' in result, "Result must contain 'sentiment' field"
        assert result['sentiment'] in ['positive', 'negative', 'neutral'], \
            f"Invalid sentiment: {result.get('sentiment')}"
        
        # Confidence score validation
        if require_confidence:
            assert 'confidence' in result, "Result must contain 'confidence' field"
            confidence = result['confidence']
            assert isinstance(confidence, (int, float)), \
                f"Confidence should be numeric, got {type(confidence)}"
            assert 0 <= confidence <= 1, \
                f"Confidence should be between 0 and 1, got {confidence}"
        
        # Emotion validation if present
        if require_emotions and 'emotions' in result:
            emotions = result['emotions']
            assert isinstance(emotions, dict), "Emotions should be a dictionary"
            for emotion, score in emotions.items():
                assert isinstance(emotion, str), "Emotion names should be strings"
                assert isinstance(score, (int, float)), "Emotion scores should be numeric"
                assert 0 <= score <= 1, f"Emotion score should be 0-1, got {score}"
    
    @staticmethod
    def assert_sentiment_distribution(results: List[Dict[str, Any]], 
                                    expected_positive_ratio: Optional[float] = None,
                                    expected_negative_ratio: Optional[float] = None,
                                    tolerance: float = 0.1):
        """Assert sentiment distribution meets expectations"""
        sentiments = [r.get('sentiment') for r in results if 'sentiment' in r]
        total = len(sentiments)
        
        if total == 0:
            pytest.fail("No valid sentiment results found")
        
        # Calculate actual ratios
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        positive_ratio = positive_count / total
        negative_ratio = negative_count / total
        neutral_ratio = neutral_count / total
        
        # Check distribution sums to 1
        assert abs(positive_ratio + negative_ratio + neutral_ratio - 1.0) < 0.01, \
            "Sentiment distribution should sum to 1"
        
        # Check expected ratios if provided
        if expected_positive_ratio is not None:
            assert abs(positive_ratio - expected_positive_ratio) <= tolerance, \
                f"Positive ratio {positive_ratio:.3f} not within {tolerance} of expected {expected_positive_ratio}"
        
        if expected_negative_ratio is not None:
            assert abs(negative_ratio - expected_negative_ratio) <= tolerance, \
                f"Negative ratio {negative_ratio:.3f} not within {tolerance} of expected {expected_negative_ratio}"
    
    @staticmethod
    def assert_confidence_quality(results: List[Dict[str, Any]], 
                                min_avg_confidence: float = 0.5,
                                require_high_confidence_cases: bool = True):
        """Assert confidence scores indicate good model performance"""
        confidences = [r.get('confidence', 0) for r in results if 'confidence' in r]
        
        if not confidences:
            pytest.fail("No confidence scores found in results")
        
        # Check average confidence
        avg_confidence = sum(confidences) / len(confidences)
        assert avg_confidence >= min_avg_confidence, \
            f"Average confidence {avg_confidence:.3f} below minimum {min_avg_confidence}"
        
        # Check for some high confidence cases
        if require_high_confidence_cases:
            high_confidence_count = sum(1 for c in confidences if c > 0.8)
            assert high_confidence_count > 0, \
                "Should have at least some high confidence predictions (>0.8)"
        
        # Check confidence range
        assert all(0 <= c <= 1 for c in confidences), \
            "All confidence scores should be between 0 and 1"
    
    @staticmethod
    def assert_sentiment_consistency(comment: str, result: Dict[str, Any]):
        """Assert sentiment result is reasonable for obvious cases"""
        comment_lower = comment.lower()
        sentiment = result.get('sentiment')
        
        # Check obvious positive indicators
        positive_words = ['excelente', 'perfecto', 'increíble', 'maravilloso', 'fantástico']
        if any(word in comment_lower for word in positive_words):
            if sentiment == 'negative':
                pytest.fail(f"Comment '{comment}' contains positive words but classified as negative")
        
        # Check obvious negative indicators  
        negative_words = ['terrible', 'horrible', 'pésimo', 'malo', 'odio']
        if any(word in comment_lower for word in negative_words):
            if sentiment == 'positive':
                pytest.fail(f"Comment '{comment}' contains negative words but classified as positive")
    
    @staticmethod
    def assert_batch_consistency(individual_results: List[Dict], 
                               batch_results: List[Dict],
                               tolerance: float = 0.1):
        """Assert batch processing gives similar results to individual processing"""
        assert len(individual_results) == len(batch_results), \
            "Individual and batch results should have same length"
        
        sentiment_matches = 0
        confidence_diffs = []
        
        for ind, batch in zip(individual_results, batch_results):
            # Check sentiment agreement
            if ind.get('sentiment') == batch.get('sentiment'):
                sentiment_matches += 1
            
            # Check confidence similarity
            ind_conf = ind.get('confidence', 0)
            batch_conf = batch.get('confidence', 0)
            confidence_diffs.append(abs(ind_conf - batch_conf))
        
        # At least 70% sentiment agreement
        agreement_ratio = sentiment_matches / len(individual_results)
        assert agreement_ratio >= 0.7, \
            f"Sentiment agreement {agreement_ratio:.3f} below 70%"
        
        # Average confidence difference should be small
        if confidence_diffs:
            avg_conf_diff = sum(confidence_diffs) / len(confidence_diffs)
            assert avg_conf_diff <= tolerance, \
                f"Average confidence difference {avg_conf_diff:.3f} exceeds tolerance {tolerance}"


class DataAssertions:
    """Custom assertions for data processing and validation"""
    
    @staticmethod
    def assert_valid_dataframe(df: pd.DataFrame, 
                             required_columns: Optional[List[str]] = None,
                             min_rows: int = 0,
                             max_rows: Optional[int] = None):
        """Assert dataframe has valid structure"""
        assert isinstance(df, pd.DataFrame), f"Expected DataFrame, got {type(df)}"
        
        # Check row count
        assert len(df) >= min_rows, f"DataFrame has {len(df)} rows, expected at least {min_rows}"
        
        if max_rows is not None:
            assert len(df) <= max_rows, f"DataFrame has {len(df)} rows, expected at most {max_rows}"
        
        # Check required columns
        if required_columns:
            missing_columns = set(required_columns) - set(df.columns)
            assert not missing_columns, f"Missing required columns: {missing_columns}"
    
    @staticmethod
    def assert_no_data_leakage(train_df: pd.DataFrame, 
                             test_df: pd.DataFrame, 
                             id_column: str = 'ID'):
        """Assert no data leakage between train and test sets"""
        if id_column in train_df.columns and id_column in test_df.columns:
            train_ids = set(train_df[id_column])
            test_ids = set(test_df[id_column])
            overlap = train_ids.intersection(test_ids)
            assert not overlap, f"Data leakage detected: {len(overlap)} overlapping IDs"
    
    @staticmethod
    def assert_data_quality(df: pd.DataFrame, 
                          text_column: str = 'Comentario',
                          max_missing_ratio: float = 0.1,
                          min_text_length: int = 3):
        """Assert data quality meets standards"""
        # Check missing data ratio
        missing_ratio = df[text_column].isna().sum() / len(df)
        assert missing_ratio <= max_missing_ratio, \
            f"Missing data ratio {missing_ratio:.3f} exceeds maximum {max_missing_ratio}"
        
        # Check text length
        valid_texts = df[text_column].dropna()
        if len(valid_texts) > 0:
            short_texts = valid_texts.str.len() < min_text_length
            short_ratio = short_texts.sum() / len(valid_texts)
            assert short_ratio <= 0.05, \
                f"Too many short texts: {short_ratio:.3f} of comments are under {min_text_length} characters"
    
    @staticmethod
    def assert_temporal_consistency(df: pd.DataFrame, 
                                  date_column: str = 'Fecha',
                                  allow_future: bool = False):
        """Assert temporal data consistency"""
        if date_column not in df.columns:
            return  # Skip if no date column
        
        dates = pd.to_datetime(df[date_column], errors='coerce')
        valid_dates = dates.dropna()
        
        if len(valid_dates) == 0:
            return  # Skip if no valid dates
        
        # Check for future dates if not allowed
        if not allow_future:
            future_dates = valid_dates > pd.Timestamp.now()
            assert not future_dates.any(), \
                f"Found {future_dates.sum()} future dates when not allowed"
        
        # Check for reasonable date range (not too old)
        min_date = pd.Timestamp('2000-01-01')
        old_dates = valid_dates < min_date
        assert not old_dates.any(), \
            f"Found {old_dates.sum()} dates before {min_date}"


class PerformanceAssertions:
    """Custom assertions for performance testing"""
    
    @staticmethod
    def assert_execution_time(execution_time: float, 
                            max_time: float, 
                            operation_name: str = "Operation"):
        """Assert execution time is within acceptable limits"""
        assert execution_time <= max_time, \
            f"{operation_name} took {execution_time:.3f}s, exceeded limit {max_time}s"
        
        assert execution_time >= 0, \
            f"Invalid execution time: {execution_time}"
    
    @staticmethod
    def assert_memory_usage(memory_used_mb: float, 
                          max_memory_mb: float,
                          operation_name: str = "Operation"):
        """Assert memory usage is within acceptable limits"""
        assert memory_used_mb <= max_memory_mb, \
            f"{operation_name} used {memory_used_mb:.2f}MB, exceeded limit {max_memory_mb}MB"
        
        assert memory_used_mb >= 0, \
            f"Invalid memory usage: {memory_used_mb}MB"
    
    @staticmethod
    def assert_throughput(operations_count: int, 
                        execution_time: float, 
                        min_ops_per_second: float):
        """Assert throughput meets minimum requirements"""
        if execution_time <= 0:
            pytest.fail("Invalid execution time for throughput calculation")
        
        actual_throughput = operations_count / execution_time
        assert actual_throughput >= min_ops_per_second, \
            f"Throughput {actual_throughput:.2f} ops/sec below minimum {min_ops_per_second}"
    
    @staticmethod
    def assert_scalability(small_time: float, 
                         large_time: float, 
                         size_ratio: float,
                         max_growth_factor: float = 2.0):
        """Assert that processing time scales reasonably with data size"""
        if small_time <= 0:
            pytest.fail("Invalid small dataset execution time")
        
        actual_growth = large_time / small_time
        expected_max_growth = size_ratio * max_growth_factor
        
        assert actual_growth <= expected_max_growth, \
            f"Processing time grew by {actual_growth:.2f}x but expected max {expected_max_growth:.2f}x " \
            f"for {size_ratio:.2f}x data increase"


class FileAssertions:
    """Custom assertions for file operations"""
    
    @staticmethod
    def assert_file_created(file_path: Union[str, Path], 
                          min_size: int = 0,
                          max_age_seconds: Optional[float] = None):
        """Assert file was created successfully"""
        path = Path(file_path)
        assert path.exists(), f"File not found: {path}"
        assert path.is_file(), f"Path is not a file: {path}"
        
        # Check file size
        size = path.stat().st_size
        assert size >= min_size, f"File size {size} bytes below minimum {min_size}"
        
        # Check file age if specified
        if max_age_seconds is not None:
            import time
            file_age = time.time() - path.stat().st_mtime
            assert file_age <= max_age_seconds, \
                f"File is {file_age:.1f}s old, exceeds maximum {max_age_seconds}s"
    
    @staticmethod
    def assert_file_format(file_path: Union[str, Path], 
                         expected_format: str):
        """Assert file has expected format"""
        path = Path(file_path)
        
        if expected_format.lower() == 'csv':
            try:
                df = pd.read_csv(path)
                assert isinstance(df, pd.DataFrame)
            except Exception as e:
                pytest.fail(f"File is not valid CSV: {e}")
        
        elif expected_format.lower() in ['xlsx', 'excel']:
            try:
                df = pd.read_excel(path)
                assert isinstance(df, pd.DataFrame)
            except Exception as e:
                pytest.fail(f"File is not valid Excel: {e}")
        
        elif expected_format.lower() == 'json':
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                assert isinstance(data, (dict, list))
            except Exception as e:
                pytest.fail(f"File is not valid JSON: {e}")
    
    @staticmethod
    def assert_file_encoding(file_path: Union[str, Path], 
                           expected_encoding: str = 'utf-8'):
        """Assert file has expected encoding"""
        path = Path(file_path)
        
        try:
            with open(path, 'r', encoding=expected_encoding) as f:
                content = f.read()
            assert isinstance(content, str)
        except UnicodeDecodeError:
            pytest.fail(f"File is not encoded in {expected_encoding}")


class APIAssertions:
    """Custom assertions for API testing"""
    
    @staticmethod
    def assert_api_response(response: Dict[str, Any], 
                          expected_status: str = 'success',
                          required_fields: Optional[List[str]] = None):
        """Assert API response has expected structure"""
        assert isinstance(response, dict), f"Response should be dict, got {type(response)}"
        
        # Check status
        assert 'status' in response, "Response must contain 'status' field"
        assert response['status'] == expected_status, \
            f"Expected status '{expected_status}', got '{response.get('status')}'"
        
        # Check required fields
        if required_fields:
            missing_fields = set(required_fields) - set(response.keys())
            assert not missing_fields, f"Missing required fields: {missing_fields}"
    
    @staticmethod
    def assert_api_error(response: Dict[str, Any], 
                       expected_error_code: Optional[str] = None):
        """Assert API error response has expected structure"""
        assert isinstance(response, dict), f"Response should be dict, got {type(response)}"
        assert response.get('status') == 'error', "Expected error status"
        assert 'error' in response, "Error response must contain 'error' field"
        
        if expected_error_code:
            assert response.get('code') == expected_error_code, \
                f"Expected error code '{expected_error_code}', got '{response.get('code')}'"
    
    @staticmethod
    def assert_rate_limit_respected(call_times: List[float], 
                                  max_calls_per_minute: int):
        """Assert API calls respect rate limits"""
        if len(call_times) < 2:
            return  # Need at least 2 calls to check rate
        
        # Check calls within 1-minute windows
        for i in range(len(call_times)):
            window_start = call_times[i]
            calls_in_window = sum(1 for t in call_times[i:] if t - window_start <= 60)
            
            assert calls_in_window <= max_calls_per_minute, \
                f"Rate limit exceeded: {calls_in_window} calls in 1 minute, limit is {max_calls_per_minute}"


# Convenience function to get all assertion classes
def get_all_assertions():
    """Get all assertion classes for easy importing"""
    return {
        'SentimentAssertions': SentimentAssertions,
        'DataAssertions': DataAssertions,
        'PerformanceAssertions': PerformanceAssertions,
        'FileAssertions': FileAssertions,
        'APIAssertions': APIAssertions,
    }