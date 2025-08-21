# Language Processing Engine Documentation

The Language Processing Engine handles multilingual content analysis, specializing in Spanish (Paraguayan dialect) and Guaraní, with support for code-switching and mixed-language expressions common in Paraguay.

## 🌍 Overview

This engine provides comprehensive language detection, translation, and processing capabilities specifically tuned for the Paraguayan telecommunications market, handling the unique linguistic landscape where Spanish and Guaraní coexist.

### Core Capabilities
- **Language Detection** - Identifies Spanish, Guaraní, and mixed content
- **Automatic Translation** - Guaraní to Spanish translation for analysis
- **Dialect Recognition** - Paraguayan Spanish variant detection
- **Code-Switching Handling** - Mixed language within single comments
- **Cultural Localization** - Context-aware language interpretation

## 🗣️ Language Models

### Supported Languages
```python
class LanguageModels:
    """
    Language models for Paraguayan market
    """
    
    SUPPORTED_LANGUAGES = {
        'spanish': {
            'code': 'es-PY',
            'name': 'Spanish (Paraguay)',
            'variants': ['formal', 'informal', 'regional'],
            'confidence_threshold': 0.85,
            'analysis_model': 'native'
        },
        'guarani': {
            'code': 'gn',
            'name': 'Guaraní',
            'variants': ['jopara', 'academic', 'rural'],
            'confidence_threshold': 0.75,
            'analysis_model': 'translation_required'
        },
        'mixed': {
            'code': 'es-gn-mix',
            'name': 'Spanish-Guaraní Mix (Jopara)',
            'variants': ['urban_mix', 'rural_mix'],
            'confidence_threshold': 0.70,
            'analysis_model': 'hybrid'
        },
        'portuguese': {
            'code': 'pt-BR',
            'name': 'Portuguese (Border)',
            'variants': ['brazilian'],
            'confidence_threshold': 0.80,
            'analysis_model': 'translation_required'
        }
    }
```

### Guaraní Language Patterns
```python
GUARANI_PATTERNS = {
    'common_words': {
        'mba\'e': 'what/thing',
        'ndaipóri': 'there is not/no',
        'porã': 'good/nice',
        'vai': 'bad/ugly',
        'heta': 'many/much',
        'michĩ': 'little/small',
        'tuicha': 'big/large',
        'pya\'e': 'fast/quick',
        'mbegue': 'slow'
    },
    'expressions': {
        'che': 'I/my',
        'nde': 'you/your',
        'ha\'e': 'he/she/it',
        'ore': 'we (exclusive)',
        'ñande': 'we (inclusive)',
        'peẽ': 'you (plural)',
        'ha\'ekuéra': 'they'
    },
    'tech_terms': {
        'ñanduti': 'internet/web',
        'pumbyry': 'telephone',
        'kuatia ñe\'ẽ': 'message',
        'jehecha': 'video/see',
        'ñe\'ẽryru': 'email'
    }
}
```

## 🔍 Language Detection

### Multi-Layer Detection System
```python
class LanguageDetector:
    """
    Advanced language detection for Paraguay market
    """
    
    def detect_language(self, text):
        """
        Multi-layer language detection process
        """
        # Layer 1: Character-based detection
        char_analysis = self.analyze_character_patterns(text)
        
        # Layer 2: Word-based detection
        word_analysis = self.analyze_word_patterns(text)
        
        # Layer 3: N-gram analysis
        ngram_analysis = self.analyze_ngrams(text)
        
        # Layer 4: Diacritic detection (ñ, ã, ẽ, ĩ, õ, ũ, ỹ)
        diacritic_analysis = self.detect_guarani_diacritics(text)
        
        # Layer 5: Statistical model
        statistical_result = self.apply_statistical_model(text)
        
        # Combine results
        final_detection = self.combine_detection_results({
            'character': char_analysis,
            'word': word_analysis,
            'ngram': ngram_analysis,
            'diacritic': diacritic_analysis,
            'statistical': statistical_result
        })
        
        return final_detection
```

