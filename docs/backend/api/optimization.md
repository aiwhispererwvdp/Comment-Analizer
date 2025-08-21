# API Optimization Documentation

This document covers comprehensive optimization strategies for the Personal Paraguay Fiber Comments Analysis System's API layer, focusing on performance, cost reduction, and scalability.

## 🚀 Overview

API optimization ensures efficient resource utilization, reduced latency, lower costs, and improved user experience through intelligent request management, caching, batching, and performance tuning.

### Optimization Goals
- **Reduce API Costs** - Minimize external API usage charges
- **Improve Response Times** - Faster analysis results
- **Increase Throughput** - Handle more concurrent users
- **Enhance Reliability** - Reduce failures and timeouts
- **Scale Efficiently** - Handle growth without linear cost increase

## 🎯 Request Optimization

### Request Batching
```python
class RequestBatcher:
    """
    Intelligent request batching for API efficiency
    """
    
    def __init__(self, batch_size=50, max_wait_ms=100):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.pending_requests = []
        self.batch_processor = BatchProcessor()
    
    async def add_request(self, request):
        """
        Add request to batch queue
        """
        self.pending_requests.append(request)
        
        # Process if batch is full
        if len(self.pending_requests) >= self.batch_size:
            return await self.process_batch()
        
        # Or wait for more requests (with timeout)
        await self.wait_for_batch_or_timeout()
        
    async def process_batch(self):
        """
        Process accumulated requests as batch
        """
        if not self.pending_requests:
            return []
        
        # Combine requests for single API call
        batch_request = self.combine_requests(self.pending_requests)
        
        # Make single API call for entire batch
        batch_response = await self.api_client.process_batch(batch_request)
        
        # Split response back to individual results
        individual_results = self.split_batch_response(batch_response)
        
        # Clear processed requests
        self.pending_requests.clear()
        
        return individual_results
```

### Request Deduplication
```python
class RequestDeduplicator:
    """
    Eliminate duplicate API requests
    """
    
    def __init__(self, ttl_seconds=60):
        self.request_cache = {}
        self.ttl = ttl_seconds
        self.pending_requests = {}  # Requests in flight
    
    async def deduplicated_request(self, request_key, request_func):
        """
        Ensure only one request for same data
        """
        # Check if we have recent result
        if request_key in self.request_cache:
            cached_result, timestamp = self.request_cache[request_key]
            if time.time() - timestamp < self.ttl:
                return cached_result
        
        # Check if request is already in flight
        if request_key in self.pending_requests:
            # Wait for existing request to complete
            return await self.pending_requests[request_key]
        
        # Create new request
        future = asyncio.create_future()
        self.pending_requests[request_key] = future
        
        try:
            result = await request_func()
            self.request_cache[request_key] = (result, time.time())
            future.set_result(result)
            return result
        finally:
            del self.pending_requests[request_key]
```

## 💾 Intelligent Caching

### Multi-tier Cache Strategy
```python
class MultiTierCache:
    """
    Hierarchical caching for optimal performance
    """
    
    def __init__(self):
        self.l1_memory = MemoryCache(size_mb=100, ttl=300)
        self.l2_disk = DiskCache(size_mb=1000, ttl=3600)
        self.l3_distributed = RedisCache(ttl=86400)
        
    async def get_with_fallback(self, key, fetch_func):
        """
        Try caches in order, fall back to API
        """
        # L1: Memory cache (fastest)
        result = self.l1_memory.get(key)
        if result:
            return result
        
        # L2: Disk cache
        result = self.l2_disk.get(key)
        if result:
            self.l1_memory.set(key, result)  # Promote to L1
            return result
        
        # L3: Distributed cache
        result = await self.l3_distributed.get(key)
        if result:
            self.promote_to_upper_tiers(key, result)
            return result
        
        # Fetch from API
        result = await fetch_func()
        await self.cache_in_all_tiers(key, result)
        return result
```

