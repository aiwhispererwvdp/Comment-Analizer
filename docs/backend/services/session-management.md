# Session Management Service Documentation

The Session Management Service provides secure, scalable session handling for the Personal Paraguay Fiber Comments Analysis System, managing user state, data persistence, and multi-user support.

## 🎯 Overview

This service manages user sessions across the application lifecycle, maintaining state consistency, handling concurrent users, and ensuring data isolation between sessions.

### Core Capabilities
- **Session Creation and Lifecycle** - Complete session management
- **State Persistence** - Maintain user data across requests
- **Multi-user Support** - Concurrent session handling
- **Data Isolation** - Secure separation of user data
- **Session Recovery** - Resume interrupted sessions

## 🏗️ Architecture

### Session Management Architecture
```python
class SessionManager:
    """
    Central session management system
    """
    
    def __init__(self):
        self.active_sessions = {}
        self.session_store = SessionStore()
        self.session_validator = SessionValidator()
        self.cleanup_scheduler = CleanupScheduler()
        self.max_sessions_per_user = 3
        self.session_timeout_minutes = 30
    
    async def create_session(self, user_identifier=None):
        """
        Create new user session
        """
        # Generate unique session ID
        session_id = self.generate_session_id()
        
        # Create session object
        session = UserSession(
            session_id=session_id,
            user_identifier=user_identifier,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=self.session_timeout_minutes)
        )
        
        # Store session
        self.active_sessions[session_id] = session
        await self.session_store.persist(session)
        
        # Set up cleanup
        self.cleanup_scheduler.schedule_cleanup(session_id, session.expires_at)
        
        return session
```

## 🔐 Session Security

### Secure Session Generation
```python
class SessionSecurity:
    """
    Security features for session management
    """
    
    def generate_session_id(self):
        """
        Generate cryptographically secure session ID
        """
        # Generate random bytes
        random_bytes = secrets.token_bytes(32)
        
        # Add timestamp for uniqueness
        timestamp = str(time.time()).encode()
        
        # Create hash
        session_data = random_bytes + timestamp
        session_id = hashlib.sha256(session_data).hexdigest()
        
        return session_id
    
    def validate_session_token(self, token):
        """
        Validate session token security
        """
        # Check token format
        if not self.is_valid_format(token):
            return False
        
        # Check token hasn't been tampered with
        if not self.verify_token_integrity(token):
            return False
        
        # Check token isn't expired
        if self.is_token_expired(token):
            return False
        
        return True
    
    def encrypt_session_data(self, data):
        """
        Encrypt sensitive session data
        """
        key = self.get_encryption_key()
        cipher = Fernet(key)
        
        # Serialize data
        serialized = pickle.dumps(data)
        
        # Encrypt
        encrypted = cipher.encrypt(serialized)
        
        return encrypted
```

## 📊 Session State Management

### State Storage
```python
class SessionState:
    """
    Manage session state data
    """
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.state = {
            'user_data': {},
            'analysis_data': {},
            'ui_state': {},
            'preferences': {},
            'temporary_data': {}
        }
        self.state_version = 1
        self.last_modified = datetime.now()
    
    def update_state(self, category, key, value):
        """
        Update session state with versioning
        """
        # Store previous version
        self.create_state_snapshot()
        
        # Update state
        if category not in self.state:
            self.state[category] = {}
        
        self.state[category][key] = value
        self.last_modified = datetime.now()
        self.state_version += 1
        
        # Persist changes
        self.persist_state()
    
    def get_state(self, category=None, key=None):
        """
        Retrieve state data
        """
        if category is None:
            return self.state
        
        if key is None:
            return self.state.get(category, {})
        
        return self.state.get(category, {}).get(key)
    
    def create_state_snapshot(self):
        """
        Create snapshot for recovery
        """
        snapshot = {
            'version': self.state_version,
            'timestamp': datetime.now(),
            'state': copy.deepcopy(self.state)
        }
        
        self.save_snapshot(snapshot)
```

