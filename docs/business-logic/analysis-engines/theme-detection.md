# Theme Detection Engine Documentation

The Theme Detection Engine identifies and categorizes the primary topics and discussion points in customer feedback, enabling Personal Paraguay to understand what customers are talking about most frequently and prioritize improvements accordingly.

## 🎯 Overview

The theme detection engine uses natural language processing and pattern recognition to automatically identify, categorize, and rank themes in customer comments about fiber-to-the-home services.

### Core Capabilities
- **Automatic Topic Identification** - Discovers themes without predefined categories
- **Business Category Mapping** - Maps themes to business areas
- **Keyword Extraction** - Identifies important terms and phrases
- **Pattern Clustering** - Groups related themes together
- **Priority Ranking** - Ranks themes by frequency and impact

## 🏗️ Technical Architecture

### Engine Components
```python
class ThemeDetectionEngine:
    """
    Advanced theme and topic detection system
    """
    def __init__(self):
        self.topic_extractor = TopicExtractor()
        self.pattern_recognizer = PatternRecognizer()
        self.keyword_analyzer = KeywordAnalyzer()
        self.business_categorizer = BusinessCategorizer()
        self.theme_clusterer = ThemeClusterer()
```

### Detection Pipeline
```
Input Comments → Preprocessing → Keyword Extraction → Topic Modeling 
    → Pattern Recognition → Business Categorization → Theme Ranking → Results
```

## 📊 Theme Categories

### Telecommunications Business Themes

#### Service Quality Themes
```python
SERVICE_QUALITY_THEMES = {
    'internet_speed': {
        'keywords': ['velocidad', 'rápido', 'lento', 'mbps', 'download', 'upload'],
        'patterns': ['internet.*lento', 'velocidad.*baja', 'demora.*cargar'],
        'business_impact': 'high',
        'department': 'technical'
    },
    'connection_stability': {
        'keywords': ['estable', 'corte', 'intermitente', 'cae', 'desconecta'],
        'patterns': ['se corta', 'pierde conexión', 'no es estable'],
        'business_impact': 'high',
        'department': 'technical'
    },
    'coverage_area': {
        'keywords': ['cobertura', 'señal', 'alcance', 'zona', 'área'],
        'patterns': ['no llega', 'sin cobertura', 'mala señal'],
        'business_impact': 'medium',
        'department': 'infrastructure'
    }
}
```

#### Customer Experience Themes
```python
CUSTOMER_EXPERIENCE_THEMES = {
    'customer_service': {
        'keywords': ['atención', 'servicio', 'personal', 'empleado', 'agente'],
        'patterns': ['atención al cliente', 'mal servicio', 'buen trato'],
        'business_impact': 'high',
        'department': 'customer_service'
    },
    'installation_process': {
        'keywords': ['instalación', 'técnico', 'configurar', 'setup', 'instalar'],
        'patterns': ['instalación rápida', 'técnico profesional', 'demora instalación'],
        'business_impact': 'medium',
        'department': 'field_service'
    },
    'support_response': {
        'keywords': ['soporte', 'ayuda', 'respuesta', 'solución', 'resolver'],
        'patterns': ['no responden', 'rápida solución', 'sin ayuda'],
        'business_impact': 'high',
        'department': 'support'
    }
}
```

#### Business & Pricing Themes
```python
BUSINESS_THEMES = {
    'pricing': {
        'keywords': ['precio', 'costo', 'tarifa', 'pago', 'factura', 'caro', 'barato'],
        'patterns': ['precio alto', 'muy caro', 'buen precio', 'aumentó tarifa'],
        'business_impact': 'high',
        'department': 'sales'
    },
    'billing': {
        'keywords': ['factura', 'cobro', 'cuenta', 'pagar', 'débito'],
        'patterns': ['factura incorrecta', 'cobro doble', 'error facturación'],
        'business_impact': 'medium',
        'department': 'billing'
    },
    'contract_terms': {
        'keywords': ['contrato', 'plan', 'promoción', 'oferta', 'condiciones'],
        'patterns': ['cambiar plan', 'mejorar contrato', 'sin permanencia'],
        'business_impact': 'medium',
        'department': 'sales'
    }
}
```

