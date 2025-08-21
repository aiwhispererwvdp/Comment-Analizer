# Data Models Documentation

## Overview

This document defines all data models used in the Personal Paraguay Fiber Comments Analysis system, including input models, output models, and internal data structures. Each model includes JSON schema definitions, Python classes, validation rules, and usage examples.

## 📊 Core Data Models

### Comment Model
```python
@dataclass
class Comment:
    """
    Individual customer comment data structure
    """
    id: str                           # Unique identifier
    text: str                         # Original comment text
    timestamp: Optional[datetime]     # When comment was made
    source: Optional[str]             # Source system/channel
    customer_id: Optional[str]        # Customer identifier (anonymized)
    metadata: Dict[str, Any]          # Additional metadata
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'source': self.source,
            'customer_id': self.customer_id,
            'metadata': self.metadata
        }
```

### Analysis Request Model
```python
@dataclass
class AnalysisRequest:
    """
    Request model for comment analysis
    """
    comments: List[Comment]           # Comments to analyze
    analysis_config: AnalysisConfig   # Analysis configuration
    batch_config: Optional[BatchConfig] # Batch processing settings
    user_session: str                 # User session identifier
    request_id: str                   # Unique request ID
    timestamp: datetime               # Request timestamp
    
    class AnalysisConfig:
        analysis_depth: str           # 'basic' | 'standard' | 'comprehensive'
        include_sentiment: bool = True
        include_themes: bool = True
        include_emotions: bool = True
        include_translation: bool = True
        language_preference: str = 'auto'
        confidence_threshold: float = 0.7
    
    class BatchConfig:
        batch_size: int = 100
        parallel_processing: bool = True
        max_concurrent: int = 10
        timeout_seconds: int = 300
```

### Analysis Result Model
```python
@dataclass
class AnalysisResult:
    """
    Complete analysis result for a comment
    """
    comment_id: str                   # Reference to original comment
    original_text: str                # Original comment text
    processed_text: Optional[str]     # Processed/translated text
    language: LanguageResult          # Language detection result
    sentiment: SentimentResult        # Sentiment analysis result
    themes: List[ThemeResult]         # Detected themes
    emotions: EmotionResult           # Emotion analysis result
    quality_metrics: QualityMetrics   # Analysis quality indicators
    processing_metadata: ProcessingMetadata
    
    @dataclass
    class LanguageResult:
        detected_language: str        # 'spanish' | 'guarani' | 'mixed'
        confidence: float             # 0.0-1.0
        dialect: Optional[str]        # Regional dialect
        requires_translation: bool
        translation: Optional[TranslationResult]
    
    @dataclass
    class SentimentResult:
        classification: str           # 'positive' | 'negative' | 'neutral' | 'mixed'
        score: float                  # -1.0 to 1.0
        confidence: float             # 0.0-1.0
        intensity: str                # 'low' | 'medium' | 'high'
        aspects: List[AspectSentiment]
    
    @dataclass
    class ThemeResult:
        theme_name: str
        category: str                 # Business category
        confidence: float
        keywords: List[str]
        relevance_score: float
        business_impact: str          # 'low' | 'medium' | 'high' | 'critical'
    
    @dataclass
    class EmotionResult:
        primary_emotion: str
        emotion_scores: Dict[str, float]  # {'joy': 0.7, 'anger': 0.2, ...}
        intensity: float
        behavioral_prediction: Optional[str]
        confidence: float
```

## 📈 Business Intelligence Models

### Aggregated Analysis Model
```python
@dataclass
class AggregatedAnalysis:
    """
    Aggregated analysis results for multiple comments
    """
    total_comments: int
    analysis_period: DateRange
    overall_sentiment: OverallSentiment
    theme_distribution: ThemeDistribution
    emotion_summary: EmotionSummary
    language_statistics: LanguageStatistics
    business_insights: BusinessInsights
    quality_metrics: AggregatedQualityMetrics
    
    @dataclass
    class OverallSentiment:
        average_score: float
        distribution: Dict[str, float]  # {'positive': 0.6, 'negative': 0.3, 'neutral': 0.1}
        trend: str                      # 'improving' | 'stable' | 'declining'
        confidence: float
    
    @dataclass
    class ThemeDistribution:
        themes: List[ThemeStatistics]
        top_themes: List[str]
        emerging_themes: List[str]
        declining_themes: List[str]
    
    @dataclass
    class BusinessInsights:
        key_findings: List[str]
        recommendations: List[Recommendation]
        risk_indicators: List[RiskIndicator]
        opportunities: List[Opportunity]
        priority_actions: List[Action]
```

