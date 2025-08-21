# Duplicate Cleaner Documentation

The Duplicate Cleaner module provides intelligent detection and removal of duplicate comments, ensuring data quality and preventing skewed analysis results while preserving meaningful variations.

## 🎯 Overview

This module implements sophisticated algorithms to identify and handle duplicate content, near-duplicates, and repetitive patterns in customer feedback, using multiple detection methods and configurable thresholds.

### Core Capabilities
- **Exact Duplicate Detection** - Identical content identification
- **Near-Duplicate Detection** - Similar content with variations
- **Fuzzy Matching** - Handle typos and formatting differences  
- **Semantic Similarity** - Content-based duplicate detection
- **Intelligent Preservation** - Keep meaningful variations

## 🏗️ Deduplication Architecture

### Multi-Level Detection Pipeline
```python
class DuplicationDetectionArchitecture:
    """
    Multi-stage duplicate detection architecture
    """
    
    DETECTION_LEVELS = [
        'exact_match',      # Identical text
        'normalized_match', # After normalization
        'fuzzy_match',     # Similarity scoring
        'semantic_match',  # Meaning-based
        'pattern_match'    # Repetitive patterns
    ]
    
    SIMILARITY_METHODS = {
        'text_similarity': ['levenshtein', 'jaccard', 'cosine'],
        'semantic_similarity': ['word_vectors', 'sentence_embeddings'],
        'structural_similarity': ['length_ratio', 'word_order']
    }
```

## 🧹 Core Deduplication Engine

### Comprehensive Duplicate Cleaner
```python
class DuplicateCleaner:
    """
    Advanced duplicate detection and cleaning system
    """
    
    def __init__(self):
        self.text_normalizer = TextNormalizer()
        self.similarity_calculator = SimilarityCalculator()
        self.semantic_analyzer = SemanticAnalyzer()
        self.pattern_detector = PatternDetector()
        self.preservation_manager = PreservationManager()
        
        # Thresholds
        self.exact_threshold = 1.0
        self.fuzzy_threshold = 0.85
        self.semantic_threshold = 0.8
        self.pattern_threshold = 0.9
    
    def clean_duplicates(self, comments, options=None):
        """
        Clean duplicates using multi-level detection
        """
        if not comments:
            return []
        
        # Apply options
        thresholds = self.apply_options(options)
        
        # Stage 1: Exact duplicates
        stage1_result = self.remove_exact_duplicates(comments)
        
        # Stage 2: Normalized duplicates
        stage2_result = self.remove_normalized_duplicates(
            stage1_result['unique'],
            thresholds
        )
        
        # Stage 3: Fuzzy duplicates
        stage3_result = self.remove_fuzzy_duplicates(
            stage2_result['unique'],
            thresholds
        )
        
        # Stage 4: Semantic duplicates
        stage4_result = self.remove_semantic_duplicates(
            stage3_result['unique'],
            thresholds
        )
        
        # Stage 5: Pattern-based duplicates
        final_result = self.remove_pattern_duplicates(
            stage4_result['unique'],
            thresholds
        )
        
        # Compile results
        return {
            'unique_comments': final_result['unique'],
            'duplicate_groups': self.compile_duplicate_groups([
                stage1_result['duplicates'],
                stage2_result['duplicates'],
                stage3_result['duplicates'],
                stage4_result['duplicates'],
                final_result['duplicates']
            ]),
            'statistics': self.calculate_statistics(comments, final_result)
        }
    
    def remove_exact_duplicates(self, comments):
        """
        Remove exact text duplicates
        """
        seen = set()
        unique = []
        duplicates = []
        
        for comment in comments:
            text = comment.get('text', '').strip()
            
            if text not in seen:
                seen.add(text)
                unique.append(comment)
            else:
                duplicates.append({
                    'comment': comment,
                    'duplicate_of': self.find_original(unique, text),
                    'type': 'exact'
                })
        
        return {
            'unique': unique,
            'duplicates': duplicates
        }
```

## 🔍 Similarity Detection

