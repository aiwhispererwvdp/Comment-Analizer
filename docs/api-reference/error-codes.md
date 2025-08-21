# Error Codes Documentation

## Overview

This document provides a comprehensive guide to all error codes used in the Personal Paraguay Fiber Comments Analysis system. Each error includes the code, description, common causes, resolution steps, and examples.

---

## HTTP Status Codes

### 4xx Client Errors

#### 400 Bad Request
**Description:** The server cannot process the request due to invalid input or malformed data.

**Common Scenarios:**
- Missing required fields
- Invalid data types
- Malformed JSON
- Parameter out of range

**Example Response:**
```json
{
    "error": {
        "code": "BAD_REQUEST",
        "message": "Invalid request format",
        "details": {
            "field": "comments",
            "requirement": "array of comment objects",
            "received": "string"
        },
        "timestamp": "2024-01-15T10:30:00Z",
        "trace_id": "req_123456"
    }
}
```

**Resolution Steps:**
1. Validate request format against API documentation
2. Check required fields are present
3. Verify data types match expected schema
4. Ensure parameter values are within valid ranges

---

#### 401 Unauthorized
**Description:** Authentication is required or has failed.

**Common Scenarios:**
- Missing API key
- Invalid API key
- Expired API key
- Malformed authentication header

**Example Response:**
```json
{
    "error": {
        "code": "UNAUTHORIZED",
        "message": "Invalid or missing API key",
        "details": {
            "auth_method": "api_key",
            "header_name": "X-API-Key"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

**Resolution Steps:**
1. Verify API key is included in request headers
2. Check API key format: `X-API-Key: your_api_key`
3. Ensure API key is valid and not expired
4. Regenerate API key if necessary

---

#### 403 Forbidden
**Description:** The request is valid but access is denied due to insufficient permissions.

**Common Scenarios:**
- Quota exceeded
- Feature not available for current plan
- Rate limit exceeded for premium features
- Restricted geographic access

**Example Response:**
```json
{
    "error": {
        "code": "FORBIDDEN",
        "message": "Quota exceeded for current plan",
        "details": {
            "current_usage": 5000,
            "monthly_limit": 5000,
            "reset_date": "2024-02-01T00:00:00Z",
            "upgrade_url": "https://example.com/upgrade"
        }
    }
}
```

**Resolution Steps:**
1. Check current quota usage
2. Wait for quota reset
3. Upgrade plan if needed
4. Contact support for limit increases

---

#### 404 Not Found
**Description:** The requested resource does not exist.

**Common Scenarios:**
- Invalid analysis ID
- Deleted or expired data
- Incorrect endpoint URL
- File not found

**Example Response:**
```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Analysis not found",
        "details": {
            "analysis_id": "a123-b456",
            "possible_causes": [
                "Analysis ID does not exist",
                "Analysis has expired",
                "Access denied to this analysis"
            ]
        }
    }
}
```

**Resolution Steps:**
1. Verify resource ID is correct
2. Check if resource has expired
3. Confirm access permissions
4. Use list endpoints to find available resources

---

#### 413 Payload Too Large
**Description:** The request payload exceeds size limits.

**Common Scenarios:**
- File upload exceeds 50MB limit
- Batch request too large
- JSON payload too large
- Base64 encoded content exceeds limits

**Example Response:**
```json
{
    "error": {
        "code": "PAYLOAD_TOO_LARGE",
        "message": "File size exceeds maximum limit",
        "details": {
            "file_size_bytes": 56623104,
            "max_size_bytes": 52428800,
            "max_size_mb": 50,
            "suggestions": [
                "Split file into smaller chunks",
                "Compress file before upload",
                "Remove unnecessary columns"
            ]
        }
    }
}
```

**Resolution Steps:**
1. Check file size before upload
2. Split large files into chunks
3. Remove unnecessary data
4. Use file compression

---

#### 429 Too Many Requests
**Description:** Rate limit exceeded for the current time window.

**Common Scenarios:**
- Too many requests per minute
- Burst limit exceeded
- Daily quota reached
- Concurrent request limit exceeded

**Example Response:**
```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Too many requests",
        "details": {
            "limit": 60,
            "window": "per_minute",
            "retry_after": 45,
            "reset_time": "2024-01-15T10:31:00Z"
        }
    }
}
```

**Headers:**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705123456
Retry-After: 45
```

