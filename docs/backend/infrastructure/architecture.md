# System Architecture Documentation

This document provides a comprehensive overview of the Personal Paraguay Fiber Comments Analysis System architecture, including component relationships, data flow, and design decisions.

## 🏗️ High-Level Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │   Web UI    │ │   Mobile    │ │    API Interface    │   │
│  │ (Streamlit) │ │  Interface  │ │   (Future)          │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 Application Services Layer                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │  Analysis   │ │ File Upload │ │   Session Management│   │
│  │  Service    │ │   Service   │ │     Service         │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │  Sentiment  │ │   Theme     │ │    Language         │   │
│  │  Analysis   │ │ Detection   │ │   Processing        │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 External Integration Layer                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │   OpenAI    │ │    Cache    │ │     Monitoring      │   │
│  │     API     │ │   Manager   │ │      System         │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Data Storage Layer                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │    File     │ │   Session   │ │       Cache         │   │
│  │   Storage   │ │   Storage   │ │      Storage        │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Frontend Architecture

### Streamlit Application Structure
```
Frontend Components
├── Main Application (main.py)
│   ├── Navigation Handler
│   ├── Session State Manager
│   └── Component Coordinator
├── UI Components
│   ├── File Upload Interface
│   ├── Analysis Dashboard
│   ├── Results Display
│   └── Cost Monitoring
├── Theme System
│   ├── Light Theme
│   ├── Dark Theme
│   ├── Mobile Theme
│   └── Custom Styling
└── Responsive Framework
    ├── Desktop Layout
    ├── Tablet Layout
    └── Mobile Layout
```

### Component Communication Pattern
```python
# Component interaction flow
User Input → UI Component → State Manager → Service Layer → Business Logic
     ↑                                                              ↓
Results Display ← Result Processor ← Response Handler ← External API
```

### State Management
```python
# Streamlit session state structure
st.session_state = {
    'user_data': {
        'uploaded_file': FileObject,
        'analysis_config': AnalysisConfig,
        'budget_settings': BudgetConfig
    },
    'analysis_state': {
        'current_progress': float,
        'batch_status': BatchStatus,
        'results': AnalysisResults
    },
    'ui_state': {
        'current_page': str,
        'theme': str,
        'mobile_mode': bool
    }
}
```

## ⚙️ Backend Services Architecture

### Service Layer Design
```
Service Architecture
├── Analysis Orchestration Service
│   ├── Pipeline Manager
│   ├── Quality Controller
│   ├── Progress Tracker
│   └── Result Aggregator
├── File Processing Service
│   ├── Format Detector
│   ├── Data Validator
│   ├── Content Cleaner
│   └── Structure Analyzer
├── Session Management Service
│   ├── State Persistence
│   ├── User Session Tracking
│   ├── Multi-user Support
│   └── Session Recovery
└── API Integration Service
    ├── Request Manager
    ├── Response Handler
    ├── Error Recovery
    └── Rate Limiter
```

### Service Communication
```python
# Inter-service communication pattern
class ServiceBus:
    """Central communication hub for services"""
    
    def __init__(self):
        self.services = {
            'analysis': AnalysisService(),
            'file_processing': FileProcessingService(),
            'session': SessionService(),
            'api_integration': APIService()
        }
    
    def request(self, service_name, method, *args, **kwargs):
        """Route requests between services"""
        service = self.services[service_name]
        return getattr(service, method)(*args, **kwargs)
```

## 🧠 Business Logic Architecture

### Analysis Engine Design
```
Analysis Engines
├── Sentiment Analysis Engine
│   ├── GPT-4 Analyzer
│   ├── Confidence Calculator
│   ├── Emotion Detector
│   └── Cultural Context Processor
├── Theme Detection Engine
│   ├── Topic Extractor
│   ├── Pattern Recognizer
│   ├── Keyword Analyzer
│   └── Business Categorizer
├── Language Processing Engine
│   ├── Language Detector
│   ├── Translation Service
│   ├── Dialect Processor
│   └── Mixed Language Handler
└── Integration Engine
    ├── Multi-engine Coordinator
    ├── Result Synthesizer
    ├── Quality Validator
    └── Output Formatter
```

