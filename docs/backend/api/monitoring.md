# Monitoring System Documentation

The Monitoring System provides comprehensive observability into the Personal Paraguay Fiber Comments Analysis System, tracking performance, usage, costs, and system health.

## 🎯 Overview

The monitoring system implements multi-dimensional observability to ensure system reliability, performance optimization, and cost control while providing actionable insights for system improvement.

### Core Capabilities
- **Performance Monitoring** - Real-time performance metrics
- **Usage Analytics** - API usage and cost tracking
- **Health Monitoring** - System health and availability
- **Alert Management** - Proactive issue detection
- **Business Metrics** - Analysis quality and effectiveness

## 🏗️ Monitoring Architecture

### Monitoring Stack
```python
class MonitoringArchitecture:
    """
    Comprehensive monitoring system architecture
    """
    
    MONITORING_LAYERS = {
        'application': {
            'metrics': ['response_time', 'throughput', 'error_rate'],
            'collection_interval': 10,  # seconds
            'retention': 30  # days
        },
        'infrastructure': {
            'metrics': ['cpu', 'memory', 'disk', 'network'],
            'collection_interval': 30,
            'retention': 7
        },
        'business': {
            'metrics': ['analysis_quality', 'user_satisfaction', 'cost_efficiency'],
            'collection_interval': 300,
            'retention': 90
        },
        'security': {
            'metrics': ['auth_failures', 'rate_limit_violations', 'suspicious_activity'],
            'collection_interval': 60,
            'retention': 90
        }
    }
```

## 📊 Metrics Collection

### Core Metrics Collector
```python
class MetricsCollector:
    """
    Central metrics collection system
    """
    
    def __init__(self):
        self.metrics_store = MetricsStore()
        self.collectors = {
            'performance': PerformanceCollector(),
            'usage': UsageCollector(),
            'business': BusinessMetricsCollector(),
            'system': SystemMetricsCollector()
        }
    
    async def collect_metrics(self):
        """
        Collect all metrics asynchronously
        """
        metrics = {}
        
        for name, collector in self.collectors.items():
            try:
                metrics[name] = await collector.collect()
            except Exception as e:
                logger.error(f"Failed to collect {name} metrics: {e}")
                metrics[name] = None
        
        # Store metrics with timestamp
        self.metrics_store.store(metrics, timestamp=datetime.now())
        
        # Check thresholds and trigger alerts
        self.check_alert_conditions(metrics)
        
        return metrics
```

### Performance Metrics
```python
class PerformanceMetrics:
    """
    Application performance monitoring
    """
    
    @dataclass
    class Metrics:
        response_time_ms: float
        requests_per_second: float
        concurrent_users: int
        queue_depth: int
        processing_time_ms: float
        cache_hit_rate: float
        error_rate: float
        
    def track_request(self, request_id: str):
        """
        Track individual request performance
        """
        start_time = time.time()
        
        def end_tracking(status='success'):
            duration = (time.time() - start_time) * 1000
            
            self.metrics.append({
                'request_id': request_id,
                'duration_ms': duration,
                'status': status,
                'timestamp': datetime.now()
            })
            
            # Update aggregated metrics
            self.update_aggregates(duration, status)
        
        return end_tracking
```

## 💰 Cost Monitoring

### API Usage Tracking
```python
class APIUsageMonitor:
    """
    Track API usage and associated costs
    """
    
    def __init__(self):
        self.usage_db = UsageDatabase()
        self.cost_calculator = CostCalculator()
        self.budget_manager = BudgetManager()
    
    def track_api_call(self, provider, endpoint, tokens=None):
        """
        Track individual API call and cost
        """
        usage_record = {
            'provider': provider,
            'endpoint': endpoint,
            'tokens': tokens,
            'timestamp': datetime.now(),
            'cost': self.cost_calculator.calculate(provider, endpoint, tokens)
        }
        
        # Store usage record
        self.usage_db.insert(usage_record)
        
        # Update budget tracking
        self.budget_manager.update_usage(usage_record['cost'])
        
        # Check budget alerts
        if self.budget_manager.is_near_limit():
            self.trigger_budget_alert()
        
        return usage_record
```