**Resolution Steps:**
1. Implement exponential backoff
2. Respect Retry-After header
3. Reduce request frequency
4. Consider upgrading plan for higher limits

---

### 5xx Server Errors

#### 500 Internal Server Error
**Description:** An unexpected error occurred on the server.

**Common Scenarios:**
- Unhandled exceptions
- Database connection failures
- Third-party service errors
- Configuration issues

**Example Response:**
```json
{
    "error": {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred",
        "details": {
            "error_id": "err_567890",
            "timestamp": "2024-01-15T10:30:00Z",
            "support_contact": "support@example.com"
        }
    }
}
```

**Resolution Steps:**
1. Retry the request after a delay
2. Check system status page
3. Contact support with error_id
4. Implement proper error handling

---

#### 502 Bad Gateway
**Description:** Server received invalid response from upstream service.

**Common Scenarios:**
- OpenAI API failures
- Database connectivity issues
- Microservice communication failures
- Load balancer issues

**Resolution Steps:**
1. Retry request with exponential backoff
2. Check third-party service status
3. Verify network connectivity
4. Contact support if persistent

---

#### 503 Service Unavailable
**Description:** Service is temporarily unavailable due to maintenance or overload.

**Common Scenarios:**
- Scheduled maintenance
- System overload
- Database maintenance
- Service deployment

**Example Response:**
```json
{
    "error": {
        "code": "SERVICE_UNAVAILABLE",
        "message": "Service temporarily unavailable",
        "details": {
            "maintenance_mode": true,
            "estimated_duration": "30 minutes",
            "retry_after": 1800,
            "status_page": "https://status.example.com"
        }
    }
}
```

**Resolution Steps:**
1. Wait and retry later
2. Check status page for updates
3. Implement circuit breaker pattern
4. Use cached results if available

---

#### 504 Gateway Timeout
**Description:** Server did not receive timely response from upstream service.

**Common Scenarios:**
- OpenAI API timeouts
- Large file processing timeouts
- Database query timeouts
- Network latency issues

**Resolution Steps:**
1. Reduce request complexity
2. Split large requests into batches
3. Implement client-side timeouts
4. Retry with exponential backoff

---

## Custom Application Error Codes

### Analysis Errors (1001-1099)

#### 1001 - ANALYSIS_FAILED
**Description:** The analysis process failed to complete successfully.

**Common Causes:**
- Invalid input data format
- Analysis timeout
- Insufficient resources
- Model processing error

**Example:**
```json
{
    "error": {
        "code": 1001,
        "name": "ANALYSIS_FAILED",
        "message": "Sentiment analysis failed to process comment",
        "details": {
            "comment_id": "c123",
            "analysis_type": "sentiment",
            "failure_reason": "Text contains unsupported characters",
            "suggestion": "Remove special characters and try again"
        }
    }
}
```

**Resolution:**
1. Validate input text format
2. Remove unsupported characters
3. Reduce text length if too long
4. Retry with different analysis parameters

---

#### 1002 - INVALID_FILE_FORMAT
**Description:** Uploaded file format is not supported or corrupted.

**Common Causes:**
- Unsupported file extension
- Corrupted file data
- Incorrect MIME type
- Password-protected files

**Supported Formats:**
- Excel: `.xlsx`, `.xls`
- CSV: `.csv`
- JSON: `.json`
- Text: `.txt`

**Example:**
```json
{
    "error": {
        "code": 1002,
        "name": "INVALID_FILE_FORMAT",
        "message": "File format not supported",
        "details": {
            "filename": "data.pdf",
            "detected_type": "application/pdf",
            "supported_types": ["xlsx", "xls", "csv", "json", "txt"],
            "suggestion": "Convert file to Excel or CSV format"
        }
    }
}
```

**Resolution:**
1. Check file extension is supported
2. Ensure file is not corrupted
3. Remove password protection
4. Convert to supported format

---

#### 1003 - LANGUAGE_NOT_SUPPORTED
**Description:** Text language is not supported by the analysis engine.

**Supported Languages:**
- Spanish (es)
- English (en)
- Guaraní (gn)
- Auto-detection (auto)

**Example:**
```json
{
    "error": {
        "code": 1003,
        "name": "LANGUAGE_NOT_SUPPORTED",
        "message": "Detected language not supported",
        "details": {
            "detected_language": "fr",
            "confidence": 0.95,
            "supported_languages": ["es", "en", "gn"],
            "suggestion": "Provide text in Spanish, English, or Guaraní"
        }
    }
}
```

