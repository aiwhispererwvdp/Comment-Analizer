# Language Detector Documentation

The Language Detector module provides sophisticated multi-language detection capabilities, specifically optimized for Spanish, Guaraní, and mixed-language content common in Paraguayan customer feedback.

## 🎯 Overview

This module implements advanced language detection algorithms to accurately identify languages in customer comments, handling code-switching, mixed languages, and regional dialects with high precision.

### Core Capabilities
- **Multi-Language Detection** - Spanish, Guaraní, English, Portuguese
- **Mixed Language Support** - Handle code-switching and Jopará
- **Dialect Recognition** - Paraguayan Spanish variations
- **Confidence Scoring** - Reliability metrics for detection
- **Performance Optimization** - Fast detection for real-time processing

## 🏗️ Detection Architecture

### Language Detection Pipeline
```python
class LanguageDetectionArchitecture:
    """
    Multi-stage language detection architecture
    """
    
    DETECTION_STAGES = [
        'preprocessing',
        'character_analysis',
        'lexical_analysis',
        'statistical_modeling',
        'contextual_analysis',
        'confidence_calculation'
    ]
    
    SUPPORTED_LANGUAGES = {
        'es': {'name': 'Spanish', 'iso_639_1': 'es', 'variants': ['es-PY', 'es-AR']},
        'gn': {'name': 'Guaraní', 'iso_639_1': 'gn', 'variants': ['gn-PY']},
        'jopara': {'name': 'Jopará', 'iso_639_1': 'gn-es', 'mixed': True},
        'en': {'name': 'English', 'iso_639_1': 'en', 'variants': ['en-US']},
        'pt': {'name': 'Portuguese', 'iso_639_1': 'pt', 'variants': ['pt-BR']}
    }
```

## 🔍 Core Detection Engine

### Advanced Language Detector
```python
class LanguageDetector:
    """
    Sophisticated language detection with Guaraní support
    """
    
    def __init__(self):
        self.character_analyzer = CharacterAnalyzer()
        self.lexical_analyzer = LexicalAnalyzer()
        self.statistical_model = StatisticalLanguageModel()
        self.guarani_detector = GuaraniDetector()
        self.confidence_calculator = ConfidenceCalculator()
        
        # Load language models
        self.load_language_models()
    
    def detect(self, text, detailed=False):
        """
        Detect language with confidence scoring
        """
        if not text or len(text.strip()) < 3:
            return {'language': 'unknown', 'confidence': 0.0}
        
        # Preprocess text
        processed_text = self.preprocess(text)
        
        # Multiple detection methods
        detection_results = {
            'character': self.character_analyzer.analyze(processed_text),
            'lexical': self.lexical_analyzer.analyze(processed_text),
            'statistical': self.statistical_model.predict(processed_text),
            'guarani': self.guarani_detector.detect(processed_text)
        }
        
        # Check for mixed language
        if self.is_mixed_language(detection_results):
            return self.handle_mixed_language(text, detection_results, detailed)
        
        # Combine results
        final_result = self.combine_results(detection_results)
        
        # Calculate confidence
        confidence = self.confidence_calculator.calculate(
            detection_results,
            final_result
        )
        
        if detailed:
            return {
                'language': final_result,
                'confidence': confidence,
                'details': detection_results,
                'language_distribution': self.get_language_distribution(text)
            }
        
        return {
            'language': final_result,
            'confidence': confidence
        }
    
    def detect_batch(self, texts):
        """
        Efficient batch language detection
        """
        results = []
        
        # Group similar texts for efficiency
        grouped = self.group_similar_texts(texts)
        
        for group in grouped:
            if len(group) == 1:
                # Single text
                results.append(self.detect(group[0]))
            else:
                # Process group together
                group_result = self.detect_group(group)
                results.extend(group_result)
        
        return results
```

## 🎭 Guaraní Detection

