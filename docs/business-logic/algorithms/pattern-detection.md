# Pattern Detection Documentation

The Pattern Detection module identifies recurring themes, issues, and behavioral patterns in customer feedback using advanced pattern recognition algorithms and machine learning techniques.

## 🎯 Overview

This module implements sophisticated pattern detection algorithms to automatically discover hidden insights, recurring issues, and emerging trends in customer feedback data, enabling proactive business responses.

### Core Capabilities
- **Theme Pattern Detection** - Identify recurring topics and themes
- **Issue Pattern Recognition** - Detect common problems and complaints
- **Temporal Pattern Analysis** - Track patterns over time
- **Anomaly Detection** - Identify unusual patterns and outliers
- **Behavioral Pattern Mining** - Customer behavior insights

## 🏗️ Pattern Detection Architecture

### Multi-Layer Pattern Recognition
```python
class PatternDetectionArchitecture:
    """
    Comprehensive pattern detection system architecture
    """
    
    PATTERN_TYPES = {
        'textual': {
            'methods': ['ngram_analysis', 'topic_modeling', 'keyword_extraction'],
            'scope': ['word_level', 'phrase_level', 'sentence_level'],
            'languages': ['spanish', 'guarani', 'mixed']
        },
        'semantic': {
            'methods': ['semantic_clustering', 'concept_extraction', 'entity_recognition'],
            'scope': ['topic_level', 'intent_level', 'emotion_level'],
            'models': ['word2vec', 'bert', 'sentence_transformers']
        },
        'temporal': {
            'methods': ['time_series_analysis', 'trend_detection', 'seasonal_patterns'],
            'scope': ['daily', 'weekly', 'monthly', 'seasonal'],
            'metrics': ['frequency', 'intensity', 'sentiment_trends']
        },
        'behavioral': {
            'methods': ['sequence_mining', 'association_rules', 'clustering'],
            'scope': ['user_journeys', 'complaint_patterns', 'satisfaction_patterns'],
            'algorithms': ['apriori', 'fpgrowth', 'sequential_patterns']
        }
    }
```

## 🔍 Core Pattern Engine

### Advanced Pattern Detector
```python
class PatternDetector:
    """
    Advanced pattern detection with multiple algorithms
    """
    
    def __init__(self):
        self.text_analyzer = TextPatternAnalyzer()
        self.semantic_analyzer = SemanticPatternAnalyzer()
        self.temporal_analyzer = TemporalPatternAnalyzer()
        self.behavioral_analyzer = BehavioralPatternAnalyzer()
        self.anomaly_detector = AnomalyDetector()
        
        # Pattern storage
        self.pattern_store = PatternStore()
        self.pattern_cache = PatternCache()
    
    def detect_patterns(self, comments, pattern_types='all'):
        """
        Detect patterns across multiple dimensions
        """
        results = {
            'textual_patterns': [],
            'semantic_patterns': [],
            'temporal_patterns': [],
            'behavioral_patterns': [],
            'anomalies': [],
            'meta_patterns': []
        }
        
        # Textual pattern detection
        if pattern_types in ['all', 'textual']:
            results['textual_patterns'] = self.text_analyzer.detect(comments)
        
        # Semantic pattern detection
        if pattern_types in ['all', 'semantic']:
            results['semantic_patterns'] = self.semantic_analyzer.detect(comments)
        
        # Temporal pattern detection
        if pattern_types in ['all', 'temporal']:
            results['temporal_patterns'] = self.temporal_analyzer.detect(comments)
        
        # Behavioral pattern detection
        if pattern_types in ['all', 'behavioral']:
            results['behavioral_patterns'] = self.behavioral_analyzer.detect(comments)
        
        # Anomaly detection
        if pattern_types in ['all', 'anomalies']:
            results['anomalies'] = self.anomaly_detector.detect(comments)
        
        # Meta-pattern analysis (patterns of patterns)
        results['meta_patterns'] = self.detect_meta_patterns(results)
        
        # Store patterns for future reference
        self.pattern_store.store_patterns(results)
        
        return results
    
    def detect_emerging_patterns(self, new_comments, historical_patterns):
        """
        Detect new and emerging patterns
        """
        # Detect patterns in new data
        new_patterns = self.detect_patterns(new_comments)
        
        # Compare with historical patterns
        emerging = []
        evolving = []
        declining = []
        
        for pattern_type, patterns in new_patterns.items():
            if pattern_type == 'meta_patterns':
                continue
                
            for pattern in patterns:
                pattern_signature = self.generate_pattern_signature(pattern)
                
                # Check if pattern exists in history
                historical_match = self.find_historical_match(
                    pattern_signature,
                    historical_patterns.get(pattern_type, [])
                )
                
                if not historical_match:
                    # New emerging pattern
                    emerging.append({
                        'pattern': pattern,
                        'type': 'emerging',
                        'first_seen': datetime.now(),
                        'growth_rate': self.calculate_growth_rate(pattern)
                    })
                else:
                    # Existing pattern - check evolution
                    evolution = self.analyze_pattern_evolution(
                        pattern,
                        historical_match
                    )
                    
                    if evolution['status'] == 'growing':
                        evolving.append({
                            'pattern': pattern,
                            'type': 'evolving',
                            'evolution': evolution
                        })
        
        # Check for declining patterns
        declining = self.find_declining_patterns(
            historical_patterns,
            new_patterns
        )
        
        return {
            'emerging': emerging,
            'evolving': evolving,
            'declining': declining,
            'stable': self.find_stable_patterns(historical_patterns, new_patterns)
        }
```

