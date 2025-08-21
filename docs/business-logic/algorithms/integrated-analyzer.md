# Integrated Analyzer Documentation

The Integrated Analyzer module orchestrates the complete analysis pipeline, combining multiple AI engines to provide comprehensive insights from customer feedback data.

## 🎯 Overview

This module serves as the central coordination point for all analysis operations, intelligently combining sentiment analysis, theme detection, emotion analysis, and language processing to deliver unified, actionable insights.

### Core Capabilities
- **Multi-Engine Coordination** - Orchestrate multiple analysis engines
- **Intelligent Workflow Management** - Optimize analysis sequences
- **Result Integration** - Combine and cross-validate results
- **Adaptive Processing** - Adjust analysis based on content characteristics
- **Quality Assurance** - Ensure analysis accuracy and consistency

## 🏗️ Integrated Analysis Architecture

### Multi-Engine Analysis Framework
```python
class IntegratedAnalysisArchitecture:
    """
    Comprehensive integrated analysis system architecture
    """
    
    ANALYSIS_ENGINES = {
        'sentiment': {
            'primary': SentimentAnalyzer,
            'fallback': RuleBased SentimentAnalyzer,
            'confidence_threshold': 0.7,
            'languages': ['es', 'gn', 'en', 'jopara']
        },
        'theme': {
            'primary': ThemeDetector,
            'fallback': KeywordThemeDetector,
            'confidence_threshold': 0.6,
            'min_themes': 1,
            'max_themes': 5
        },
        'emotion': {
            'primary': EmotionAnalyzer,
            'fallback': LexiconEmotionAnalyzer,
            'confidence_threshold': 0.6,
            'emotion_categories': ['joy', 'anger', 'sadness', 'fear', 'surprise', 'disgust']
        },
        'language': {
            'primary': LanguageDetector,
            'fallback': SimpleLanguageDetector,
            'confidence_threshold': 0.8,
            'supported_languages': ['es', 'gn', 'jopara', 'en', 'pt']
        }
    }
    
    WORKFLOW_STRATEGIES = {
        'sequential': 'Process engines one after another',
        'parallel': 'Process all engines simultaneously',
        'adaptive': 'Dynamically choose based on content',
        'cascade': 'Use results from one engine to inform others'
    }
```

## 🎼 Core Integration Engine

### Master Analysis Orchestrator
```python
class IntegratedAnalyzer:
    """
    Master analyzer that coordinates all analysis engines
    """
    
    def __init__(self):
        # Initialize analysis engines
        self.engines = {
            'sentiment': SentimentAnalyzer(),
            'theme': ThemeDetector(),
            'emotion': EmotionAnalyzer(),
            'language': LanguageDetector(),
            'pattern': PatternDetector()
        }
        
        # Initialize coordination components
        self.workflow_manager = WorkflowManager()
        self.result_integrator = ResultIntegrator()
        self.quality_assurance = QualityAssurance()
        self.conflict_resolver = ConflictResolver()
        self.confidence_calculator = ConfidenceCalculator()
        
        # Performance and optimization
        self.cache_manager = CacheManager()
        self.batch_optimizer = BatchOptimizer()
        
    async def analyze_comprehensive(self, comments, analysis_config=None):
        """
        Perform comprehensive analysis on comments
        """
        # Validate and prepare input
        validated_comments = self.validate_input(comments)
        if not validated_comments:
            return self.create_empty_results()
        
        # Apply configuration
        config = self.apply_analysis_config(analysis_config)
        
        # Create analysis session
        session = AnalysisSession(
            session_id=self.generate_session_id(),
            comments=validated_comments,
            config=config
        )
        
        try:
            # Phase 1: Pre-analysis preparation
            prepared_data = await self.prepare_for_analysis(validated_comments, session)
            
            # Phase 2: Core analysis execution
            raw_results = await self.execute_analysis_workflow(prepared_data, session)
            
            # Phase 3: Result integration and validation
            integrated_results = await self.integrate_results(raw_results, session)
            
            # Phase 4: Quality assurance and refinement
            final_results = await self.apply_quality_assurance(integrated_results, session)
            
            # Phase 5: Generate insights and recommendations
            insights = await self.generate_insights(final_results, session)
            
            return {
                'results': final_results,
                'insights': insights,
                'session_info': session.get_summary(),
                'quality_metrics': self.calculate_quality_metrics(final_results)
            }
            
        except Exception as e:
            return await self.handle_analysis_error(e, session)
    
    async def execute_analysis_workflow(self, comments, session):
        """
        Execute the analysis workflow based on strategy
        """
        strategy = session.config.get('workflow_strategy', 'adaptive')
        
        if strategy == 'sequential':
            return await self.execute_sequential_workflow(comments, session)
        elif strategy == 'parallel':
            return await self.execute_parallel_workflow(comments, session)
        elif strategy == 'cascade':
            return await self.execute_cascade_workflow(comments, session)
        elif strategy == 'adaptive':
            return await self.execute_adaptive_workflow(comments, session)
        
        raise ValueError(f"Unknown workflow strategy: {strategy}")
```

