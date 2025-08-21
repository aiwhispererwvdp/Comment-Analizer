"""
Emotion Percentage Analysis Tool
Analyzes emotional content in comments and provides detailed statistics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    """Advanced emotion analysis tool with percentage calculations and trends"""
    
    def __init__(self):
        """Initialize emotion analyzer with comprehensive emotion patterns"""
        
        # Extended emotion categories with weighted keywords
        self.emotion_categories = {
            'joy': {
                'keywords': ['feliz', 'contento', 'alegre', 'excelente', 'perfecto', 
                           'genial', 'maravilloso', 'increíble', 'fantástico', 'super',
                           'buenísimo', 'me encanta', 'amor', 'adoro', 'mejor'],
                'weight': 1.0,
                'color': '#4CAF50'
            },
            'satisfaction': {
                'keywords': ['satisfecho', 'conforme', 'bien', 'bueno', 'correcto',
                           'adecuado', 'cumple', 'funciona', 'sirve', 'útil',
                           'recomiendo', 'positivo', 'mejoro', 'estable'],
                'weight': 0.8,
                'color': '#8BC34A'
            },
            'frustration': {
                'keywords': ['frustrado', 'molesto', 'cansado', 'harto', 'fastidio',
                           'no funciona', 'no sirve', 'no anda', 'mal', 'pésimo',
                           'terrible', 'horrible', 'desastre', 'siempre falla'],
                'weight': -0.9,
                'color': '#F44336'
            },
            'anger': {
                'keywords': ['enojado', 'furioso', 'indignado', 'bronca', 'rabia',
                           'ira', 'odio', 'detesto', 'inaceptable', 'vergüenza',
                           'indignante', 'inadmisible', 'intolerable'],
                'weight': -1.0,
                'color': '#D32F2F'
            },
            'disappointment': {
                'keywords': ['decepción', 'decepcionado', 'esperaba más', 'triste',
                           'desilusión', 'lástima', 'podría ser mejor', 'regular',
                           'más o menos', 'meh', 'no es lo que', 'mediocre'],
                'weight': -0.6,
                'color': '#FF9800'
            },
            'anxiety': {
                'keywords': ['preocupado', 'ansioso', 'nervioso', 'inquieto', 'tenso',
                           'estresado', 'agobiado', 'desesperado', 'urgente', 'miedo',
                           'temor', 'angustia', 'incertidumbre'],
                'weight': -0.7,
                'color': '#9C27B0'
            },
            'gratitude': {
                'keywords': ['gracias', 'agradezco', 'agradecido', 'agradecer', 'amable',
                           'atento', 'ayuda', 'solucionó', 'resolvió', 'apoyo',
                           'colaboración', 'servicial', 'cordial'],
                'weight': 0.9,
                'color': '#2196F3'
            },
            'neutral': {
                'keywords': ['normal', 'regular', 'ok', 'está bien', 'aceptable',
                           'promedio', 'estándar', 'común', 'ni bien ni mal'],
                'weight': 0.0,
                'color': '#9E9E9E'
            }
        }
        
        # Emotion intensity modifiers
        self.intensity_modifiers = {
            'very_high': ['muy', 'super', 'extremadamente', 'totalmente', 'completamente', 
                         'absolutamente', 'demasiado', 'sumamente'],
            'high': ['bastante', 'mucho', 'tan', 'realmente', 'verdaderamente'],
            'low': ['poco', 'algo', 'un poco', 'ligeramente', 'apenas']
        }
        
        # Initialize results storage
        self.analysis_results = {}
        self.emotion_timeline = None
        
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in a single text with intensity scores
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with emotion scores
        """
        if pd.isna(text) or not text:
            return {'neutral': 1.0}
        
        text_lower = str(text).lower()
        emotion_scores = defaultdict(float)
        
        # Check for each emotion category
        for emotion, config in self.emotion_categories.items():
            for keyword in config['keywords']:
                if keyword in text_lower:
                    # Base score
                    score = config['weight']
                    
                    # Check for intensity modifiers
                    for modifier_type, modifiers in self.intensity_modifiers.items():
                        for modifier in modifiers:
                            pattern = f"{modifier}\\s+{keyword}"
                            if re.search(pattern, text_lower):
                                if modifier_type == 'very_high':
                                    score *= 1.5
                                elif modifier_type == 'high':
                                    score *= 1.2
                                elif modifier_type == 'low':
                                    score *= 0.7
                                break
                    
                    emotion_scores[emotion] += abs(score)
        
        # Normalize scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_score
        else:
            emotion_scores['neutral'] = 1.0
        
        return dict(emotion_scores)
    
    def analyze_emotion_percentages(self, df: pd.DataFrame, 
                                   text_column: str = 'Comentario Final') -> Dict:
        """
        Analyze emotion percentages across all comments
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            
        Returns:
            Dictionary with emotion statistics
        """
        total_comments = len(df)
        emotion_counts = defaultdict(int)
        emotion_intensities = defaultdict(list)
        emotion_by_score = defaultdict(lambda: defaultdict(int))
        
        # Analyze each comment
        for idx, row in df.iterrows():
            text = row[text_column]
            emotions = self.detect_emotions(text)
            
            # Get dominant emotion
            if emotions:
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])
                emotion_counts[dominant_emotion[0]] += 1
                emotion_intensities[dominant_emotion[0]].append(dominant_emotion[1])
                
                # Track by score if available
                if 'Nota' in df.columns and not pd.isna(row['Nota']):
                    score_category = self._categorize_score(row['Nota'])
                    emotion_by_score[dominant_emotion[0]][score_category] += 1
        
        # Calculate percentages
        emotion_percentages = {}
        for emotion, count in emotion_counts.items():
            percentage = (count / total_comments * 100) if total_comments > 0 else 0
            emotion_percentages[emotion] = {
                'count': count,
                'percentage': round(percentage, 2),
                'avg_intensity': round(np.mean(emotion_intensities[emotion]), 3) if emotion_intensities[emotion] else 0,
                'color': self.emotion_categories.get(emotion, {}).get('color', '#808080')
            }
        
        # Sort by percentage
        emotion_percentages = dict(sorted(emotion_percentages.items(), 
                                        key=lambda x: x[1]['percentage'], 
                                        reverse=True))
        
        # Calculate emotion balance
        positive_emotions = ['joy', 'satisfaction', 'gratitude']
        negative_emotions = ['frustration', 'anger', 'disappointment', 'anxiety']
        
        positive_percentage = sum(emotion_percentages.get(e, {}).get('percentage', 0) 
                                for e in positive_emotions)
        negative_percentage = sum(emotion_percentages.get(e, {}).get('percentage', 0) 
                                for e in negative_emotions)
        neutral_percentage = emotion_percentages.get('neutral', {}).get('percentage', 0)
        
        results = {
            'total_analyzed': total_comments,
            'emotion_percentages': emotion_percentages,
            'emotion_balance': {
                'positive': round(positive_percentage, 2),
                'negative': round(negative_percentage, 2),
                'neutral': round(neutral_percentage, 2)
            },
            'emotion_by_score': dict(emotion_by_score),
            'dominant_emotion': max(emotion_percentages.items(), 
                                  key=lambda x: x[1]['percentage'])[0] if emotion_percentages else 'neutral'
        }
        
        self.analysis_results = results
        return results
    
    def analyze_emotion_trends(self, df: pd.DataFrame, 
                             text_column: str = 'Comentario Final',
                             date_column: str = 'Fecha') -> pd.DataFrame:
        """
        Analyze emotion trends over time
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            date_column: Column name containing dates
            
        Returns:
            DataFrame with emotion trends
        """
        if date_column not in df.columns:
            logger.warning(f"Date column '{date_column}' not found")
            return pd.DataFrame()
        
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])
        
        # Group by week/month
        df['period'] = df[date_column].dt.to_period('W')
        
        emotion_trends = []
        for period, group in df.groupby('period'):
            period_emotions = defaultdict(int)
            for text in group[text_column]:
                emotions = self.detect_emotions(text)
                if emotions:
                    dominant = max(emotions.items(), key=lambda x: x[1])[0]
                    period_emotions[dominant] += 1
            
            # Calculate percentages for period
            total = sum(period_emotions.values())
            if total > 0:
                for emotion, count in period_emotions.items():
                    emotion_trends.append({
                        'period': str(period),
                        'emotion': emotion,
                        'count': count,
                        'percentage': round(count / total * 100, 2)
                    })
        
        self.emotion_timeline = pd.DataFrame(emotion_trends)
        return self.emotion_timeline
    
    def generate_emotion_report(self, df: pd.DataFrame, 
                               text_column: str = 'Comentario Final') -> Dict:
        """
        Generate comprehensive emotion analysis report
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            
        Returns:
            Complete emotion analysis report
        """
        # Basic emotion analysis
        emotion_stats = self.analyze_emotion_percentages(df, text_column)
        
        # Correlation with scores
        emotion_score_correlation = self._analyze_emotion_score_correlation(df, text_column)
        
        # Find most emotional comments
        emotional_comments = self._find_most_emotional_comments(df, text_column)
        
        # Generate insights
        insights = self._generate_emotion_insights(emotion_stats, emotion_score_correlation)
        
        report = {
            'summary': emotion_stats,
            'score_correlation': emotion_score_correlation,
            'emotional_comments': emotional_comments,
            'insights': insights,
            'recommendations': self._generate_recommendations(emotion_stats)
        }
        
        return report
    
    def _categorize_score(self, score: float) -> str:
        """Categorize NPS score"""
        if score >= 9:
            return 'promoter'
        elif score >= 7:
            return 'passive'
        else:
            return 'detractor'
    
    def _analyze_emotion_score_correlation(self, df: pd.DataFrame, 
                                          text_column: str) -> Dict:
        """Analyze correlation between emotions and scores"""
        if 'Nota' not in df.columns:
            return {}
        
        correlation_data = defaultdict(list)
        
        for idx, row in df.iterrows():
            if pd.isna(row['Nota']):
                continue
                
            emotions = self.detect_emotions(row[text_column])
            if emotions:
                dominant = max(emotions.items(), key=lambda x: x[1])[0]
                correlation_data[dominant].append(row['Nota'])
        
        correlations = {}
        for emotion, scores in correlation_data.items():
            if scores:
                correlations[emotion] = {
                    'avg_score': round(np.mean(scores), 2),
                    'std_score': round(np.std(scores), 2),
                    'min_score': min(scores),
                    'max_score': max(scores),
                    'sample_size': len(scores)
                }
        
        return correlations
    
    def _find_most_emotional_comments(self, df: pd.DataFrame, 
                                     text_column: str, 
                                     top_n: int = 5) -> Dict:
        """Find most emotional comments for each category"""
        emotional_comments = defaultdict(list)
        
        for idx, row in df.iterrows():
            text = row[text_column]
            if pd.isna(text):
                continue
                
            emotions = self.detect_emotions(text)
            if emotions:
                dominant = max(emotions.items(), key=lambda x: x[1])
                emotional_comments[dominant[0]].append({
                    'text': text[:200] + '...' if len(str(text)) > 200 else text,
                    'intensity': dominant[1],
                    'score': row.get('Nota', None)
                })
        
        # Get top N for each emotion
        top_comments = {}
        for emotion, comments in emotional_comments.items():
            sorted_comments = sorted(comments, key=lambda x: x['intensity'], reverse=True)
            top_comments[emotion] = sorted_comments[:top_n]
        
        return top_comments
    
    def _generate_emotion_insights(self, stats: Dict, correlations: Dict) -> List[str]:
        """Generate insights from emotion analysis"""
        insights = []
        
        # Dominant emotion insight
        if stats.get('dominant_emotion'):
            dominant = stats['dominant_emotion']
            percentage = stats['emotion_percentages'][dominant]['percentage']
            insights.append(f"The dominant emotion is {dominant} ({percentage}% of comments)")
        
        # Balance insight
        balance = stats.get('emotion_balance', {})
        if balance.get('negative', 0) > balance.get('positive', 0):
            diff = balance['negative'] - balance['positive']
            insights.append(f"Negative emotions outweigh positive by {diff:.1f}%")
        elif balance.get('positive', 0) > balance.get('negative', 0):
            diff = balance['positive'] - balance['negative']
            insights.append(f"Positive emotions outweigh negative by {diff:.1f}%")
        
        # Score correlation insight
        if correlations:
            highest_score_emotion = max(correlations.items(), 
                                       key=lambda x: x[1]['avg_score'])[0]
            lowest_score_emotion = min(correlations.items(), 
                                      key=lambda x: x[1]['avg_score'])[0]
            
            insights.append(f"{highest_score_emotion.capitalize()} correlates with highest scores")
            insights.append(f"{lowest_score_emotion.capitalize()} correlates with lowest scores")
        
        return insights
    
    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """Generate recommendations based on emotion analysis"""
        recommendations = []
        balance = stats.get('emotion_balance', {})
        
        if balance.get('negative', 0) > 40:
            recommendations.append("High negative emotion detected - prioritize customer support improvements")
        
        if stats.get('emotion_percentages', {}).get('frustration', {}).get('percentage', 0) > 20:
            recommendations.append("Significant frustration detected - review service reliability")
        
        if stats.get('emotion_percentages', {}).get('anxiety', {}).get('percentage', 0) > 15:
            recommendations.append("Customer anxiety elevated - improve communication and transparency")
        
        if balance.get('positive', 0) > 60:
            recommendations.append("Strong positive sentiment - leverage for testimonials and marketing")
        
        return recommendations
    
    def visualize_emotions(self, save_path: Optional[str] = None):
        """Create emotion visualization charts"""
        if not self.analysis_results:
            logger.warning("No analysis results to visualize")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Emotion distribution pie chart
        emotion_data = self.analysis_results['emotion_percentages']
        labels = list(emotion_data.keys())
        sizes = [data['percentage'] for data in emotion_data.values()]
        colors = [data['color'] for data in emotion_data.values()]
        
        axes[0, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        axes[0, 0].set_title('Emotion Distribution')
        
        # Emotion balance bar chart
        balance = self.analysis_results['emotion_balance']
        axes[0, 1].bar(balance.keys(), balance.values(), 
                      color=['#4CAF50', '#F44336', '#9E9E9E'])
        axes[0, 1].set_title('Emotion Balance')
        axes[0, 1].set_ylabel('Percentage')
        
        # Emotion intensity heatmap (if timeline available)
        if self.emotion_timeline is not None and not self.emotion_timeline.empty:
            pivot = self.emotion_timeline.pivot_table(
                index='emotion', columns='period', values='percentage', fill_value=0
            )
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', ax=axes[1, 0])
            axes[1, 0].set_title('Emotion Trends Over Time')
        
        # Top emotions bar chart
        top_emotions = list(emotion_data.items())[:5]
        axes[1, 1].barh([e[0] for e in top_emotions], 
                       [e[1]['percentage'] for e in top_emotions],
                       color=[e[1]['color'] for e in top_emotions])
        axes[1, 1].set_title('Top 5 Emotions')
        axes[1, 1].set_xlabel('Percentage')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Emotion visualization saved to {save_path}")
        
        return fig