## 📝 Text Pattern Analysis

### N-gram and Phrase Pattern Detection
```python
class TextPatternAnalyzer:
    """
    Analyze textual patterns in comments
    """
    
    def __init__(self):
        self.ngram_analyzer = NgramAnalyzer()
        self.phrase_extractor = PhraseExtractor()
        self.keyword_extractor = KeywordExtractor()
        self.collocation_finder = CollocationFinder()
    
    def detect(self, comments):
        """
        Detect textual patterns
        """
        patterns = {
            'frequent_ngrams': self.find_frequent_ngrams(comments),
            'key_phrases': self.extract_key_phrases(comments),
            'collocations': self.find_collocations(comments),
            'linguistic_patterns': self.find_linguistic_patterns(comments),
            'complaint_patterns': self.find_complaint_patterns(comments)
        }
        
        return patterns
    
    def find_frequent_ngrams(self, comments, n_range=(1, 4)):
        """
        Find frequently occurring n-grams
        """
        all_text = ' '.join([comment.get('text', '') for comment in comments])
        
        ngram_patterns = {}
        
        for n in range(n_range[0], n_range[1] + 1):
            ngrams = self.ngram_analyzer.extract_ngrams(all_text, n)
            
            # Filter by frequency and significance
            frequent_ngrams = [
                ngram for ngram, freq in ngrams.most_common(100)
                if freq > len(comments) * 0.05  # Appears in 5% of comments
            ]
            
            # Score ngrams by relevance
            scored_ngrams = []
            for ngram in frequent_ngrams:
                score = self.calculate_ngram_relevance(ngram, comments)
                if score > 0.3:
                    scored_ngrams.append({
                        'ngram': ngram,
                        'frequency': ngrams[ngram],
                        'relevance_score': score,
                        'examples': self.find_ngram_examples(ngram, comments)
                    })
            
            ngram_patterns[f'{n}grams'] = sorted(
                scored_ngrams,
                key=lambda x: x['relevance_score'],
                reverse=True
            )
        
        return ngram_patterns
    
    def extract_key_phrases(self, comments):
        """
        Extract meaningful key phrases
        """
        phrases = []
        
        for comment in comments:
            text = comment.get('text', '')
            
            # Extract noun phrases
            noun_phrases = self.phrase_extractor.extract_noun_phrases(text)
            
            # Extract verb phrases
            verb_phrases = self.phrase_extractor.extract_verb_phrases(text)
            
            # Extract complaint phrases
            complaint_phrases = self.extract_complaint_phrases(text)
            
            phrases.extend([
                {'phrase': phrase, 'type': 'noun', 'comment': comment}
                for phrase in noun_phrases
            ])
            phrases.extend([
                {'phrase': phrase, 'type': 'verb', 'comment': comment}
                for phrase in verb_phrases
            ])
            phrases.extend([
                {'phrase': phrase, 'type': 'complaint', 'comment': comment}
                for phrase in complaint_phrases
            ])
        
        # Group and rank phrases
        phrase_groups = self.group_similar_phrases(phrases)
        ranked_phrases = self.rank_phrase_groups(phrase_groups)
        
        return ranked_phrases
    
    def find_complaint_patterns(self, comments):
        """
        Identify common complaint patterns
        """
        complaint_indicators = [
            r'no funciona',
            r'muy lento',
            r'mala calidad',
            r'servicio malo',
            r'atención terrible',
            r'no recomiendo',
            r'pérdida de tiempo',
            r'decepcionante'
        ]
        
        patterns = []
        
        for indicator in complaint_indicators:
            matching_comments = []
            
            for comment in comments:
                text = comment.get('text', '').lower()
                if re.search(indicator, text):
                    matching_comments.append(comment)
            
            if len(matching_comments) > 2:  # At least 3 occurrences
                patterns.append({
                    'pattern': indicator,
                    'type': 'complaint',
                    'frequency': len(matching_comments),
                    'percentage': len(matching_comments) / len(comments) * 100,
                    'examples': matching_comments[:5],
                    'severity': self.calculate_complaint_severity(matching_comments)
                })
        
        return sorted(patterns, key=lambda x: x['frequency'], reverse=True)
```

