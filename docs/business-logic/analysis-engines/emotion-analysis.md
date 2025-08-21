# Emotion Analysis Engine Documentation

The Emotion Analysis Engine provides deep emotional intelligence capabilities, detecting nuanced emotional states in customer feedback to understand not just what customers think, but how they feel about Personal Paraguay's services.

## 🎯 Overview

This engine goes beyond basic sentiment to detect complex emotional states, intensity levels, and emotional transitions, providing a comprehensive understanding of customer emotional experiences.

### Core Capabilities
- **Multi-emotion Detection** - Identifies multiple simultaneous emotions
- **Intensity Measurement** - Quantifies emotional strength
- **Emotional Journey Mapping** - Tracks emotion changes
- **Cultural Emotion Adaptation** - Considers cultural expression differences
- **Behavioral Prediction** - Links emotions to likely actions

## 🧠 Emotion Model

### Primary Emotions Framework
```python
class EmotionModel:
    """
    Comprehensive emotion detection model based on psychological frameworks
    """
    
    PRIMARY_EMOTIONS = {
        'joy': {
            'description': 'Happiness, satisfaction, pleasure',
            'indicators': ['feliz', 'contento', 'alegre', 'satisfecho', 'encantado'],
            'behavioral_tendency': 'recommendation',
            'business_impact': 'positive_retention'
        },
        'anger': {
            'description': 'Frustration, rage, irritation',
            'indicators': ['enojado', 'furioso', 'molesto', 'indignado', 'harto'],
            'behavioral_tendency': 'complaint_escalation',
            'business_impact': 'churn_risk'
        },
        'sadness': {
            'description': 'Disappointment, unhappiness, regret',
            'indicators': ['triste', 'decepcionado', 'desilusionado', 'lamentable'],
            'behavioral_tendency': 'service_abandonment',
            'business_impact': 'silent_churn'
        },
        'fear': {
            'description': 'Worry, anxiety, concern',
            'indicators': ['preocupado', 'ansioso', 'temeroso', 'inquieto'],
            'behavioral_tendency': 'information_seeking',
            'business_impact': 'support_demand'
        },
        'surprise': {
            'description': 'Astonishment, amazement, shock',
            'indicators': ['sorprendido', 'asombrado', 'impactado', 'inesperado'],
            'behavioral_tendency': 'viral_sharing',
            'business_impact': 'variable'
        },
        'disgust': {
            'description': 'Revulsion, contempt, distaste',
            'indicators': ['asco', 'repugnante', 'desagradable', 'inaceptable'],
            'behavioral_tendency': 'brand_rejection',
            'business_impact': 'reputation_damage'
        }
    }
```

### Secondary Emotions
```python
SECONDARY_EMOTIONS = {
    'frustration': {
        'primary_components': ['anger', 'sadness'],
        'triggers': ['repeated_issues', 'unmet_expectations'],
        'intensity_multiplier': 1.3
    },
    'satisfaction': {
        'primary_components': ['joy', 'contentment'],
        'triggers': ['met_expectations', 'good_service'],
        'intensity_multiplier': 0.8
    },
    'anxiety': {
        'primary_components': ['fear', 'uncertainty'],
        'triggers': ['service_changes', 'billing_issues'],
        'intensity_multiplier': 1.1
    },
    'excitement': {
        'primary_components': ['joy', 'surprise'],
        'triggers': ['new_features', 'speed_improvements'],
        'intensity_multiplier': 1.2
    }
}
```

## 📊 Emotion Detection Process

### Multi-layer Analysis
```python
class EmotionAnalyzer:
    """
    Comprehensive emotion analysis system
    """
    
    def analyze_emotions(self, text):
        """
        Multi-layer emotion detection process
        """
        # Layer 1: Lexical Analysis
        lexical_emotions = self.detect_lexical_emotions(text)
        
        # Layer 2: Contextual Analysis
        contextual_emotions = self.analyze_context_emotions(text)
        
        # Layer 3: Intensity Analysis
        emotion_intensities = self.measure_intensities(text)
        
        # Layer 4: Cultural Adaptation
        adapted_emotions = self.apply_cultural_filters(
            lexical_emotions, 
            contextual_emotions,
            culture='paraguayan'
        )
        
        # Layer 5: Emotion Synthesis
        final_emotions = self.synthesize_emotions(
            adapted_emotions,
            emotion_intensities
        )
        
        return final_emotions
```