### Advanced Similarity Calculator
```python
class SimilarityCalculator:
    """
    Calculate text similarity using multiple algorithms
    """
    
    def __init__(self):
        self.tokenizer = TextTokenizer()
        self.stemmer = SpanishStemmer()
        self.vectorizer = TfidfVectorizer()
    
    def calculate_similarity(self, text1, text2, method='composite'):
        """
        Calculate similarity between two texts
        """
        if method == 'composite':
            return self.composite_similarity(text1, text2)
        
        methods = {
            'levenshtein': self.levenshtein_similarity,
            'jaccard': self.jaccard_similarity,
            'cosine': self.cosine_similarity,
            'semantic': self.semantic_similarity
        }
        
        if method in methods:
            return methods[method](text1, text2)
        
        raise ValueError(f"Unknown similarity method: {method}")
    
    def composite_similarity(self, text1, text2):
        """
        Composite similarity using multiple methods
        """
        # Calculate individual similarities
        similarities = {
            'levenshtein': self.levenshtein_similarity(text1, text2),
            'jaccard': self.jaccard_similarity(text1, text2),
            'cosine': self.cosine_similarity(text1, text2)
        }
        
        # Weighted combination
        weights = {
            'levenshtein': 0.3,
            'jaccard': 0.3,
            'cosine': 0.4
        }
        
        composite_score = sum(
            similarities[method] * weight
            for method, weight in weights.items()
        )
        
        return {
            'composite': composite_score,
            'individual': similarities
        }
    
    def levenshtein_similarity(self, text1, text2):
        """
        Calculate Levenshtein distance similarity
        """
        distance = Levenshtein.distance(text1, text2)
        max_len = max(len(text1), len(text2))
        
        if max_len == 0:
            return 1.0
        
        similarity = 1 - (distance / max_len)
        return similarity
    
    def jaccard_similarity(self, text1, text2):
        """
        Calculate Jaccard similarity of word sets
        """
        # Tokenize and normalize
        words1 = set(self.tokenizer.tokenize(text1.lower()))
        words2 = set(self.tokenizer.tokenize(text2.lower()))
        
        # Remove stopwords
        words1 = self.remove_stopwords(words1)
        words2 = self.remove_stopwords(words2)
        
        # Calculate Jaccard index
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def cosine_similarity(self, text1, text2):
        """
        Calculate cosine similarity using TF-IDF vectors
        """
        # Create TF-IDF vectors
        documents = [text1, text2]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        
        return similarity
```

## 🧠 Semantic Analysis

### Semantic Duplicate Detector
```python
class SemanticAnalyzer:
    """
    Detect semantic duplicates using NLP techniques
    """
    
    def __init__(self):
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.topic_modeler = TopicModeler()
        self.emotion_analyzer = EmotionAnalyzer()
    
    def find_semantic_duplicates(self, comments, threshold=0.8):
        """
        Find semantically similar comments
        """
        # Extract texts
        texts = [comment.get('text', '') for comment in comments]
        
        # Generate embeddings
        embeddings = self.sentence_transformer.encode(texts)
        
        # Calculate pairwise similarities
        similarities = cosine_similarity(embeddings)
        
        # Find duplicate pairs
        duplicate_pairs = []
        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                similarity = similarities[i][j]
                
                if similarity >= threshold:
                    # Additional semantic checks
                    if self.validate_semantic_similarity(
                        comments[i], comments[j], similarity
                    ):
                        duplicate_pairs.append({
                            'comment1': comments[i],
                            'comment2': comments[j],
                            'similarity': similarity,
                            'type': 'semantic'
                        })
        
        return duplicate_pairs
    
    def validate_semantic_similarity(self, comment1, comment2, similarity):
        """
        Additional validation for semantic similarity
        """
        text1 = comment1.get('text', '')
        text2 = comment2.get('text', '')
        
        # Check sentiment consistency
        sentiment1 = self.get_sentiment(text1)
        sentiment2 = self.get_sentiment(text2)
        
        if abs(sentiment1 - sentiment2) > 0.3:
            return False  # Different sentiments
        
        # Check topic consistency
        topic1 = self.topic_modeler.get_topic(text1)
        topic2 = self.topic_modeler.get_topic(text2)
        
        if topic1 != topic2:
            return False  # Different topics
        
        # Check emotional consistency
        emotion1 = self.emotion_analyzer.analyze(text1)
        emotion2 = self.emotion_analyzer.analyze(text2)
        
        emotion_similarity = self.calculate_emotion_similarity(emotion1, emotion2)
        if emotion_similarity < 0.7:
            return False  # Different emotions
        
        return True
```

## 🔄 Text Normalization

