#!/usr/bin/env python
"""
Integration test to verify the testing framework is working correctly
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root))

def test_framework_components():
    """Test that all framework components work together"""
    
    print("Testing Framework Components Integration...")
    
    # Test 1: Base classes
    try:
        from tests.base.test_base import BaseUnitTest, BaseIntegrationTest
        print("[OK] Base classes imported successfully")
    except Exception as e:
        print(f"[FAIL] Base classes failed: {e}")
        return False
    
    # Test 2: Mixins
    try:
        from tests.mixins.test_mixins import AssertionMixin, MockingMixin
        print("[OK] Mixins imported successfully")
    except Exception as e:
        print(f"[FAIL] Mixins failed: {e}")
        return False
    
    # Test 3: Factories
    try:
        from tests.factories.test_factories import CommentFactory, UserFactory
        comment = CommentFactory.create()
        user = UserFactory.create()
        assert 'text' in comment
        assert 'username' in user
        print("[OK] Factories working correctly")
    except Exception as e:
        import traceback
        print(f"[FAIL] Factories failed: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False
    
    # Test 4: Mock builders
    try:
        from tests.builders.mock_builders import SentimentAnalyzerMockBuilder, mock_sentiment_analyzer
        
        # Test builder pattern
        mock = (SentimentAnalyzerMockBuilder()
               .with_sentiment_result("positive", 0.9)
               .build())
        result = mock.analyze("test")
        assert result['sentiment'] == 'positive'
        
        # Test convenience function
        simple_mock = mock_sentiment_analyzer("negative", 0.8)
        result2 = simple_mock.analyze("test")
        assert result2['sentiment'] == 'negative'
        
        print("[OK] Mock builders working correctly")
    except Exception as e:
        print(f"[FAIL] Mock builders failed: {e}")
        return False
    
    # Test 5: Custom assertions
    try:
        from tests.assertions.custom_assertions import SentimentAssertions
        
        # Test valid sentiment result
        test_result = {'sentiment': 'positive', 'confidence': 0.8}
        SentimentAssertions.assert_valid_sentiment_result(test_result)
        
        # Test sentiment consistency
        SentimentAssertions.assert_sentiment_consistency("Excelente servicio", test_result)
        
        print("[OK] Custom assertions working correctly")
    except Exception as e:
        print(f"[FAIL] Custom assertions failed: {e}")
        return False
    
    # Test 6: Performance framework
    try:
        from tests.performance.performance_framework import PerformanceBenchmark, PerformanceThresholds
        
        benchmark = PerformanceBenchmark()
        
        def test_function():
            return sum(range(1000))
        
        metrics = benchmark.measure_execution(test_function)
        assert metrics.execution_time > 0
        assert metrics.throughput_ops_per_sec > 0
        
        print("[OK] Performance framework working correctly")
    except Exception as e:
        print(f"[FAIL] Performance framework failed: {e}")
        return False
    
    # Test 7: Configuration management
    try:
        from tests.config import TestEnvironment, get_test_config, set_test_environment
        
        # Test environment switching
        set_test_environment(TestEnvironment.UNIT)
        config = get_test_config()
        assert config.environment == TestEnvironment.UNIT
        
        set_test_environment(TestEnvironment.PERFORMANCE)
        config = get_test_config()
        assert config.environment == TestEnvironment.PERFORMANCE
        
        print("[OK] Configuration management working correctly")
    except Exception as e:
        print(f"[FAIL] Configuration management failed: {e}")
        return False
    
    # Test 8: Actual sentiment analysis integration
    try:
        from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
        from sentiment_analysis.basic_analyzer import BasicAnalysisMethod
        
        # Test enhanced analyzer
        analyzer = EnhancedAnalyzer()
        result = analyzer.analyze("Excelente servicio de fibra óptica")
        assert result['sentiment'] in ['positive', 'negative', 'neutral']
        assert 0 <= result['confidence'] <= 1
        
        # Test basic analyzer
        basic = BasicAnalysisMethod()
        results = basic.analyze(["Buen servicio"])
        assert len(results) == 1
        assert results[0]['sentiment'] in ['positive', 'negative', 'neutral']
        
        print("[OK] Sentiment analysis integration working correctly")
    except Exception as e:
        print(f"[FAIL] Sentiment analysis integration failed: {e}")
        return False
    
    # Test 9: Complete workflow test
    try:
        # Create test data using factory
        test_comments = CommentFactory.create_batch(5)
        
        # Use enhanced analyzer
        analyzer = EnhancedAnalyzer()
        results = []
        
        for comment in test_comments:
            result = analyzer.analyze(comment['text'])
            results.append(result)
        
        # Use custom assertions
        from tests.assertions.custom_assertions import SentimentAssertions
        for result in results:
            SentimentAssertions.assert_valid_sentiment_result(result)
        
        # Check distribution
        sentiments = [r['sentiment'] for r in results]
        unique_sentiments = set(sentiments)
        assert len(unique_sentiments) > 0
        
        print("[OK] Complete workflow test passed")
    except Exception as e:
        print(f"[FAIL] Complete workflow test failed: {e}")
        return False
    
    print("\n[SUCCESS] ALL FRAMEWORK COMPONENTS WORKING CORRECTLY! [SUCCESS]")
    return True


def test_pytest_integration():
    """Test that pytest can run our framework tests"""
    import subprocess
    
    print("\nTesting pytest integration...")
    
    try:
        # Run a subset of our parameterized tests
        result = subprocess.run([
            'python', '-m', 'pytest', 
            'tests/unit/test_sentiment_parameterized.py::TestSentimentParameterized::test_basic_sentiment_classification',
            '-v', '--tb=short', '--disable-warnings', '--no-cov', '-q'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("[OK] Pytest integration working correctly")
            lines = result.stdout.split('\n')
            passed_tests = [line for line in lines if 'PASSED' in line]
            print(f"[OK] {len(passed_tests)} parameterized tests passed")
            return True
        else:
            print(f"[FAIL] Pytest integration failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Pytest integration failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING FRAMEWORK INTEGRATION TEST")
    print("=" * 60)
    
    # Test framework components
    components_ok = test_framework_components()
    
    # Test pytest integration
    pytest_ok = test_pytest_integration()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if components_ok and pytest_ok:
        print("[SUCCESS] TESTING FRAMEWORK IS FULLY FUNCTIONAL! [SUCCESS]")
        print("\nThe comprehensive testing framework has been successfully implemented and verified:")
        print("[OK] All base classes, mixins, factories, builders working")
        print("[OK] Custom assertions and performance framework operational")
        print("[OK] Configuration management functional")
        print("[OK] Integration with actual sentiment analysis working")
        print("[OK] Pytest integration confirmed")
        print("\nThe framework is ready for production use!")
        sys.exit(0)
    else:
        print("[FAIL] Some components failed - see details above")
        sys.exit(1)