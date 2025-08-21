"""
Performance testing framework for sentiment analysis system
Provides benchmarking, load testing, and performance monitoring capabilities
"""

import time
import psutil
import gc
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional, Union
import pandas as pd
import numpy as np
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings


@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    operation_name: str
    execution_time: float
    memory_used_mb: float
    cpu_percent: float
    throughput_ops_per_sec: float
    error_count: int = 0
    success_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        total = self.success_count + self.error_count
        return (self.success_count / total) if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'operation_name': self.operation_name,
            'execution_time': self.execution_time,
            'memory_used_mb': self.memory_used_mb,
            'cpu_percent': self.cpu_percent,
            'throughput_ops_per_sec': self.throughput_ops_per_sec,
            'error_count': self.error_count,
            'success_count': self.success_count,
            'success_rate': self.success_rate,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class PerformanceThresholds:
    """Performance threshold configuration"""
    max_execution_time: float = 5.0  # seconds
    max_memory_usage_mb: float = 500.0  # MB
    min_throughput_ops_per_sec: float = 10.0
    max_cpu_percent: float = 80.0
    min_success_rate: float = 0.95


class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self):
        self.is_monitoring = False
        self.metrics_history = []
        self.monitor_thread = None
        self.monitor_interval = 1.0  # seconds
    
    def start_monitoring(self, interval: float = 1.0):
        """Start performance monitoring"""
        self.monitor_interval = interval
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        process = psutil.Process()
        
        while self.is_monitoring:
            try:
                memory_mb = process.memory_info().rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                
                self.metrics_history.append({
                    'timestamp': datetime.now(),
                    'memory_mb': memory_mb,
                    'cpu_percent': cpu_percent
                })
                
                time.sleep(self.monitor_interval)
            except Exception:
                break
    
    def get_peak_usage(self) -> Dict[str, float]:
        """Get peak resource usage"""
        if not self.metrics_history:
            return {'memory_mb': 0, 'cpu_percent': 0}
        
        peak_memory = max(m['memory_mb'] for m in self.metrics_history)
        peak_cpu = max(m['cpu_percent'] for m in self.metrics_history)
        
        return {'memory_mb': peak_memory, 'cpu_percent': peak_cpu}
    
    def clear_history(self):
        """Clear monitoring history"""
        self.metrics_history.clear()