### Cost Analytics
```python
class CostAnalytics:
    """
    Analyze API usage costs and trends
    """
    
    def generate_cost_report(self, period='daily'):
        """
        Generate comprehensive cost report
        """
        report = {
            'period': period,
            'total_cost': 0,
            'cost_by_provider': {},
            'cost_by_endpoint': {},
            'cost_trend': [],
            'efficiency_metrics': {},
            'recommendations': []
        }
        
        # Calculate costs
        usage_data = self.get_usage_data(period)
        
        for record in usage_data:
            report['total_cost'] += record['cost']
            
            # By provider
            provider = record['provider']
            report['cost_by_provider'][provider] = \
                report['cost_by_provider'].get(provider, 0) + record['cost']
        
        # Calculate efficiency
        report['efficiency_metrics'] = {
            'cost_per_comment': report['total_cost'] / self.total_comments_analyzed,
            'cache_savings': self.calculate_cache_savings(),
            'optimization_potential': self.identify_optimization_opportunities()
        }
        
        return report
```

## 📈 Health Monitoring

### System Health Checks
```python
class HealthMonitor:
    """
    System health monitoring and checks
    """
    
    def __init__(self):
        self.health_checks = {
            'api_connectivity': self.check_api_connectivity,
            'database_health': self.check_database_health,
            'cache_health': self.check_cache_health,
            'disk_space': self.check_disk_space,
            'memory_usage': self.check_memory_usage
        }
        self.health_status = {}
    
    async def perform_health_check(self):
        """
        Perform comprehensive health check
        """
        overall_health = 'healthy'
        checks_result = {}
        
        for check_name, check_func in self.health_checks.items():
            try:
                result = await check_func()
                checks_result[check_name] = result
                
                if result['status'] == 'unhealthy':
                    overall_health = 'unhealthy'
                elif result['status'] == 'degraded' and overall_health == 'healthy':
                    overall_health = 'degraded'
                    
            except Exception as e:
                checks_result[check_name] = {
                    'status': 'error',
                    'message': str(e)
                }
                overall_health = 'unhealthy'
        
        return {
            'overall_status': overall_health,
            'checks': checks_result,
            'timestamp': datetime.now()
        }
```

### Service Availability
```python
class AvailabilityMonitor:
    """
    Track service availability and uptime
    """
    
    def __init__(self):
        self.uptime_start = datetime.now()
        self.downtime_events = []
        self.availability_target = 0.999  # 99.9% target
    
    def calculate_availability(self, period_days=30):
        """
        Calculate service availability percentage
        """
        period_start = datetime.now() - timedelta(days=period_days)
        total_seconds = period_days * 24 * 3600
        
        downtime_seconds = 0
        for event in self.downtime_events:
            if event['start'] >= period_start:
                duration = (event['end'] - event['start']).total_seconds()
                downtime_seconds += duration
        
        availability = (total_seconds - downtime_seconds) / total_seconds
        
        return {
            'availability_percentage': availability * 100,
            'downtime_minutes': downtime_seconds / 60,
            'meets_sla': availability >= self.availability_target,
            'incident_count': len(self.downtime_events)
        }
```

## 🚨 Alert System