### State Persistence
```python
class StatePersistence:
    """
    Persist session state to storage
    """
    
    def __init__(self):
        self.storage_backend = self.initialize_storage()
        self.cache = StateCache()
        
    async def persist_state(self, session_id, state_data):
        """
        Save state to persistent storage
        """
        # Serialize state
        serialized = self.serialize_state(state_data)
        
        # Store in cache for fast access
        self.cache.set(session_id, state_data)
        
        # Persist to storage
        await self.storage_backend.save(
            key=f"session:{session_id}",
            value=serialized,
            ttl=3600  # 1 hour TTL
        )
        
        return True
    
    async def retrieve_state(self, session_id):
        """
        Retrieve state from storage
        """
        # Check cache first
        cached = self.cache.get(session_id)
        if cached:
            return cached
        
        # Retrieve from storage
        serialized = await self.storage_backend.get(f"session:{session_id}")
        
        if serialized:
            state_data = self.deserialize_state(serialized)
            
            # Update cache
            self.cache.set(session_id, state_data)
            
            return state_data
        
        return None
```

## 🔄 Session Lifecycle

### Session Creation and Initialization
```python
class SessionLifecycle:
    """
    Manage complete session lifecycle
    """
    
    async def initialize_session(self, request_context):
        """
        Initialize new session with context
        """
        # Create session
        session = await self.create_session()
        
        # Set initial context
        session.set_context({
            'ip_address': request_context.get('ip'),
            'user_agent': request_context.get('user_agent'),
            'created_from': request_context.get('referrer'),
            'initial_locale': request_context.get('locale', 'es-PY')
        })
        
        # Initialize default state
        await self.initialize_default_state(session)
        
        # Set up monitoring
        self.monitor_session(session)
        
        return session
    
    async def initialize_default_state(self, session):
        """
        Set default session state
        """
        default_state = {
            'user_data': {
                'uploaded_files': [],
                'analysis_history': [],
                'preferences': self.get_default_preferences()
            },
            'analysis_data': {
                'current_dataset': None,
                'results': None,
                'processing_status': 'idle'
            },
            'ui_state': {
                'current_page': 'upload',
                'theme': 'light',
                'expanded_sections': []
            }
        }
        
        session.state.update(default_state)
```

### Session Validation and Refresh
```python
class SessionValidator:
    """
    Validate and refresh sessions
    """
    
    def validate_session(self, session_id):
        """
        Comprehensive session validation
        """
        session = self.get_session(session_id)
        
        if not session:
            return {'valid': False, 'reason': 'session_not_found'}
        
        # Check expiration
        if session.is_expired():
            return {'valid': False, 'reason': 'session_expired'}
        
        # Check security
        if not self.validate_session_security(session):
            return {'valid': False, 'reason': 'security_violation'}
        
        # Check activity
        if self.is_session_idle(session):
            return {'valid': False, 'reason': 'session_idle'}
        
        return {'valid': True}
    
    async def refresh_session(self, session_id):
        """
        Refresh session timeout
        """
        session = self.get_session(session_id)
        
        if session and not session.is_expired():
            # Extend expiration
            session.expires_at = datetime.now() + timedelta(
                minutes=self.session_timeout_minutes
            )
            
            # Update last activity
            session.last_activity = datetime.now()
            
            # Persist changes
            await self.persist_session(session)
            
            return True
        
        return False
```

### Session Cleanup
```python
class SessionCleanup:
    """
    Clean up expired and inactive sessions
    """
    
    def __init__(self):
        self.cleanup_interval_seconds = 300  # 5 minutes
        self.idle_timeout_minutes = 30
        
    async def cleanup_expired_sessions(self):
        """
        Remove expired sessions
        """
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if session.expires_at < current_time:
                expired_sessions.append(session_id)
        
        # Clean up expired sessions
        for session_id in expired_sessions:
            await self.cleanup_session(session_id)
        
        return len(expired_sessions)
    
    async def cleanup_session(self, session_id):
        """
        Complete session cleanup
        """
        try:
            # Save final state
            session = self.active_sessions.get(session_id)
            if session:
                await self.save_session_archive(session)
            
            # Clear session data
            await self.clear_session_data(session_id)
            
            # Remove from active sessions
            self.active_sessions.pop(session_id, None)
            
            # Clear from cache
            self.cache.delete(session_id)
            
            # Clear from storage
            await self.storage.delete(f"session:{session_id}")
            
            # Log cleanup
            logger.info(f"Session {session_id} cleaned up")
            
        except Exception as e:
            logger.error(f"Error cleaning up session {session_id}: {e}")
```