### Processing Pipeline
```python
class AnalysisPipeline:
    """Main analysis processing pipeline"""
    
    def execute(self, data, config):
        # 1. Data Preprocessing
        cleaned_data = self.preprocess_data(data)
        
        # 2. Language Processing
        language_results = self.process_languages(cleaned_data)
        
        # 3. Parallel Analysis
        sentiment_results = self.analyze_sentiment(language_results)
        theme_results = self.detect_themes(language_results)
        emotion_results = self.analyze_emotions(language_results)
        
        # 4. Result Integration
        integrated_results = self.integrate_results(
            sentiment_results, theme_results, emotion_results
        )
        
        # 5. Quality Validation
        validated_results = self.validate_quality(integrated_results)
        
        # 6. Business Intelligence
        insights = self.generate_insights(validated_results)
        
        return insights
```

## 🔌 External Integration Architecture

### API Integration Layer
```
External Integrations
├── OpenAI Integration
│   ├── Request Builder
│   ├── Response Parser
│   ├── Error Handler
│   └── Cost Tracker
├── Cache Management
│   ├── Redis-compatible Cache
│   ├── Smart Cache Keys
│   ├── TTL Management
│   └── Cache Invalidation
└── Monitoring Integration
    ├── Performance Metrics
    ├── Error Tracking
    ├── Usage Analytics
    └── Alert System
```

### API Request Flow
```python
class APIRequestFlow:
    """Handles external API request lifecycle"""
    
    async def process_request(self, request_data):
        # 1. Pre-processing
        request = self.build_request(request_data)
        
        # 2. Cache Check
        cached_response = await self.check_cache(request)
        if cached_response:
            return cached_response
        
        # 3. Rate Limiting
        await self.rate_limiter.acquire()
        
        # 4. API Call
        response = await self.make_api_call(request)
        
        # 5. Response Processing
        processed_response = self.process_response(response)
        
        # 6. Cache Storage
        await self.cache_response(request, processed_response)
        
        # 7. Metrics Tracking
        self.track_metrics(request, response)
        
        return processed_response
```

## 📊 Data Architecture

### Data Flow Diagram
```
Data Flow Architecture
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Raw Input  │───▶│  Validation │───▶│  Processing │
│    Data     │    │  & Cleaning │    │  Pipeline   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Export    │◀───│   Result    │◀───│  Analysis   │
│  Generation │    │ Aggregation │    │   Engine    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Data Models
```python
# Core data structures
@dataclass
class CommentData:
    """Individual comment data structure"""
    id: str
    text: str
    language: str
    metadata: Dict[str, Any]
    timestamp: Optional[datetime] = None

@dataclass
class AnalysisResult:
    """Analysis result structure"""
    comment_id: str
    sentiment: SentimentResult
    themes: List[ThemeResult]
    emotions: EmotionResult
    confidence: float
    processing_time: float

@dataclass
class BusinessInsights:
    """Business intelligence structure"""
    overall_sentiment: float
    top_themes: List[str]
    pain_points: List[str]
    recommendations: List[str]
    quality_metrics: QualityMetrics
```

### Storage Strategy
```python
class StorageManager:
    """Manages different storage requirements"""
    
    def __init__(self):
        self.session_storage = SessionStorage()  # Temporary user data
        self.cache_storage = CacheStorage()      # API response cache
        self.file_storage = FileStorage()        # Upload/export files
        self.metrics_storage = MetricsStorage()  # Performance metrics
    
    def store_analysis_session(self, session_data):
        """Store complete analysis session"""
        session_id = self.generate_session_id()
        
        # Store in multiple layers
        self.session_storage.store(session_id, session_data)
        self.metrics_storage.log_session(session_id, session_data.metrics)
        
        return session_id
```

## 🔒 Security Architecture

### Security Layers
```
Security Architecture
├── Input Security Layer
│   ├── File Upload Validation
│   ├── Content Sanitization
│   ├── Size Limit Enforcement
│   └── Malware Scanning
├── Application Security Layer
│   ├── Input Validation
│   ├── Rate Limiting
│   ├── Session Management
│   └── CSRF Protection
├── API Security Layer
│   ├── API Key Management
│   ├── Request Signing
│   ├── Encryption in Transit
│   └── Error Sanitization
└── Data Security Layer
    ├── Data Encryption
    ├── Access Control
    ├── Audit Logging
    └── Secure Deletion