### Smart Cache Invalidation
```python
class SmartCacheInvalidation:
    """
    Intelligent cache invalidation strategies
    """
    
    def __init__(self):
        self.dependency_graph = {}
        self.invalidation_rules = []
    
    def invalidate_dependent_caches(self, key):
        """
        Invalidate related cache entries
        """
        # Find all dependent keys
        dependent_keys = self.get_dependent_keys(key)
        
        # Invalidate in order of dependency
        for dep_key in self.topological_sort(dependent_keys):
            self.cache.delete(dep_key)
            
    def smart_refresh(self, key):
        """
        Refresh cache intelligently
        """
        # Check if refresh is needed
        if not self.needs_refresh(key):
            return
        
        # Refresh in background (don't block user)
        asyncio.create_task(self.background_refresh(key))
        
    def needs_refresh(self, key):
        """
        Determine if cache needs refreshing
        """
        entry = self.cache.get_metadata(key)
        
        # Check age
        age = time.time() - entry['created']
        if age > entry['soft_ttl']:
            return True
        
        # Check usage pattern
        if entry['access_count'] > 100 and age > 60:
            return True
        
        return False
```

## ⚡ Performance Optimization

### Connection Pooling
```python
class ConnectionPoolManager:
    """
    Manage connection pools for API clients
    """
    
    def __init__(self):
        self.pools = {
            'openai': aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300
            ),
            'azure': aiohttp.TCPConnector(
                limit=50,
                limit_per_host=20
            )
        }
        
    async def get_session(self, service):
        """
        Get optimized session for service
        """
        connector = self.pools.get(service)
        
        return aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'Connection': 'keep-alive'}
        )
```

### Parallel Processing
```python
class ParallelProcessor:
    """
    Process multiple requests in parallel
    """
    
    def __init__(self, max_concurrent=10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
        
    async def process_parallel(self, items, process_func):
        """
        Process items in parallel with concurrency limit
        """
        async def process_with_limit(item):
            async with self.semaphore:
                return await process_func(item)
        
        # Create tasks for all items
        tasks = [process_with_limit(item) for item in items]
        
        # Process in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any errors
        return self.handle_results(results)
```

### Response Compression
```python
class ResponseCompression:
    """
    Compress API responses for efficiency
    """
    
    def compress_response(self, data):
        """
        Compress response data
        """
        json_str = json.dumps(data)
        compressed = gzip.compress(json_str.encode())
        
        # Only use compression if it saves space
        if len(compressed) < len(json_str) * 0.9:
            return {
                'compressed': True,
                'data': base64.b64encode(compressed).decode(),
                'original_size': len(json_str),
                'compressed_size': len(compressed)
            }
        
        return {'compressed': False, 'data': data}
    
    def decompress_response(self, response):
        """
        Decompress response if needed
        """
        if response.get('compressed'):
            compressed_data = base64.b64decode(response['data'])
            decompressed = gzip.decompress(compressed_data)
            return json.loads(decompressed)
        
        return response['data']
```

## 🎯 Cost Optimization

### Token Optimization
```python
class TokenOptimizer:
    """
    Optimize token usage for language models
    """
    
    def optimize_prompt(self, prompt, max_tokens=2000):
        """
        Optimize prompt to use fewer tokens
        """
        # Remove unnecessary whitespace
        prompt = ' '.join(prompt.split())
        
        # Use abbreviations where possible
        prompt = self.apply_abbreviations(prompt)
        
        # Remove redundant instructions
        prompt = self.remove_redundancy(prompt)
        
        # Truncate if still too long
        if self.count_tokens(prompt) > max_tokens:
            prompt = self.smart_truncate(prompt, max_tokens)
        
        return prompt
    
    def batch_optimize_tokens(self, texts):
        """
        Optimize token usage for batch processing
        """
        # Find common prefixes/suffixes
        common_prefix = self.find_common_prefix(texts)
        common_suffix = self.find_common_suffix(texts)
        
        # Create optimized batch prompt
        batch_prompt = f"{common_prefix}\n"
        for text in texts:
            unique_part = text.replace(common_prefix, '').replace(common_suffix, '')
            batch_prompt += f"- {unique_part}\n"
        batch_prompt += common_suffix
        
        return batch_prompt
```