## 🔍 Theme Detection Methods

### 1. Keyword-Based Detection
```python
class KeywordAnalyzer:
    """
    Extracts and analyzes keywords for theme identification
    """
    
    def extract_keywords(self, text):
        """
        Extract relevant keywords using TF-IDF and frequency analysis
        """
        # Remove stopwords
        cleaned_text = self.remove_stopwords(text)
        
        # Extract n-grams (1-3 words)
        ngrams = self.extract_ngrams(cleaned_text, n_range=(1, 3))
        
        # Calculate importance scores
        keyword_scores = self.calculate_tfidf_scores(ngrams)
        
        # Filter by relevance threshold
        relevant_keywords = [k for k, score in keyword_scores.items() if score > 0.3]
        
        return relevant_keywords
```

### 2. Pattern Recognition
```python
class PatternRecognizer:
    """
    Identifies recurring patterns and expressions
    """
    
    def detect_patterns(self, comments):
        """
        Find common patterns across multiple comments
        """
        patterns = {
            'complaint_patterns': [
                r'no (funciona|sirve|anda)',
                r'(pésimo|horrible|terrible) servicio',
                r'(muy|demasiado) (lento|caro)'
            ],
            'praise_patterns': [
                r'(excelente|muy bueno|genial)',
                r'(rápido|veloz) y (estable|confiable)',
                r'(recomiendo|lo mejor)'
            ],
            'request_patterns': [
                r'(necesito|quiero|solicito)',
                r'(podrían|deberían) (mejorar|cambiar)',
                r'(cuando|cuándo) (van a|tendrán)'
            ]
        }
        
        detected_patterns = []
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, comments, re.IGNORECASE):
                    detected_patterns.append({
                        'type': pattern_type,
                        'pattern': pattern,
                        'context': self.extract_context(pattern, comments)
                    })
        
        return detected_patterns
```

### 3. Topic Modeling
```python
class TopicModeling:
    """
    Advanced topic modeling using LDA-like approaches
    """
    
    def model_topics(self, comments_corpus):
        """
        Discover latent topics in comment corpus
        """
        # Preprocess corpus
        processed_corpus = self.preprocess_corpus(comments_corpus)
        
        # Create document-term matrix
        doc_term_matrix = self.create_doc_term_matrix(processed_corpus)
        
        # Apply topic modeling
        topics = self.apply_lda(doc_term_matrix, num_topics=10)
        
        # Label topics based on dominant terms
        labeled_topics = self.label_topics(topics)
        
        return labeled_topics
```

## 📈 Theme Ranking and Prioritization

### Ranking Criteria
```python
class ThemeRanker:
    """
    Ranks themes by business importance
    """
    
    def calculate_theme_priority(self, theme_data):
        """
        Multi-factor theme prioritization
        """
        factors = {
            'frequency': theme_data['occurrence_count'] / total_comments,
            'sentiment_impact': abs(theme_data['avg_sentiment']),  # How negative
            'business_impact': BUSINESS_IMPACT_SCORES[theme_data['category']],
            'trend': self.calculate_trend_score(theme_data['time_series']),
            'customer_segment': self.get_segment_importance(theme_data['segments'])
        }
        
        weights = {
            'frequency': 0.25,
            'sentiment_impact': 0.3,
            'business_impact': 0.2,
            'trend': 0.15,
            'customer_segment': 0.1
        }
        
        priority_score = sum(factors[k] * weights[k] for k in factors)
        return priority_score
```

### Priority Matrix
```python
PRIORITY_MATRIX = {
    'critical': {
        'criteria': 'high_frequency AND high_negative_sentiment',
        'action': 'immediate_attention',
        'escalation': 'executive_level'
    },
    'high': {
        'criteria': 'high_frequency OR high_negative_sentiment',
        'action': 'urgent_review',
        'escalation': 'department_head'
    },
    'medium': {
        'criteria': 'moderate_frequency AND moderate_impact',
        'action': 'scheduled_review',
        'escalation': 'team_lead'
    },
    'low': {
        'criteria': 'low_frequency OR low_impact',
        'action': 'monitor',
        'escalation': 'analyst'
    }
}
```

