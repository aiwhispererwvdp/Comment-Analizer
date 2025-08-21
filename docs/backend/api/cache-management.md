# Cache Management Documentation

The Cache Management system provides intelligent caching of API responses and analysis results to improve performance, reduce costs, and enhance user experience in the Personal Paraguay Fiber Comments Analysis System.

## 🎯 Overview

The cache management system implements a multi-layer caching strategy to minimize API calls, reduce latency, and optimize resource utilization while maintaining data freshness and accuracy.

### Core Capabilities
- **Response Caching** - Store and retrieve API responses
- **Smart Invalidation** - Intelligent cache refresh strategies
- **Memory Management** - Efficient memory utilization
- **Distributed Caching** - Support for Redis and other cache stores
- **Performance Monitoring** - Cache hit rate tracking

## 🏗️ Cache Architecture

### Multi-Layer Cache Strategy
```python
class CacheArchitecture:
    """
    Multi-layer caching system
    """
    
    CACHE_LAYERS = {
        'L1_memory': {
            'type': 'in_memory',
            'ttl': 300,  # 5 minutes
            'max_size': 1000,
            'eviction': 'LRU'
        },
        'L2_disk': {
            'type': 'disk_cache',
            'ttl': 3600,  # 1 hour
            'max_size': 10000,
            'path': 'data/cache'
        },
        'L3_distributed': {
            'type': 'redis',
            'ttl': 86400,  # 24 hours
            'max_size': 100000,
            'connection': 'redis://localhost:6379'
        }
    }
```

### Cache Flow
```
Request → L1 Memory Cache → L2 Disk Cache → L3 Distributed Cache → API Call
    ↓         ↓                ↓                   ↓                    ↓
Response ← Cache Hit      ← Cache Hit        ← Cache Hit         ← API Response
```

## 📦 Cache Implementation

### Core Cache Manager
```python
class CacheManager:
    """
    Central cache management system
    """
    
    def __init__(self, config):
        self.memory_cache = MemoryCache(config['memory'])
        self.disk_cache = DiskCache(config['disk'])
        self.distributed_cache = RedisCache(config['redis'])
        self.statistics = CacheStatistics()
    
    async def get(self, key):
        """
        Multi-layer cache retrieval
        """
        # Try L1 - Memory
        result = self.memory_cache.get(key)
        if result:
            self.statistics.record_hit('L1')
            return result
        
        # Try L2 - Disk
        result = self.disk_cache.get(key)
        if result:
            self.statistics.record_hit('L2')
            self.memory_cache.set(key, result)  # Promote to L1
            return result
        
        # Try L3 - Distributed
        result = await self.distributed_cache.get(key)
        if result:
            self.statistics.record_hit('L3')
            self.promote_to_upper_layers(key, result)
            return result
        
        self.statistics.record_miss()
        return None
    
    async def set(self, key, value, ttl=None):
        """
        Store in all cache layers
        """
        # Store in all layers with appropriate TTL
        self.memory_cache.set(key, value, ttl or 300)
        self.disk_cache.set(key, value, ttl or 3600)
        await self.distributed_cache.set(key, value, ttl or 86400)
```

### Cache Key Generation
```python
class CacheKeyGenerator:
    """
    Generates consistent cache keys
    """
    
    @staticmethod
    def generate_analysis_key(comment, config):
        """
        Generate cache key for analysis results
        """
        # Create deterministic key from comment and config
        content_hash = hashlib.sha256(comment.encode()).hexdigest()[:16]
        config_hash = hashlib.md5(
            json.dumps(config, sort_keys=True).encode()
        ).hexdigest()[:8]
        
        return f"analysis:{content_hash}:{config_hash}"
    
    @staticmethod
    def generate_api_key(endpoint, params):
        """
        Generate cache key for API responses
        """
        params_str = json.dumps(params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        
        return f"api:{endpoint}:{params_hash}"
```

## 🔄 Cache Invalidation

### Invalidation Strategies
```python
class CacheInvalidation:
    """
    Smart cache invalidation system
    """
    
    INVALIDATION_STRATEGIES = {
        'time_based': {
            'description': 'Expire after fixed time period',
            'default_ttl': 3600
        },
        'event_based': {
            'description': 'Invalidate on specific events',
            'events': ['config_change', 'model_update', 'force_refresh']
        },
        'pattern_based': {
            'description': 'Invalidate matching patterns',
            'patterns': ['analysis:*', 'api:openai:*']
        },
        'dependency_based': {
            'description': 'Invalidate dependent caches',
            'track_dependencies': True
        }
    }
    
    def invalidate_by_pattern(self, pattern):
        """
        Invalidate all keys matching pattern
        """
        keys_to_invalidate = self.find_matching_keys(pattern)
        
        for key in keys_to_invalidate:
            self.invalidate_key(key)
            self.invalidate_dependencies(key)
        
        return len(keys_to_invalidate)
```