### API Call Reduction
```python
class APICallReducer:
    """
    Strategies to reduce API calls
    """
    
    def __init__(self):
        self.similarity_threshold = 0.85
        self.pattern_cache = {}
        
    def find_similar_cached(self, text):
        """
        Find similar already-processed text
        """
        text_embedding = self.get_embedding(text)
        
        for cached_text, cached_result in self.cache.items():
            similarity = self.calculate_similarity(
                text_embedding, 
                cached_result['embedding']
            )
            
            if similarity > self.similarity_threshold:
                # Adjust confidence based on similarity
                adjusted_result = cached_result.copy()
                adjusted_result['confidence'] *= similarity
                return adjusted_result
        
        return None
    
    def use_pattern_matching(self, text):
        """
        Use patterns instead of API for simple cases
        """
        # Check for obvious patterns
        if self.is_clearly_positive(text):
            return {'sentiment': 'positive', 'confidence': 0.95}
        
        if self.is_clearly_negative(text):
            return {'sentiment': 'negative', 'confidence': 0.95}
        
        # No clear pattern, need API
        return None
```

## 🔄 Rate Limiting and Throttling

### Adaptive Rate Limiting
```python
class AdaptiveRateLimiter:
    """
    Dynamic rate limiting based on API responses
    """
    
    def __init__(self):
        self.current_rate = 60  # requests per minute
        self.min_rate = 10
        self.max_rate = 100
        self.rate_adjuster = RateAdjuster()
        
    async def acquire(self):
        """
        Acquire permission to make request
        """
        # Calculate delay based on current rate
        delay = 60.0 / self.current_rate
        
        # Wait if necessary
        time_since_last = time.time() - self.last_request_time
        if time_since_last < delay:
            await asyncio.sleep(delay - time_since_last)
        
        self.last_request_time = time.time()
        
    def adjust_rate(self, response):
        """
        Adjust rate based on API response
        """
        if response.status == 429:  # Rate limited
            self.current_rate = max(self.min_rate, self.current_rate * 0.5)
        elif response.status == 200:
            # Gradually increase rate if successful
            self.current_rate = min(self.max_rate, self.current_rate * 1.1)
```

### Request Queue Management
```python
class RequestQueueManager:
    """
    Manage request queue for optimal throughput
    """
    
    def __init__(self):
        self.queues = {
            'high': asyncio.PriorityQueue(),
            'normal': asyncio.Queue(),
            'low': asyncio.Queue()
        }
        self.processing = False
        
    async def add_request(self, request, priority='normal'):
        """
        Add request to appropriate queue
        """
        queue = self.queues[priority]
        
        if priority == 'high':
            # Priority queue uses (priority_number, request) tuple
            await queue.put((self.get_priority_score(request), request))
        else:
            await queue.put(request)
        
        if not self.processing:
            asyncio.create_task(self.process_queues())
    
    async def process_queues(self):
        """
        Process queues with priority
        """
        self.processing = True
        
        while any(not q.empty() for q in self.queues.values()):
            # Process high priority first
            if not self.queues['high'].empty():
                _, request = await self.queues['high'].get()
                await self.process_request(request)
            
            # Then normal
            elif not self.queues['normal'].empty():
                request = await self.queues['normal'].get()
                await self.process_request(request)
            
            # Finally low priority
            elif not self.queues['low'].empty():
                request = await self.queues['low'].get()
                await self.process_request(request)
        
        self.processing = False
```

## 📊 Load Balancing

### Multi-Provider Load Balancing
```python
class LoadBalancer:
    """
    Balance load across multiple API providers
    """
    
    def __init__(self):
        self.providers = {
            'openai': {'weight': 0.7, 'health': 1.0, 'cost': 0.002},
            'azure': {'weight': 0.2, 'health': 1.0, 'cost': 0.001},
            'google': {'weight': 0.1, 'health': 1.0, 'cost': 0.0015}
        }
        
    def select_provider(self):
        """
        Select provider based on weighted round-robin
        """
        # Calculate effective weights (weight * health)
        effective_weights = {
            name: config['weight'] * config['health']
            for name, config in self.providers.items()
        }
        
        # Select based on probability
        total_weight = sum(effective_weights.values())
        rand = random.uniform(0, total_weight)
        
        cumulative = 0
        for provider, weight in effective_weights.items():
            cumulative += weight
            if rand <= cumulative:
                return provider
        
        return list(self.providers.keys())[0]  # Fallback
    
    def update_health(self, provider, success):
        """
        Update provider health based on results
        """
        current_health = self.providers[provider]['health']
        
        if success:
            # Increase health (max 1.0)
            new_health = min(1.0, current_health * 1.1)
        else:
            # Decrease health (min 0.1)
            new_health = max(0.1, current_health * 0.9)
        
        self.providers[provider]['health'] = new_health
```