### Alert Configuration
```python
class AlertManager:
    """
    Manage monitoring alerts and notifications
    """
    
    ALERT_RULES = {
        'high_error_rate': {
            'condition': lambda m: m['error_rate'] > 0.05,
            'severity': 'critical',
            'message': 'Error rate exceeds 5%',
            'cooldown': 300  # 5 minutes
        },
        'slow_response': {
            'condition': lambda m: m['p95_response_time'] > 2000,
            'severity': 'warning',
            'message': 'P95 response time > 2 seconds',
            'cooldown': 600
        },
        'budget_threshold': {
            'condition': lambda m: m['budget_used_percent'] > 80,
            'severity': 'warning',
            'message': 'Budget usage exceeds 80%',
            'cooldown': 3600
        },
        'cache_miss_rate': {
            'condition': lambda m: m['cache_hit_rate'] < 0.3,
            'severity': 'info',
            'message': 'Cache hit rate below 30%',
            'cooldown': 1800
        },
        'api_failure': {
            'condition': lambda m: m['api_success_rate'] < 0.95,
            'severity': 'critical',
            'message': 'API success rate below 95%',
            'cooldown': 300
        }
    }
    
    def check_alerts(self, metrics):
        """
        Check metrics against alert rules
        """
        triggered_alerts = []
        
        for alert_name, rule in self.ALERT_RULES.items():
            if self.should_check_alert(alert_name):
                if rule['condition'](metrics):
                    alert = self.create_alert(alert_name, rule, metrics)
                    triggered_alerts.append(alert)
                    self.send_notification(alert)
        
        return triggered_alerts
```

### Notification Channels
```python
class NotificationChannels:
    """
    Multi-channel alert notification system
    """
    
    def __init__(self):
        self.channels = {
            'email': EmailNotifier(),
            'slack': SlackNotifier(),
            'webhook': WebhookNotifier(),
            'dashboard': DashboardNotifier()
        }
    
    def send_alert(self, alert, channels=['email', 'dashboard']):
        """
        Send alert through specified channels
        """
        for channel_name in channels:
            if channel_name in self.channels:
                try:
                    self.channels[channel_name].send(alert)
                except Exception as e:
                    logger.error(f"Failed to send alert via {channel_name}: {e}")
```

## 📊 Dashboard Metrics

### Real-time Dashboard
```python
class MonitoringDashboard:
    """
    Real-time monitoring dashboard data
    """
    
    def get_dashboard_data(self):
        """
        Compile dashboard display data
        """
        return {
            'system_status': {
                'health': self.health_monitor.get_current_status(),
                'uptime': self.calculate_uptime(),
                'active_users': self.get_active_users(),
                'queue_depth': self.get_queue_depth()
            },
            'performance': {
                'avg_response_time': self.get_avg_response_time(),
                'requests_per_minute': self.get_rpm(),
                'error_rate': self.get_error_rate(),
                'cache_hit_rate': self.get_cache_hit_rate()
            },
            'business_metrics': {
                'comments_analyzed': self.get_comments_analyzed_today(),
                'avg_confidence': self.get_avg_confidence(),
                'sentiment_distribution': self.get_sentiment_distribution(),
                'top_themes': self.get_top_themes()
            },
            'cost_metrics': {
                'today_cost': self.get_today_cost(),
                'month_to_date': self.get_mtd_cost(),
                'budget_remaining': self.get_budget_remaining(),
                'cost_per_comment': self.get_avg_cost_per_comment()
            }
        }
```

## 📈 Analytics and Reporting

### Performance Analytics
```python
class PerformanceAnalytics:
    """
    Analyze performance trends and patterns
    """
    
    def analyze_performance_trends(self, period_days=7):
        """
        Analyze performance trends over time
        """
        metrics_history = self.get_metrics_history(period_days)
        
        analysis = {
            'response_time_trend': self.calculate_trend(
                metrics_history, 'response_time'
            ),
            'throughput_trend': self.calculate_trend(
                metrics_history, 'throughput'
            ),
            'error_rate_trend': self.calculate_trend(
                metrics_history, 'error_rate'
            ),
            'peak_usage_times': self.identify_peak_times(metrics_history),
            'performance_anomalies': self.detect_anomalies(metrics_history),
            'optimization_opportunities': self.identify_optimizations(metrics_history)
        }
        
        return analysis
```

### Quality Metrics
```python
class QualityMetrics:
    """
    Monitor analysis quality metrics
    """
    
    def track_quality_metrics(self, analysis_results):
        """
        Track quality of analysis results
        """
        metrics = {
            'avg_confidence': np.mean([r['confidence'] for r in analysis_results]),
            'low_confidence_rate': sum(1 for r in analysis_results if r['confidence'] < 0.7) / len(analysis_results),
            'complete_analysis_rate': sum(1 for r in analysis_results if r['complete']) / len(analysis_results),
            'processing_errors': sum(1 for r in analysis_results if r.get('error')),
            'quality_score': self.calculate_quality_score(analysis_results)
        }
        
        return metrics
```