### Emotion Intensity Calculation
```python
def calculate_emotion_intensity(self, emotion_indicators):
    """
    Calculate intensity score for each emotion (0-1 scale)
    """
    intensity_factors = {
        'word_strength': self.assess_word_intensity(emotion_indicators),
        'repetition': self.count_repetitions(emotion_indicators),
        'punctuation': self.analyze_punctuation_emphasis(),
        'capitalization': self.detect_capitalization_emphasis(),
        'emoticons': self.parse_emoticons(),
        'intensifiers': self.detect_intensifiers()  # muy, super, demasiado
    }
    
    weights = {
        'word_strength': 0.35,
        'repetition': 0.15,
        'punctuation': 0.15,
        'capitalization': 0.10,
        'emoticons': 0.15,
        'intensifiers': 0.10
    }
    
    intensity_score = sum(
        factors[key] * weights[key] 
        for key in intensity_factors
    )
    
    return min(1.0, intensity_score)  # Cap at 1.0
```

## 🌍 Cultural Emotion Expression

### Paraguayan Emotional Context
```python
class CulturalEmotionAdapter:
    """
    Adapts emotion detection for Paraguayan cultural context
    """
    
    CULTURAL_EXPRESSIONS = {
        'indirect_anger': {
            'patterns': ['no está tan bien', 'podría ser mejor', 'no es lo ideal'],
            'actual_emotion': 'frustration',
            'intensity_adjustment': 1.5  # Understated anger is stronger
        },
        'polite_disappointment': {
            'patterns': ['esperaba un poco más', 'no es exactamente', 'tal vez'],
            'actual_emotion': 'disappointment',
            'intensity_adjustment': 1.3
        },
        'enthusiastic_joy': {
            'patterns': ['de diez', 'espectacular', 'lo máximo', 'brutal'],
            'actual_emotion': 'high_satisfaction',
            'intensity_adjustment': 0.9  # Already expressed strongly
        },
        'guarani_emotions': {
            'vy\'a': 'joy',
            'pochy': 'anger',
            'ñembyasy': 'sadness',
            'kyhyje': 'fear',
            'ñeñandu': 'feeling/emotion'
        }
    }
```

### Regional Expression Variations
```python
def adjust_for_regional_expression(self, emotion_data, region):
    """
    Adjust emotion interpretation based on regional expression patterns
    """
    regional_adjustments = {
        'urban_asuncion': {
            'directness': 0.9,  # More direct expression
            'intensity': 1.0    # Emotions expressed as felt
        },
        'rural_areas': {
            'directness': 0.6,  # More indirect
            'intensity': 1.4    # Understated emotions are stronger
        },
        'border_regions': {
            'directness': 0.8,
            'intensity': 1.1    # Mixed cultural influences
        }
    }
    
    adjustment = regional_adjustments.get(region, {'directness': 1.0, 'intensity': 1.0})
    
    return self.apply_adjustments(emotion_data, adjustment)
```

## 📈 Emotional Journey Mapping