class PerformanceBenchmark:
    """Performance benchmarking utilities"""
    
    def __init__(self, thresholds: Optional[PerformanceThresholds] = None):
        self.thresholds = thresholds or PerformanceThresholds()
        self.monitor = PerformanceMonitor()
        self.results = []
    
    def measure_execution(self, func: Callable, *args, **kwargs) -> PerformanceMetrics:
        """Measure execution performance of a function"""
        # Get initial system state
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        # Force garbage collection for accurate measurement
        gc.collect()
        
        # Start monitoring
        self.monitor.start_monitoring(0.1)
        
        # Execute function
        start_time = time.time()
        success = False
        error = None
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            error = e
            result = None
        finally:
            end_time = time.time()
            self.monitor.stop_monitoring()
        
        execution_time = end_time - start_time
        
        # Calculate memory usage
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = max(0, final_memory - initial_memory)
        
        # Get peak usage from monitoring
        peak_usage = self.monitor.get_peak_usage()
        memory_used = max(memory_used, peak_usage['memory_mb'] - initial_memory)
        
        # Calculate throughput (operations per second)
        throughput = 1.0 / execution_time if execution_time > 0 else 0
        
        metrics = PerformanceMetrics(
            operation_name=func.__name__,
            execution_time=execution_time,
            memory_used_mb=memory_used,
            cpu_percent=peak_usage['cpu_percent'],
            throughput_ops_per_sec=throughput,
            error_count=1 if not success else 0,
            success_count=1 if success else 0
        )
        
        self.results.append(metrics)
        self.monitor.clear_history()
        
        if not success:
            raise error
        
        return metrics
    
    def benchmark_batch_processing(self, func: Callable, data_batches: List[Any], 
                                 batch_sizes: List[int]) -> Dict[int, PerformanceMetrics]:
        """Benchmark batch processing with different batch sizes"""
        results = {}
        
        for batch_size in batch_sizes:
            print(f"Benchmarking batch size: {batch_size}")
            
            # Create batch of specified size
            if isinstance(data_batches[0], list):
                batch_data = data_batches[0][:batch_size]
            else:
                batch_data = [data_batches[0]] * batch_size
            
            metrics = self.measure_execution(func, batch_data)
            metrics.operation_name = f"{func.__name__}_batch_{batch_size}"
            
            # Adjust throughput for batch size
            metrics.throughput_ops_per_sec = batch_size / metrics.execution_time
            
            results[batch_size] = metrics
        
        return results
    
    def stress_test(self, func: Callable, test_data: Any, 
                   duration_seconds: float = 60, max_concurrent: int = 10) -> Dict[str, Any]:
        """Perform stress testing"""
        print(f"Starting stress test for {duration_seconds} seconds with {max_concurrent} concurrent operations")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        results = []
        errors = []
        
        self.monitor.start_monitoring(0.5)
        
        def run_operation():
            try:
                operation_start = time.time()
                func(test_data)
                operation_time = time.time() - operation_start
                return {'success': True, 'time': operation_time}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            while time.time() < end_time:
                if len(futures) < max_concurrent:
                    future = executor.submit(run_operation)
                    futures.append(future)
                
                # Check completed futures
                completed_futures = [f for f in futures if f.done()]
                for future in completed_futures:
                    try:
                        result = future.result()
                        if result['success']:
                            results.append(result)
                        else:
                            errors.append(result['error'])
                    except Exception as e:
                        errors.append(str(e))
                    futures.remove(future)
                
                time.sleep(0.01)  # Small delay to prevent busy waiting
            
            # Wait for remaining futures
            for future in as_completed(futures, timeout=10):
                try:
                    result = future.result()
                    if result['success']:
                        results.append(result)
                    else:
                        errors.append(result['error'])
                except Exception as e:
                    errors.append(str(e))
        
        self.monitor.stop_monitoring()
        
        # Calculate statistics
        total_operations = len(results) + len(errors)
        success_rate = len(results) / total_operations if total_operations > 0 else 0
        
        execution_times = [r['time'] for r in results]
        avg_time = statistics.mean(execution_times) if execution_times else 0
        p95_time = np.percentile(execution_times, 95) if execution_times else 0
        p99_time = np.percentile(execution_times, 99) if execution_times else 0
        
        peak_usage = self.monitor.get_peak_usage()
        
        return {
            'total_operations': total_operations,
            'successful_operations': len(results),
            'failed_operations': len(errors),
            'success_rate': success_rate,
            'operations_per_second': total_operations / duration_seconds,
            'avg_execution_time': avg_time,
            'p95_execution_time': p95_time,
            'p99_execution_time': p99_time,
            'peak_memory_mb': peak_usage['memory_mb'],
            'peak_cpu_percent': peak_usage['cpu_percent'],
            'errors': errors[:10]  # First 10 errors for debugging
        }
    
    def load_test(self, func: Callable, test_data: List[Any], 
                 concurrent_users: List[int]) -> Dict[int, Dict[str, Any]]:
        """Perform load testing with varying concurrent users"""
        results = {}
        
        for user_count in concurrent_users:
            print(f"Load testing with {user_count} concurrent users")
            
            start_time = time.time()
            successful_operations = 0
            failed_operations = 0
            execution_times = []
            
            self.monitor.start_monitoring(0.5)
            
            with ThreadPoolExecutor(max_workers=user_count) as executor:
                futures = []
                
                # Submit all tasks
                for data in test_data[:user_count]:  # One operation per user
                    future = executor.submit(self._timed_execution, func, data)
                    futures.append(future)
                
                # Collect results
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result['success']:
                            successful_operations += 1
                            execution_times.append(result['execution_time'])
                        else:
                            failed_operations += 1
                    except Exception:
                        failed_operations += 1
            
            self.monitor.stop_monitoring()
            
            total_time = time.time() - start_time
            peak_usage = self.monitor.get_peak_usage()
            
            results[user_count] = {
                'concurrent_users': user_count,
                'successful_operations': successful_operations,
                'failed_operations': failed_operations,
                'success_rate': successful_operations / (successful_operations + failed_operations),
                'total_execution_time': total_time,
                'avg_response_time': statistics.mean(execution_times) if execution_times else 0,
                'p95_response_time': np.percentile(execution_times, 95) if execution_times else 0,
                'throughput_ops_per_sec': successful_operations / total_time,
                'peak_memory_mb': peak_usage['memory_mb'],
                'peak_cpu_percent': peak_usage['cpu_percent']
            }
            
            self.monitor.clear_history()
        
        return results
    
    def _timed_execution(self, func: Callable, data: Any) -> Dict[str, Any]:
        """Execute function with timing"""
        start_time = time.time()
        try:
            func(data)
            execution_time = time.time() - start_time
            return {'success': True, 'execution_time': execution_time}
        except Exception as e:
            execution_time = time.time() - start_time
            return {'success': False, 'execution_time': execution_time, 'error': str(e)}
    
    def validate_thresholds(self, metrics: PerformanceMetrics) -> Dict[str, bool]:
        """Validate metrics against thresholds"""
        return {
            'execution_time_ok': metrics.execution_time <= self.thresholds.max_execution_time,
            'memory_usage_ok': metrics.memory_used_mb <= self.thresholds.max_memory_usage_mb,
            'throughput_ok': metrics.throughput_ops_per_sec >= self.thresholds.min_throughput_ops_per_sec,
            'cpu_usage_ok': metrics.cpu_percent <= self.thresholds.max_cpu_percent,
            'success_rate_ok': metrics.success_rate >= self.thresholds.min_success_rate
        }
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate performance test report"""
        if not self.results:
            return "No performance results to report"
        
        report_data = {
            'test_summary': {
                'total_tests': len(self.results),
                'test_timestamp': datetime.now().isoformat(),
                'thresholds': {
                    'max_execution_time': self.thresholds.max_execution_time,
                    'max_memory_usage_mb': self.thresholds.max_memory_usage_mb,
                    'min_throughput_ops_per_sec': self.thresholds.min_throughput_ops_per_sec,
                    'max_cpu_percent': self.thresholds.max_cpu_percent,
                    'min_success_rate': self.thresholds.min_success_rate
                }
            },
            'results': [metric.to_dict() for metric in self.results]
        }
        
        # Generate text report
        report_lines = [
            "=" * 80,
            "PERFORMANCE TEST REPORT",
            "=" * 80,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Tests: {len(self.results)}",
            "",
            "THRESHOLDS:",
            f"  Max Execution Time: {self.thresholds.max_execution_time}s",
            f"  Max Memory Usage: {self.thresholds.max_memory_usage_mb}MB",
            f"  Min Throughput: {self.thresholds.min_throughput_ops_per_sec} ops/sec",
            f"  Max CPU Usage: {self.thresholds.max_cpu_percent}%",
            f"  Min Success Rate: {self.thresholds.min_success_rate * 100}%",
            "",
            "RESULTS:",
            "-" * 80
        ]
        
        for metric in self.results:
            validation = self.validate_thresholds(metric)
            status = "PASS" if all(validation.values()) else "FAIL"
            
            report_lines.extend([
                f"Operation: {metric.operation_name} [{status}]",
                f"  Execution Time: {metric.execution_time:.3f}s {'✓' if validation['execution_time_ok'] else '✗'}",
                f"  Memory Used: {metric.memory_used_mb:.2f}MB {'✓' if validation['memory_usage_ok'] else '✗'}",
                f"  Throughput: {metric.throughput_ops_per_sec:.2f} ops/sec {'✓' if validation['throughput_ok'] else '✗'}",
                f"  CPU Usage: {metric.cpu_percent:.1f}% {'✓' if validation['cpu_usage_ok'] else '✗'}",
                f"  Success Rate: {metric.success_rate * 100:.1f}% {'✓' if validation['success_rate_ok'] else '✗'}",
                ""
            ])
        
        report_text = "\n".join(report_lines)
        
        # Save to file if path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save text report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            
            # Save JSON report
            json_path = Path(output_path).with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"Reports saved to {output_path} and {json_path}")
        
        return report_text
    
    def plot_performance_trends(self, output_path: Optional[str] = None):
        """Generate performance trend plots"""
        if not self.results:
            return
        
        # Suppress matplotlib warnings
        warnings.filterwarnings('ignore')
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        operations = [m.operation_name for m in self.results]
        execution_times = [m.execution_time for m in self.results]
        memory_usage = [m.memory_used_mb for m in self.results]
        throughput = [m.throughput_ops_per_sec for m in self.results]
        cpu_usage = [m.cpu_percent for m in self.results]
        
        # Execution time plot
        axes[0, 0].bar(operations, execution_times, color='skyblue')
        axes[0, 0].axhline(y=self.thresholds.max_execution_time, color='red', linestyle='--', label='Threshold')
        axes[0, 0].set_title('Execution Time')
        axes[0, 0].set_ylabel('Seconds')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].legend()
        
        # Memory usage plot
        axes[0, 1].bar(operations, memory_usage, color='lightgreen')
        axes[0, 1].axhline(y=self.thresholds.max_memory_usage_mb, color='red', linestyle='--', label='Threshold')
        axes[0, 1].set_title('Memory Usage')
        axes[0, 1].set_ylabel('MB')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].legend()
        
        # Throughput plot
        axes[1, 0].bar(operations, throughput, color='orange')
        axes[1, 0].axhline(y=self.thresholds.min_throughput_ops_per_sec, color='red', linestyle='--', label='Threshold')
        axes[1, 0].set_title('Throughput')
        axes[1, 0].set_ylabel('Operations/Second')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].legend()
        
        # CPU usage plot
        axes[1, 1].bar(operations, cpu_usage, color='pink')
        axes[1, 1].axhline(y=self.thresholds.max_cpu_percent, color='red', linestyle='--', label='Threshold')
        axes[1, 1].set_title('CPU Usage')
        axes[1, 1].set_ylabel('Percentage')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Performance plots saved to {output_path}")
        else:
            plt.show()
        
        plt.close()


# Decorator for easy performance measurement
def measure_performance(thresholds: Optional[PerformanceThresholds] = None):
    """Decorator to measure function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            benchmark = PerformanceBenchmark(thresholds)
            metrics = benchmark.measure_execution(func, *args, **kwargs)
            
            print(f"Performance metrics for {func.__name__}:")
            print(f"  Execution time: {metrics.execution_time:.3f}s")
            print(f"  Memory used: {metrics.memory_used_mb:.2f}MB")
            print(f"  Throughput: {metrics.throughput_ops_per_sec:.2f} ops/sec")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Context manager for performance monitoring
class PerformanceContext:
    """Context manager for performance monitoring"""
    
    def __init__(self, operation_name: str, thresholds: Optional[PerformanceThresholds] = None):
        self.operation_name = operation_name
        self.benchmark = PerformanceBenchmark(thresholds)
        self.start_time = None
        self.metrics = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.benchmark.monitor.start_monitoring(0.1)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.benchmark.monitor.stop_monitoring()
        
        execution_time = time.time() - self.start_time
        peak_usage = self.benchmark.monitor.get_peak_usage()
        
        self.metrics = PerformanceMetrics(
            operation_name=self.operation_name,
            execution_time=execution_time,
            memory_used_mb=peak_usage['memory_mb'],
            cpu_percent=peak_usage['cpu_percent'],
            throughput_ops_per_sec=1.0 / execution_time if execution_time > 0 else 0,
            success_count=1 if exc_type is None else 0,
            error_count=0 if exc_type is None else 1
        )
        
        return False  # Don't suppress exceptions