## 🔄 Workflow Management

### Intelligent Workflow Orchestration
```python
class WorkflowManager:
    """
    Manage analysis workflow execution and optimization
    """
    
    def __init__(self):
        self.workflow_optimizer = WorkflowOptimizer()
        self.dependency_manager = DependencyManager()
        self.performance_monitor = PerformanceMonitor()
    
    async def execute_adaptive_workflow(self, comments, session):
        """
        Execute adaptive workflow based on content characteristics
        """
        # Analyze content characteristics
        content_profile = self.analyze_content_characteristics(comments)
        
        # Determine optimal workflow
        optimal_workflow = self.workflow_optimizer.optimize_workflow(
            content_profile,
            session.config
        )
        
        # Execute workflow with dynamic optimization
        results = {}
        
        for stage in optimal_workflow['stages']:
            stage_results = await self.execute_workflow_stage(
                stage,
                comments,
                results,  # Previous results for context
                session
            )
            
            # Update results
            results.update(stage_results)
            
            # Optimize next stage based on current results
            if stage != optimal_workflow['stages'][-1]:
                next_stage_optimization = self.optimize_next_stage(
                    results,
                    optimal_workflow,
                    stage
                )
                optimal_workflow = self.apply_stage_optimization(
                    optimal_workflow,
                    next_stage_optimization
                )
        
        return results
    
    async def execute_cascade_workflow(self, comments, session):
        """
        Execute cascade workflow where each engine informs the next
        """
        cascade_results = {}
        
        # Stage 1: Language detection (informs all other analyses)
        language_results = await self.engines['language'].analyze_batch(comments)
        cascade_results['language'] = language_results
        
        # Stage 2: Sentiment analysis (informed by language detection)
        sentiment_config = self.create_language_informed_config(
            language_results,
            'sentiment'
        )
        sentiment_results = await self.engines['sentiment'].analyze_batch(
            comments,
            config=sentiment_config
        )
        cascade_results['sentiment'] = sentiment_results
        
        # Stage 3: Theme detection (informed by sentiment and language)
        theme_config = self.create_multi_informed_config(
            [language_results, sentiment_results],
            'theme'
        )
        theme_results = await self.engines['theme'].analyze_batch(
            comments,
            config=theme_config
        )
        cascade_results['theme'] = theme_results
        
        # Stage 4: Emotion analysis (informed by all previous)
        emotion_config = self.create_comprehensive_informed_config(
            cascade_results,
            'emotion'
        )
        emotion_results = await self.engines['emotion'].analyze_batch(
            comments,
            config=emotion_config
        )
        cascade_results['emotion'] = emotion_results
        
        return cascade_results
```

## 🔗 Result Integration