### Tracking Emotional Transitions
```python
class EmotionalJourneyMapper:
    """
    Maps customer emotional journey through their interactions
    """
    
    def map_emotional_journey(self, customer_interactions):
        """
        Track how emotions evolve over time
        """
        journey = {
            'stages': [],
            'transitions': [],
            'overall_trajectory': None,
            'critical_points': []
        }
        
        for i, interaction in enumerate(customer_interactions):
            # Analyze emotion at each stage
            stage_emotion = self.analyze_emotions(interaction)
            journey['stages'].append({
                'timestamp': interaction['timestamp'],
                'primary_emotion': stage_emotion['primary'],
                'intensity': stage_emotion['intensity'],
                'trigger': self.identify_trigger(interaction)
            })
            
            # Identify transitions
            if i > 0:
                transition = self.analyze_transition(
                    journey['stages'][i-1],
                    journey['stages'][i]
                )
                journey['transitions'].append(transition)
                
                # Mark critical points
                if transition['magnitude'] > 0.5:
                    journey['critical_points'].append({
                        'point': i,
                        'type': transition['type'],
                        'impact': transition['magnitude']
                    })
        
        # Determine overall trajectory
        journey['overall_trajectory'] = self.calculate_trajectory(journey['stages'])
        
        return journey
```

### Emotion Transition Patterns
```python
EMOTION_TRANSITIONS = {
    'escalation': {
        'pattern': 'frustration → anger',
        'trigger': 'unresolved_issue',
        'risk': 'high',
        'intervention': 'immediate_support'
    },
    'resolution': {
        'pattern': 'anger → satisfaction',
        'trigger': 'problem_solved',
        'risk': 'low',
        'intervention': 'reinforce_positive'
    },
    'deterioration': {
        'pattern': 'satisfaction → disappointment',
        'trigger': 'service_degradation',
        'risk': 'medium',
        'intervention': 'proactive_contact'
    },
    'delight': {
        'pattern': 'neutral → joy',
        'trigger': 'exceeded_expectations',
        'risk': 'none',
        'intervention': 'capture_testimonial'
    }
}
```

## 🎯 Behavioral Prediction

### Emotion-Behavior Correlation
```python
class BehaviorPredictor:
    """
    Predicts customer behavior based on emotional states
    """
    
    EMOTION_BEHAVIOR_MAP = {
        'high_anger': {
            'likely_actions': ['complaint', 'social_media_post', 'churn'],
            'probability': 0.7,
            'urgency': 'immediate'
        },
        'high_joy': {
            'likely_actions': ['recommendation', 'positive_review', 'upgrade'],
            'probability': 0.6,
            'urgency': 'moderate'
        },
        'high_fear': {
            'likely_actions': ['support_contact', 'information_search', 'plan_change'],
            'probability': 0.5,
            'urgency': 'high'
        },
        'high_sadness': {
            'likely_actions': ['silent_churn', 'reduced_usage', 'passive_complaint'],
            'probability': 0.4,
            'urgency': 'moderate'
        }
    }
    
    def predict_behavior(self, emotion_profile):
        """
        Predict likely customer actions based on emotions
        """
        predictions = []
        
        for emotion, intensity in emotion_profile.items():
            if intensity > 0.7:  # High intensity threshold
                behavior_pattern = self.EMOTION_BEHAVIOR_MAP.get(f'high_{emotion}')
                if behavior_pattern:
                    predictions.append({
                        'emotion': emotion,
                        'intensity': intensity,
                        'likely_actions': behavior_pattern['likely_actions'],
                        'probability': behavior_pattern['probability'] * intensity,
                        'recommended_intervention': self.get_intervention(emotion, intensity)
                    })
        
        return sorted(predictions, key=lambda x: x['probability'], reverse=True)
```

## 🔧 Implementation Details

### OpenAI GPT-4 Integration
```python
def analyze_emotions_with_gpt4(comment):
    """
    Use GPT-4 for sophisticated emotion analysis
    """
    prompt = f"""
    Analyze the emotional content of this customer comment about fiber internet service.
    Consider Paraguayan cultural context and expression patterns.
    
    Comment: "{comment}"
    
    Provide detailed emotion analysis:
    1. Primary emotion and intensity (0-1)
    2. Secondary emotions present
    3. Emotional triggers identified
    4. Cultural expression factors
    5. Predicted behavioral tendency
    
    Return as JSON with:
    {{
        "primary_emotion": "emotion_name",
        "primary_intensity": 0.0-1.0,
        "secondary_emotions": {{"emotion": intensity}},
        "triggers": ["trigger1", "trigger2"],
        "cultural_factors": ["factor1", "factor2"],
        "behavioral_prediction": "likely_action",
        "confidence": 0.0-1.0
    }}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2  # Low for consistency in emotion detection
    )
    
    return parse_emotion_response(response)
```

