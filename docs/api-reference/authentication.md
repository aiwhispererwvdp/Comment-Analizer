# Authentication & Authorization Documentation

## Overview

The Personal Paraguay Fiber Comments Analysis API uses API key authentication for securing access to all endpoints. This document covers authentication methods, authorization levels, security best practices, and troubleshooting.

---

## Authentication Methods

### API Key Authentication

**Primary Method**: HTTP Header-based API Key Authentication

All API requests must include a valid API key in the request headers:

```http
X-API-Key: your_api_key_here
```

#### API Key Format
- **Prefix**: `sk-` (for secret keys)
- **Length**: 64 characters after prefix
- **Characters**: Alphanumeric (a-z, A-Z, 0-9)
- **Example**: `sk-1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`

#### Request Example
```bash
curl -X POST https://api.paraguay-fiber-analysis.com/v1/analyze \
  -H "X-API-Key: sk-your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "comments": [
      {"text": "Excelente servicio"}
    ],
    "analysis_types": ["sentiment"]
  }'
```

---

## Obtaining API Keys

### 1. Dashboard Access
1. Navigate to [Dashboard](https://dashboard.paraguay-fiber-analysis.com)
2. Sign up or log in to your account
3. Go to "API Keys" section
4. Click "Generate New API Key"
5. Copy and securely store your key

### 2. Key Types

#### Development Keys
- **Prefix**: `sk-dev-`
- **Purpose**: Testing and development
- **Rate Limit**: 100 requests/hour
- **Features**: Basic analysis only
- **Cost**: Free

#### Production Keys
- **Prefix**: `sk-prod-`
- **Purpose**: Production use
- **Rate Limit**: Based on plan (1K-10K/hour)
- **Features**: All analysis capabilities
- **Cost**: Usage-based pricing

#### Organization Keys
- **Prefix**: `sk-org-`
- **Purpose**: Team/organization use
- **Rate Limit**: Enterprise limits
- **Features**: All features + team management
- **Cost**: Enterprise pricing

---

## API Key Management

### Security Best Practices

#### 1. Secure Storage
```bash
# ✅ Good: Environment variables
export ANALYSIS_API_KEY="sk-your_key_here"

# ✅ Good: Configuration files (not in version control)
# config.env
ANALYSIS_API_KEY=sk-your_key_here

# ❌ Bad: Hardcoded in source code
api_key = "sk-your_key_here"  # Never do this!
```

#### 2. Key Rotation
- **Recommended Frequency**: Every 90 days
- **Process**:
  1. Generate new API key
  2. Update all applications
  3. Test with new key
  4. Delete old key
  5. Monitor for any issues

#### 3. Access Control
- Use different keys for different environments
- Limit key permissions where possible
- Monitor key usage regularly
- Revoke unused keys immediately

#### 4. Environment Separation
```bash
# Development
ANALYSIS_API_KEY_DEV=sk-dev-abc123...

# Staging  
ANALYSIS_API_KEY_STAGING=sk-prod-def456...

# Production
ANALYSIS_API_KEY_PROD=sk-prod-ghi789...
```

---

## Rate Limiting

### Rate Limit Tiers

#### Free Tier
- **Requests**: 100/hour, 500/day
- **Batch Size**: Max 10 comments
- **Features**: Basic sentiment only
- **Burst**: 10 requests/minute

#### Standard Tier
- **Requests**: 1,000/hour, 5,000/day
- **Batch Size**: Max 100 comments
- **Features**: Sentiment + emotion analysis
- **Burst**: 60 requests/minute

#### Premium Tier
- **Requests**: 10,000/hour, 50,000/day
- **Batch Size**: Max 1,000 comments
- **Features**: All analysis types
- **Burst**: 200 requests/minute

#### Enterprise Tier
- **Requests**: Custom limits
- **Batch Size**: Custom limits
- **Features**: All features + priority support
- **Burst**: Custom limits

### Rate Limit Headers

Every API response includes rate limit information:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705123456
X-RateLimit-Retry-After: 3600
```

**Header Descriptions:**
- `X-RateLimit-Limit`: Total requests allowed in current window
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `X-RateLimit-Retry-After`: Seconds until next request allowed

### Rate Limit Responses

#### 429 Too Many Requests
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 1000,
      "window": "per_hour",
      "reset_time": "2024-01-15T11:00:00Z",
      "retry_after": 300
    }
  }
}
```

### Handling Rate Limits

#### Client-Side Implementation
```python
import time
import requests
from typing import Optional

class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.paraguay-fiber-analysis.com/v1"
        
    def make_request(self, endpoint: str, data: dict, max_retries: int = 3) -> dict:
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        for attempt in range(max_retries):
            response = requests.post(f"{self.base_url}{endpoint}", 
                                   json=data, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                response.raise_for_status()
        
        raise Exception(f"Failed after {max_retries} attempts")
```

#### Exponential Backoff
```javascript
async function makeRequest(url, data, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-API-Key': process.env.ANALYSIS_API_KEY,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                return await response.json();
            }
            
            if (response.status === 429) {
                const retryAfter = response.headers.get('Retry-After');
                const delay = retryAfter ? parseInt(retryAfter) * 1000 : Math.pow(2, attempt) * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
                continue;
            }
            
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        } catch (error) {
            if (attempt === maxRetries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        }
    }
}
```

---

## Security Features

### HTTPS Enforcement
- **All requests must use HTTPS**
- HTTP requests are automatically rejected
- TLS 1.2 or higher required
- Certificate validation enforced

### Request Validation
- API key format validation
- Request signature verification (enterprise)
- IP allowlisting (enterprise)
- User-Agent validation

### Response Security
- No sensitive data in error messages
- Rate limit information included
- Request IDs for debugging
- CORS headers properly configured

---

## Authorization Levels

### Permission Scopes

#### read
- Access to analysis results
- View historical data
- Download exports
- View account information

#### write
- Create new analyses
- Upload files
- Modify settings
- Delete data

#### admin
- Manage API keys
- Access usage metrics
- Configure team settings
- Billing management

### Scope Examples
```json
{
  "api_key": "sk-prod-abc123...",
  "scopes": ["read", "write"],
  "permissions": {
    "analyze": true,
    "export": true,
    "upload": true,
    "admin": false
  }
}
```

---

## CORS Configuration

### Allowed Origins
- `https://dashboard.paraguay-fiber-analysis.com`
- `https://*.paraguay-fiber-analysis.com`
- `http://localhost:*` (development only)

### Allowed Methods
- `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

### Allowed Headers
- `Content-Type`
- `Authorization`
- `X-API-Key`
- `X-Client-Version`
- `X-Request-ID`

### Preflight Requests
```http
OPTIONS /api/v1/analyze
Access-Control-Request-Method: POST
Access-Control-Request-Headers: X-API-Key, Content-Type
```

**Response:**
```http
Access-Control-Allow-Origin: https://dashboard.paraguay-fiber-analysis.com
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: X-API-Key, Content-Type
Access-Control-Max-Age: 86400
```

---

## Error Handling

### Authentication Errors

#### Invalid API Key
```json
{
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid",
    "details": {
      "key_prefix": "sk-invalid-...",
      "suggestion": "Verify your API key in the dashboard"
    }
  }
}
```

#### Expired API Key
```json
{
  "error": {
    "code": "API_KEY_EXPIRED",
    "message": "API key has expired",
    "details": {
      "expired_at": "2024-01-01T00:00:00Z",
      "suggestion": "Generate a new API key"
    }
  }
}
```

#### Missing API Key
```json
{
  "error": {
    "code": "MISSING_API_KEY",
    "message": "API key is required",
    "details": {
      "header_name": "X-API-Key",
      "suggestion": "Include your API key in the X-API-Key header"
    }
  }
}
```

### Authorization Errors

#### Insufficient Permissions
```json
{
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "Your API key does not have permission for this action",
    "details": {
      "required_scope": "write",
      "current_scopes": ["read"],
      "suggestion": "Upgrade your plan or use a key with write permissions"
    }
  }
}
```

#### Account Suspended
```json
{
  "error": {
    "code": "ACCOUNT_SUSPENDED",
    "message": "Your account has been suspended",
    "details": {
      "reason": "payment_failure",
      "contact": "billing@paraguay-fiber-analysis.com"
    }
  }
}
```

---

## Security Best Practices

### For Developers

#### 1. Environment Variables
```bash
# .env file (add to .gitignore)
ANALYSIS_API_KEY=sk-your_key_here
ANALYSIS_BASE_URL=https://api.paraguay-fiber-analysis.com/v1
```

#### 2. Configuration Management
```python
import os
from typing import Optional