### Smart Refresh
```python
class SmartCacheRefresh:
    """
    Intelligent cache refresh system
    """
    
    def should_refresh(self, cache_entry):
        """
        Determine if cache should be refreshed
        """
        factors = {
            'age': self.calculate_age_factor(cache_entry),
            'usage': self.calculate_usage_factor(cache_entry),
            'confidence': self.calculate_confidence_factor(cache_entry),
            'cost': self.calculate_cost_factor(cache_entry)
        }
        
        refresh_score = self.calculate_refresh_score(factors)
        
        return refresh_score > self.refresh_threshold
    
    async def background_refresh(self, key):
        """
        Refresh cache in background
        """
        # Don't block user request
        asyncio.create_task(self.refresh_cache_entry(key))
```

## 💾 Memory Management

### Memory-Efficient Caching
```python
class MemoryEfficientCache:
    """
    Memory-optimized cache implementation
    """
    
    def __init__(self, max_memory_mb=500):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.current_memory = 0
        self.cache = OrderedDict()
        self.size_tracker = {}
    
    def set(self, key, value):
        """
        Store with memory tracking
        """
        # Calculate size
        size = self.calculate_size(value)
        
        # Evict if necessary
        while self.current_memory + size > self.max_memory:
            self.evict_lru()
        
        # Store value
        self.cache[key] = value
        self.size_tracker[key] = size
        self.current_memory += size
    
    def evict_lru(self):
        """
        Evict least recently used items
        """
        if self.cache:
            key, _ = self.cache.popitem(last=False)
            size = self.size_tracker.pop(key, 0)
            self.current_memory -= size
```

### Compression
```python
class CompressedCache:
    """
    Cache with compression support
    """
    
    def set(self, key, value):
        """
        Store compressed value
        """
        # Serialize and compress
        serialized = pickle.dumps(value)
        compressed = zlib.compress(serialized)
        
        # Store if compression is beneficial
        if len(compressed) < len(serialized) * 0.9:
            self.cache[key] = {
                'data': compressed,
                'compressed': True
            }
        else:
            self.cache[key] = {
                'data': serialized,
                'compressed': False
            }
    
    def get(self, key):
        """
        Retrieve and decompress value
        """
        entry = self.cache.get(key)
        if not entry:
            return None
        
        if entry['compressed']:
            decompressed = zlib.decompress(entry['data'])
            return pickle.loads(decompressed)
        else:
            return pickle.loads(entry['data'])
```

## 📊 Cache Performance

### Hit Rate Monitoring
```python
class CacheStatistics:
    """
    Cache performance monitoring
    """
    
    def __init__(self):
        self.hits = {'L1': 0, 'L2': 0, 'L3': 0}
        self.misses = 0
        self.total_requests = 0
        self.response_times = []
    
    def calculate_hit_rate(self):
        """
        Calculate overall cache hit rate
        """
        total_hits = sum(self.hits.values())
        
        if self.total_requests == 0:
            return 0.0
        
        return total_hits / self.total_requests
    
    def get_layer_statistics(self):
        """
        Get per-layer statistics
        """
        stats = {}
        for layer, hits in self.hits.items():
            stats[layer] = {
                'hits': hits,
                'hit_rate': hits / max(self.total_requests, 1),
                'avg_response_time': self.calculate_avg_response_time(layer)
            }
        return stats
```

### Performance Optimization
```python
class CacheOptimizer:
    """
    Optimize cache performance based on metrics
    """
    
    def optimize_cache_sizes(self, statistics):
        """
        Dynamically adjust cache sizes
        """
        recommendations = []
        
        # Analyze hit rates
        for layer, stats in statistics.items():
            if stats['hit_rate'] < 0.3:
                recommendations.append({
                    'layer': layer,
                    'action': 'increase_size',
                    'reason': 'low_hit_rate'
                })
            elif stats['hit_rate'] > 0.9:
                recommendations.append({
                    'layer': layer,
                    'action': 'consider_reduction',
                    'reason': 'very_high_hit_rate'
                })
        
        return recommendations
```