## 🧠 Semantic Pattern Analysis

### Topic and Concept Pattern Detection
```python
class SemanticPatternAnalyzer:
    """
    Analyze semantic patterns using NLP and ML
    """
    
    def __init__(self):
        self.topic_modeler = LatentDirichletAllocation(n_components=10)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.clusterer = DBSCAN(eps=0.3, min_samples=3)
        self.entity_recognizer = EntityRecognizer()
    
    def detect(self, comments):
        """
        Detect semantic patterns
        """
        patterns = {
            'topic_clusters': self.find_topic_clusters(comments),
            'semantic_clusters': self.find_semantic_clusters(comments),
            'entity_patterns': self.find_entity_patterns(comments),
            'sentiment_patterns': self.find_sentiment_patterns(comments),
            'intent_patterns': self.find_intent_patterns(comments)
        }
        
        return patterns
    
    def find_topic_clusters(self, comments):
        """
        Find topic-based clusters using LDA
        """
        # Prepare text corpus
        texts = [comment.get('text', '') for comment in comments]
        
        # Vectorize texts
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=self.get_stopwords(),
            ngram_range=(1, 2)
        )
        doc_term_matrix = vectorizer.fit_transform(texts)
        
        # Fit LDA model
        self.topic_modeler.fit(doc_term_matrix)
        
        # Get topic assignments
        topic_assignments = self.topic_modeler.transform(doc_term_matrix)
        
        # Create topic clusters
        clusters = []
        feature_names = vectorizer.get_feature_names_out()
        
        for topic_idx in range(self.topic_modeler.n_components):
            # Get top words for topic
            top_words_idx = self.topic_modeler.components_[topic_idx].argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            
            # Get comments belonging to this topic
            topic_comments = []
            for comment_idx, comment in enumerate(comments):
                if topic_assignments[comment_idx][topic_idx] > 0.3:
                    topic_comments.append({
                        'comment': comment,
                        'probability': topic_assignments[comment_idx][topic_idx]
                    })
            
            if topic_comments:
                clusters.append({
                    'topic_id': topic_idx,
                    'keywords': top_words,
                    'comments': topic_comments,
                    'size': len(topic_comments),
                    'coherence_score': self.calculate_topic_coherence(
                        topic_idx, doc_term_matrix
                    )
                })
        
        return sorted(clusters, key=lambda x: x['size'], reverse=True)
    
    def find_semantic_clusters(self, comments):
        """
        Find semantically similar comment clusters
        """
        # Generate embeddings
        texts = [comment.get('text', '') for comment in comments]
        embeddings = self.embedder.encode(texts)
        
        # Perform clustering
        cluster_labels = self.clusterer.fit_predict(embeddings)
        
        # Group comments by clusters
        clusters = defaultdict(list)
        for comment_idx, label in enumerate(cluster_labels):
            if label != -1:  # Ignore noise points
                clusters[label].append({
                    'comment': comments[comment_idx],
                    'embedding': embeddings[comment_idx]
                })
        
        # Analyze clusters
        cluster_analysis = []
        for cluster_id, cluster_comments in clusters.items():
            if len(cluster_comments) >= 3:  # Minimum cluster size
                analysis = self.analyze_semantic_cluster(cluster_comments)
                cluster_analysis.append({
                    'cluster_id': cluster_id,
                    'size': len(cluster_comments),
                    'comments': cluster_comments,
                    'centroid': analysis['centroid'],
                    'representative_comment': analysis['representative'],
                    'common_themes': analysis['themes'],
                    'cohesion_score': analysis['cohesion']
                })
        
        return sorted(cluster_analysis, key=lambda x: x['size'], reverse=True)
```