### Specialized Guaraní Detector
```python
class GuaraniDetector:
    """
    Specialized detector for Guaraní and Jopará
    """
    
    def __init__(self):
        self.guarani_patterns = self.load_guarani_patterns()
        self.jopara_indicators = self.load_jopara_indicators()
        self.nasal_detector = NasalVowelDetector()
        
    def detect(self, text):
        """
        Detect Guaraní with dialect variations
        """
        features = {
            'guarani_words': self.count_guarani_words(text),
            'nasal_vowels': self.nasal_detector.detect(text),
            'particles': self.detect_particles(text),
            'morphology': self.analyze_morphology(text),
            'jopara_score': self.calculate_jopara_score(text)
        }
        
        # Pure Guaraní detection
        if features['guarani_words'] > 0.7:
            return {
                'language': 'gn',
                'variant': 'pure',
                'confidence': features['guarani_words']
            }
        
        # Jopará detection (mixed Spanish-Guaraní)
        if features['jopara_score'] > 0.5:
            return {
                'language': 'jopara',
                'variant': 'mixed',
                'confidence': features['jopara_score'],
                'mixture_ratio': self.calculate_mixture_ratio(text)
            }
        
        return None
    
    def count_guarani_words(self, text):
        """
        Count Guaraní words in text
        """
        words = text.lower().split()
        guarani_count = 0
        
        for word in words:
            if self.is_guarani_word(word):
                guarani_count += 1
        
        return guarani_count / len(words) if words else 0
    
    def is_guarani_word(self, word):
        """
        Check if word is Guaraní
        """
        # Check common Guaraní words
        common_words = {
            'che', 'nde', 'ha', 'pe', 'mba\'e', 'avei', 'katu',
            'porã', 'vai', 'guasu', 'michi', 'puku', 'mbegue',
            'heta', 'mbovy', 'ñande', 'ore', 'peẽ', 'ha\'ekuéra'
        }
        
        if word in common_words:
            return True
        
        # Check Guaraní patterns
        guarani_patterns = [
            r'.*mb.*',  # mb combination
            r'.*nd.*',  # nd combination
            r'.*ng.*',  # ng combination
            r'.*ñ.*',   # ñ character
            r'.*\'.*',  # glottal stop
            r'.*ã.*',   # nasal vowel
            r'.*ẽ.*',   # nasal vowel
            r'.*ĩ.*',   # nasal vowel
            r'.*õ.*',   # nasal vowel
            r'.*ũ.*',   # nasal vowel
            r'.*ỹ.*'    # nasal y
        ]
        
        for pattern in guarani_patterns:
            if re.match(pattern, word):
                return True
        
        return False
    
    def detect_particles(self, text):
        """
        Detect Guaraní grammatical particles
        """
        particles = {
            'ko': 'demonstrative',
            'pe': 'locative',
            'gui': 'ablative',
            'ndi': 'negative',
            'na': 'negative',
            've': 'more',
            'ite': 'very',
            'pa': 'question',
            'piko': 'question'
        }
        
        found_particles = []
        words = text.lower().split()
        
        for word in words:
            for particle, type in particles.items():
                if word.endswith(particle) or word == particle:
                    found_particles.append((particle, type))
        
        return found_particles
```

## 📊 Statistical Models

### N-gram Language Model
```python
class StatisticalLanguageModel:
    """
    Statistical n-gram models for language identification
    """
    
    def __init__(self):
        self.models = {}
        self.n = 3  # trigram model
        self.load_pretrained_models()
    
    def predict(self, text):
        """
        Predict language using n-gram analysis
        """
        # Generate n-grams from text
        text_ngrams = self.generate_ngrams(text, self.n)
        
        # Calculate probability for each language
        scores = {}
        
        for lang, model in self.models.items():
            score = self.calculate_probability(text_ngrams, model)
            scores[lang] = score
        
        # Return language with highest score
        if scores:
            best_lang = max(scores, key=scores.get)
            return {
                'language': best_lang,
                'score': scores[best_lang],
                'all_scores': scores
            }
        
        return None
    
    def generate_ngrams(self, text, n):
        """
        Generate character n-grams from text
        """
        text = ' ' + text.lower() + ' '
        ngrams = []
        
        for i in range(len(text) - n + 1):
            ngram = text[i:i + n]
            ngrams.append(ngram)
        
        return ngrams
    
    def train_model(self, texts, language):
        """
        Train n-gram model for a language
        """
        model = defaultdict(int)
        total_ngrams = 0
        
        for text in texts:
            ngrams = self.generate_ngrams(text, self.n)
            for ngram in ngrams:
                model[ngram] += 1
                total_ngrams += 1
        
        # Convert to probabilities
        for ngram in model:
            model[ngram] = model[ngram] / total_ngrams
        
        self.models[language] = dict(model)
        
        return model
```

## 🔤 Character Analysis