### Multi-Engine Result Integration
```python
class ResultIntegrator:
    """
    Integrate results from multiple analysis engines
    """
    
    def __init__(self):
        self.cross_validator = CrossValidator()
        self.consensus_builder = ConsensusBuilder()
        self.conflict_resolver = ConflictResolver()
        self.confidence_aggregator = ConfidenceAggregator()
    
    async def integrate_results(self, raw_results, session):
        """
        Integrate and validate results from multiple engines
        """
        integrated_results = []
        
        # Process each comment's results
        for comment_idx, comment in enumerate(session.comments):
            comment_results = self.extract_comment_results(
                raw_results,
                comment_idx
            )
            
            # Cross-validate results between engines
            validation_report = self.cross_validator.validate(comment_results)
            
            # Resolve conflicts between engines
            resolved_results = self.conflict_resolver.resolve(
                comment_results,
                validation_report
            )
            
            # Build consensus where possible
            consensus_results = self.consensus_builder.build_consensus(
                resolved_results
            )
            
            # Calculate integrated confidence scores
            confidence_scores = self.confidence_aggregator.aggregate(
                consensus_results
            )
            
            # Create integrated result
            integrated_result = self.create_integrated_result(
                comment,
                consensus_results,
                confidence_scores,
                validation_report
            )
            
            integrated_results.append(integrated_result)
        
        return integrated_results
    
    def create_integrated_result(self, comment, results, confidence, validation):
        """
        Create comprehensive integrated result for a comment
        """
        return {
            'comment_id': comment.get('id'),
            'original_text': comment.get('text'),
            'analysis': {
                'language': {
                    'detected': results['language']['primary'],
                    'confidence': confidence['language'],
                    'alternatives': results['language'].get('alternatives', [])
                },
                'sentiment': {
                    'polarity': results['sentiment']['polarity'],
                    'score': results['sentiment']['score'],
                    'confidence': confidence['sentiment'],
                    'emotions': results['sentiment'].get('emotions', [])
                },
                'themes': {
                    'primary_themes': results['theme']['primary'],
                    'secondary_themes': results['theme'].get('secondary', []),
                    'confidence': confidence['theme'],
                    'theme_scores': results['theme'].get('scores', {})
                },
                'emotions': {
                    'primary_emotion': results['emotion']['primary'],
                    'emotion_distribution': results['emotion']['distribution'],
                    'confidence': confidence['emotion'],
                    'intensity': results['emotion'].get('intensity', 0.5)
                }
            },
            'quality_indicators': {
                'overall_confidence': confidence['overall'],
                'cross_validation_score': validation['score'],
                'consensus_level': validation['consensus_level'],
                'potential_issues': validation.get('issues', [])
            },
            'metadata': {
                'processing_timestamp': datetime.now(),
                'engines_used': list(results.keys()),
                'processing_time': validation.get('processing_time'),
                'analysis_version': session.config.get('version', '1.0')
            }
        }
```

## 🎯 Conflict Resolution

### Intelligent Conflict Resolution
```python
class ConflictResolver:
    """
    Resolve conflicts between different analysis engines
    """
    
    def __init__(self):
        self.confidence_evaluator = ConfidenceEvaluator()
        self.consensus_calculator = ConsensusCalculator()
        self.historical_accuracy = HistoricalAccuracy()
    
    def resolve(self, comment_results, validation_report):
        """
        Resolve conflicts between engine results
        """
        resolved = {}
        conflicts = validation_report.get('conflicts', {})
        
        for analysis_type, conflict_info in conflicts.items():
            if conflict_info['severity'] == 'low':
                # Minor conflicts - use highest confidence result
                resolved[analysis_type] = self.resolve_by_confidence(
                    comment_results[analysis_type]
                )
            
            elif conflict_info['severity'] == 'medium':
                # Medium conflicts - use weighted consensus
                resolved[analysis_type] = self.resolve_by_weighted_consensus(
                    comment_results[analysis_type],
                    conflict_info
                )
            
            elif conflict_info['severity'] == 'high':
                # High conflicts - use historical accuracy + manual review flag
                resolved[analysis_type] = self.resolve_by_historical_accuracy(
                    comment_results[analysis_type],
                    conflict_info
                )
                resolved[analysis_type]['requires_manual_review'] = True
            
            else:
                # No conflicts - use best result
                resolved[analysis_type] = self.select_best_result(
                    comment_results[analysis_type]
                )
        
        return resolved
    
    def resolve_by_weighted_consensus(self, engine_results, conflict_info):
        """
        Resolve conflicts using weighted consensus
        """
        weights = self.calculate_engine_weights(engine_results, conflict_info)
        
        # For sentiment analysis
        if 'sentiment' in engine_results:
            weighted_sentiment = self.calculate_weighted_sentiment(
                engine_results['sentiment'],
                weights
            )
            return weighted_sentiment
        
        # For theme detection
        elif 'theme' in engine_results:
            consensus_themes = self.build_theme_consensus(
                engine_results['theme'],
                weights
            )
            return consensus_themes
        
        # For emotion analysis
        elif 'emotion' in engine_results:
            blended_emotions = self.blend_emotion_results(
                engine_results['emotion'],
                weights
            )
            return blended_emotions
        
        return engine_results
```