**Resolution:**
1. Check text language
2. Use supported languages only
3. Set language manually if auto-detection fails
4. Translate text to supported language

---

#### 1004 - API_KEY_INVALID
**Description:** Provided API key is invalid, expired, or malformed.

**Common Causes:**
- Incorrect API key format
- Expired key
- Revoked key
- Wrong environment key

**Example:**
```json
{
    "error": {
        "code": 1004,
        "name": "API_KEY_INVALID",
        "message": "OpenAI API key is invalid",
        "details": {
            "key_prefix": "sk-...",
            "validation_error": "Key format invalid",
            "documentation": "https://docs.openai.com/api-reference/authentication"
        }
    }
}
```

**Resolution:**
1. Verify API key format (sk-...)
2. Check key expiration date
3. Regenerate API key if needed
4. Update environment variables

---

#### 1005 - QUOTA_EXCEEDED
**Description:** Usage quota has been exceeded for the current period.

**Quota Types:**
- Daily request limit
- Monthly API calls
- Token usage limit
- File upload limit

**Example:**
```json
{
    "error": {
        "code": 1005,
        "name": "QUOTA_EXCEEDED",
        "message": "Monthly quota exceeded",
        "details": {
            "quota_type": "api_calls",
            "current_usage": 10000,
            "quota_limit": 10000,
            "reset_date": "2024-02-01T00:00:00Z",
            "days_until_reset": 15
        }
    }
}
```

**Resolution:**
1. Wait for quota reset
2. Optimize request efficiency
3. Upgrade to higher tier
4. Use caching to reduce API calls

---

### Data Processing Errors (1100-1199)

#### 1101 - DUPLICATE_DETECTION_FAILED
**Description:** Duplicate detection process encountered an error.

**Example:**
```json
{
    "error": {
        "code": 1101,
        "name": "DUPLICATE_DETECTION_FAILED",
        "message": "Unable to process duplicate detection",
        "details": {
            "total_comments": 5000,
            "processed_comments": 2500,
            "failure_point": "similarity_calculation"
        }
    }
}
```

---

#### 1102 - DATA_VALIDATION_ERROR
**Description:** Input data fails validation requirements.

**Example:**
```json
{
    "error": {
        "code": 1102,
        "name": "DATA_VALIDATION_ERROR",
        "message": "Required column missing",
        "details": {
            "missing_columns": ["Comentario"],
            "available_columns": ["ID", "Fecha", "Usuario"],
            "suggestion": "Ensure 'Comentario' column exists in your data"
        }
    }
}
```

---

#### 1103 - ENCODING_ERROR
**Description:** File encoding cannot be detected or processed.

**Example:**
```json
{
    "error": {
        "code": 1103,
        "name": "ENCODING_ERROR",
        "message": "Unable to decode file content",
        "details": {
            "attempted_encodings": ["utf-8", "latin-1", "cp1252"],
            "suggestion": "Save file with UTF-8 encoding"
        }
    }
}
```

---

### API Connection Errors (1200-1299)

#### 1201 - CONNECTION_TIMEOUT
**Description:** Connection to external service timed out.

**Example:**
```json
{
    "error": {
        "code": 1201,
        "name": "CONNECTION_TIMEOUT",
        "message": "OpenAI API connection timeout",
        "details": {
            "timeout_seconds": 120,
            "retry_count": 3,
            "suggestion": "Reduce batch size or try again later"
        }
    }
}
```

---

#### 1202 - API_RATE_LIMIT
**Description:** External API rate limit exceeded.

**Example:**
```json
{
    "error": {
        "code": 1202,
        "name": "API_RATE_LIMIT",
        "message": "OpenAI API rate limit exceeded",
        "details": {
            "retry_after": 60,
            "limit_type": "requests_per_minute",
            "current_limit": 50
        }
    }
}
```

---

### Export Errors (1300-1399)

#### 1301 - EXPORT_GENERATION_FAILED
**Description:** Failed to generate export file.

**Example:**
```json
{
    "error": {
        "code": 1301,
        "name": "EXPORT_GENERATION_FAILED",
        "message": "Excel export generation failed",
        "details": {
            "export_format": "xlsx",
            "data_size": "large",
            "suggestion": "Try CSV format for large datasets"
        }
    }
}
```

