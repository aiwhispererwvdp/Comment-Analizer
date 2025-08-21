# API Endpoints Documentation

## Overview

The Personal Paraguay Fiber Comments Analysis system currently operates as a Streamlit application with internal APIs. This document outlines both the current internal API structure and the planned REST API endpoints for future implementation.

## Current Internal APIs

### 1. Analysis Service API

The system uses internal service classes that function as APIs for various analysis operations.

#### RobustAPIClient

**Purpose:** Manages all OpenAI API interactions with robust error handling, timeouts, and circuit breaker pattern.

**Location:** `src/api/api_client.py`

**Key Methods:**

##### chat_completion()
```python
def chat_completion(messages: List[Dict], model: str = "gpt-4o-mini", **kwargs) -> Any
```

**Parameters:**
- `messages` (List[Dict]): Chat messages in OpenAI format
- `model` (str): Model to use (default: "gpt-4o-mini")
- `**kwargs`: Additional OpenAI API parameters

**Returns:**
- OpenAI completion response object

**Error Handling:**
- `CustomAPITimeoutError`: When API call exceeds timeout
- `CustomAPIConnectionError`: When connection fails
- `APIRateLimitError`: When rate limit is exceeded
- `AnalysisProcessingError`: For other API errors

**Example:**
```python
client = create_robust_client(api_key)
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a sentiment analyzer"},
        {"role": "user", "content": "Analyze: 'Great service!'"}
    ],
    temperature=0.3,
    max_tokens=100
)
```

**Rate Limiting:**
- Max retries: 5
- Base delay: 1 second
- Max delay: 60 seconds
- Backoff factor: 2
- Rate limit delay: 60 seconds

#### ConnectionHealthChecker

**Purpose:** Monitors API connection health status.

##### check_health()
```python
def check_health() -> bool
```

**Returns:**
- `True` if API is accessible
- `False` if API connection fails

**Health Check Response:**
```json
{
    "is_healthy": true,
    "last_check": 1705123456.789,
    "time_since_check": 30.5
}
```

---

## Planned REST API Endpoints

### Base URL
```
https://api.paraguay-fiber-analysis.com/v1
```

### Authentication
All API requests require authentication via API key in the header:
```
X-API-Key: your_api_key_here
```

---

### 1. Analysis Endpoints

#### POST /api/analyze
**Description:** Perform comprehensive comment analysis

**Request:**
```http
POST /api/analyze
Content-Type: application/json
X-API-Key: your_api_key

{
    "comments": [
        {
            "id": "001",
            "text": "Excelente servicio de fibra óptica",
            "date": "2024-01-15",
            "metadata": {
                "customer_id": "C123",
                "location": "Asunción"
            }
        }
    ],
    "analysis_types": ["sentiment", "emotion", "theme"],
    "language": "auto",
    "batch_size": 100
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "analysis_id": "a123-b456-c789",
    "timestamp": "2024-01-15T10:30:00Z",
    "results": {
        "sentiment": {
            "positive": 0.85,
            "neutral": 0.10,
            "negative": 0.05,
            "confidence": 0.92
        },
        "emotions": {
            "joy": 0.7,
            "satisfaction": 0.8,
            "anger": 0.0,
            "frustration": 0.0
        },
        "themes": [
            {"name": "service_quality", "score": 0.9},
            {"name": "internet_speed", "score": 0.7}
        ]
    },
    "metadata": {
        "processing_time_ms": 1250,
        "tokens_used": 450,
        "cost_usd": 0.0012
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Missing required field: comments",
        "details": {
            "field": "comments",
            "requirement": "array of comment objects"
        }
    }
}
```

---

#### POST /api/sentiment/basic
**Description:** Basic sentiment analysis without AI

**Request:**
```json
{
    "text": "El servicio es excelente",
    "language": "es"
}
```

**Response:**
```json
{
    "sentiment": "positive",
    "score": 0.85,
    "confidence": 0.78,
    "method": "rule_based"
}
```

---

#### POST /api/sentiment/advanced
**Description:** AI-powered sentiment analysis

**Request:**
```json
{
    "text": "El servicio es excelente pero a veces falla",
    "context": "customer_feedback",
    "detailed": true
}
```

**Response:**
```json
{
    "sentiment": "mixed",
    "positive_score": 0.6,
    "negative_score": 0.3,
    "neutral_score": 0.1,
    "confidence": 0.88,
    "aspects": {
        "service_quality": "positive",
        "reliability": "negative"
    },
    "explanation": "Positive sentiment about service quality, concerns about reliability"
}
```

---

#### POST /api/sentiment/batch
**Description:** Batch sentiment analysis

**Request:**
```json
{
    "comments": ["text1", "text2", "text3"],
    "parallel": true,
    "max_batch_size": 100
}
```

**Response:**
```json
{
    "batch_id": "batch_123",
    "status": "processing",
    "total": 3,
    "processed": 0,
    "eta_seconds": 5
}
```

---

### 2. Theme Detection Endpoints

#### POST /api/themes/extract
**Description:** Extract themes from comments

**Request:**
```json
{
    "comments": ["..."],
    "min_frequency": 2,
    "max_themes": 10,
    "language": "es"
}
```

**Response:**
```json
{
    "themes": [
        {
            "id": "t1",
            "name": "internet_speed",
            "frequency": 45,
            "percentage": 0.23,
            "keywords": ["velocidad", "rápido", "lento", "mbps"],
            "sentiment": "positive"
        }
    ],
    "total_comments": 200,
    "processing_time_ms": 850
}
```

