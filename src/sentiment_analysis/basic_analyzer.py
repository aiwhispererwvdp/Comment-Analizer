"""
Basic Analyzer Module
Provides a simple rule-based analysis method as an example of extending the system
"""

from typing import List, Dict, Any
import re
from interfaces.analysis import AnalysisMethod
from data_processing.language_detector import LanguageDetector
from collections import Counter

class BasicAnalysisMethod(AnalysisMethod):
    """
    Simple rule-based implementation of analysis method
    This is primarily an example of how to add new analysis methods
    """
    
    @property
    def name(self) -> str:
        return "basic"
    
    @property
    def description(self) -> str:
        return "Simple rule-based analysis for quick sentiment detection (example method)"
    
    def __init__(self):
        """Initialize the basic analyzer"""
        self.language_detector = LanguageDetector()
        
        # Simple sentiment dictionaries
        self.positive_words = {
            'es': ['bueno', 'excelente', 'genial', 'increíble', 'perfecto', 'mejor', 'rápido', 'feliz', 'satisfecho', 'recomiendo'],
            'gn': ['porã', 'iporã', 'mba\'ete', 'vy\'a', 'avy\'a']
        }
        
        self.negative_words = {
            'es': ['malo', 'pésimo', 'terrible', 'horrible', 'lento', 'problema', 'error', 'falla', 'desconexión', 'caro'],
            'gn': ['vai', 'ivai', 'mba\'evai', 'ndavy\'ai']
        }
    
    def analyze_batch(self, comments: List[str], **kwargs) -> List[Dict]:
        """
        Analyze a batch of comments using simple rule-based approach
        
        Args:
            comments: List of text comments to analyze
            **kwargs: Additional parameters (unused in this method)
            
        Returns:
            List of dictionaries containing analysis results
        """
        results = []
        
        for i, comment in enumerate(comments, 1):
            # Get language
            lang_result = self.language_detector.detect_language(comment)
            language = lang_result['language']
            
            # Detect sentiment
            sentiment_result = self._detect_sentiment(comment, language)
            
            # Find themes and pain points using simple keyword matching
            themes = self._extract_themes(comment, language)
            pain_points = self._extract_pain_points(comment, language)
            
            # Create result object
            results.append({
                "comment_number": i,
                "sentiment": sentiment_result["sentiment"],
                "confidence": sentiment_result["confidence"],
                "language": language,
                "translation": comment,  # Basic analyzer doesn't translate
                "themes": themes[:3],    # Limit to 3 themes
                "pain_points": pain_points,
                "emotions": [sentiment_result["sentiment"]]  # Simple mapping
            })
        
        return results
    
    def _detect_sentiment(self, text: str, language: str) -> Dict:
        """Simple rule-based sentiment detection"""
        text = text.lower()
        
        positive_count = 0
        for lang, words in self.positive_words.items():
            for word in words:
                positive_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
        
        negative_count = 0
        for lang, words in self.negative_words.items():
            for word in words:
                negative_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
        
        # Simple scoring
        sentiment_score = positive_count - negative_count
        
        if sentiment_score > 0:
            sentiment = "positive"
            confidence = min(0.7, 0.5 + (0.05 * sentiment_score))
        elif sentiment_score < 0:
            sentiment = "negative"
            confidence = min(0.7, 0.5 + (0.05 * abs(sentiment_score)))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence
        }
    
    def _extract_themes(self, text: str, language: str) -> List[str]:
        """Extract themes based on keyword matching"""
        text = text.lower()
        
        # Common telecom themes
        telecom_themes = [
            'internet', 'conexión', 'wifi', 'fibra', 'velocidad', 'señal', 
            'instalación', 'técnico', 'router', 'precio', 'factura', 'servicio',
            'cliente', 'atención'
        ]
        
        found_themes = []
        for theme in telecom_themes:
            if theme in text:
                found_themes.append(theme)
        
        return found_themes if found_themes else ["sin_clasificar"]
    
    def _extract_pain_points(self, text: str, language: str) -> List[str]:
        """Extract pain points based on negative contexts"""
        text = text.lower()
        
        pain_patterns = [
            (r'lent[oa]', 'velocidad_lenta'),
            (r'ca[ií]da', 'caída_conexión'),
            (r'desconect', 'desconexión'),
            (r'car[oa]', 'precio_alto'),
            (r'demor[aa]', 'demora'),
            (r'problem[aa]', 'problema_técnico'),
            (r'error', 'error'),
            (r'factur[aa]', 'problema_facturación')
        ]
        
        pain_points = []
        for pattern, pain_point in pain_patterns:
            if re.search(pattern, text):
                pain_points.append(pain_point)
        
        return pain_points
    
    def get_insights(self, results: List[Dict]) -> Dict:
        """Generate insights from analysis results"""
        if not results:
            return {
                "total_comments": 0,
                "sentiment_distribution": {},
                "sentiment_percentages": {},
                "top_themes": {},
                "top_pain_points": {},
                "language_distribution": {},
                "avg_confidence": 0,
                "guarani_percentage": 0
            }
        
        # Count sentiments
        sentiments = [r['sentiment'] for r in results]
        sentiment_counts = Counter(sentiments)
        total = len(results)
        
        # Calculate percentages
        sentiment_percentages = {k: round((v/total)*100, 1) for k, v in sentiment_counts.items()}
        
        # Gather themes and pain points
        themes = []
        pain_points = []
        languages = []
        confidences = []
        
        for result in results:
            themes.extend(result.get('themes', []))
            pain_points.extend(result.get('pain_points', []))
            languages.append(result.get('language', 'es'))
            confidences.append(result.get('confidence', 0.5))
        
        # Calculate frequencies
        theme_counts = Counter(themes).most_common(10)
        pain_point_counts = Counter(pain_points).most_common(10)
        language_counts = Counter(languages)
        
        # Calculate averages
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate Guarani percentage
        guarani_count = language_counts.get('gn', 0) + language_counts.get('mixed', 0)
        guarani_percentage = (guarani_count / total) * 100 if total > 0 else 0
        
        return {
            "total_comments": total,
            "sentiment_distribution": dict(sentiment_counts),
            "sentiment_percentages": sentiment_percentages,
            "top_themes": dict(theme_counts),
            "top_pain_points": dict(pain_point_counts),
            "language_distribution": dict(language_counts),
            "avg_confidence": round(avg_confidence, 2),
            "guarani_percentage": round(guarani_percentage, 1)
        }
    
    def get_recommendations(self, insights: Dict) -> List[str]:
        """Generate recommendations based on insights"""
        recommendations = []
        
        # Add sentiment-based recommendations
        negative_pct = insights.get('sentiment_percentages', {}).get('negative', 0)
        if negative_pct > 30:
            recommendations.append(f"Atención: {negative_pct}% comentarios negativos - requiere revisión")
        elif negative_pct > 15:
            recommendations.append(f"Monitorear: {negative_pct}% comentarios negativos")
            
        # Add pain point recommendations
        pain_points = insights.get('top_pain_points', {})
        if pain_points:
            top_issues = list(pain_points.keys())[:3]
            if top_issues:
                recommendations.append(f"Enfocarse en resolver: {', '.join(top_issues)}")
        
        return recommendations or ["No hay recomendaciones específicas basadas en el análisis básico"] 