## ⏰ Temporal Pattern Analysis

### Time-Based Pattern Detection
```python
class TemporalPatternAnalyzer:
    """
    Analyze patterns over time
    """
    
    def __init__(self):
        self.time_series_analyzer = TimeSeriesAnalyzer()
        self.trend_detector = TrendDetector()
        self.seasonality_detector = SeasonalityDetector()
        self.anomaly_detector = TemporalAnomalyDetector()
    
    def detect(self, comments):
        """
        Detect temporal patterns
        """
        # Group comments by time periods
        time_series = self.create_time_series(comments)
        
        patterns = {
            'hourly_patterns': self.analyze_hourly_patterns(time_series),
            'daily_patterns': self.analyze_daily_patterns(time_series),
            'weekly_patterns': self.analyze_weekly_patterns(time_series),
            'monthly_patterns': self.analyze_monthly_patterns(time_series),
            'trend_patterns': self.detect_trends(time_series),
            'seasonal_patterns': self.detect_seasonality(time_series),
            'anomaly_periods': self.detect_temporal_anomalies(time_series)
        }
        
        return patterns
    
    def create_time_series(self, comments):
        """
        Create time series from comments
        """
        time_series = {
            'volume': defaultdict(int),
            'sentiment': defaultdict(list),
            'topics': defaultdict(list),
            'satisfaction': defaultdict(list)
        }
        
        for comment in comments:
            timestamp = comment.get('timestamp')
            if not timestamp:
                continue
            
            # Parse timestamp
            dt = self.parse_timestamp(timestamp)
            
            # Group by different time periods
            hour_key = dt.strftime('%Y-%m-%d %H:00')
            day_key = dt.strftime('%Y-%m-%d')
            week_key = dt.strftime('%Y-W%U')
            month_key = dt.strftime('%Y-%m')
            
            # Volume metrics
            time_series['volume'][hour_key] += 1
            
            # Sentiment metrics
            sentiment = comment.get('sentiment_score', 0)
            time_series['sentiment'][day_key].append(sentiment)
            
            # Topic metrics
            topics = comment.get('topics', [])
            time_series['topics'][day_key].extend(topics)
            
            # Satisfaction metrics
            satisfaction = comment.get('satisfaction_score')
            if satisfaction is not None:
                time_series['satisfaction'][day_key].append(satisfaction)
        
        return time_series
    
    def detect_trends(self, time_series):
        """
        Detect trending patterns
        """
        trends = {}
        
        for metric, data in time_series.items():
            if metric == 'volume':
                # Volume trend analysis
                dates = sorted(data.keys())
                volumes = [data[date] for date in dates]
                
                trend = self.trend_detector.detect_trend(volumes)
                trends[f'{metric}_trend'] = {
                    'direction': trend['direction'],
                    'strength': trend['strength'],
                    'significance': trend['p_value'],
                    'slope': trend['slope']
                }
            
            elif metric in ['sentiment', 'satisfaction']:
                # Average sentiment/satisfaction trend
                dates = sorted(data.keys())
                averages = [
                    np.mean(data[date]) if data[date] else 0
                    for date in dates
                ]
                
                trend = self.trend_detector.detect_trend(averages)
                trends[f'{metric}_trend'] = {
                    'direction': trend['direction'],
                    'strength': trend['strength'],
                    'significance': trend['p_value'],
                    'slope': trend['slope']
                }
        
        return trends
```

