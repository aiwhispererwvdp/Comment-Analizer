# Sentiment Analysis Engine Documentation

The Sentiment Analysis Engine is the core component responsible for determining customer satisfaction levels, emotional states, and opinion polarity in customer feedback about Personal Paraguay's fiber-to-the-home services.

## 🎯 Overview

The sentiment analysis engine uses advanced AI models to classify customer comments into positive, negative, or neutral sentiments while also detecting nuanced emotions and confidence levels.

### Core Capabilities
- **Multi-dimensional Sentiment Classification** - Beyond simple positive/negative
- **Emotion Detection** - Joy, anger, sadness, fear, surprise
- **Confidence Scoring** - Reliability metrics for each analysis
- **Cultural Context Awareness** - Paraguayan cultural nuances
- **Multilingual Support** - Spanish and Guaraní sentiment detection

## 🧠 Technical Architecture

### Engine Components
```python
class SentimentAnalysisEngine:
    """
    Advanced sentiment analysis with cultural context
    """
    def __init__(self):
        self.openai_analyzer = OpenAISentimentAnalyzer()
        self.emotion_detector = EmotionDetector()
        self.confidence_calculator = ConfidenceCalculator()
        self.cultural_processor = CulturalContextProcessor()
```

### Analysis Pipeline
```
Input Comment → Language Detection → Cultural Context Processing 
    → Sentiment Analysis → Emotion Detection → Confidence Scoring → Result
```

## 📊 Sentiment Classification

### Classification Categories

#### Primary Sentiments
- **Positive** (Score: 0.6 to 1.0)
  - Customer satisfaction expressions
  - Service praise and compliments
  - Recommendations to others
  - Problem resolution acknowledgments

- **Negative** (Score: -1.0 to -0.2)
  - Service complaints
  - Problem reports
  - Frustration expressions
  - Cancellation threats

- **Neutral** (Score: -0.2 to 0.6)
  - Factual statements
  - Information requests
  - Technical descriptions
  - Neutral observations

#### Mixed Sentiments
```python
def detect_mixed_sentiment(comment):
    """
    Handles comments with both positive and negative elements
    
    Example: "The speed is great but customer service is terrible"
    Returns: {
        'overall': 'mixed',
        'positive_aspects': ['speed'],
        'negative_aspects': ['customer_service'],
        'dominant_sentiment': 'negative'
    }
    """
```

### Sentiment Intensity Levels
- **Strong Positive** (>0.85): Extremely satisfied, enthusiastic
- **Moderate Positive** (0.6-0.85): Generally satisfied
- **Mild Positive** (0.3-0.6): Slightly positive
- **Neutral** (-0.3 to 0.3): Balanced or factual
- **Mild Negative** (-0.6 to -0.3): Slightly dissatisfied
- **Moderate Negative** (-0.85 to -0.6): Clearly dissatisfied
- **Strong Negative** (<-0.85): Extremely dissatisfied, angry

## 😊 Emotion Detection

### Emotion Model
```python
class EmotionDetector:
    """
    Multi-dimensional emotion analysis
    """
    
    EMOTIONS = {
        'joy': {
            'keywords': ['excelente', 'feliz', 'contento', 'genial'],
            'patterns': ['muy satisfecho', 'super rápido', 'lo mejor'],
            'weight': 1.2  # Positive multiplier
        },
        'anger': {
            'keywords': ['furioso', 'enojado', 'harto', 'terrible'],
            'patterns': ['no puedo más', 'es un desastre', 'pésimo servicio'],
            'weight': 1.5  # Strong negative indicator
        },
        'sadness': {
            'keywords': ['decepcionado', 'triste', 'lamentable'],
            'patterns': ['esperaba más', 'no es lo que prometieron'],
            'weight': 1.1
        },
        'fear': {
            'keywords': ['preocupado', 'inquieto', 'dudoso'],
            'patterns': ['no sé si', 'me preocupa que', 'tengo miedo de'],
            'weight': 1.0
        },
        'surprise': {
            'keywords': ['sorprendido', 'asombrado', 'increíble'],
            'patterns': ['no esperaba', 'me sorprendió', 'wow'],
            'weight': 0.8  # Can be positive or negative
        }
    }
```