class Config:
    def __init__(self):
        self.api_key: Optional[str] = os.getenv('ANALYSIS_API_KEY')
        self.base_url: str = os.getenv('ANALYSIS_BASE_URL', 'https://api.paraguay-fiber-analysis.com/v1')
        
        if not self.api_key:
            raise ValueError("ANALYSIS_API_KEY environment variable is required")
            
        if not self.api_key.startswith('sk-'):
            raise ValueError("Invalid API key format")
```

#### 3. Error Handling
```python
class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class AuthorizationError(Exception):
    """Raised when authorization fails"""
    pass

def handle_auth_error(response):
    if response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    elif response.status_code == 403:
        raise AuthorizationError("Insufficient permissions")
```

#### 4. Logging Security
```python
import logging

# ✅ Good: Log without sensitive data
logger.info(f"API request failed", extra={
    "endpoint": "/analyze",
    "status_code": 401,
    "key_prefix": api_key[:8] + "..."  # Only log prefix
})

# ❌ Bad: Log full API key
logger.error(f"Auth failed with key: {api_key}")  # Never do this!
```

### For Organizations

#### 1. Key Management Policy
- Rotate keys every 90 days
- Use different keys per environment
- Implement key approval process
- Monitor key usage patterns
- Revoke keys when employees leave

#### 2. Access Control
- Implement least privilege principle
- Use role-based access control
- Regular access reviews
- Audit API key usage
- Monitor for anomalous activity

#### 3. Incident Response
- Immediate key revocation process
- Incident documentation
- Post-incident key rotation
- Security team notification
- Customer communication plan

---

## Monitoring & Auditing

### Usage Monitoring
```bash
# Get usage metrics
curl -X GET "https://api.paraguay-fiber-analysis.com/v1/metrics?period=day" \
  -H "X-API-Key: sk-your_key_here"