### Guaraní Diacritic Detection
```python
def detect_guarani_diacritics(self, text):
    """
    Detect Guaraní-specific diacritical marks
    """
    guarani_diacritics = {
        'ã': 'nasal_a',
        'ẽ': 'nasal_e',
        'ĩ': 'nasal_i',
        'õ': 'nasal_o',
        'ũ': 'nasal_u',
        'ỹ': 'nasal_y',
        '\'': 'glottal_stop'  # Puso
    }
    
    diacritic_count = 0
    for char in text:
        if char in guarani_diacritics:
            diacritic_count += 1
    
    # Calculate probability based on diacritic frequency
    text_length = len(text)
    diacritic_ratio = diacritic_count / max(text_length, 1)
    
    # Guaraní typically has 5-15% diacritical marks
    if diacritic_ratio > 0.05:
        return {'language': 'guarani', 'confidence': min(0.9, diacritic_ratio * 10)}
    
    return {'language': 'unknown', 'confidence': 0.0}
```

## 🔄 Code-Switching Detection

### Jopara (Mixed Language) Processing
```python
class JoparaProcessor:
    """
    Handles Spanish-Guaraní code-switching (Jopara)
    """
    
    def process_jopara(self, text):
        """
        Process mixed Spanish-Guaraní text
        """
        segments = []
        current_segment = {'text': '', 'language': None}
        
        words = text.split()
        for word in words:
            word_lang = self.detect_word_language(word)
            
            if word_lang != current_segment['language']:
                if current_segment['text']:
                    segments.append(current_segment)
                current_segment = {'text': word, 'language': word_lang}
            else:
                current_segment['text'] += ' ' + word
        
        if current_segment['text']:
            segments.append(current_segment)
        
        return {
            'segments': segments,
            'primary_language': self.determine_primary_language(segments),
            'mixing_pattern': self.analyze_mixing_pattern(segments),
            'translation_needed': self.needs_translation(segments)
        }
```

### Common Code-Switching Patterns
```python
CODE_SWITCHING_PATTERNS = {
    'insertion': {
        'example': 'El internet ko\'ãga está muy lento',
        'pattern': 'Spanish base + Guaraní word',
        'frequency': 'high'
    },
    'alternation': {
        'example': 'Ndaipóri señal, no hay conexión',
        'pattern': 'Complete clause switching',
        'frequency': 'medium'
    },
    'congruent_lexicalization': {
        'example': 'La conexión ha\'e muy vai últimamente',
        'pattern': 'Shared grammatical structure',
        'frequency': 'high'
    }
}
```

## 🔄 Translation Services

### Guaraní to Spanish Translation
```python
class GuaraniTranslator:
    """
    Translates Guaraní text to Spanish for analysis
    """
    
    def translate_guarani_to_spanish(self, guarani_text):
        """
        Translate Guaraní text to Spanish
        """
        # Step 1: Tokenize Guaraní text
        tokens = self.tokenize_guarani(guarani_text)
        
        # Step 2: Dictionary-based translation
        dict_translation = self.dictionary_translate(tokens)
        
        # Step 3: Context-aware translation
        context_translation = self.apply_context_rules(dict_translation)
        
        # Step 4: Neural translation (if available)
        if self.neural_model_available:
            neural_translation = self.neural_translate(guarani_text)
            
            # Step 5: Combine translations
            final_translation = self.combine_translations(
                dict_translation,
                context_translation,
                neural_translation
            )
        else:
            final_translation = context_translation
        
        return {
            'original': guarani_text,
            'translation': final_translation,
            'confidence': self.calculate_translation_confidence(final_translation),
            'method': 'hybrid' if self.neural_model_available else 'dictionary'
        }
```

### Translation Dictionary
```python
GUARANI_SPANISH_DICTIONARY = {
    # Common telecommunications terms
    'ñanduti': 'internet',
    'mbegue': 'lento',
    'pya\'e': 'rápido',
    'oñembyai': 'se cortó',
    'ndoikói': 'no funciona',
    'oiko porã': 'funciona bien',
    
    # Service-related terms
    'mba\'eichapa': 'cómo',
    'mba\'érepa': 'por qué',
    'araka\'e': 'cuándo',
    'moõ': 'dónde',
    'mboy': 'cuánto',
    
    # Sentiment expressions
    'iporãite': 'muy bueno',
    'ivaíete': 'muy malo',
    'avy\'a': 'estoy feliz',
    'che ñembyasy': 'estoy triste',
    'che poxy': 'estoy enojado',
    
    # Common phrases
    'ndaipóri problema': 'no hay problema',
    'oĩ problema': 'hay problema',
    'eipotápa': '¿quieres?',
    'aguyjé': 'gracias',
    'mba\'éichapa reime': 'cómo estás'
}
```