### Character-Based Detection
```python
class CharacterAnalyzer:
    """
    Analyze character distributions for language detection
    """
    
    def __init__(self):
        self.char_frequencies = self.load_character_frequencies()
        self.special_chars = self.load_special_characters()
    
    def analyze(self, text):
        """
        Analyze character distribution
        """
        # Count character frequencies
        char_counts = defaultdict(int)
        total_chars = 0
        
        for char in text.lower():
            if char.isalpha():
                char_counts[char] += 1
                total_chars += 1
        
        # Convert to frequencies
        char_freq = {}
        for char, count in char_counts.items():
            char_freq[char] = count / total_chars
        
        # Compare with language profiles
        language_scores = {}
        
        for lang, profile in self.char_frequencies.items():
            score = self.calculate_similarity(char_freq, profile)
            language_scores[lang] = score
        
        # Check for special characters
        special_char_lang = self.detect_by_special_chars(text)
        if special_char_lang:
            language_scores[special_char_lang] = \
                language_scores.get(special_char_lang, 0) + 0.3
        
        # Return best match
        if language_scores:
            best_lang = max(language_scores, key=language_scores.get)
            return {
                'language': best_lang,
                'score': language_scores[best_lang]
            }
        
        return None
    
    def detect_by_special_chars(self, text):
        """
        Detect language by special characters
        """
        # Guaraní special characters
        if any(c in text for c in 'ãẽĩõũỹ'):
            return 'gn'
        
        # Spanish special characters
        if 'ñ' in text and not any(c in text for c in 'ãẽĩõũỹ'):
            return 'es'
        
        return None
```

## 🎯 Mixed Language Detection

### Jopará and Code-Switching Handler
```python
class MixedLanguageDetector:
    """
    Handle mixed language content (Jopará, code-switching)
    """
    
    def __init__(self):
        self.spanish_detector = SpanishDetector()
        self.guarani_detector = GuaraniDetector()
        self.boundary_detector = LanguageBoundaryDetector()
    
    def analyze_mixed_content(self, text):
        """
        Analyze mixed language content
        """
        # Split into segments
        segments = self.segment_text(text)
        
        # Detect language for each segment
        segment_languages = []
        for segment in segments:
            lang = self.detect_segment_language(segment)
            segment_languages.append({
                'text': segment,
                'language': lang['language'],
                'confidence': lang['confidence']
            })
        
        # Analyze mixing pattern
        mixing_pattern = self.analyze_mixing_pattern(segment_languages)
        
        # Determine overall classification
        if mixing_pattern['type'] == 'jopara':
            return {
                'language': 'jopara',
                'primary': mixing_pattern['primary_language'],
                'secondary': mixing_pattern['secondary_language'],
                'mixing_ratio': mixing_pattern['ratio'],
                'segments': segment_languages
            }
        
        elif mixing_pattern['type'] == 'code_switching':
            return {
                'language': 'mixed',
                'languages': mixing_pattern['languages'],
                'switching_points': mixing_pattern['switch_points'],
                'segments': segment_languages
            }
        
        return {
            'language': mixing_pattern['dominant_language'],
            'confidence': mixing_pattern['confidence']
        }
    
    def segment_text(self, text):
        """
        Segment text by potential language boundaries
        """
        # Use punctuation and conjunctions as boundaries
        boundaries = r'[.!?;,]|\s(?:y|e|o|u|pero|ha|térã)\s'
        segments = re.split(boundaries, text)
        
        # Filter empty segments
        return [s.strip() for s in segments if s.strip()]
    
    def analyze_mixing_pattern(self, segments):
        """
        Analyze pattern of language mixing
        """
        if not segments:
            return {'type': 'unknown'}
        
        # Count languages
        lang_counts = defaultdict(int)
        for seg in segments:
            lang_counts[seg['language']] += 1
        
        # Calculate mixing metrics
        total_segments = len(segments)
        languages = list(lang_counts.keys())
        
        # Jopará pattern: frequent mixing of Spanish and Guaraní
        if set(languages) == {'es', 'gn'} or 'jopara' in languages:
            spanish_ratio = lang_counts.get('es', 0) / total_segments
            guarani_ratio = lang_counts.get('gn', 0) / total_segments
            
            return {
                'type': 'jopara',
                'primary_language': 'es' if spanish_ratio > guarani_ratio else 'gn',
                'secondary_language': 'gn' if spanish_ratio > guarani_ratio else 'es',
                'ratio': {'es': spanish_ratio, 'gn': guarani_ratio}
            }
        
        # Code-switching pattern
        switches = self.count_language_switches(segments)
        if switches > 1:
            return {
                'type': 'code_switching',
                'languages': languages,
                'switch_points': switches,
                'dominant_language': max(lang_counts, key=lang_counts.get)
            }
        
        # Single dominant language
        return {
            'type': 'monolingual',
            'dominant_language': max(lang_counts, key=lang_counts.get),
            'confidence': max(lang_counts.values()) / total_segments
        }
```