## 🎯 Business Category Mapping

### Automatic Categorization
```python
class BusinessCategorizer:
    """
    Maps themes to business departments and processes
    """
    
    BUSINESS_CATEGORIES = {
        'technical_operations': {
            'themes': ['internet_speed', 'connection_stability', 'technical_issues'],
            'department': 'Network Operations',
            'kpi_impact': ['uptime', 'speed_metrics', 'reliability']
        },
        'customer_service': {
            'themes': ['support_response', 'agent_interaction', 'complaint_handling'],
            'department': 'Customer Service',
            'kpi_impact': ['csat', 'first_call_resolution', 'response_time']
        },
        'field_service': {
            'themes': ['installation', 'maintenance', 'technician_service'],
            'department': 'Field Operations',
            'kpi_impact': ['installation_time', 'service_quality', 'technician_rating']
        },
        'commercial': {
            'themes': ['pricing', 'plans', 'promotions', 'competition'],
            'department': 'Sales & Marketing',
            'kpi_impact': ['pricing_satisfaction', 'plan_adoption', 'churn_rate']
        },
        'billing_finance': {
            'themes': ['billing_issues', 'payment_problems', 'invoice_errors'],
            'department': 'Finance',
            'kpi_impact': ['billing_accuracy', 'payment_timeliness', 'dispute_rate']
        }
    }
```

## 🔧 Implementation Details

### OpenAI Integration for Theme Detection
```python
def detect_themes_with_gpt4(comment_batch):
    """
    Use GPT-4 for advanced theme detection
    """
    prompt = f"""
    Analyze these customer comments about fiber internet service and identify the main themes.
    
    Comments:
    {format_comments(comment_batch)}
    
    Identify:
    1. Primary themes discussed (max 5)
    2. Keywords for each theme
    3. Business category for each theme
    4. Frequency of each theme
    5. Average sentiment for each theme
    
    Focus on telecommunications-specific themes like:
    - Internet speed and performance
    - Connection stability
    - Customer service quality
    - Pricing and billing
    - Installation and technical support
    
    Return as JSON with theme analysis.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # Some creativity for theme discovery
    )
    
    return parse_theme_response(response)
```

### Batch Theme Analysis
```python
def analyze_themes_in_batch(comments, batch_size=100):
    """
    Efficient batch processing for theme detection
    """
    all_themes = {}
    
    for batch in chunks(comments, batch_size):
        # Extract themes from batch
        batch_themes = detect_themes_with_gpt4(batch)
        
        # Aggregate themes
        for theme, data in batch_themes.items():
            if theme in all_themes:
                all_themes[theme]['count'] += data['count']
                all_themes[theme]['comments'].extend(data['comments'])
            else:
                all_themes[theme] = data
    
    # Rank themes by importance
    ranked_themes = rank_themes_by_priority(all_themes)
    
    return ranked_themes
```

## 📊 Theme Clustering

### Hierarchical Theme Organization
```python
class ThemeClusterer:
    """
    Groups related themes into clusters
    """
    
    def create_theme_hierarchy(self, themes):
        """
        Organize themes into hierarchical structure
        """
        hierarchy = {
            'service_quality': {
                'parent': None,
                'children': ['internet_speed', 'connection_stability', 'coverage'],
                'weight': 0.35
            },
            'customer_experience': {
                'parent': None,
                'children': ['customer_service', 'support', 'communication'],
                'weight': 0.30
            },
            'technical': {
                'parent': 'service_quality',
                'children': ['equipment', 'configuration', 'maintenance'],
                'weight': 0.20
            },
            'commercial': {
                'parent': None,
                'children': ['pricing', 'plans', 'billing'],
                'weight': 0.15
            }
        }
        
        return self.build_hierarchy_tree(themes, hierarchy)
```

### Theme Relationships
```python
def identify_theme_relationships(themes):
    """
    Find correlations between themes
    """
    relationships = {
        'causal': [
            ('slow_speed', 'customer_complaint'),
            ('billing_error', 'support_contact')
        ],
        'correlated': [
            ('good_speed', 'positive_sentiment'),
            ('installation_delay', 'negative_sentiment')
        ],
        'inverse': [
            ('high_price', 'value_perception'),
            ('good_service', 'churn_intention')
        ]
    }
    
    return analyze_relationships(themes, relationships)
```