## 🏆 Quality Assurance

### Comprehensive Quality Control
```python
class QualityAssurance:
    """
    Ensure quality and accuracy of integrated analysis results
    """
    
    def __init__(self):
        self.accuracy_validator = AccuracyValidator()
        self.consistency_checker = ConsistencyChecker()
        self.completeness_verifier = CompletenessVerifier()
        self.reliability_assessor = ReliabilityAssessor()
    
    async def apply_quality_assurance(self, results, session):
        """
        Apply comprehensive quality assurance to results
        """
        qa_results = []
        
        for result in results:
            # Validate accuracy
            accuracy_score = self.accuracy_validator.validate(result)
            
            # Check consistency
            consistency_report = self.consistency_checker.check(result)
            
            # Verify completeness
            completeness_score = self.completeness_verifier.verify(result)
            
            # Assess reliability
            reliability_score = self.reliability_assessor.assess(result)
            
            # Calculate overall quality score
            quality_score = self.calculate_overall_quality(
                accuracy_score,
                consistency_report,
                completeness_score,
                reliability_score
            )
            
            # Apply quality improvements if needed
            if quality_score < 0.7:
                improved_result = await self.improve_result_quality(
                    result,
                    {
                        'accuracy': accuracy_score,
                        'consistency': consistency_report,
                        'completeness': completeness_score,
                        'reliability': reliability_score
                    }
                )
            else:
                improved_result = result
            
            # Add quality metadata
            improved_result['quality_assurance'] = {
                'overall_score': quality_score,
                'accuracy_score': accuracy_score,
                'consistency_score': consistency_report['score'],
                'completeness_score': completeness_score,
                'reliability_score': reliability_score,
                'qa_timestamp': datetime.now()
            }
            
            qa_results.append(improved_result)
        
        return qa_results
```

## 📊 Insight Generation

### Automated Insight Generation
```python
class InsightGenerator:
    """
    Generate actionable insights from integrated analysis results
    """
    
    def __init__(self):
        self.pattern_analyzer = PatternAnalyzer()
        self.trend_detector = TrendDetector()
        self.anomaly_detector = AnomalyDetector()
        self.recommendation_engine = RecommendationEngine()
    
    async def generate_insights(self, results, session):
        """
        Generate comprehensive insights from analysis results
        """
        insights = {
            'overview': self.generate_overview_insights(results),
            'sentiment_insights': self.generate_sentiment_insights(results),
            'theme_insights': self.generate_theme_insights(results),
            'emotional_insights': self.generate_emotional_insights(results),
            'language_insights': self.generate_language_insights(results),
            'quality_insights': self.generate_quality_insights(results),
            'actionable_recommendations': await self.generate_recommendations(results),
            'alerts': self.generate_alerts(results)
        }
        
        return insights
    
    def generate_overview_insights(self, results):
        """
        Generate high-level overview insights
        """
        total_comments = len(results)
        
        # Sentiment distribution
        sentiment_dist = self.calculate_sentiment_distribution(results)
        
        # Theme distribution
        theme_dist = self.calculate_theme_distribution(results)
        
        # Language distribution
        language_dist = self.calculate_language_distribution(results)
        
        # Quality metrics
        avg_confidence = np.mean([
            r['quality_indicators']['overall_confidence']
            for r in results
        ])
        
        return {
            'total_comments_analyzed': total_comments,
            'sentiment_distribution': sentiment_dist,
            'top_themes': theme_dist['top_5'],
            'language_breakdown': language_dist,
            'average_confidence': avg_confidence,
            'processing_quality': 'high' if avg_confidence > 0.8 else 'medium' if avg_confidence > 0.6 else 'low'
        }
    
    async def generate_recommendations(self, results):
        """
        Generate actionable business recommendations
        """
        recommendations = []
        
        # Sentiment-based recommendations
        sentiment_issues = self.identify_sentiment_issues(results)
        for issue in sentiment_issues:
            rec = await self.recommendation_engine.generate_sentiment_recommendation(issue)
            recommendations.append(rec)
        
        # Theme-based recommendations
        theme_opportunities = self.identify_theme_opportunities(results)
        for opportunity in theme_opportunities:
            rec = await self.recommendation_engine.generate_theme_recommendation(opportunity)
            recommendations.append(rec)
        
        # Quality-based recommendations
        quality_improvements = self.identify_quality_improvements(results)
        for improvement in quality_improvements:
            rec = await self.recommendation_engine.generate_quality_recommendation(improvement)
            recommendations.append(rec)
        
        # Prioritize recommendations
        prioritized_recommendations = self.prioritize_recommendations(recommendations)
        
        return prioritized_recommendations
```