---

## Error Handling Best Practices

### Client-Side Error Handling

#### Exponential Backoff
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            if (error.status === 429 || error.status >= 500) {
                const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
                await new Promise(resolve => setTimeout(resolve, delay));
                continue;
            }
            throw error;
        }
    }
    throw new Error('Max retries exceeded');
}
```

#### Error Classification
```python
def classify_error(error_code):
    if 1001 <= error_code <= 1099:
        return "analysis_error"
    elif 1100 <= error_code <= 1199:
        return "data_processing_error"
    elif 1200 <= error_code <= 1299:
        return "api_connection_error"
    elif 1300 <= error_code <= 1399:
        return "export_error"
    else:
        return "unknown_error"
```

#### Graceful Degradation
```python
try:
    result = analyze_with_ai(comment)
except APIConnectionError:
    # Fallback to rule-based analysis
    result = analyze_with_rules(comment)
except AnalysisProcessingError:
    # Return basic metrics
    result = basic_analysis(comment)
```

---

### Server-Side Error Logging

#### Structured Logging
```python
logger.error(
    "Analysis failed",
    extra={
        "error_code": 1001,
        "comment_id": comment.id,
        "analysis_type": "sentiment",
        "user_session": session_id,
        "request_id": request_id,
        "stack_trace": traceback.format_exc()
    }
)
```

#### Error Metrics
```python
# Track error rates by type
error_counter.labels(
    error_type="analysis_failed",
    component="sentiment_analyzer"
).inc()

# Track error response times
error_histogram.labels(
    error_code="1001"
).observe(processing_time)
```

---

## Error Response Format

### Standard Error Response
All error responses follow this standard format:

```json
{
    "error": {
        "code": "string|number",
        "name": "string",
        "message": "string",
        "details": {
            "field": "string",
            "requirement": "string",
            "suggestion": "string"
        },
        "timestamp": "ISO 8601 datetime",
        "trace_id": "string",
        "documentation_url": "string"
    }
}
```

### Field Descriptions

- **code**: Error identifier (HTTP status or custom code)
- **name**: Human-readable error name
- **message**: Brief error description
- **details**: Additional context and resolution hints
- **timestamp**: When the error occurred
- **trace_id**: Unique identifier for debugging
- **documentation_url**: Link to relevant documentation

---

## Monitoring and Alerting

### Error Rate Thresholds
- **Warning**: Error rate > 5% for 5 minutes
- **Critical**: Error rate > 15% for 2 minutes
- **Emergency**: Error rate > 50% for 1 minute

### Key Metrics to Monitor
1. **Overall error rate**
2. **Error rate by endpoint**
3. **Error rate by error code**
4. **Response time for errors**
5. **Error recovery time**

### Alert Escalation
1. **Level 1**: Automated retry/recovery
2. **Level 2**: Team notification
3. **Level 3**: Manager escalation
4. **Level 4**: Customer communication

---

## Support and Documentation

### Getting Help
- **Documentation**: [API Documentation](./endpoints.md)
- **Support Email**: support@example.com
- **Status Page**: https://status.example.com
- **Community Forum**: https://community.example.com

### Reporting Bugs
When reporting errors, include:
1. Error code and message
2. Request payload (sanitized)
3. Timestamp
4. Steps to reproduce
5. Expected vs actual behavior

### Error Code Quick Reference

| Code | Name | Category | Severity |
|------|------|----------|----------|
| 1001 | ANALYSIS_FAILED | Analysis | High |
| 1002 | INVALID_FILE_FORMAT | Validation | Medium |
| 1003 | LANGUAGE_NOT_SUPPORTED | Analysis | Medium |
| 1004 | API_KEY_INVALID | Auth | High |
| 1005 | QUOTA_EXCEEDED | Rate Limit | Medium |
| 1101 | DUPLICATE_DETECTION_FAILED | Processing | Medium |
| 1102 | DATA_VALIDATION_ERROR | Validation | Medium |
| 1103 | ENCODING_ERROR | Processing | Medium |
| 1201 | CONNECTION_TIMEOUT | Network | High |
| 1202 | API_RATE_LIMIT | Rate Limit | Medium |
| 1301 | EXPORT_GENERATION_FAILED | Export | Medium |