"""
Improved Analysis Module based on actual Personal Paraguay dataset insights
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re

class ImprovedAnalysis:
    def __init__(self):
        """Initialize with insights from actual data analysis"""
        
        # Based on actual data: NPS perfectly maps to Nota
        self.nps_mapping = {
            'detractor': range(0, 7),   # 0-6
            'pasivo': range(7, 9),      # 7-8
            'promotor': range(9, 11)    # 9-10
        }
        
        # Top themes from actual data (with occurrence rates)
        self.key_themes = {
            'servicio': {
                'keywords': ['servicio', 'servicios', 'serv'],
                'occurrence_rate': 0.176,
                'typical_sentiment': 'mixed'
            },
            'mejora_necesaria': {
                'keywords': ['mejorar', 'mejore', 'mejora', 'mejoren', 'mejoría'],
                'occurrence_rate': 0.141,
                'typical_sentiment': 'negative'
            },
            'calidad_positiva': {
                'keywords': ['bueno', 'buena', 'excelente', 'bien', 'mejor', 'perfecto'],
                'occurrence_rate': 0.098,
                'typical_sentiment': 'positive'
            },
            'precio': {
                'keywords': ['precio', 'caro', 'costoso', 'barato', 'pago', 'cobra', 'costo'],
                'occurrence_rate': 0.081,
                'typical_sentiment': 'negative'
            },
            'internet': {
                'keywords': ['internet', 'conexion', 'conexión', 'conecta', 'conectar'],
                'occurrence_rate': 0.071,
                'typical_sentiment': 'mixed'
            },
            'atencion_cliente': {
                'keywords': ['atencion', 'atención', 'atiende', 'cliente', 'servicio al cliente'],
                'occurrence_rate': 0.066,
                'typical_sentiment': 'mixed'
            },
            'velocidad': {
                'keywords': ['velocidad', 'lento', 'lenta', 'rapido', 'rápido', 'lentitud'],
                'occurrence_rate': 0.059,
                'typical_sentiment': 'negative'
            },
            'señal_conexion': {
                'keywords': ['señal', 'senal', 'conexion', 'conexión', 'conecta', 'desconecta'],
                'occurrence_rate': 0.051,
                'typical_sentiment': 'negative'
            },
            'problemas': {
                'keywords': ['malo', 'mala', 'problema', 'falla', 'error', 'mal'],
                'occurrence_rate': 0.026,
                'typical_sentiment': 'negative'
            }
        }
        
        # Common meaningless responses (to filter or flag)
        self.non_informative_responses = [
            'no', 'No', 'NO', '.', 'ninguna', 'Ninguna', 'nada', 'Nada', 
            'ninguno', 'Ninguno', 'ok', 'Ok', 'OK', 'si', 'Si', 'SI'
        ]
        
        # Competitor mentions (actual data shows Tigo at 1.3%)
        self.competitors = {
            'tigo': ['tigo', 'TIGO'],
            'copaco': ['copaco', 'COPACO'],
            'claro': ['claro', 'CLARO'],
            'vox': ['vox', 'VOX']
        }
        
        # Service quality indicators
        self.quality_indicators = {
            'intermittent': ['corte', 'cortes', 'cae', 'caida', 'caídas', 'intermitente', 'intermitencia'],
            'slow': ['lento', 'lenta', 'lentitud', 'demora', 'tarda'],
            'no_service': ['no funciona', 'sin internet', 'sin servicio', 'no hay', 'no anda'],
            'limited': ['limitada', 'limitado', 'límite', 'restricción']
        }
        
        # Actual NPS distribution from data
        self.nps_distribution = {
            'detractor': 0.44,  # 44%
            'pasivo': 0.236,    # 23.6%
            'promotor': 0.324   # 32.4%
        }

    def calculate_real_nps(self, df):
        """Calculate NPS from actual data"""
        if 'NPS' in df.columns:
            total = len(df)
            promoters = len(df[df['NPS'] == 'Promotor'])
            detractors = len(df[df['NPS'] == 'Detractor'])
            nps = ((promoters - detractors) / total * 100) if total > 0 else 0
            
            return {
                'nps_score': round(nps, 1),
                'promoters': promoters,
                'passives': len(df[df['NPS'] == 'Pasivo']),
                'detractors': detractors,
                'distribution': {
                    'promoter_pct': round(promoters/total*100, 1),
                    'passive_pct': round(len(df[df['NPS'] == 'Pasivo'])/total*100, 1),
                    'detractor_pct': round(detractors/total*100, 1)
                }
            }
        return None

    def analyze_comment_quality(self, comment):
        """Assess the quality and informativeness of a comment"""
        if pd.isna(comment) or comment == "":
            return {'quality': 'empty', 'informative': False, 'length': 0}
        
        comment_str = str(comment).strip()
        length = len(comment_str)
        
        # Check if it's a non-informative response
        if comment_str in self.non_informative_responses:
            return {
                'quality': 'non_informative',
                'informative': False,
                'length': length,
                'type': 'single_word'
            }
        
        # Check length-based quality
        if length < 3:
            quality = 'too_short'
            informative = False
        elif length < 10:
            quality = 'short'
            informative = False
        elif length < 20:
            quality = 'brief'
            informative = True
        elif length < 50:
            quality = 'moderate'
            informative = True
        else:
            quality = 'detailed'
            informative = True
        
        # Count words
        word_count = len(comment_str.split())
        
        return {
            'quality': quality,
            'informative': informative,
            'length': length,
            'word_count': word_count,
            'type': 'single_word' if word_count == 1 else 'multi_word'
        }

    def detect_themes_improved(self, comment):
        """Improved theme detection based on actual data patterns"""
        if pd.isna(comment) or comment == "":
            return {'themes': [], 'theme_scores': {}}
        
        comment_lower = str(comment).lower()
        detected_themes = []
        theme_scores = {}
        
        for theme_name, theme_data in self.key_themes.items():
            score = 0
            for keyword in theme_data['keywords']:
                if keyword in comment_lower:
                    score += 1
                    
            if score > 0:
                detected_themes.append(theme_name)
                theme_scores[theme_name] = score
                
        return {
            'themes': detected_themes,
            'theme_scores': theme_scores,
            'primary_theme': max(theme_scores, key=theme_scores.get) if theme_scores else None
        }

    def analyze_service_issues(self, comment):
        """Detect specific service quality issues"""
        if pd.isna(comment) or comment == "":
            return {'issues': [], 'severity': 'none'}
        
        comment_lower = str(comment).lower()
        issues = []
        
        for issue_type, keywords in self.quality_indicators.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    issues.append(issue_type)
                    break
        
        # Determine severity
        if 'no_service' in issues:
            severity = 'critical'
        elif 'intermittent' in issues:
            severity = 'high'
        elif 'slow' in issues or 'limited' in issues:
            severity = 'medium'
        elif issues:
            severity = 'low'
        else:
            severity = 'none'
        
        return {
            'issues': list(set(issues)),
            'severity': severity,
            'issue_count': len(set(issues))
        }

    def enhanced_sentiment_analysis(self, comment, nota=None):
        """Enhanced sentiment using both text and rating"""
        # First, check if we have a rating (Nota)
        if nota is not None:
            if nota <= 4:
                base_sentiment = 'negativo'
                confidence = 0.9
            elif nota <= 6:
                base_sentiment = 'negativo'
                confidence = 0.7
            elif nota <= 8:
                base_sentiment = 'neutral'
                confidence = 0.8
            else:
                base_sentiment = 'positivo'
                confidence = 0.9
        else:
            base_sentiment = 'neutral'
            confidence = 0.5
        
        # Analyze comment if informative
        quality = self.analyze_comment_quality(comment)
        if quality['informative']:
            comment_lower = str(comment).lower()
            
            # Positive indicators
            positive_words = ['excelente', 'bueno', 'buena', 'bien', 'mejor', 'perfecto', 
                            'satisfecho', 'conforme', 'feliz', 'contento']
            # Negative indicators  
            negative_words = ['malo', 'mala', 'mal', 'pésimo', 'terrible', 'horrible',
                            'problema', 'falla', 'lento', 'caro', 'mejorar', 'corte']
            
            pos_count = sum(1 for word in positive_words if word in comment_lower)
            neg_count = sum(1 for word in negative_words if word in comment_lower)
            
            # Adjust sentiment based on text
            if neg_count > pos_count:
                text_sentiment = 'negativo'
            elif pos_count > neg_count:
                text_sentiment = 'positivo'
            else:
                text_sentiment = 'neutral'
            
            # Combine rating and text sentiment
            if nota is not None:
                # If both agree, increase confidence
                if base_sentiment == text_sentiment:
                    confidence = min(1.0, confidence + 0.1)
                # If they disagree strongly, use rating but lower confidence
                elif (base_sentiment == 'positivo' and text_sentiment == 'negativo') or \
                     (base_sentiment == 'negativo' and text_sentiment == 'positivo'):
                    confidence = max(0.5, confidence - 0.2)
            else:
                # No rating, use text sentiment
                base_sentiment = text_sentiment
                confidence = 0.7 if (pos_count + neg_count) > 0 else 0.5
        
        return {
            'sentiment': base_sentiment,
            'confidence': round(confidence, 2),
            'based_on': 'rating_and_text' if nota is not None and quality['informative'] else 
                       'rating_only' if nota is not None else 'text_only'
        }

    def calculate_customer_satisfaction_index(self, df):
        """Calculate a comprehensive satisfaction index"""
        if 'Nota' not in df.columns:
            return None
        
        # Basic metrics
        avg_rating = df['Nota'].mean()
        
        # Rating distribution
        high_ratings = len(df[df['Nota'] >= 9]) / len(df) * 100
        low_ratings = len(df[df['Nota'] <= 4]) / len(df) * 100
        
        # Calculate CSI (Customer Satisfaction Index)
        # Weighted formula: 40% avg rating, 30% high ratings, 30% inverse of low ratings
        csi = (avg_rating/10 * 40) + (high_ratings/100 * 30) + ((100-low_ratings)/100 * 30)
        
        # Determine satisfaction level
        if csi >= 80:
            level = 'Excelente'
        elif csi >= 70:
            level = 'Bueno'
        elif csi >= 60:
            level = 'Regular'
        elif csi >= 50:
            level = 'Bajo'
        else:
            level = 'Crítico'
        
        return {
            'csi_score': round(csi, 1),
            'level': level,
            'avg_rating': round(avg_rating, 2),
            'high_ratings_pct': round(high_ratings, 1),
            'low_ratings_pct': round(low_ratings, 1),
            'interpretation': self._interpret_csi(csi)
        }
    
    def _interpret_csi(self, csi):
        """Provide interpretation of CSI score"""
        if csi >= 80:
            return "Los clientes están muy satisfechos. Mantener el nivel de servicio."
        elif csi >= 70:
            return "Satisfacción buena pero con espacio para mejoras."
        elif csi >= 60:
            return "Satisfacción regular. Se requieren mejoras significativas."
        elif csi >= 50:
            return "Baja satisfacción. Acciones urgentes necesarias."
        else:
            return "Satisfacción crítica. Requiere intervención inmediata de gerencia."

    def generate_insights(self, analysis_results):
        """Generate actionable insights from analysis"""
        insights = []
        
        # NPS insight
        if 'nps' in analysis_results and analysis_results['nps']:
            nps_score = analysis_results['nps']['nps_score']
            if nps_score < -20:
                insights.append({
                    'type': 'critical',
                    'area': 'NPS',
                    'insight': f'NPS crítico ({nps_score}). Más detractores que promotores.',
                    'action': 'Implementar programa urgente de mejora de satisfacción'
                })
            elif nps_score < 0:
                insights.append({
                    'type': 'warning',
                    'area': 'NPS',
                    'insight': f'NPS negativo ({nps_score}). Balance desfavorable.',
                    'action': 'Identificar principales causas de insatisfacción'
                })
        
        # Theme insights
        if 'theme_summary' in analysis_results:
            top_themes = analysis_results['theme_summary'][:3]
            for theme in top_themes:
                if theme['name'] == 'mejora_necesaria' and theme['percentage'] > 10:
                    insights.append({
                        'type': 'warning',
                        'area': 'Mejoras',
                        'insight': f'{theme["percentage"]:.1f}% piden mejoras',
                        'action': 'Priorizar áreas de mejora mencionadas'
                    })
                elif theme['name'] == 'precio' and theme['percentage'] > 5:
                    insights.append({
                        'type': 'warning',
                        'area': 'Precio',
                        'insight': f'{theme["percentage"]:.1f}% mencionan precio',
                        'action': 'Revisar estrategia de pricing'
                    })
        
        # Service issues insight
        if 'service_issues' in analysis_results:
            critical_issues = sum(1 for issue in analysis_results['service_issues'] 
                                if issue['severity'] == 'critical')
            if critical_issues > 10:
                insights.append({
                    'type': 'critical',
                    'area': 'Servicio',
                    'insight': f'{critical_issues} casos críticos sin servicio',
                    'action': 'Respuesta técnica inmediata requerida'
                })
        
        return insights