## 🚀 Streaming and Chunking

### Response Streaming
```python
class ResponseStreamer:
    """
    Stream large responses for better UX
    """
    
    async def stream_analysis(self, comments):
        """
        Stream analysis results as they complete
        """
        async def analyze_and_yield(comment):
            result = await self.analyze_comment(comment)
            return result
        
        # Process comments in chunks
        chunk_size = 10
        for i in range(0, len(comments), chunk_size):
            chunk = comments[i:i + chunk_size]
            
            # Process chunk in parallel
            tasks = [analyze_and_yield(c) for c in chunk]
            results = await asyncio.gather(*tasks)
            
            # Yield chunk results
            for result in results:
                yield result
```

### Progressive Loading
```python
class ProgressiveLoader:
    """
    Load and process data progressively
    """
    
    def __init__(self):
        self.chunk_size = 100
        self.progress_callback = None
        
    async def process_progressively(self, data, callback):
        """
        Process data in chunks with progress updates
        """
        total = len(data)
        processed = 0
        results = []
        
        for chunk_start in range(0, total, self.chunk_size):
            chunk_end = min(chunk_start + self.chunk_size, total)
            chunk = data[chunk_start:chunk_end]
            
            # Process chunk
            chunk_results = await self.process_chunk(chunk)
            results.extend(chunk_results)
            
            # Update progress
            processed += len(chunk)
            if callback:
                await callback({
                    'processed': processed,
                    'total': total,
                    'percentage': (processed / total) * 100,
                    'current_results': chunk_results
                })
        
        return results
```

## 🔧 Configuration and Tuning

### Optimization Configuration
```python
OPTIMIZATION_CONFIG = {
    'batching': {
        'enabled': True,
        'batch_size': 50,
        'max_wait_ms': 100
    },
    'caching': {
        'enabled': True,
        'multi_tier': True,
        'similarity_matching': True,
        'similarity_threshold': 0.85
    },
    'rate_limiting': {
        'adaptive': True,
        'initial_rate': 60,
        'min_rate': 10,
        'max_rate': 100
    },
    'parallel_processing': {
        'enabled': True,
        'max_concurrent': 10,
        'timeout_seconds': 30
    },
    'compression': {
        'enabled': True,
        'min_size_bytes': 1024
    },
    'load_balancing': {
        'enabled': False,  # Enable if multiple providers
        'strategy': 'weighted_round_robin'
    }
}
```

### Performance Tuning
```python
def auto_tune_performance(metrics):
    """
    Automatically tune performance parameters
    """
    recommendations = []
    
    # Check cache hit rate
    if metrics['cache_hit_rate'] < 0.3:
        recommendations.append({
            'parameter': 'cache_ttl',
            'action': 'increase',
            'reason': 'Low cache hit rate'
        })
    
    # Check response times
    if metrics['p95_response_time'] > 2000:
        recommendations.append({
            'parameter': 'batch_size',
            'action': 'increase',
            'reason': 'High response times'
        })
    
    # Check error rate
    if metrics['error_rate'] > 0.05:
        recommendations.append({
            'parameter': 'rate_limit',
            'action': 'decrease',
            'reason': 'High error rate'
        })
    
    return recommendations
```

## 🔗 Related Documentation
- [Cache Management](cache-management.md) - Caching strategies
- [Monitoring](monitoring.md) - Performance monitoring
- [Architecture](../infrastructure/architecture.md) - System design
- [Performance](../infrastructure/performance.md) - System performance