### Emotion Analysis Process
1. **Text Preprocessing** - Clean and normalize text
2. **Keyword Detection** - Identify emotion indicators
3. **Pattern Matching** - Find emotional expressions
4. **Intensity Calculation** - Measure emotion strength
5. **Emotion Mapping** - Map to standard emotions

### Emotion Scoring
```python
def calculate_emotion_scores(comment):
    """
    Returns emotion scores from 0 to 1 for each emotion
    
    Output: {
        'joy': 0.7,
        'anger': 0.1,
        'sadness': 0.2,
        'fear': 0.0,
        'surprise': 0.3
    }
    """
```

## 🎯 Confidence Scoring

### Confidence Calculation Factors
```python
class ConfidenceCalculator:
    """
    Calculates confidence in sentiment analysis results
    """
    
    def calculate_confidence(self, analysis_result):
        factors = {
            'text_clarity': self.assess_text_clarity(),
            'language_confidence': self.assess_language_detection(),
            'sentiment_strength': self.assess_sentiment_strength(),
            'emotion_consistency': self.assess_emotion_consistency(),
            'model_certainty': self.get_model_confidence()
        }
        
        # Weighted average of all factors
        weights = {
            'text_clarity': 0.2,
            'language_confidence': 0.15,
            'sentiment_strength': 0.25,
            'emotion_consistency': 0.2,
            'model_certainty': 0.2
        }
        
        return self.weighted_average(factors, weights)
```

### Confidence Levels
- **Very High** (90-100%): Highly reliable results
- **High** (80-89%): Reliable for decision making
- **Medium** (70-79%): Generally reliable
- **Low** (60-69%): Review recommended
- **Very Low** (<60%): Manual review required

## 🌍 Cultural Context Processing

### Paraguayan Context Adaptation
```python
class CulturalContextProcessor:
    """
    Adapts sentiment analysis for Paraguayan cultural context
    """
    
    CULTURAL_MODIFIERS = {
        'guarani_expressions': {
            'ndaipóri problema': ('no problem', 'positive'),
            'heterei': ('very much', 'intensifier'),
            'mbore': ('boring/slow', 'negative')
        },
        'local_slang': {
            'de diez': ('excellent', 'strong_positive'),
            'plata': ('money', 'neutral'),
            'pio': ('nothing/not working', 'negative')
        },
        'cultural_patterns': {
            'indirect_complaint': 0.7,  # Tendency to complain indirectly
            'positive_politeness': 1.2,  # Overly polite even when dissatisfied
            'group_reference': 1.1  # References to family/community
        }
    }
```

### Regional Variations
- **Urban Areas** (Asunción): More direct communication
- **Rural Areas**: More indirect, polite expressions
- **Border Regions**: Mixed language influences

## 🔧 Implementation Details

### API Integration
```python
def analyze_sentiment_with_openai(comment):
    """
    OpenAI GPT-4 sentiment analysis
    """
    prompt = f"""
    Analyze the sentiment of this customer comment about fiber internet service in Paraguay.
    Consider cultural context and local expressions.
    
    Comment: "{comment}"
    
    Return JSON with:
    - sentiment: positive/negative/neutral/mixed
    - score: -1.0 to 1.0
    - confidence: 0-100%
    - emotions: joy, anger, sadness, fear, surprise (0-1 each)
    - cultural_notes: any cultural context considerations
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1  # Low temperature for consistency
    )
    
    return parse_sentiment_response(response)
```

### Batch Processing
```python
def process_sentiment_batch(comments, batch_size=50):
    """
    Efficient batch processing for large datasets
    """
    results = []
    for batch in chunks(comments, batch_size):
        batch_prompt = create_batch_sentiment_prompt(batch)
        batch_results = analyze_batch_sentiment(batch_prompt)
        results.extend(batch_results)
    return results
```

## 📈 Quality Assurance