## 🔧 Monitoring Configuration

### Configuration Settings
```python
MONITORING_CONFIG = {
    'enabled': True,
    'collection_interval': 10,  # seconds
    'retention_days': 30,
    'metrics': {
        'performance': True,
        'usage': True,
        'business': True,
        'system': True
    },
    'alerts': {
        'enabled': True,
        'channels': ['email', 'dashboard'],
        'severity_levels': ['critical', 'warning'],
        'rate_limiting': True
    },
    'dashboard': {
        'refresh_interval': 5,  # seconds
        'max_data_points': 1000,
        'enable_historical': True
    },
    'storage': {
        'backend': 'sqlite',  # or 'postgresql', 'influxdb'
        'path': 'data/monitoring/metrics.db',
        'compression': True
    }
}
```

## 📊 Visualization Integration

### Metrics Export
```python
class MetricsExporter:
    """
    Export metrics for visualization tools
    """
    
    def export_prometheus_metrics(self):
        """
        Export metrics in Prometheus format
        """
        metrics = []
        
        # System metrics
        metrics.append(f'system_uptime_seconds {self.get_uptime_seconds()}')
        metrics.append(f'http_requests_total {self.get_total_requests()}')
        metrics.append(f'http_request_duration_seconds {self.get_avg_duration()}')
        metrics.append(f'cache_hit_ratio {self.get_cache_hit_ratio()}')
        
        # Business metrics
        metrics.append(f'comments_analyzed_total {self.get_total_comments()}')
        metrics.append(f'analysis_confidence_average {self.get_avg_confidence()}')
        
        # Cost metrics
        metrics.append(f'api_cost_dollars_total {self.get_total_cost()}')
        metrics.append(f'cost_per_comment_dollars {self.get_cost_per_comment()}')
        
        return '\n'.join(metrics)
```

## 🔍 Troubleshooting with Monitoring

### Debug Metrics
```python
class DebugMonitoring:
    """
    Enhanced monitoring for debugging
    """
    
    def enable_debug_monitoring(self):
        """
        Enable detailed debug monitoring
        """
        self.config['collection_interval'] = 1  # More frequent
        self.config['log_level'] = 'DEBUG'
        self.config['capture_stack_traces'] = True
        self.config['detailed_timings'] = True
        
    def capture_debug_snapshot(self):
        """
        Capture comprehensive debug information
        """
        return {
            'timestamp': datetime.now(),
            'system_state': self.get_system_state(),
            'active_requests': self.get_active_requests(),
            'memory_dump': self.get_memory_analysis(),
            'thread_dump': self.get_thread_dump(),
            'cache_state': self.get_cache_state(),
            'error_log': self.get_recent_errors()
        }
```

## 📈 Capacity Planning

### Resource Utilization
```python
def analyze_capacity_needs(historical_data):
    """
    Analyze capacity requirements based on usage
    """
    analysis = {
        'current_utilization': {
            'cpu': calculate_avg_cpu_usage(historical_data),
            'memory': calculate_avg_memory_usage(historical_data),
            'api_quota': calculate_api_quota_usage(historical_data)
        },
        'growth_projection': project_growth(historical_data),
        'capacity_recommendations': {
            'immediate_needs': identify_immediate_needs(historical_data),
            'future_requirements': project_future_requirements(historical_data),
            'cost_implications': calculate_scaling_costs(historical_data)
        }
    }
    
    return analysis
```

## 🔗 Related Documentation
- [Cache Management](cache-management.md) - Cache monitoring integration
- [API Optimization](optimization.md) - Performance optimization
- [System Architecture](../infrastructure/architecture.md) - System design
- [Troubleshooting](../../deployment/troubleshooting.md) - Using monitoring for debugging