## 📊 Emotion Metrics and Visualization

### Emotion Distribution Analysis
```python
def analyze_emotion_distribution(emotion_results):
    """
    Statistical analysis of emotion patterns
    """
    distribution = {
        'emotion_frequencies': {},
        'intensity_averages': {},
        'emotion_combinations': {},
        'temporal_patterns': {},
        'demographic_variations': {}
    }
    
    # Calculate frequencies
    for result in emotion_results:
        primary = result['primary_emotion']
        distribution['emotion_frequencies'][primary] = 
            distribution['emotion_frequencies'].get(primary, 0) + 1
        
        # Track intensity
        if primary not in distribution['intensity_averages']:
            distribution['intensity_averages'][primary] = []
        distribution['intensity_averages'][primary].append(result['intensity'])
    
    # Calculate averages
    for emotion, intensities in distribution['intensity_averages'].items():
        distribution['intensity_averages'][emotion] = np.mean(intensities)
    
    return distribution
```

### Emotion Visualization Data
```json
{
  "emotion_radar_chart": {
    "joy": 0.65,
    "anger": 0.25,
    "sadness": 0.15,
    "fear": 0.10,
    "surprise": 0.30,
    "disgust": 0.05
  },
  "emotion_timeline": [
    {"timestamp": "2024-01-01", "dominant_emotion": "joy", "intensity": 0.7},
    {"timestamp": "2024-01-02", "dominant_emotion": "frustration", "intensity": 0.6}
  ],
  "emotion_heatmap": {
    "morning": {"joy": 0.4, "anger": 0.3},
    "afternoon": {"joy": 0.6, "anger": 0.2},
    "evening": {"joy": 0.5, "anger": 0.4}
  }
}
```

## 🚀 Optimization and Performance

### Caching Strategy
```python
class EmotionCacheManager:
    """
    Efficient caching for emotion analysis results
    """
    
    def get_cached_emotion(self, text_hash):
        """
        Retrieve cached emotion analysis if available
        """
        cache_key = f"emotion:{text_hash}"
        cached_result = self.cache.get(cache_key)
        
        if cached_result and not self.is_expired(cached_result):
            return cached_result['emotions']
        
        return None
    
    def cache_emotion_result(self, text_hash, emotions, ttl=3600):
        """
        Cache emotion analysis results
        """
        cache_key = f"emotion:{text_hash}"
        self.cache.set(cache_key, {
            'emotions': emotions,
            'timestamp': datetime.now(),
            'ttl': ttl
        })
```

## 📈 Business Applications

### Emotion-Driven Insights
```python
def generate_emotion_insights(emotion_analysis):
    """
    Convert emotion data into business insights
    """
    insights = {
        'customer_mood': calculate_overall_mood(emotion_analysis),
        'emotional_drivers': identify_emotion_triggers(emotion_analysis),
        'risk_segments': identify_at_risk_customers(emotion_analysis),
        'opportunity_segments': find_advocacy_opportunities(emotion_analysis),
        'intervention_priorities': prioritize_interventions(emotion_analysis)
    }
    
    return format_for_business_action(insights)
```

### Actionable Recommendations
- **High Anger Detection** → Immediate support escalation
- **Joy Peaks** → Capture testimonials and reviews
- **Fear Patterns** → Proactive communication campaigns
- **Sadness Trends** → Service improvement initiatives
- **Surprise Events** → Viral marketing opportunities

## 🔗 Related Documentation
- [Sentiment Analysis](sentiment-analysis.md) - Overall sentiment detection
- [Behavioral Prediction](../algorithms/pattern-detection.md) - Customer behavior patterns
- [Customer Journey](../../user-guides/business-guide.md) - Emotional journey mapping
- [Real-time Monitoring](../../backend/api/monitoring.md) - Emotion tracking dashboard