## 👥 Multi-User Support

### Concurrent Session Management
```python
class MultiUserSessionManager:
    """
    Handle multiple concurrent user sessions
    """
    
    def __init__(self):
        self.user_sessions = defaultdict(list)  # user_id -> [session_ids]
        self.session_locks = {}  # session_id -> asyncio.Lock
        self.max_concurrent_per_user = 3
    
    async def create_user_session(self, user_id):
        """
        Create session for specific user
        """
        # Check existing sessions for user
        existing_sessions = self.user_sessions[user_id]
        
        # Enforce session limit
        if len(existing_sessions) >= self.max_concurrent_per_user:
            # Remove oldest session
            oldest_session = existing_sessions[0]
            await self.terminate_session(oldest_session)
        
        # Create new session
        session = await self.create_session(user_identifier=user_id)
        
        # Track user session
        self.user_sessions[user_id].append(session.session_id)
        
        # Create session lock for thread safety
        self.session_locks[session.session_id] = asyncio.Lock()
        
        return session
    
    async def get_user_sessions(self, user_id):
        """
        Get all active sessions for user
        """
        session_ids = self.user_sessions.get(user_id, [])
        sessions = []
        
        for session_id in session_ids:
            session = await self.get_session(session_id)
            if session and not session.is_expired():
                sessions.append(session)
        
        return sessions
```

### Session Isolation
```python
class SessionIsolation:
    """
    Ensure data isolation between sessions
    """
    
    def __init__(self):
        self.isolation_level = 'strict'
        self.data_namespaces = {}
    
    def create_session_namespace(self, session_id):
        """
        Create isolated namespace for session
        """
        namespace = {
            'session_id': session_id,
            'data_directory': f"data/sessions/{session_id}",
            'cache_prefix': f"cache:{session_id}:",
            'temp_directory': f"temp/sessions/{session_id}"
        }
        
        # Create directories
        Path(namespace['data_directory']).mkdir(parents=True, exist_ok=True)
        Path(namespace['temp_directory']).mkdir(parents=True, exist_ok=True)
        
        self.data_namespaces[session_id] = namespace
        
        return namespace
    
    def validate_data_access(self, session_id, resource_path):
        """
        Validate session can access resource
        """
        namespace = self.data_namespaces.get(session_id)
        
        if not namespace:
            return False
        
        # Check if resource is within session namespace
        resource_path = Path(resource_path).resolve()
        allowed_path = Path(namespace['data_directory']).resolve()
        
        try:
            resource_path.relative_to(allowed_path)
            return True
        except ValueError:
            return False
```

## 📈 Session Analytics

### Session Metrics
```python
class SessionMetrics:
    """
    Track session metrics and analytics
    """
    
    def __init__(self):
        self.metrics_store = MetricsStore()
        
    def track_session_event(self, session_id, event_type, event_data=None):
        """
        Track session events for analytics
        """
        event = {
            'session_id': session_id,
            'event_type': event_type,
            'timestamp': datetime.now(),
            'data': event_data or {}
        }
        
        self.metrics_store.record_event(event)
        
        # Update session statistics
        self.update_session_stats(session_id, event_type)
    
    def get_session_analytics(self, session_id):
        """
        Get analytics for specific session
        """
        return {
            'duration': self.calculate_session_duration(session_id),
            'page_views': self.get_page_view_count(session_id),
            'analyses_performed': self.get_analysis_count(session_id),
            'files_uploaded': self.get_upload_count(session_id),
            'api_calls': self.get_api_call_count(session_id),
            'estimated_cost': self.calculate_session_cost(session_id),
            'activity_timeline': self.get_activity_timeline(session_id)
        }
    
    def get_aggregate_metrics(self, time_period='daily'):
        """
        Get aggregated session metrics
        """
        return {
            'active_sessions': len(self.active_sessions),
            'total_sessions': self.get_total_sessions(time_period),
            'avg_session_duration': self.get_avg_duration(time_period),
            'peak_concurrent': self.get_peak_concurrent(time_period),
            'unique_users': self.get_unique_users(time_period),
            'total_analyses': self.get_total_analyses(time_period)
        }
```