## 🎯 Behavioral Pattern Mining

### Customer Behavior Analysis
```python
class BehavioralPatternAnalyzer:
    """
    Analyze customer behavioral patterns
    """
    
    def __init__(self):
        self.sequence_miner = SequenceMiner()
        self.association_miner = AssociationRuleMiner()
        self.journey_analyzer = CustomerJourneyAnalyzer()
    
    def detect(self, comments):
        """
        Detect behavioral patterns
        """
        patterns = {
            'feedback_sequences': self.find_feedback_sequences(comments),
            'issue_escalation_patterns': self.find_escalation_patterns(comments),
            'satisfaction_journeys': self.analyze_satisfaction_journeys(comments),
            'complaint_behaviors': self.analyze_complaint_behaviors(comments),
            'engagement_patterns': self.analyze_engagement_patterns(comments)
        }
        
        return patterns
    
    def find_feedback_sequences(self, comments):
        """
        Find common sequences in customer feedback
        """
        # Group comments by customer
        customer_sequences = defaultdict(list)
        
        for comment in comments:
            customer_id = comment.get('customer_id')
            if customer_id:
                customer_sequences[customer_id].append(comment)
        
        # Sort by timestamp for each customer
        for customer_id in customer_sequences:
            customer_sequences[customer_id].sort(
                key=lambda x: x.get('timestamp', '')
            )
        
        # Extract sequences
        sequences = []
        for customer_id, customer_comments in customer_sequences.items():
            if len(customer_comments) > 1:
                sequence = self.extract_comment_sequence(customer_comments)
                sequences.append({
                    'customer_id': customer_id,
                    'sequence': sequence,
                    'length': len(sequence),
                    'timespan': self.calculate_timespan(customer_comments)
                })
        
        # Find common patterns in sequences
        common_patterns = self.sequence_miner.find_patterns(
            [seq['sequence'] for seq in sequences]
        )
        
        return {
            'sequences': sequences,
            'common_patterns': common_patterns,
            'pattern_frequency': self.calculate_pattern_frequency(common_patterns)
        }
    
    def find_escalation_patterns(self, comments):
        """
        Find patterns in issue escalation
        """
        escalation_patterns = []
        
        # Group by issue or customer
        issue_groups = self.group_by_issue(comments)
        
        for issue_id, issue_comments in issue_groups.items():
            # Sort by timestamp
            issue_comments.sort(key=lambda x: x.get('timestamp', ''))
            
            # Analyze escalation
            escalation = self.analyze_escalation_sequence(issue_comments)
            
            if escalation['is_escalated']:
                escalation_patterns.append({
                    'issue_id': issue_id,
                    'comments': issue_comments,
                    'escalation_stages': escalation['stages'],
                    'escalation_speed': escalation['speed'],
                    'resolution_status': escalation['resolution']
                })
        
        return escalation_patterns
```

## 🚨 Anomaly Detection