---

#### POST /api/themes/analyze
**Description:** Detailed theme analysis

**Request:**
```json
{
    "theme_id": "internet_speed",
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-01-31"
    }
}
```

**Response:**
```json
{
    "theme": "internet_speed",
    "trend": "improving",
    "sentiment_over_time": [...],
    "related_themes": ["service_quality", "technical_support"],
    "recommendations": [
        "Monitor peak hour performance",
        "Investigate specific geographic areas with complaints"
    ]
}
```

---

### 3. Utility Endpoints

#### GET /api/health
**Description:** System health check

**Response (200 OK):**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "services": {
        "api": "operational",
        "database": "operational",
        "openai": "operational",
        "cache": "operational"
    },
    "version": "2.0.0"
}
```

---

#### GET /api/status
**Description:** Detailed system status

**Response:**
```json
{
    "uptime_seconds": 86400,
    "requests_today": 1520,
    "active_sessions": 12,
    "queue_length": 3,
    "average_response_time_ms": 250,
    "error_rate": 0.002
}
```

---

#### GET /api/metrics
**Description:** Usage metrics and statistics

**Request Parameters:**
- `period`: "hour", "day", "week", "month"
- `metric_type`: "usage", "performance", "errors"

**Response:**
```json
{
    "period": "day",
    "metrics": {
        "total_requests": 5420,
        "unique_users": 85,
        "total_comments_processed": 12500,
        "api_calls": {
            "openai": 450,
            "internal": 4970
        },
        "costs": {
            "openai_usd": 12.50,
            "compute_hours": 2.5
        },
        "performance": {
            "avg_response_ms": 245,
            "p95_response_ms": 890,
            "p99_response_ms": 1250
        }
    }
}
```

---

### 4. File Upload Endpoints (Future)

#### POST /api/upload
**Description:** Upload file for analysis

**Request:**
```http
POST /api/upload
Content-Type: multipart/form-data

file: [binary data]
type: "excel"
```

**Response:**
```json
{
    "file_id": "f123-456",
    "filename": "comments_jan_2024.xlsx",
    "size_bytes": 524288,
    "rows_detected": 1250,
    "status": "ready_for_analysis"
}
```

---

### 5. Export Endpoints (Future)

#### GET /api/export/{analysis_id}
**Description:** Export analysis results

**Request Parameters:**
- `format`: "excel", "csv", "pdf", "json"
- `include`: "summary", "detailed", "visualizations"

**Response:**
```json
{
    "export_url": "https://downloads.example.com/export_123.xlsx",
    "expires_at": "2024-01-16T10:30:00Z",
    "size_bytes": 1048576
}
```

---

## Error Codes

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Too Many Requests
- **500**: Internal Server Error
- **503**: Service Unavailable

### Custom Error Codes
- **1001**: ANALYSIS_FAILED
- **1002**: INVALID_FILE_FORMAT
- **1003**: LANGUAGE_NOT_SUPPORTED
- **1004**: API_KEY_INVALID
- **1005**: QUOTA_EXCEEDED
- **1006**: BATCH_TOO_LARGE
- **1007**: TIMEOUT_ERROR
- **1008**: CONNECTION_ERROR

---

## Rate Limiting

### Default Limits
- **Requests per minute**: 60
- **Requests per hour**: 1000
- **Requests per day**: 10000
- **Max batch size**: 1000 comments
- **Max file size**: 50 MB

### Rate Limit Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705123456
```

### Rate Limit Response (429)
```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Too many requests",
        "retry_after": 60
    }
}
```

---

## Authentication & Security

### API Key Management
1. Generate API key from dashboard
2. Store securely (never in code)
3. Rotate regularly (recommended: 90 days)
4. Use environment variables

### Security Headers
```http
X-API-Key: your_api_key
X-Request-ID: unique_request_id
X-Client-Version: 1.0.0
```

### HTTPS Required
All API calls must use HTTPS. HTTP requests will be rejected.

---

## SDK Examples

### Python
```python
from paraguay_fiber_api import Client

client = Client(api_key="your_api_key")

# Analyze sentiment
result = client.analyze_sentiment("Excelente servicio!")
print(f"Sentiment: {result.sentiment}")

# Batch analysis
results = client.batch_analyze(comments_list)
for r in results:
    print(f"{r.id}: {r.sentiment}")
```

### JavaScript
```javascript
const client = new ParaguayFiberAPI({
    apiKey: 'your_api_key'
});

// Analyze comment
const result = await client.analyze({
    text: 'Excelente servicio!',
    types: ['sentiment', 'emotion']
});

console.log(result.sentiment);
```

### cURL
```bash
curl -X POST https://api.paraguay-fiber-analysis.com/v1/api/analyze \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "comments": [{"text": "Excelente servicio!"}],
    "analysis_types": ["sentiment"]
  }'
```

---

## Webhooks (Future)

### Configuration
```json
{
    "url": "https://your-domain.com/webhook",
    "events": ["analysis.completed", "batch.finished"],
    "secret": "webhook_secret"
}
```

### Webhook Payload
```json
{
    "event": "analysis.completed",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "analysis_id": "a123",
        "status": "success",
        "results_url": "https://api.example.com/results/a123"
    }
}
```

---

## Migration Guide

### From Internal API to REST API
1. Replace direct function calls with HTTP requests
2. Add authentication headers
3. Handle async responses
4. Implement error retry logic
5. Update response parsing

### Backwards Compatibility
- Internal APIs will remain available
- Gradual migration path
- Dual support period: 6 months
- Deprecation notices in advance