## 🔐 Cache Security

### Secure Caching
```python
class SecureCache:
    """
    Security-enhanced cache implementation
    """
    
    def __init__(self, encryption_key=None):
        self.cipher = Fernet(encryption_key) if encryption_key else None
        self.cache = {}
    
    def set(self, key, value, sensitive=False):
        """
        Store with optional encryption
        """
        serialized = pickle.dumps(value)
        
        if sensitive and self.cipher:
            encrypted = self.cipher.encrypt(serialized)
            self.cache[key] = {
                'data': encrypted,
                'encrypted': True
            }
        else:
            self.cache[key] = {
                'data': serialized,
                'encrypted': False
            }
    
    def get(self, key):
        """
        Retrieve and decrypt if necessary
        """
        entry = self.cache.get(key)
        if not entry:
            return None
        
        if entry['encrypted'] and self.cipher:
            decrypted = self.cipher.decrypt(entry['data'])
            return pickle.loads(decrypted)
        else:
            return pickle.loads(entry['data'])
```

## 🌐 Distributed Caching

### Redis Integration
```python
class RedisCache:
    """
    Redis-based distributed cache
    """
    
    def __init__(self, redis_url='redis://localhost:6379'):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600
    
    async def get(self, key):
        """
        Get from Redis
        """
        try:
            value = await self.redis_client.get(key)
            if value:
                return pickle.loads(value)
        except Exception as e:
            logger.error(f"Redis get error: {e}")
        return None
    
    async def set(self, key, value, ttl=None):
        """
        Set in Redis with TTL
        """
        try:
            serialized = pickle.dumps(value)
            await self.redis_client.setex(
                key,
                ttl or self.default_ttl,
                serialized
            )
        except Exception as e:
            logger.error(f"Redis set error: {e}")
```

## 🎯 Cache Strategies

### Analysis Result Caching
```python
def cache_analysis_results(comment, analysis_result):
    """
    Cache sentiment analysis results
    """
    # Generate cache key
    cache_key = generate_analysis_key(comment)
    
    # Determine TTL based on confidence
    if analysis_result['confidence'] > 0.9:
        ttl = 86400  # 24 hours for high confidence
    elif analysis_result['confidence'] > 0.7:
        ttl = 3600   # 1 hour for medium confidence
    else:
        ttl = 300    # 5 minutes for low confidence
    
    # Store in cache
    cache_manager.set(cache_key, analysis_result, ttl)
```

### Similar Comment Detection
```python
class SimilarityCache:
    """
    Cache based on comment similarity
    """
    
    def find_similar_cached(self, comment, threshold=0.85):
        """
        Find similar comments in cache
        """
        comment_embedding = self.get_embedding(comment)
        
        for cached_key, cached_data in self.cache.items():
            similarity = self.calculate_similarity(
                comment_embedding,
                cached_data['embedding']
            )
            
            if similarity > threshold:
                return cached_data['result']
        
        return None
```

## 📈 Cost Optimization

### API Call Reduction
```python
def calculate_cost_savings(cache_statistics):
    """
    Calculate cost savings from caching
    """
    api_cost_per_request = 0.002  # $0.002 per API call
    
    total_hits = sum(cache_statistics.hits.values())
    saved_api_calls = total_hits
    
    cost_savings = saved_api_calls * api_cost_per_request
    
    return {
        'saved_api_calls': saved_api_calls,
        'cost_savings_usd': cost_savings,
        'cache_efficiency': cache_statistics.calculate_hit_rate()
    }
```

## 🔧 Configuration

### Cache Configuration
```python
CACHE_CONFIG = {
    'enabled': True,
    'memory_cache': {
        'enabled': True,
        'max_size': 1000,
        'ttl': 300,
        'eviction_policy': 'LRU'
    },
    'disk_cache': {
        'enabled': True,
        'path': 'data/cache',
        'max_size_mb': 500,
        'ttl': 3600
    },
    'redis_cache': {
        'enabled': False,
        'url': 'redis://localhost:6379',
        'ttl': 86400,
        'key_prefix': 'paraguay_analysis'
    },
    'compression': {
        'enabled': True,
        'min_size_bytes': 1024
    }
}
```

## 🔗 Related Documentation
- [API Optimization](optimization.md) - API performance optimization
- [Monitoring](monitoring.md) - Cache monitoring and metrics
- [Performance](../infrastructure/performance.md) - System performance
- [Configuration](../../getting-started/configuration.md) - Cache configuration