## 🔄 Session Recovery

### Session Recovery Mechanism
```python
class SessionRecovery:
    """
    Recover interrupted or failed sessions
    """
    
    def __init__(self):
        self.recovery_window_minutes = 60
        self.recovery_storage = RecoveryStorage()
        
    async def save_recovery_point(self, session_id):
        """
        Save session recovery point
        """
        session = self.get_session(session_id)
        
        if not session:
            return False
        
        recovery_data = {
            'session_id': session_id,
            'timestamp': datetime.now(),
            'state': session.get_complete_state(),
            'metadata': {
                'last_activity': session.last_activity,
                'page': session.current_page,
                'processing_status': session.processing_status
            }
        }
        
        await self.recovery_storage.save(recovery_data)
        
        return True
    
    async def recover_session(self, recovery_token):
        """
        Recover session from recovery point
        """
        # Retrieve recovery data
        recovery_data = await self.recovery_storage.get(recovery_token)
        
        if not recovery_data:
            return None
        
        # Check if recovery window is still valid
        age = datetime.now() - recovery_data['timestamp']
        if age.total_seconds() > self.recovery_window_minutes * 60:
            return None
        
        # Create new session with recovered state
        session = await self.create_session()
        session.restore_state(recovery_data['state'])
        
        # Update metadata
        session.metadata['recovered_from'] = recovery_token
        session.metadata['recovery_time'] = datetime.now()
        
        return session
```

## ⚙️ Configuration

### Session Configuration
```python
SESSION_CONFIG = {
    'session': {
        'timeout_minutes': 30,
        'idle_timeout_minutes': 20,
        'max_sessions_per_user': 3,
        'enable_recovery': True,
        'recovery_window_minutes': 60
    },
    'storage': {
        'backend': 'redis',  # 'memory', 'redis', 'database'
        'redis_url': 'redis://localhost:6379',
        'persistence': True,
        'encryption': True
    },
    'security': {
        'secure_cookies': True,
        'session_encryption': True,
        'csrf_protection': True,
        'ip_validation': False
    },
    'cleanup': {
        'enabled': True,
        'interval_seconds': 300,
        'archive_expired': True
    },
    'analytics': {
        'track_events': True,
        'track_metrics': True,
        'retention_days': 30
    }
}
```

## 🔐 Security Considerations

### Session Security Best Practices
```python
class SessionSecurityManager:
    """
    Implement session security best practices
    """
    
    def __init__(self):
        self.security_config = SESSION_CONFIG['security']
        
    def secure_session_cookie(self, session_id):
        """
        Create secure session cookie
        """
        cookie_data = {
            'session_id': session_id,
            'created': datetime.now().isoformat(),
            'fingerprint': self.generate_fingerprint()
        }
        
        # Sign cookie
        signed_cookie = self.sign_cookie(cookie_data)
        
        cookie_options = {
            'httponly': True,
            'secure': self.security_config['secure_cookies'],
            'samesite': 'lax',
            'max_age': SESSION_CONFIG['session']['timeout_minutes'] * 60
        }
        
        return signed_cookie, cookie_options
    
    def validate_session_security(self, session, request):
        """
        Validate session security constraints
        """
        # Check CSRF token
        if self.security_config['csrf_protection']:
            if not self.validate_csrf_token(session, request):
                return False
        
        # Check IP address
        if self.security_config['ip_validation']:
            if not self.validate_ip_address(session, request):
                return False
        
        # Check session fingerprint
        if not self.validate_fingerprint(session, request):
            return False
        
        return True
```

## 🔗 Related Documentation
- [File Upload Service](file-upload-service.md) - File handling integration
- [Analysis Service](analysis-service.md) - Analysis session management
- [Security](../infrastructure/security.md) - Security implementation
- [Cache Management](../api/cache-management.md) - Session caching