### Validation Rules
```python
SENTIMENT_VALIDATION_RULES = {
    'consistency_check': {
        'description': 'Emotions should align with sentiment',
        'rule': lambda r: validate_emotion_sentiment_consistency(r)
    },
    'confidence_threshold': {
        'description': 'Minimum confidence for production use',
        'rule': lambda r: r['confidence'] >= 0.7
    },
    'score_range': {
        'description': 'Score must be between -1 and 1',
        'rule': lambda r: -1 <= r['score'] <= 1
    }
}
```

### Performance Metrics
- **Accuracy Target**: >90% for clear Spanish text
- **Processing Speed**: <2 seconds per comment
- **Batch Efficiency**: 50-100 comments per API call
- **Cache Hit Rate**: >40% for similar comments

## 🎨 Sentiment Visualization

### Result Structure
```json
{
  "comment_id": "12345",
  "original_text": "El servicio es excelente pero el precio es alto",
  "sentiment": {
    "classification": "mixed",
    "score": 0.3,
    "positive_aspects": ["service_quality"],
    "negative_aspects": ["pricing"],
    "dominant": "positive"
  },
  "emotions": {
    "joy": 0.6,
    "anger": 0.2,
    "sadness": 0.1,
    "fear": 0.0,
    "surprise": 0.1
  },
  "confidence": {
    "overall": 0.85,
    "factors": {
      "text_clarity": 0.9,
      "language_confidence": 0.95,
      "sentiment_strength": 0.7,
      "emotion_consistency": 0.85,
      "model_certainty": 0.85
    }
  },
  "cultural_context": {
    "language": "spanish",
    "regional_variant": "paraguayan",
    "cultural_modifiers_applied": ["indirect_expression"]
  }
}
```

## 🔍 Common Patterns

### Telecommunications-Specific Patterns
```python
TELECOM_SENTIMENT_PATTERNS = {
    'speed_satisfaction': {
        'positive': ['rápido', 'veloz', 'instantáneo', 'vuela'],
        'negative': ['lento', 'tarda', 'demora', 'tortuga']
    },
    'reliability': {
        'positive': ['estable', 'confiable', 'siempre funciona'],
        'negative': ['se cae', 'intermitente', 'no funciona']
    },
    'customer_service': {
        'positive': ['amables', 'atentos', 'resolvieron', 'excelente atención'],
        'negative': ['mala atención', 'no responden', 'groseros']
    },
    'pricing': {
        'positive': ['buen precio', 'económico', 'vale la pena'],
        'negative': ['caro', 'expensive', 'mucha plata']
    }
}
```

## 🚀 Optimization Strategies

### Performance Optimization
1. **Caching Similar Comments** - Cache results for duplicate/similar comments
2. **Batch Processing** - Process multiple comments in single API calls
3. **Parallel Processing** - Analyze independent comments concurrently
4. **Smart Sampling** - For large datasets, analyze representative samples

### Accuracy Improvements
1. **Continuous Learning** - Track manual corrections and improve
2. **Domain Adaptation** - Telecommunications-specific training
3. **Cultural Training** - Paraguayan expression recognition
4. **Feedback Loop** - Use business outcomes to validate accuracy

## 📊 Business Applications

### Use Cases
- **Customer Satisfaction Tracking** - Monitor overall satisfaction trends
- **Issue Prioritization** - Identify most negative feedback for urgent action
- **Success Story Identification** - Find highly positive comments for marketing
- **Churn Prediction** - Identify extremely dissatisfied customers at risk

### Metrics and KPIs
- **Net Sentiment Score** - Overall positive vs negative ratio
- **Emotion Distribution** - Breakdown of customer emotions
- **Confidence Average** - Overall analysis reliability
- **Trend Analysis** - Sentiment changes over time

## 🔗 Related Documentation
- [Theme Detection](theme-detection.md) - Identifying discussion topics
- [Emotion Analysis](emotion-analysis.md) - Detailed emotion processing
- [Language Processing](language-processing.md) - Multilingual handling
- [OpenAI Integration](../../backend/api/openai-integration.md) - API details