```

### Security Implementation
```python
class SecurityManager:
    """Centralized security management"""
    
    def validate_upload(self, file_data):
        """Multi-layer file validation"""
        # 1. File type validation
        self.validate_file_type(file_data)
        
        # 2. Size validation
        self.validate_file_size(file_data)
        
        # 3. Content validation
        self.validate_file_content(file_data)
        
        # 4. Malware scanning
        self.scan_for_malware(file_data)
        
        return True
    
    def sanitize_input(self, user_input):
        """Input sanitization"""
        # Remove potentially dangerous content
        sanitized = self.remove_html_tags(user_input)
        sanitized = self.escape_special_chars(sanitized)
        sanitized = self.limit_length(sanitized)
        
        return sanitized
```

## ⚡ Performance Architecture

### Performance Optimization Strategy
```
Performance Layers
├── Frontend Optimization
│   ├── Component Lazy Loading
│   ├── State Optimization
│   ├── Rendering Optimization
│   └── Asset Optimization
├── Backend Optimization
│   ├── Async Processing
│   ├── Connection Pooling
│   ├── Memory Management
│   └── CPU Optimization
├── External API Optimization
│   ├── Intelligent Batching
│   ├── Response Caching
│   ├── Request Deduplication
│   └── Parallel Processing
└── Infrastructure Optimization
    ├── Resource Monitoring
    ├── Auto-scaling
    ├── Load Balancing
    └── CDN Integration
```

### Performance Monitoring
```python
class PerformanceMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alerting_system = AlertingSystem()
    
    def monitor_request(self, request_func):
        """Monitor request performance"""
        start_time = time.time()
        memory_before = self.get_memory_usage()
        
        try:
            result = request_func()
            self.record_success(start_time, memory_before)
            return result
        except Exception as e:
            self.record_error(e, start_time, memory_before)
            raise
    
    def record_metrics(self, operation, duration, memory_delta):
        """Record performance metrics"""
        self.metrics_collector.record({
            'operation': operation,
            'duration': duration,
            'memory_delta': memory_delta,
            'timestamp': datetime.now()
        })
```

## 🚀 Scalability Architecture

### Horizontal Scaling Design
```
Scalability Strategy
├── Stateless Application Design
│   ├── No Server-side State
│   ├── Session Storage Separation
│   ├── Configuration Externalization
│   └── Load Balancer Compatibility
├── Service Decomposition
│   ├── Microservice Ready
│   ├── Independent Scaling
│   ├── Service Isolation
│   └── Container Support
├── Data Layer Scaling
│   ├── Read Replicas
│   ├── Cache Layers
│   ├── Data Partitioning
│   └── CDN Integration
└── Resource Optimization
    ├── Auto-scaling Rules
    ├── Resource Monitoring
    ├── Performance Tuning
    └── Cost Optimization
```

### Deployment Architecture
```yaml
# Docker deployment example
version: '3.8'
services:
  app:
    image: paraguay-analysis:latest
    replicas: 3
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    ports:
      - "8501-8503:8501"
  
  cache:
    image: redis:alpine
    volumes:
      - cache_data:/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## 🔮 Future Architecture Enhancements

### Planned Architectural Improvements
1. **Microservices Migration**
   - Service decomposition
   - API gateway implementation
   - Inter-service communication
   - Independent deployment

2. **Real-time Processing**
   - Streaming data processing
   - WebSocket integration
   - Live dashboard updates
   - Real-time analytics

3. **Advanced Analytics**
   - Machine learning pipeline
   - Predictive analytics
   - Automated insights
   - Custom model training

4. **Enterprise Features**
   - Multi-tenant architecture
   - Role-based access control
   - Audit logging
   - Compliance reporting

### Migration Strategy
```python
class ArchitectureMigration:
    """Manages architectural evolution"""
    
    def migrate_to_microservices(self):
        """Gradual migration to microservices"""
        # Phase 1: Service extraction
        self.extract_analysis_service()
        
        # Phase 2: API gateway
        self.implement_api_gateway()
        
        # Phase 3: Service mesh
        self.deploy_service_mesh()
        
        # Phase 4: Advanced features
        self.add_advanced_capabilities()
```

---

## 📚 Related Documentation

- **[Backend Services](../README.md)** - Service layer overview
- **[API Integration](../api/)** - External API documentation
- **[Performance Guide](performance.md)** - Performance optimization
- **[Security Framework](security.md)** - Security implementation
- **[Deployment Guide](../../deployment/)** - Production deployment