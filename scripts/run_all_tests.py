#!/usr/bin/env python
"""
Automated Test Runner for Personal Paraguay Fiber Comments Analysis System
Runs all tests and generates comprehensive reports
"""

import sys
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime
import json
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)


class TestRunner:
    """Automated test runner with reporting"""
    
    def __init__(self, verbose=False, coverage=True, html_report=True):
        self.verbose = verbose
        self.coverage = coverage
        self.html_report = html_report
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(text.center(60))
        print("=" * 60 + "\n")
    
    def print_status(self, test_type, passed, total, duration):
        """Print test status"""
        status = "PASSED" if passed == total else "FAILED"
        color = '\033[92m' if passed == total else '\033[91m'
        reset = '\033[0m'
        
        print(f"{test_type:20} {color}{status}{reset} ({passed}/{total} passed) - {duration:.2f}s")
    
    def run_unit_tests(self):
        """Run unit tests"""
        self.print_header("RUNNING UNIT TESTS")
        
        start = time.time()
        cmd = ["pytest", "tests/unit/", "-v" if self.verbose else "-q"]
        
        if self.coverage:
            cmd.extend(["--cov=src", "--cov-report=term-missing"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start
        
        # Parse results
        output = result.stdout + result.stderr
        passed = output.count(" passed")
        failed = output.count(" failed")
        total = passed + failed
        
        self.results['unit'] = {
            'passed': passed,
            'failed': failed,
            'total': total,
            'duration': duration,
            'output': output if self.verbose else None
        }
        
        self.print_status("Unit Tests", passed, total, duration)
        return failed == 0
    
    def run_integration_tests(self):
        """Run integration tests"""
        self.print_header("RUNNING INTEGRATION TESTS")
        
        start = time.time()
        cmd = ["pytest", "tests/integration/", "-v" if self.verbose else "-q"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start
        
        # Parse results
        output = result.stdout + result.stderr
        passed = output.count(" passed")
        failed = output.count(" failed")
        total = passed + failed
        
        # Handle case where no integration tests exist yet
        if total == 0:
            print("No integration tests found - creating directory...")
            Path("tests/integration").mkdir(exist_ok=True)
            passed = 0
            total = 0
        
        self.results['integration'] = {
            'passed': passed,
            'failed': failed,
            'total': total,
            'duration': duration,
            'output': output if self.verbose else None
        }
        
        self.print_status("Integration Tests", passed, total, duration)
        return failed == 0
    
    def run_performance_tests(self):
        """Run performance tests"""
        self.print_header("RUNNING PERFORMANCE TESTS")
        
        # Simple performance test
        from tests.fixtures.test_data_generator import TestDataGenerator
        
        start = time.time()
        try:
            generator = TestDataGenerator()
            
            # Test small dataset generation
            small_start = time.time()
            small_df = generator.generate_small_dataset(10)
            small_time = time.time() - small_start
            
            # Test medium dataset generation
            medium_start = time.time()
            medium_df = generator.generate_medium_dataset(100)
            medium_time = time.time() - medium_start
            
            # Test large dataset generation
            large_start = time.time()
            large_df = generator.generate_large_dataset(1000)
            large_time = time.time() - large_start
            
            duration = time.time() - start
            
            # Check performance thresholds
            passed = 0
            total = 3
            
            if small_time < 1.0:
                passed += 1
                print(f"  Small dataset (10 rows): {small_time:.3f}s ✓")
            else:
                print(f"  Small dataset (10 rows): {small_time:.3f}s ✗ (>1s)")
            
            if medium_time < 5.0:
                passed += 1
                print(f"  Medium dataset (100 rows): {medium_time:.3f}s ✓")
            else:
                print(f"  Medium dataset (100 rows): {medium_time:.3f}s ✗ (>5s)")
            
            if large_time < 10.0:
                passed += 1
                print(f"  Large dataset (1000 rows): {large_time:.3f}s ✓")
            else:
                print(f"  Large dataset (1000 rows): {large_time:.3f}s ✗ (>10s)")
            
            self.results['performance'] = {
                'passed': passed,
                'failed': total - passed,
                'total': total,
                'duration': duration,
                'metrics': {
                    'small_time': small_time,
                    'medium_time': medium_time,
                    'large_time': large_time
                }
            }
            
        except Exception as e:
            print(f"Performance tests failed: {e}")
            self.results['performance'] = {
                'passed': 0,
                'failed': 1,
                'total': 1,
                'duration': time.time() - start,
                'error': str(e)
            }
            passed = 0
            total = 1
            duration = time.time() - start
        
        self.print_status("Performance Tests", passed, total, duration)
        return passed == total
    
    def run_security_tests(self):
        """Run basic security tests"""
        self.print_header("RUNNING SECURITY TESTS")
        
        start = time.time()
        passed = 0
        total = 4
        
        # Test 1: Check for exposed API keys
        print("  Checking for exposed API keys...")
        cmd = ["grep", "-r", "sk-", "src/", "--include=*.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not result.stdout:
            passed += 1
            print("    ✓ No exposed API keys found")
        else:
            print("    ✗ Potential API keys found in code")
        
        # Test 2: Check for SQL injection vulnerabilities
        print("  Checking for SQL injection risks...")
        cmd = ["grep", "-r", "execute.*%", "src/", "--include=*.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not result.stdout:
            passed += 1
            print("    ✓ No obvious SQL injection risks")
        else:
            print("    ✗ Potential SQL injection risks found")
        
        # Test 3: Check for hardcoded passwords
        print("  Checking for hardcoded passwords...")
        cmd = ["grep", "-r", "password.*=.*['\"]", "src/", "--include=*.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not result.stdout:
            passed += 1
            print("    ✓ No hardcoded passwords found")
        else:
            print("    ✗ Potential hardcoded passwords found")
        
        # Test 4: Check for debug mode in production
        print("  Checking debug configuration...")
        try:
            from config import Config
            if not getattr(Config, 'DEBUG', False):
                passed += 1
                print("    ✓ Debug mode is disabled")
            else:
                print("    ✗ Debug mode is enabled")
        except:
            print("    ✗ Could not check debug configuration")
        
        duration = time.time() - start
        
        self.results['security'] = {
            'passed': passed,
            'failed': total - passed,
            'total': total,
            'duration': duration
        }
        
        self.print_status("Security Tests", passed, total, duration)
        return passed == total
    
    def run_code_quality_checks(self):
        """Run code quality checks"""
        self.print_header("RUNNING CODE QUALITY CHECKS")
        
        start = time.time()
        passed = 0
        total = 2
        
        # Run flake8
        print("  Running flake8...")
        cmd = ["flake8", "src/", "--max-line-length=100", "--count"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            passed += 1
            print("    ✓ Flake8 passed")
        else:
            errors = len(result.stdout.strip().split('\n')) if result.stdout else 0
            print(f"    ✗ Flake8 found {errors} issues")
        
        # Run black check
        print("  Running black...")
        cmd = ["black", "src/", "--check", "--quiet"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            passed += 1
            print("    ✓ Black formatting check passed")
        else:
            print("    ✗ Black formatting issues found")
        
        duration = time.time() - start
        
        self.results['quality'] = {
            'passed': passed,
            'failed': total - passed,
            'total': total,
            'duration': duration
        }
        
        self.print_status("Code Quality", passed, total, duration)
        return passed == total
    
    def generate_coverage_report(self):
        """Generate coverage report"""
        if self.coverage and self.html_report:
            self.print_header("GENERATING COVERAGE REPORT")
            
            cmd = ["pytest", "--cov=src", "--cov-report=html:htmlcov", "--quiet"]
            subprocess.run(cmd, capture_output=True)
            
            print("HTML coverage report generated in htmlcov/")
            print("Open htmlcov/index.html to view the report")
    
    def generate_summary_report(self):
        """Generate summary report"""
        self.print_header("TEST SUMMARY REPORT")
        
        total_passed = sum(r['passed'] for r in self.results.values())
        total_failed = sum(r['failed'] for r in self.results.values())
        total_tests = sum(r['total'] for r in self.results.values())
        total_duration = sum(r['duration'] for r in self.results.values())
        
        print(f"Total Tests:    {total_tests}")
        print(f"Passed:         {total_passed}")
        print(f"Failed:         {total_failed}")
        print(f"Pass Rate:      {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        print(f"Total Duration: {total_duration:.2f}s")
        print()
        
        # Detailed results
        print("Detailed Results:")
        print("-" * 50)
        for test_type, result in self.results.items():
            status = "✓" if result['failed'] == 0 else "✗"
            print(f"{status} {test_type:15} {result['passed']:3}/{result['total']:3} passed ({result['duration']:.2f}s)")
        
        # Save report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed': total_passed,
                    'failed': total_failed,
                    'pass_rate': total_passed/total_tests if total_tests > 0 else 0,
                    'duration': total_duration
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_file}")
        
        # Return exit code
        return 0 if total_failed == 0 else 1
    
    def run_all(self):
        """Run all tests"""
        self.start_time = time.time()
        
        print("\n" + "=" * 60)
        print("PERSONAL PARAGUAY FIBER COMMENTS ANALYSIS")
        print("AUTOMATED TEST SUITE")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all test suites
        self.run_unit_tests()
        self.run_integration_tests()
        self.run_performance_tests()
        self.run_security_tests()
        self.run_code_quality_checks()
        
        # Generate reports
        self.generate_coverage_report()
        exit_code = self.generate_summary_report()
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        print("\n" + "=" * 60)
        print(f"Test suite completed in {total_time:.2f} seconds")
        print("=" * 60 + "\n")
        
        return exit_code


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run automated test suite')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-coverage', action='store_true', help='Skip coverage report')
    parser.add_argument('--no-html', action='store_true', help='Skip HTML report generation')
    parser.add_argument('--quick', action='store_true', help='Run only unit tests')
    
    args = parser.parse_args()
    
    runner = TestRunner(
        verbose=args.verbose,
        coverage=not args.no_coverage,
        html_report=not args.no_html
    )
    
    if args.quick:
        runner.run_unit_tests()
        if not args.no_coverage:
            runner.generate_coverage_report()
        return 0
    else:
        return runner.run_all()


if __name__ == '__main__':
    sys.exit(main())