## 📊 Dialect Recognition

### Paraguayan Spanish Characteristics
```python
class ParaguayanSpanishDetector:
    """
    Detects Paraguayan Spanish dialect features
    """
    
    PARAGUAYAN_FEATURES = {
        'vocabulary': {
            'plata': 'dinero',
            'piola': 'bueno/tranquilo',
            'tipo': 'como/así',
            'luego': 'pues/entonces',
            'vaina': 'cosa',
            'chuchi': 'elegante'
        },
        'expressions': {
            'qué pio': 'qué diablos',
            'de balde': 'gratis',
            'al pedo': 'en vano',
            'está pynandi': 'está descalzo',
            'de repente': 'tal vez'
        },
        'grammatical': {
            'voseo': True,  # Use of 'vos' instead of 'tú'
            'leismo': False,
            'diminutive': '-ito/-ita',
            'guarani_influence': True
        }
    }
    
    def detect_dialect(self, text):
        """
        Identify Paraguayan Spanish dialect markers
        """
        markers_found = []
        
        # Check vocabulary
        for py_word, standard in self.PARAGUAYAN_FEATURES['vocabulary'].items():
            if py_word in text.lower():
                markers_found.append(('vocabulary', py_word))
        
        # Check expressions
        for expression in self.PARAGUAYAN_FEATURES['expressions']:
            if expression in text.lower():
                markers_found.append(('expression', expression))
        
        # Check voseo usage
        if self.detect_voseo(text):
            markers_found.append(('grammar', 'voseo'))
        
        confidence = min(1.0, len(markers_found) * 0.2)
        
        return {
            'dialect': 'paraguayan_spanish' if markers_found else 'standard_spanish',
            'markers': markers_found,
            'confidence': confidence
        }
```

## 🔧 Processing Pipeline

### Complete Language Processing Flow
```python
class LanguageProcessingPipeline:
    """
    End-to-end language processing pipeline
    """
    
    def process_comment(self, comment):
        """
        Complete language processing workflow
        """
        # Step 1: Detect language
        language_detection = self.detect_language(comment)
        
        # Step 2: Handle based on language
        if language_detection['language'] == 'guarani':
            # Translate to Spanish
            translation = self.translate_guarani_to_spanish(comment)
            processed_text = translation['translation']
            processing_note = 'translated_from_guarani'
            
        elif language_detection['language'] == 'mixed':
            # Process Jopara
            jopara_result = self.process_jopara(comment)
            processed_text = self.extract_processable_text(jopara_result)
            processing_note = 'mixed_language_processed'
            
        else:  # Spanish
            # Check dialect
            dialect = self.detect_dialect(comment)
            processed_text = self.normalize_dialect(comment, dialect)
            processing_note = f'spanish_{dialect["dialect"]}'
        
        # Step 3: Prepare for analysis
        analysis_ready = {
            'original_text': comment,
            'processed_text': processed_text,
            'language': language_detection,
            'processing_note': processing_note,
            'confidence': self.calculate_overall_confidence(language_detection)
        }
        
        return analysis_ready
```

## 📈 Language Statistics

### Language Distribution Analysis
```python
def analyze_language_distribution(comments):
    """
    Analyze language usage patterns in dataset
    """
    statistics = {
        'total_comments': len(comments),
        'language_counts': {},
        'code_switching_frequency': 0,
        'dialect_distribution': {},
        'translation_required': 0,
        'confidence_distribution': []
    }
    
    for comment in comments:
        result = process_comment(comment)
        
        # Count languages
        lang = result['language']['language']
        statistics['language_counts'][lang] = statistics['language_counts'].get(lang, 0) + 1
        
        # Track code-switching
        if lang == 'mixed':
            statistics['code_switching_frequency'] += 1
        
        # Track translations needed
        if result['processing_note'].startswith('translated'):
            statistics['translation_required'] += 1
        
        # Confidence distribution
        statistics['confidence_distribution'].append(result['confidence'])
    
    # Calculate percentages
    for lang, count in statistics['language_counts'].items():
        statistics[f'{lang}_percentage'] = (count / statistics['total_comments']) * 100
    
    return statistics
```