### Recommendation Model
```python
@dataclass
class Recommendation:
    """
    Business recommendation based on analysis
    """
    id: str
    title: str
    description: str
    category: str                     # 'service' | 'technical' | 'commercial' | 'operational'
    priority: str                     # 'low' | 'medium' | 'high' | 'critical'
    impact: ImpactAssessment
    supporting_data: SupportingData
    suggested_actions: List[str]
    estimated_effort: str             # 'low' | 'medium' | 'high'
    expected_outcome: str
    
    @dataclass
    class ImpactAssessment:
        affected_customers: int
        satisfaction_improvement: float
        churn_reduction: float
        revenue_impact: Optional[float]
    
    @dataclass
    class SupportingData:
        comment_count: int
        sentiment_score: float
        theme_frequency: float
        confidence: float
```

## 🔄 Processing Models

### Batch Processing Model
```python
@dataclass
class BatchJob:
    """
    Batch processing job model
    """
    job_id: str
    status: str                       # 'pending' | 'running' | 'completed' | 'failed'
    total_items: int
    processed_items: int
    failed_items: int
    start_time: datetime
    end_time: Optional[datetime]
    estimated_completion: Optional[datetime]
    current_batch: int
    total_batches: int
    errors: List[ProcessingError]
    results: Optional[BatchResults]
    
    @dataclass
    class ProcessingError:
        item_id: str
        error_type: str
        error_message: str
        timestamp: datetime
        recoverable: bool
    
    @dataclass
    class BatchResults:
        successful: List[str]
        failed: List[str]
        partial: List[str]
        statistics: BatchStatistics
```

### Cache Entry Model
```python
@dataclass
class CacheEntry:
    """
    Cache entry data model
    """
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    access_count: int
    last_accessed: datetime
    size_bytes: int
    compression: bool
    encryption: bool
    metadata: Dict[str, Any]
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return datetime.now() > self.expires_at
    
    def is_stale(self, staleness_seconds: int = 3600) -> bool:
        """Check if cache entry is stale"""
        age = (datetime.now() - self.created_at).total_seconds()
        return age > staleness_seconds
```

## 📁 File Upload Models

### Upload Request Model
```python
@dataclass
class FileUploadRequest:
    """
    File upload request model
    """
    file_id: str
    filename: str
    file_type: str                    # 'xlsx' | 'csv' | 'json' | 'txt'
    file_size: int
    mime_type: str
    upload_timestamp: datetime
    user_session: str
    validation_status: ValidationStatus
    processing_status: ProcessingStatus
    
    @dataclass
    class ValidationStatus:
        is_valid: bool
        errors: List[str]
        warnings: List[str]
        file_structure: FileStructure
    
    @dataclass
    class FileStructure:
        rows: int
        columns: int
        detected_comment_column: Optional[str]
        detected_date_column: Optional[str]
        column_types: Dict[str, str]
```

### Data Import Model
```python
@dataclass
class DataImport:
    """
    Imported data model
    """
    import_id: str
    source_file: str
    import_timestamp: datetime
    total_records: int
    valid_records: int
    invalid_records: int
    skipped_records: int
    comments: List[Comment]
    validation_report: ValidationReport
    import_metadata: Dict[str, Any]
    
    @dataclass
    class ValidationReport:
        total_validations: int
        passed_validations: int
        failed_validations: int
        validation_details: List[ValidationDetail]
    
    @dataclass
    class ValidationDetail:
        rule_name: str
        rule_type: str
        passed: bool
        message: str
        affected_records: List[int]
```

## 📊 Export Models

### Export Request Model
```python
@dataclass
class ExportRequest:
    """
    Data export request model
    """
    export_id: str
    format: str                       # 'excel' | 'csv' | 'json' | 'pdf'
    include_sections: List[str]
    filters: Optional[ExportFilters]
    customization: Optional[ExportCustomization]
    user_session: str
    request_timestamp: datetime
    
    @dataclass
    class ExportFilters:
        date_range: Optional[DateRange]
        sentiment_filter: Optional[List[str]]
        theme_filter: Optional[List[str]]
        language_filter: Optional[List[str]]
        confidence_threshold: Optional[float]
    
    @dataclass
    class ExportCustomization:
        include_charts: bool = True
        include_summary: bool = True
        include_raw_data: bool = True
        company_branding: bool = False
        custom_header: Optional[str]
        custom_footer: Optional[str]
```