### Advanced Text Normalizer
```python
class TextNormalizer:
    """
    Normalize text for duplicate detection
    """
    
    def __init__(self):
        self.stopwords = self.load_stopwords(['es', 'gn', 'en'])
        self.punctuation_translator = str.maketrans('', '', string.punctuation)
        self.accent_normalizer = AccentNormalizer()
    
    def normalize(self, text, level='standard'):
        """
        Normalize text with different levels of aggressiveness
        """
        if level == 'minimal':
            return self.minimal_normalization(text)
        elif level == 'standard':
            return self.standard_normalization(text)
        elif level == 'aggressive':
            return self.aggressive_normalization(text)
        
        return text
    
    def standard_normalization(self, text):
        """
        Standard normalization for duplicate detection
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Normalize accents
        text = self.accent_normalizer.normalize(text)
        
        # Remove punctuation except meaningful ones
        text = re.sub(r'[^\w\s¿¡!?.]', ' ', text)
        
        # Remove stopwords
        words = text.split()
        words = [w for w in words if w not in self.stopwords]
        
        return ' '.join(words)
    
    def aggressive_normalization(self, text):
        """
        Aggressive normalization for catching variations
        """
        # Start with standard normalization
        text = self.standard_normalization(text)
        
        # Remove all punctuation
        text = text.translate(self.punctuation_translator)
        
        # Stem words
        words = text.split()
        stemmed_words = [self.stem_word(word) for word in words]
        
        # Remove short words
        stemmed_words = [w for w in stemmed_words if len(w) > 2]
        
        # Sort words (to catch reordered text)
        stemmed_words.sort()
        
        return ' '.join(stemmed_words)
    
    def stem_word(self, word):
        """
        Stem word based on detected language
        """
        # Simple Spanish stemming rules
        spanish_suffixes = ['ción', 'sión', 'ando', 'iendo', 'mente']
        
        for suffix in spanish_suffixes:
            if word.endswith(suffix):
                return word[:-len(suffix)]
        
        return word
```

## 🎯 Pattern Detection

### Repetitive Pattern Detector
```python
class PatternDetector:
    """
    Detect repetitive patterns and spam-like content
    """
    
    def __init__(self):
        self.pattern_cache = {}
        self.spam_patterns = self.load_spam_patterns()
    
    def detect_patterns(self, comments):
        """
        Detect repetitive patterns in comments
        """
        patterns = {
            'repetitive_text': self.find_repetitive_text(comments),
            'template_responses': self.find_template_responses(comments),
            'spam_patterns': self.find_spam_patterns(comments),
            'generated_content': self.find_generated_content(comments)
        }
        
        return patterns
    
    def find_repetitive_text(self, comments):
        """
        Find comments with repetitive internal structure
        """
        repetitive = []
        
        for comment in comments:
            text = comment.get('text', '')
            
            # Check for repeated words
            words = text.split()
            word_counts = Counter(words)
            
            # Calculate repetition ratio
            unique_words = len(set(words))
            total_words = len(words)
            
            if total_words > 0:
                repetition_ratio = 1 - (unique_words / total_words)
                
                if repetition_ratio > 0.5:  # More than 50% repetition
                    repetitive.append({
                        'comment': comment,
                        'repetition_ratio': repetition_ratio,
                        'pattern_type': 'word_repetition'
                    })
            
            # Check for repeated phrases
            phrases = self.extract_phrases(text)
            phrase_counts = Counter(phrases)
            
            for phrase, count in phrase_counts.items():
                if count > 2 and len(phrase.split()) > 1:
                    repetitive.append({
                        'comment': comment,
                        'repeated_phrase': phrase,
                        'repetition_count': count,
                        'pattern_type': 'phrase_repetition'
                    })
        
        return repetitive
    
    def find_template_responses(self, comments):
        """
        Find comments that follow template patterns
        """
        templates = []
        
        # Extract potential templates
        for comment in comments:
            text = comment.get('text', '')
            template = self.extract_template(text)
            
            if template:
                templates.append({
                    'comment': comment,
                    'template': template,
                    'variables': self.extract_variables(text, template)
                })
        
        # Group by similar templates
        template_groups = self.group_similar_templates(templates)
        
        return template_groups
    
    def extract_template(self, text):
        """
        Extract template pattern from text
        """
        # Replace numbers with placeholder
        template = re.sub(r'\d+', '[NUM]', text)
        
        # Replace proper nouns with placeholder
        template = re.sub(r'\b[A-Z][a-z]+\b', '[NAME]', template)
        
        # Replace dates with placeholder
        template = re.sub(
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            '[DATE]',
            template
        )
        
        return template
```

## 🛡️ Preservation Logic

### Intelligent Duplicate Preservation
```python
class PreservationManager:
    """
    Manage which duplicates to preserve based on value
    """
    
    def __init__(self):
        self.value_calculator = ValueCalculator()
        self.metadata_analyzer = MetadataAnalyzer()
    
    def decide_preservation(self, duplicate_group):
        """
        Decide which comments to preserve from duplicate group
        """
        if len(duplicate_group) <= 1:
            return duplicate_group
        
        # Calculate value scores for each comment
        scored_comments = []
        for comment in duplicate_group:
            score = self.value_calculator.calculate_value(comment)
            scored_comments.append({
                'comment': comment,
                'value_score': score
            })
        
        # Sort by value score
        scored_comments.sort(key=lambda x: x['value_score'], reverse=True)
        
        # Determine preservation strategy
        strategy = self.determine_strategy(scored_comments)
        
        if strategy == 'keep_best':
            return [scored_comments[0]['comment']]
        
        elif strategy == 'keep_representative':
            return self.select_representative_samples(scored_comments)
        
        elif strategy == 'keep_all_valuable':
            threshold = self.calculate_value_threshold(scored_comments)
            return [
                sc['comment'] for sc in scored_comments
                if sc['value_score'] >= threshold
            ]
        
        return [scored_comments[0]['comment']]  # Default: keep best
    
    def determine_strategy(self, scored_comments):
        """
        Determine preservation strategy based on group characteristics
        """
        group_size = len(scored_comments)
        value_variance = self.calculate_value_variance(scored_comments)
        
        if group_size <= 3:
            return 'keep_best'
        
        elif value_variance > 0.3:
            return 'keep_all_valuable'
        
        elif group_size > 10:
            return 'keep_representative'
        
        return 'keep_best'
```