### Pattern Anomaly Detector
```python
class AnomalyDetector:
    """
    Detect anomalous patterns in feedback data
    """
    
    def __init__(self):
        self.statistical_detector = StatisticalAnomalyDetector()
        self.ml_detector = MLAnomalyDetector()
        self.pattern_detector = PatternAnomalyDetector()
    
    def detect(self, comments):
        """
        Detect anomalies using multiple methods
        """
        anomalies = {
            'statistical_anomalies': self.statistical_detector.detect(comments),
            'ml_anomalies': self.ml_detector.detect(comments),
            'pattern_anomalies': self.pattern_detector.detect(comments),
            'temporal_anomalies': self.detect_temporal_anomalies(comments),
            'content_anomalies': self.detect_content_anomalies(comments)
        }
        
        # Combine and rank anomalies
        combined_anomalies = self.combine_anomalies(anomalies)
        
        return {
            'individual_anomalies': anomalies,
            'combined_anomalies': combined_anomalies,
            'anomaly_score': self.calculate_overall_anomaly_score(combined_anomalies)
        }
    
    def detect_temporal_anomalies(self, comments):
        """
        Detect temporal anomalies
        """
        # Create time series
        timestamps = [
            self.parse_timestamp(comment.get('timestamp'))
            for comment in comments
            if comment.get('timestamp')
        ]
        
        if not timestamps:
            return []
        
        # Group by hour
        hourly_counts = defaultdict(int)
        for ts in timestamps:
            hour_key = ts.strftime('%Y-%m-%d %H:00')
            hourly_counts[hour_key] += 1
        
        # Detect volume spikes
        values = list(hourly_counts.values())
        mean_volume = np.mean(values)
        std_volume = np.std(values)
        
        anomalies = []
        for hour, count in hourly_counts.items():
            z_score = (count - mean_volume) / std_volume if std_volume > 0 else 0
            
            if abs(z_score) > 2.5:  # 2.5 standard deviations
                anomalies.append({
                    'type': 'volume_spike' if z_score > 0 else 'volume_drop',
                    'timestamp': hour,
                    'value': count,
                    'expected': mean_volume,
                    'z_score': z_score,
                    'severity': 'high' if abs(z_score) > 3 else 'medium'
                })
        
        return anomalies
```

## 📊 Pattern Visualization

### Pattern Visualization Engine
```python
class PatternVisualizer:
    """
    Create visualizations for detected patterns
    """
    
    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.network_visualizer = NetworkVisualizer()
        self.timeline_generator = TimelineGenerator()
    
    def visualize_patterns(self, patterns, output_format='html'):
        """
        Create comprehensive pattern visualizations
        """
        visualizations = {
            'pattern_summary': self.create_pattern_summary(patterns),
            'topic_network': self.create_topic_network(patterns),
            'temporal_trends': self.create_temporal_trends(patterns),
            'anomaly_timeline': self.create_anomaly_timeline(patterns),
            'behavioral_flows': self.create_behavioral_flows(patterns)
        }
        
        return visualizations
```

## 🔧 Configuration

### Pattern Detection Settings
```python
PATTERN_DETECTION_CONFIG = {
    'textual_patterns': {
        'min_frequency': 0.05,  # 5% of comments
        'ngram_range': (1, 4),
        'max_patterns': 100,
        'relevance_threshold': 0.3
    },
    'semantic_patterns': {
        'num_topics': 10,
        'clustering_eps': 0.3,
        'min_cluster_size': 3,
        'embedding_model': 'all-MiniLM-L6-v2'
    },
    'temporal_patterns': {
        'time_granularity': 'hour',
        'trend_significance': 0.05,
        'anomaly_threshold': 2.5,
        'seasonality_detection': True
    },
    'behavioral_patterns': {
        'min_sequence_length': 2,
        'escalation_threshold': 3,
        'journey_analysis': True,
        'association_confidence': 0.7
    },
    'performance': {
        'parallel_processing': True,
        'cache_patterns': True,
        'incremental_analysis': True
    }
}
```

## 🔗 Related Documentation
- [Sentiment Analysis](../analysis-engines/sentiment-analysis.md) - Sentiment patterns
- [Theme Detection](../analysis-engines/theme-detection.md) - Theme patterns
- [Batch Processing](batch-processing.md) - Efficient processing
- [Visualization](../exports/visualization.md) - Pattern visualization