## 📈 Trend Analysis

### Temporal Theme Tracking
```python
def track_theme_trends(themes_over_time):
    """
    Analyze how themes evolve over time
    """
    trends = {
        'emerging': [],  # New themes appearing
        'growing': [],   # Themes increasing in frequency
        'stable': [],    # Consistent themes
        'declining': [], # Themes decreasing
        'seasonal': []   # Themes with seasonal patterns
    }
    
    for theme, time_series in themes_over_time.items():
        trend_type = classify_trend(time_series)
        trends[trend_type].append({
            'theme': theme,
            'trend_score': calculate_trend_score(time_series),
            'prediction': predict_future_trend(time_series)
        })
    
    return trends
```

## 🎨 Output Format

### Theme Detection Results
```json
{
  "analysis_id": "theme_analysis_12345",
  "total_comments": 500,
  "themes_detected": [
    {
      "theme": "internet_speed",
      "category": "service_quality",
      "frequency": 145,
      "percentage": 29.0,
      "keywords": ["lento", "velocidad", "mbps", "download"],
      "average_sentiment": -0.4,
      "priority": "critical",
      "sample_comments": [
        "Internet muy lento, no llega ni a 10 mbps",
        "La velocidad de descarga es terrible"
      ],
      "business_impact": {
        "department": "Network Operations",
        "kpi_affected": ["speed_sla", "customer_satisfaction"],
        "estimated_impact": "high"
      }
    },
    {
      "theme": "customer_service",
      "category": "customer_experience",
      "frequency": 89,
      "percentage": 17.8,
      "keywords": ["atención", "servicio", "respuesta", "ayuda"],
      "average_sentiment": 0.6,
      "priority": "medium",
      "sample_comments": [
        "Excelente atención del personal",
        "Muy buena respuesta del soporte"
      ]
    }
  ],
  "theme_clusters": {
    "technical_issues": ["internet_speed", "connection_stability", "equipment"],
    "customer_interaction": ["customer_service", "support_response", "communication"],
    "commercial_aspects": ["pricing", "billing", "plans"]
  },
  "recommendations": [
    "Focus on improving internet speed - highest negative impact",
    "Leverage positive customer service as competitive advantage",
    "Review pricing strategy - moderate concern among customers"
  ]
}
```

## 🚀 Optimization Strategies

### Performance Optimization
1. **Keyword Caching** - Cache common keyword extractions
2. **Pattern Compilation** - Pre-compile regex patterns
3. **Incremental Analysis** - Update themes incrementally
4. **Parallel Processing** - Process themes concurrently

### Accuracy Improvements
1. **Domain Dictionary** - Telecommunications-specific terms
2. **Local Expressions** - Paraguayan Spanish/Guaraní phrases
3. **Feedback Loop** - Learn from manual theme corrections
4. **Context Windows** - Analyze surrounding text for better understanding

## 📊 Business Applications

### Strategic Use Cases
- **Product Development** - Identify feature requests and needs
- **Service Improvement** - Prioritize operational improvements
- **Marketing Insights** - Understand customer language and concerns
- **Competitive Analysis** - Track mentions of competitors
- **Risk Management** - Identify emerging issues early

### Actionable Insights
```python
def generate_theme_insights(theme_analysis):
    """
    Convert themes into actionable business insights
    """
    insights = {
        'immediate_actions': filter_critical_themes(theme_analysis),
        'improvement_opportunities': identify_improvement_areas(theme_analysis),
        'positive_reinforcement': find_success_themes(theme_analysis),
        'monitoring_required': detect_emerging_issues(theme_analysis)
    }
    
    return format_insights_for_executives(insights)
```

## 🔗 Related Documentation
- [Sentiment Analysis](sentiment-analysis.md) - Emotion and opinion detection
- [Pattern Detection](../algorithms/pattern-detection.md) - Advanced pattern recognition
- [Business Intelligence](../../user-guides/business-guide.md) - Using themes for decisions
- [Export Systems](../exports/report-generation.md) - Theme reporting