## 🔧 Performance Optimization

### Analysis Performance Optimization
```python
class AnalysisOptimizer:
    """
    Optimize integrated analysis performance
    """
    
    def __init__(self):
        self.cache_manager = AnalysisCache()
        self.parallel_processor = ParallelProcessor()
        self.resource_manager = ResourceManager()
    
    def optimize_analysis_pipeline(self, comments, config):
        """
        Optimize the analysis pipeline for performance
        """
        # Analyze workload characteristics
        workload_profile = self.analyze_workload(comments, config)
        
        # Optimize engine selection
        engine_config = self.optimize_engine_selection(workload_profile)
        
        # Optimize processing strategy
        processing_strategy = self.optimize_processing_strategy(workload_profile)
        
        # Optimize resource allocation
        resource_allocation = self.optimize_resource_allocation(workload_profile)
        
        return {
            'engine_config': engine_config,
            'processing_strategy': processing_strategy,
            'resource_allocation': resource_allocation,
            'estimated_performance': self.estimate_performance(workload_profile)
        }
```

## 🔧 Configuration

### Integrated Analysis Settings
```python
INTEGRATED_ANALYSIS_CONFIG = {
    'workflow_strategy': 'adaptive',  # sequential, parallel, cascade, adaptive
    'engines': {
        'sentiment': {
            'enabled': True,
            'model': 'transformer',
            'fallback': 'lexicon',
            'confidence_threshold': 0.7
        },
        'theme': {
            'enabled': True,
            'model': 'topic_modeling',
            'max_themes': 5,
            'confidence_threshold': 0.6
        },
        'emotion': {
            'enabled': True,
            'model': 'emotion_classifier',
            'granularity': 'detailed',
            'confidence_threshold': 0.6
        },
        'language': {
            'enabled': True,
            'model': 'multi_language',
            'supported_languages': ['es', 'gn', 'jopara', 'en'],
            'confidence_threshold': 0.8
        }
    },
    'quality_assurance': {
        'enabled': True,
        'minimum_quality_score': 0.7,
        'cross_validation': True,
        'conflict_resolution': 'weighted_consensus'
    },
    'performance': {
        'parallel_processing': True,
        'caching_enabled': True,
        'batch_optimization': True,
        'resource_monitoring': True
    },
    'insights': {
        'generate_recommendations': True,
        'detect_anomalies': True,
        'trend_analysis': True,
        'alert_generation': True
    }
}
```

## 🔗 Related Documentation
- [Sentiment Analysis](../analysis-engines/sentiment-analysis.md) - Sentiment analysis engine
- [Theme Detection](../analysis-engines/theme-detection.md) - Theme detection engine
- [Pattern Detection](pattern-detection.md) - Pattern analysis
- [Batch Processing](batch-processing.md) - Batch processing optimization