### Export Result Model
```python
@dataclass
class ExportResult:
    """
    Export operation result
    """
    export_id: str
    status: str                       # 'success' | 'partial' | 'failed'
    file_path: str
    file_size: int
    format: str
    created_at: datetime
    download_url: Optional[str]
    expiry_time: Optional[datetime]
    statistics: ExportStatistics
    
    @dataclass
    class ExportStatistics:
        total_records: int
        exported_records: int
        file_sections: List[str]
        generation_time_seconds: float
```

## 🔐 Security Models

### User Session Model
```python
@dataclass
class UserSession:
    """
    User session data model
    """
    session_id: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    user_identifier: Optional[str]
    permissions: List[str]
    rate_limits: RateLimits
    usage_statistics: UsageStatistics
    
    @dataclass
    class RateLimits:
        requests_per_minute: int
        requests_per_hour: int
        max_file_size_mb: int
        max_comments_per_batch: int
    
    @dataclass
    class UsageStatistics:
        total_requests: int
        total_comments_analyzed: int
        api_calls_made: int
        total_cost_usd: float
        last_request_time: Optional[datetime]
```

### API Key Model
```python
@dataclass
class APIKeyConfig:
    """
    API key configuration model
    """
    provider: str                     # 'openai' | 'azure' | 'google'
    key_id: str
    encrypted_key: str
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime]
    usage_limits: UsageLimits
    permissions: List[str]
    
    @dataclass
    class UsageLimits:
        daily_request_limit: Optional[int]
        monthly_request_limit: Optional[int]
        cost_limit_usd: Optional[float]
        rate_limit_rpm: Optional[int]
```

## 📈 Monitoring Models

### Performance Metrics Model
```python
@dataclass
class PerformanceMetrics:
    """
    System performance metrics
    """
    timestamp: datetime
    response_time_ms: float
    processing_time_ms: float
    api_latency_ms: float
    cache_hit_rate: float
    memory_usage_mb: float
    cpu_usage_percent: float
    active_sessions: int
    queue_size: int
    error_rate: float
    
    def to_prometheus_metrics(self) -> str:
        """Convert to Prometheus format"""
        return f"""
        response_time_milliseconds {self.response_time_ms}
        processing_time_milliseconds {self.processing_time_ms}
        cache_hit_rate_ratio {self.cache_hit_rate}
        memory_usage_megabytes {self.memory_usage_mb}
        error_rate_ratio {self.error_rate}
        """
```

### Cost Tracking Model
```python
@dataclass
class CostTracking:
    """
    API usage cost tracking
    """
    period: DateRange
    provider: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    tokens_used: int
    cost_usd: float
    cost_breakdown: Dict[str, float]
    budget_remaining: Optional[float]
    budget_alert_triggered: bool
    
    def calculate_average_cost(self) -> float:
        """Calculate average cost per request"""
        if self.successful_requests == 0:
            return 0.0
        return self.cost_usd / self.successful_requests
```

## 🔄 Response Models

### Success Response Model
```python
@dataclass
class SuccessResponse:
    """
    Successful API response model
    """
    status: str = 'success'
    code: int = 200
    data: Any
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_json(self) -> str:
        """Convert to JSON response"""
        return json.dumps({
            'status': self.status,
            'code': self.code,
            'data': self.data,
            'message': self.message,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        })
```

### Error Response Model
```python
@dataclass
class ErrorResponse:
    """
    Error response model
    """
    status: str = 'error'
    code: int
    error_type: str
    message: str
    details: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_json(self) -> str:
        """Convert to JSON response"""
        return json.dumps({
            'status': self.status,
            'code': self.code,
            'error': {
                'type': self.error_type,
                'message': self.message,
                'details': self.details
            },
            'trace_id': self.trace_id,
            'timestamp': self.timestamp.isoformat()
        })
```

## 🔗 Related Documentation
- [API Endpoints](endpoints.md) - REST API endpoints
- [Error Codes](error-codes.md) - Error code reference
- [OpenAI Integration](../backend/api/openai-integration.md) - AI integration