```

### Audit Logs
```json
{
  "events": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "event_type": "api_key_created",
      "user_id": "user_123",
      "api_key_id": "key_456",
      "ip_address": "192.168.1.1",
      "user_agent": "Dashboard/1.0"
    },
    {
      "timestamp": "2024-01-15T10:31:00Z", 
      "event_type": "api_request",
      "api_key_id": "key_456",
      "endpoint": "/analyze",
      "status_code": 200,
      "response_time_ms": 250
    }
  ]
}
```

### Security Alerts
- Unusual usage patterns
- Failed authentication attempts
- Rate limit violations
- Geographical anomalies
- API key compromises

---

## SDK Integration

### Python SDK
```python
from paraguay_fiber_api import Client

# Initialize client
client = Client(api_key=os.getenv('ANALYSIS_API_KEY'))

# Automatic retry and rate limit handling
try:
    result = client.analyze_sentiment("Excelente servicio!")
    print(f"Sentiment: {result.sentiment}")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
```

### JavaScript SDK
```javascript
import { AnalysisClient } from '@paraguay-fiber/api-client';

const client = new AnalysisClient({
  apiKey: process.env.ANALYSIS_API_KEY,
  baseURL: 'https://api.paraguay-fiber-analysis.com/v1'
});

// Built-in authentication handling
try {
  const result = await client.analyzeSentiment('Excelente servicio!');
  console.log(`Sentiment: ${result.sentiment}`);
} catch (error) {
  if (error.code === 'UNAUTHORIZED') {
    console.error('Authentication failed');
  }
}
```

---

## Troubleshooting

### Common Issues

#### 1. "Invalid API Key" Error
**Symptoms**: 401 Unauthorized responses
**Causes**:
- Typo in API key
- Using wrong environment key
- Expired key
- Missing `sk-` prefix

**Solutions**:
1. Verify key in dashboard
2. Check environment variables
3. Regenerate if necessary
4. Ensure proper format

#### 2. "Rate Limit Exceeded" Error
**Symptoms**: 429 Too Many Requests
**Causes**:
- Exceeding hourly limits
- Burst limit exceeded
- Multiple concurrent requests

**Solutions**:
1. Implement exponential backoff
2. Reduce request frequency
3. Upgrade plan
4. Use batch endpoints

#### 3. "Forbidden" Error
**Symptoms**: 403 Forbidden responses
**Causes**:
- Insufficient permissions
- Plan limitations
- Geographic restrictions

**Solutions**:
1. Check API key permissions
2. Upgrade plan
3. Contact support

### Debug Tools

#### API Key Validator
```bash
curl -X GET "https://api.paraguay-fiber-analysis.com/v1/health" \
  -H "X-API-Key: sk-your_key_here" \
  -v
```

#### Rate Limit Checker
```bash
curl -X GET "https://api.paraguay-fiber-analysis.com/v1/status" \
  -H "X-API-Key: sk-your_key_here" \
  -I | grep X-RateLimit
```

---

## Support

### Getting Help
- **Documentation**: [https://docs.paraguay-fiber-analysis.com](https://docs.paraguay-fiber-analysis.com)
- **Support Email**: support@paraguay-fiber-analysis.com
- **Status Page**: [https://status.paraguay-fiber-analysis.com](https://status.paraguay-fiber-analysis.com)
- **Community**: [https://community.paraguay-fiber-analysis.com](https://community.paraguay-fiber-analysis.com)

### Enterprise Support
- **Dedicated Support**: For enterprise customers
- **Priority Response**: 4-hour SLA
- **Technical Account Manager**: Direct contact
- **Custom Integration**: Professional services available

---

## Changelog

### v2.0.0 (Current)
- Added API key scopes
- Enhanced rate limiting
- Improved error messages
- Added audit logging

### v1.0.0
- Initial API key authentication
- Basic rate limiting
- HTTPS enforcement