## 📈 Confidence Scoring

### Confidence Calculator
```python
class ConfidenceCalculator:
    """
    Calculate detection confidence scores
    """
    
    def calculate(self, detection_results, final_language):
        """
        Calculate overall confidence score
        """
        scores = []
        weights = {
            'character': 0.2,
            'lexical': 0.3,
            'statistical': 0.3,
            'guarani': 0.2
        }
        
        for method, result in detection_results.items():
            if result and result.get('language') == final_language:
                score = result.get('score', result.get('confidence', 0.5))
                weight = weights.get(method, 0.25)
                scores.append(score * weight)
        
        # Calculate weighted average
        if scores:
            confidence = sum(scores) / sum(weights.values())
        else:
            confidence = 0.0
        
        # Adjust for text length
        confidence = self.adjust_for_length(confidence, len(text))
        
        # Ensure valid range
        return max(0.0, min(1.0, confidence))
    
    def adjust_for_length(self, confidence, text_length):
        """
        Adjust confidence based on text length
        """
        if text_length < 20:
            # Very short text, reduce confidence
            return confidence * 0.7
        elif text_length < 50:
            # Short text
            return confidence * 0.85
        elif text_length > 500:
            # Long text, increase confidence
            return min(1.0, confidence * 1.1)
        
        return confidence
```

## 🚀 Performance Optimization

### Cached Detection
```python
class CachedLanguageDetector:
    """
    Language detector with caching for performance
    """
    
    def __init__(self):
        self.detector = LanguageDetector()
        self.cache = LRUCache(maxsize=10000)
        self.bloom_filter = BloomFilter(capacity=100000)
    
    def detect(self, text):
        """
        Detect with caching
        """
        # Generate cache key
        cache_key = self.generate_cache_key(text)
        
        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Check bloom filter for definitely not cached
        if not self.bloom_filter.check(cache_key):
            # Definitely not in cache, detect
            result = self.detector.detect(text)
            
            # Add to cache and bloom filter
            self.cache[cache_key] = result
            self.bloom_filter.add(cache_key)
            
            return result
        
        # Might be in cache, detect anyway
        result = self.detector.detect(text)
        self.cache[cache_key] = result
        
        return result
```

## 🧪 Language Testing

### Detection Accuracy Testing
```python
class LanguageDetectionTester:
    """
    Test language detection accuracy
    """
    
    def test_accuracy(self, test_data):
        """
        Test detection accuracy on labeled data
        """
        detector = LanguageDetector()
        results = {
            'correct': 0,
            'incorrect': 0,
            'by_language': defaultdict(lambda: {'correct': 0, 'total': 0})
        }
        
        for text, expected_lang in test_data:
            detected = detector.detect(text)
            detected_lang = detected['language']
            
            if detected_lang == expected_lang:
                results['correct'] += 1
                results['by_language'][expected_lang]['correct'] += 1
            else:
                results['incorrect'] += 1
            
            results['by_language'][expected_lang]['total'] += 1
        
        # Calculate metrics
        total = results['correct'] + results['incorrect']
        results['accuracy'] = results['correct'] / total if total > 0 else 0
        
        # Per-language accuracy
        for lang in results['by_language']:
            lang_data = results['by_language'][lang]
            lang_data['accuracy'] = \
                lang_data['correct'] / lang_data['total'] \
                if lang_data['total'] > 0 else 0
        
        return results
```

## 🔧 Configuration

### Language Detection Settings
```python
LANGUAGE_DETECTION_CONFIG = {
    'supported_languages': ['es', 'gn', 'jopara', 'en', 'pt'],
    'default_language': 'es',
    'min_confidence': 0.5,
    'detection_methods': {
        'character_analysis': True,
        'lexical_analysis': True,
        'statistical_model': True,
        'special_detectors': True
    },
    'performance': {
        'use_cache': True,
        'cache_size': 10000,
        'batch_size': 100,
        'parallel_detection': True
    },
    'guarani_settings': {
        'detect_jopara': True,
        'nasal_vowel_support': True,
        'dialect_variants': ['academic', 'colloquial']
    }
}
```

## 🔗 Related Documentation
- [Comment Reader](comment-reader.md) - Text extraction
- [Duplicate Cleaner](duplicate-cleaner.md) - Text processing
- [Language Processing](../analysis-engines/language-processing.md) - Language analysis
- [Sentiment Analysis](../analysis-engines/sentiment-analysis.md) - Language-specific sentiment