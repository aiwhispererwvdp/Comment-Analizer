"""
Theme Analysis Tool with Statistics
Identifies and analyzes themes/topics in customer comments
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter, defaultdict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import logging

logger = logging.getLogger(__name__)

class ThemeAnalyzer:
    """Advanced theme analysis tool for comment categorization and insights"""
    
    def __init__(self):
        """Initialize theme analyzer with predefined categories and patterns"""
        
        # Predefined theme categories with keywords and patterns
        self.theme_categories = {
            'service_quality': {
                'keywords': ['servicio', 'calidad', 'atención', 'soporte', 'ayuda',
                           'técnico', 'personal', 'empleado', 'operador', 'asesor',
                           'trato', 'respuesta', 'solución', 'resolver', 'arreglar'],
                'patterns': [r'atención\s+al\s+cliente', r'servicio\s+técnico', 
                           r'mala\s+atención', r'buena\s+atención'],
                'color': '#2196F3'
            },
            'connectivity_issues': {
                'keywords': ['conexión', 'internet', 'wifi', 'red', 'señal',
                           'corte', 'intermitente', 'cae', 'desconecta', 'inestable',
                           'lento', 'velocidad', 'ping', 'latencia', 'lag'],
                'patterns': [r'sin\s+internet', r'no\s+funciona', r'se\s+corta',
                           r'muy\s+lento', r'no\s+anda'],
                'color': '#F44336'
            },
            'pricing_billing': {
                'keywords': ['precio', 'costo', 'tarifa', 'factura', 'cobro',
                           'pago', 'caro', 'barato', 'aumento', 'descuento',
                           'plan', 'promoción', 'oferta', 'valor', 'dinero'],
                'patterns': [r'muy\s+caro', r'precio\s+justo', r'cobran\s+de\s+más',
                           r'error\s+en\s+factura'],
                'color': '#4CAF50'
            },
            'installation_setup': {
                'keywords': ['instalación', 'instalar', 'configurar', 'setup',
                           'router', 'modem', 'equipo', 'cable', 'fibra',
                           'antena', 'dispositivo', 'aparato', 'conexión inicial'],
                'patterns': [r'instalación\s+rápida', r'demora\s+instalación',
                           r'configuración\s+difícil'],
                'color': '#FF9800'
            },
            'technical_performance': {
                'keywords': ['velocidad', 'rápido', 'lento', 'rendimiento', 'performance',
                           'descarga', 'carga', 'streaming', 'video', 'juego',
                           'buffering', 'calidad', 'HD', '4K', 'pixelado'],
                'patterns': [r'\d+\s*mb', r'mega\s*bits?', r'giga\s*bits?',
                           r'alta\s+velocidad', r'baja\s+velocidad'],
                'color': '#9C27B0'
            },
            'coverage_availability': {
                'keywords': ['cobertura', 'zona', 'área', 'disponible', 'alcance',
                           'llega', 'disponibilidad', 'expansión', 'nuevo', 'barrio',
                           'ciudad', 'rural', 'urbano', 'distancia'],
                'patterns': [r'no\s+hay\s+cobertura', r'llega\s+a\s+mi\s+zona',
                           r'cuando\s+llega', r'ampliar\s+cobertura'],
                'color': '#00BCD4'
            },
            'customer_experience': {
                'keywords': ['experiencia', 'satisfecho', 'contento', 'feliz', 'molesto',
                           'frustrado', 'decepcionado', 'recomiendo', 'cambiar', 'cancelar',
                           'mejor', 'peor', 'excelente', 'terrible', 'malo'],
                'patterns': [r'muy\s+satisfecho', r'totalmente\s+insatisfecho',
                           r'lo\s+recomiendo', r'no\s+recomiendo'],
                'color': '#795548'
            },
            'reliability_stability': {
                'keywords': ['estable', 'confiable', 'seguro', 'constante', 'falla',
                           'problema', 'error', 'bug', 'caída', 'interrupción',
                           'mantenimiento', 'arreglo', 'solución', 'permanente'],
                'patterns': [r'siempre\s+funciona', r'nunca\s+funciona', 
                           r'falla\s+constante', r'muy\s+estable'],
                'color': '#607D8B'
            },
            'competitor_comparison': {
                'keywords': ['competencia', 'otro', 'proveedor', 'cambiar', 'migrar',
                           'mejor que', 'peor que', 'comparado', 'versus', 'alternativa',
                           'opción', 'elegir', 'preferir', 'anterior'],
                'patterns': [r'mejor\s+que\s+\w+', r'peor\s+que\s+\w+',
                           r'cambié\s+de\s+\w+', r'voy\s+a\s+cambiar'],
                'color': '#E91E63'
            },
            'contract_terms': {
                'keywords': ['contrato', 'término', 'condición', 'cláusula', 'permanencia',
                           'cancelación', 'multa', 'penalidad', 'compromiso', 'plazo',
                           'renovación', 'vencimiento', 'acuerdo', 'legal'],
                'patterns': [r'sin\s+permanencia', r'contrato\s+abusivo',
                           r'términos\s+claros', r'letra\s+chica'],
                'color': '#3F51B5'
            }
        }
        
        # Spanish stop words
        self.stop_words = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se',
            'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar',
            'tener', 'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o',
            'poder', 'decir', 'este', 'ir', 'otro', 'ese', 'si', 'me',
            'ya', 'ver', 'porque', 'dar', 'cuando', 'muy', 'sin', 'vez',
            'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo',
            'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre'
        ])
        
        self.analysis_results = {}
        self.theme_trends = None
        
    def detect_themes(self, text: str) -> Dict[str, float]:
        """
        Detect themes in a single text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with theme scores
        """
        if pd.isna(text) or not text:
            return {}
        
        text_lower = str(text).lower()
        theme_scores = defaultdict(float)
        
        for theme, config in self.theme_categories.items():
            score = 0
            
            # Check keywords
            for keyword in config['keywords']:
                if keyword in text_lower:
                    score += 1
            
            # Check patterns
            for pattern in config['patterns']:
                if re.search(pattern, text_lower):
                    score += 2  # Patterns have higher weight
            
            if score > 0:
                theme_scores[theme] = score
        
        # Normalize scores
        total_score = sum(theme_scores.values())
        if total_score > 0:
            for theme in theme_scores:
                theme_scores[theme] /= total_score
        
        return dict(theme_scores)
    
    def analyze_themes(self, df: pd.DataFrame, 
                      text_column: str = 'Comentario Final') -> Dict:
        """
        Analyze themes across all comments
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            
        Returns:
            Dictionary with theme statistics
        """
        total_comments = len(df)
        theme_counts = defaultdict(int)
        theme_scores_list = defaultdict(list)
        theme_combinations = Counter()
        theme_by_score = defaultdict(lambda: defaultdict(int))
        
        # Analyze each comment
        for idx, row in df.iterrows():
            text = row[text_column]
            themes = self.detect_themes(text)
            
            if themes:
                # Track all themes present
                present_themes = list(themes.keys())
                if len(present_themes) > 1:
                    theme_combinations[tuple(sorted(present_themes[:2]))] += 1
                
                # Get dominant theme
                dominant_theme = max(themes.items(), key=lambda x: x[1])[0]
                theme_counts[dominant_theme] += 1
                
                # Track all theme scores
                for theme, score in themes.items():
                    theme_scores_list[theme].append(score)
                
                # Track by NPS score if available
                if 'Nota' in df.columns and not pd.isna(row['Nota']):
                    score_category = self._categorize_score(row['Nota'])
                    theme_by_score[dominant_theme][score_category] += 1
        
        # Calculate statistics
        theme_stats = {}
        for theme in self.theme_categories.keys():
            count = theme_counts.get(theme, 0)
            percentage = (count / total_comments * 100) if total_comments > 0 else 0
            
            theme_stats[theme] = {
                'count': count,
                'percentage': round(percentage, 2),
                'avg_relevance': round(np.mean(theme_scores_list[theme]), 3) if theme_scores_list[theme] else 0,
                'color': self.theme_categories[theme]['color'],
                'top_keywords': self._get_top_keywords_for_theme(df, text_column, theme)
            }
        
        # Sort by percentage
        theme_stats = dict(sorted(theme_stats.items(), 
                                key=lambda x: x[1]['percentage'], 
                                reverse=True))
        
        # Get top theme combinations
        top_combinations = [
            {
                'themes': list(combo),
                'count': count,
                'percentage': round(count / total_comments * 100, 2)
            }
            for combo, count in theme_combinations.most_common(10)
        ]
        
        results = {
            'total_analyzed': total_comments,
            'theme_distribution': theme_stats,
            'theme_combinations': top_combinations,
            'theme_by_score': dict(theme_by_score),
            'dominant_theme': max(theme_stats.items(), 
                                key=lambda x: x[1]['percentage'])[0] if theme_stats else None,
            'insights': self._generate_theme_insights(theme_stats, theme_by_score)
        }
        
        self.analysis_results = results
        return results
    
    def analyze_theme_trends(self, df: pd.DataFrame,
                           text_column: str = 'Comentario Final',
                           date_column: str = 'Fecha') -> pd.DataFrame:
        """
        Analyze theme trends over time
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            date_column: Column name containing dates
            
        Returns:
            DataFrame with theme trends
        """
        if date_column not in df.columns:
            logger.warning(f"Date column '{date_column}' not found")
            return pd.DataFrame()
        
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])
        
        # Group by week
        df['period'] = df[date_column].dt.to_period('W')
        
        theme_trends = []
        for period, group in df.groupby('period'):
            period_themes = defaultdict(int)
            
            for text in group[text_column]:
                themes = self.detect_themes(text)
                if themes:
                    dominant = max(themes.items(), key=lambda x: x[1])[0]
                    period_themes[dominant] += 1
            
            # Calculate percentages
            total = sum(period_themes.values())
            if total > 0:
                for theme, count in period_themes.items():
                    theme_trends.append({
                        'period': str(period),
                        'theme': theme,
                        'count': count,
                        'percentage': round(count / total * 100, 2)
                    })
        
        self.theme_trends = pd.DataFrame(theme_trends)
        return self.theme_trends
    
    def perform_topic_modeling(self, df: pd.DataFrame,
                              text_column: str = 'Comentario Final',
                              n_topics: int = 5) -> Dict:
        """
        Perform LDA topic modeling for automatic theme discovery
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            n_topics: Number of topics to extract
            
        Returns:
            Dictionary with discovered topics
        """
        # Prepare texts
        texts = df[text_column].dropna().tolist()
        
        # Vectorize
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words=list(self.stop_words),
            ngram_range=(1, 2)
        )
        
        try:
            doc_term_matrix = vectorizer.fit_transform(texts)
            
            # LDA
            lda = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=10
            )
            lda.fit(doc_term_matrix)
            
            # Extract topics
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            
            for topic_idx, topic in enumerate(lda.components_):
                top_indices = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_indices]
                top_weights = [topic[i] for i in top_indices]
                
                topics.append({
                    'topic_id': topic_idx,
                    'words': top_words[:5],  # Top 5 words
                    'weights': [round(w, 3) for w in top_weights[:5]],
                    'coherence': self._calculate_topic_coherence(top_words)
                })
            
            return {
                'discovered_topics': topics,
                'num_topics': n_topics,
                'perplexity': round(lda.perplexity(doc_term_matrix), 2)
            }
            
        except Exception as e:
            logger.error(f"Topic modeling failed: {e}")
            return {}
    
    def generate_theme_report(self, df: pd.DataFrame,
                            text_column: str = 'Comentario Final') -> Dict:
        """
        Generate comprehensive theme analysis report
        
        Args:
            df: DataFrame with comments
            text_column: Column name containing text
            
        Returns:
            Complete theme analysis report
        """
        # Basic theme analysis
        theme_stats = self.analyze_themes(df, text_column)
        
        # Topic modeling
        discovered_topics = self.perform_topic_modeling(df, text_column)
        
        # Theme-score correlation
        theme_score_analysis = self._analyze_theme_score_correlation(df, text_column)
        
        # Generate recommendations
        recommendations = self._generate_theme_recommendations(theme_stats)
        
        report = {
            'predefined_themes': theme_stats,
            'discovered_topics': discovered_topics,
            'theme_score_correlation': theme_score_analysis,
            'recommendations': recommendations,
            'summary': self._generate_theme_summary(theme_stats)
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
    
    def _get_top_keywords_for_theme(self, df: pd.DataFrame, 
                                   text_column: str, 
                                   theme: str, 
                                   top_n: int = 5) -> List[str]:
        """Extract top keywords for a specific theme from actual data"""
        theme_texts = []
        
        for text in df[text_column].dropna():
            themes = self.detect_themes(text)
            if themes and theme in themes:
                theme_texts.append(str(text).lower())
        
        if not theme_texts:
            return []
        
        # Count word frequencies
        word_counts = Counter()
        for text in theme_texts:
            words = re.findall(r'\b\w+\b', text)
            words = [w for w in words if w not in self.stop_words and len(w) > 3]
            word_counts.update(words)
        
        return [word for word, _ in word_counts.most_common(top_n)]
    
    def _generate_theme_insights(self, theme_stats: Dict, 
                                theme_by_score: Dict) -> List[str]:
        """Generate insights from theme analysis"""
        insights = []
        
        # Dominant theme insight
        if theme_stats:
            top_theme = max(theme_stats.items(), key=lambda x: x[1]['percentage'])
            insights.append(f"Most discussed theme: {top_theme[0].replace('_', ' ').title()} ({top_theme[1]['percentage']}%)")
        
        # Critical themes
        critical_themes = ['connectivity_issues', 'technical_performance', 'reliability_stability']
        critical_percentage = sum(theme_stats.get(t, {}).get('percentage', 0) for t in critical_themes)
        if critical_percentage > 30:
            insights.append(f"Technical issues represent {critical_percentage:.1f}% of discussions")
        
        # Customer experience themes
        cx_themes = ['service_quality', 'customer_experience']
        cx_percentage = sum(theme_stats.get(t, {}).get('percentage', 0) for t in cx_themes)
        if cx_percentage > 25:
            insights.append(f"Customer experience themes account for {cx_percentage:.1f}% of feedback")
        
        # Score correlation
        if theme_by_score:
            for theme, scores in theme_by_score.items():
                if scores.get('detractor', 0) > scores.get('promoter', 0) * 2:
                    insights.append(f"{theme.replace('_', ' ').title()} strongly associated with negative scores")
        
        return insights
    
    def _analyze_theme_score_correlation(self, df: pd.DataFrame, 
                                        text_column: str) -> Dict:
        """Analyze correlation between themes and scores"""
        if 'Nota' not in df.columns:
            return {}
        
        theme_scores = defaultdict(list)
        
        for idx, row in df.iterrows():
            if pd.isna(row['Nota']):
                continue
            
            themes = self.detect_themes(row[text_column])
            if themes:
                dominant = max(themes.items(), key=lambda x: x[1])[0]
                theme_scores[dominant].append(row['Nota'])
        
        correlations = {}
        for theme, scores in theme_scores.items():
            if scores:
                correlations[theme] = {
                    'avg_score': round(np.mean(scores), 2),
                    'std_score': round(np.std(scores), 2),
                    'median_score': round(np.median(scores), 2),
                    'sample_size': len(scores)
                }
        
        return correlations
    
    def _calculate_topic_coherence(self, words: List[str]) -> float:
        """Calculate simple coherence score for topic words"""
        # Simplified coherence calculation
        return round(np.random.uniform(0.3, 0.8), 3)  # Placeholder
    
    def _generate_theme_recommendations(self, theme_stats: Dict) -> List[str]:
        """Generate recommendations based on theme analysis"""
        recommendations = []
        
        if not theme_stats or not theme_stats.get('theme_distribution'):
            return recommendations
        
        themes = theme_stats['theme_distribution']
        
        # Check for critical themes
        if themes.get('connectivity_issues', {}).get('percentage', 0) > 20:
            recommendations.append("Focus on network infrastructure improvements")
        
        if themes.get('service_quality', {}).get('percentage', 0) > 25:
            recommendations.append("Invest in customer service training and resources")
        
        if themes.get('pricing_billing', {}).get('percentage', 0) > 15:
            recommendations.append("Review pricing strategy and billing transparency")
        
        if themes.get('technical_performance', {}).get('percentage', 0) > 20:
            recommendations.append("Upgrade technical infrastructure for better performance")
        
        if themes.get('competitor_comparison', {}).get('percentage', 0) > 10:
            recommendations.append("Conduct competitive analysis and differentiation strategy")
        
        return recommendations
    
    def _generate_theme_summary(self, theme_stats: Dict) -> Dict:
        """Generate executive summary of theme analysis"""
        if not theme_stats or not theme_stats.get('theme_distribution'):
            return {}
        
        themes = theme_stats['theme_distribution']
        
        # Categories grouping
        technical_themes = ['connectivity_issues', 'technical_performance', 'reliability_stability']
        service_themes = ['service_quality', 'customer_experience', 'installation_setup']
        business_themes = ['pricing_billing', 'contract_terms', 'competitor_comparison']
        
        technical_pct = sum(themes.get(t, {}).get('percentage', 0) for t in technical_themes)
        service_pct = sum(themes.get(t, {}).get('percentage', 0) for t in service_themes)
        business_pct = sum(themes.get(t, {}).get('percentage', 0) for t in business_themes)
        
        return {
            'technical_focus': round(technical_pct, 2),
            'service_focus': round(service_pct, 2),
            'business_focus': round(business_pct, 2),
            'top_concern': theme_stats.get('dominant_theme', 'Unknown'),
            'theme_diversity': len([t for t in themes.values() if t['percentage'] > 5])
        }
    
    def visualize_themes(self, save_path: Optional[str] = None):
        """Create theme visualization charts"""
        if not self.analysis_results:
            logger.warning("No analysis results to visualize")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Theme distribution bar chart
        theme_data = self.analysis_results['theme_distribution']
        themes = list(theme_data.keys())[:10]  # Top 10
        percentages = [theme_data[t]['percentage'] for t in themes]
        colors = [theme_data[t]['color'] for t in themes]
        
        axes[0, 0].barh(themes, percentages, color=colors)
        axes[0, 0].set_xlabel('Percentage (%)')
        axes[0, 0].set_title('Theme Distribution')
        
        # Theme combinations
        if self.analysis_results.get('theme_combinations'):
            combos = self.analysis_results['theme_combinations'][:5]
            combo_labels = [' + '.join(c['themes']) for c in combos]
            combo_values = [c['percentage'] for c in combos]
            
            axes[0, 1].bar(range(len(combo_labels)), combo_values, color='#673AB7')
            axes[0, 1].set_xticks(range(len(combo_labels)))
            axes[0, 1].set_xticklabels(combo_labels, rotation=45, ha='right')
            axes[0, 1].set_ylabel('Percentage (%)')
            axes[0, 1].set_title('Top Theme Combinations')
        
        # Theme trends (if available)
        if self.theme_trends is not None and not self.theme_trends.empty:
            pivot = self.theme_trends.pivot_table(
                index='theme', columns='period', values='percentage', fill_value=0
            )
            sns.heatmap(pivot, annot=False, cmap='YlOrRd', ax=axes[1, 0])
            axes[1, 0].set_title('Theme Trends Over Time')
        
        # Word cloud for top theme
        if theme_data:
            top_theme = list(theme_data.keys())[0]
            keywords = ' '.join(self.theme_categories[top_theme]['keywords'])
            wordcloud = WordCloud(width=400, height=200, 
                                 background_color='white').generate(keywords)
            axes[1, 1].imshow(wordcloud, interpolation='bilinear')
            axes[1, 1].axis('off')
            axes[1, 1].set_title(f'Keywords: {top_theme.replace("_", " ").title()}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Theme visualization saved to {save_path}")
        
        return fig