## 🌐 Cultural Linguistic Context

### Regional Language Variations
```python
REGIONAL_VARIATIONS = {
    'asuncion_metropolitan': {
        'spanish_dominance': 0.85,
        'guarani_usage': 0.15,
        'code_switching': 'moderate',
        'formality': 'variable'
    },
    'interior_cities': {
        'spanish_dominance': 0.60,
        'guarani_usage': 0.40,
        'code_switching': 'high',
        'formality': 'informal'
    },
    'rural_areas': {
        'spanish_dominance': 0.30,
        'guarani_usage': 0.70,
        'code_switching': 'low',
        'formality': 'traditional'
    },
    'border_regions': {
        'spanish_dominance': 0.50,
        'guarani_usage': 0.30,
        'portuguese_influence': 0.20,
        'code_switching': 'complex'
    }
}
```

### Language Preference by Context
```python
def determine_language_preference(customer_profile, interaction_type):
    """
    Determine preferred language for customer communication
    """
    preferences = {
        'technical_support': {
            'preferred': 'spanish',
            'reason': 'technical_terms',
            'guarani_acceptable': True
        },
        'billing_inquiry': {
            'preferred': 'spanish',
            'reason': 'formal_context',
            'guarani_acceptable': True
        },
        'general_feedback': {
            'preferred': 'customer_choice',
            'reason': 'comfort',
            'guarani_acceptable': True
        },
        'complaint': {
            'preferred': 'native_language',
            'reason': 'emotional_expression',
            'guarani_acceptable': True
        }
    }
    
    return preferences.get(interaction_type, {'preferred': 'spanish', 'guarani_acceptable': True})
```

## 🚀 Optimization Strategies

### Performance Optimization
```python
class LanguageProcessingOptimizer:
    """
    Optimizes language processing performance
    """
    
    def __init__(self):
        self.cache = LanguageCache()
        self.precompiled_patterns = self.precompile_patterns()
        self.translation_cache = TranslationCache()
    
    def optimize_detection(self, text):
        """
        Optimized language detection with caching
        """
        # Check cache first
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cached_result = self.cache.get(text_hash)
        
        if cached_result:
            return cached_result
        
        # Use precompiled patterns for faster matching
        result = self.detect_with_precompiled_patterns(text)
        
        # Cache result
        self.cache.set(text_hash, result, ttl=3600)
        
        return result
```

### Batch Processing
```python
def batch_process_languages(comments, batch_size=100):
    """
    Efficient batch processing for language detection
    """
    results = []
    
    for batch in chunks(comments, batch_size):
        # Process batch in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            batch_results = list(executor.map(process_comment, batch))
        
        results.extend(batch_results)
    
    return results
```

## 📊 Quality Metrics

### Translation Quality Assessment
```python
def assess_translation_quality(original, translation):
    """
    Evaluate translation quality
    """
    metrics = {
        'semantic_similarity': calculate_semantic_similarity(original, translation),
        'keyword_preservation': check_keyword_preservation(original, translation),
        'sentiment_consistency': verify_sentiment_consistency(original, translation),
        'length_ratio': len(translation) / len(original),
        'confidence_score': calculate_confidence(translation)
    }
    
    overall_quality = sum(metrics.values()) / len(metrics)
    
    return {
        'quality_score': overall_quality,
        'metrics': metrics,
        'acceptable': overall_quality > 0.7
    }
```

## 🔗 Related Documentation
- [Sentiment Analysis](sentiment-analysis.md) - Language-aware sentiment detection
- [Cultural Context](emotion-analysis.md) - Cultural expression patterns
- [Data Processing](../data-processing/language-detector.md) - Technical implementation
- [API Integration](../../backend/api/openai-integration.md) - Translation services