## 📊 Performance Optimization

### Efficient Duplicate Detection
```python
class OptimizedDuplicateDetector:
    """
    Performance-optimized duplicate detection
    """
    
    def __init__(self):
        self.hash_index = {}
        self.similarity_cache = LRUCache(maxsize=50000)
        self.bloom_filter = BloomFilter(capacity=1000000)
    
    def build_hash_index(self, comments):
        """
        Build hash index for fast exact duplicate detection
        """
        for i, comment in enumerate(comments):
            text = comment.get('text', '')
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            if text_hash not in self.hash_index:
                self.hash_index[text_hash] = []
            
            self.hash_index[text_hash].append(i)
    
    def fast_similarity_check(self, text1, text2):
        """
        Fast similarity check with caching
        """
        # Create cache key
        key = (hash(text1), hash(text2))
        
        # Check cache
        if key in self.similarity_cache:
            return self.similarity_cache[key]
        
        # Calculate similarity
        similarity = self.calculate_similarity(text1, text2)
        
        # Cache result
        self.similarity_cache[key] = similarity
        
        return similarity
    
    def parallel_detection(self, comments, num_workers=4):
        """
        Parallel duplicate detection
        """
        # Split comments into chunks
        chunk_size = len(comments) // num_workers
        chunks = [
            comments[i:i + chunk_size]
            for i in range(0, len(comments), chunk_size)
        ]
        
        # Process chunks in parallel
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(self.detect_chunk_duplicates, chunk)
                for chunk in chunks
            ]
            
            # Collect results
            chunk_results = [future.result() for future in futures]
        
        # Merge results
        return self.merge_chunk_results(chunk_results)
```

## 📈 Quality Metrics

### Deduplication Quality Assessment
```python
class QualityAssessment:
    """
    Assess quality of duplicate detection
    """
    
    def assess_quality(self, original_comments, cleaned_comments, duplicates):
        """
        Assess deduplication quality
        """
        metrics = {
            'reduction_rate': self.calculate_reduction_rate(
                original_comments, cleaned_comments
            ),
            'precision': self.calculate_precision(duplicates),
            'recall': self.estimate_recall(original_comments, duplicates),
            'f1_score': None,  # Calculated below
            'information_loss': self.estimate_information_loss(
                original_comments, cleaned_comments
            )
        }
        
        # Calculate F1 score
        if metrics['precision'] and metrics['recall']:
            metrics['f1_score'] = 2 * (
                metrics['precision'] * metrics['recall']
            ) / (metrics['precision'] + metrics['recall'])
        
        return metrics
    
    def calculate_reduction_rate(self, original, cleaned):
        """
        Calculate percentage reduction in data size
        """
        if not original:
            return 0.0
        
        return (len(original) - len(cleaned)) / len(original)
```

## 🔧 Configuration

### Duplicate Detection Settings
```python
DUPLICATE_DETECTION_CONFIG = {
    'thresholds': {
        'exact_match': 1.0,
        'fuzzy_match': 0.85,
        'semantic_match': 0.8,
        'pattern_match': 0.9
    },
    'normalization': {
        'level': 'standard',  # minimal, standard, aggressive
        'remove_stopwords': True,
        'stem_words': False,
        'normalize_accents': True
    },
    'similarity_methods': {
        'levenshtein_weight': 0.3,
        'jaccard_weight': 0.3,
        'cosine_weight': 0.4
    },
    'preservation': {
        'strategy': 'keep_best',  # keep_best, keep_representative, keep_all_valuable
        'value_threshold': 0.7,
        'max_representatives': 5
    },
    'performance': {
        'use_cache': True,
        'parallel_processing': True,
        'num_workers': 4,
        'batch_size': 1000
    }
}
```

## 🔗 Related Documentation
- [Comment Reader](comment-reader.md) - Input processing
- [Language Detector](language-detector.md) - Language-aware deduplication
- [Text Processing](../analysis-engines/language-processing.md) - Text analysis
- [Data Quality](../../user-guides/user-manual.md#data-quality) - Quality guidelines