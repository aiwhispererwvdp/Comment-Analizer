"""
Advanced Analytics Module for Personal Paraguay
Implements correlation analysis, CLV, ROI, predictive models, and more
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AdvancedAnalytics:
    def __init__(self):
        """Initialize advanced analytics with enhanced configurations"""
        
        # Enhanced CLV indicators
        self.clv_indicators = {
            'platinum': {
                'keywords': ['10 años', '15 años', '20 años', 'desde el inicio', 'primer cliente',
                            'siempre con ustedes', 'cliente fundador'],
                'value_multiplier': 5.0,
                'monthly_value': 500000  # Gs estimated
            },
            'gold': {
                'keywords': ['5 años', '7 años', 'años con ustedes', 'cliente fiel', 
                           'varios servicios', 'toda mi familia', 'recomendé muchos'],
                'value_multiplier': 3.0,
                'monthly_value': 300000
            },
            'silver': {
                'keywords': ['2 años', '3 años', 'cliente antiguo', 'siempre pago',
                           'pago puntual', 'buen cliente'],
                'value_multiplier': 2.0,
                'monthly_value': 200000
            },
            'bronze': {
                'keywords': ['nuevo cliente', 'recién contrato', 'primer mes', 
                           'acabo de contratar'],
                'value_multiplier': 1.0,
                'monthly_value': 150000
            },
            'at_risk': {
                'keywords': ['me voy', 'cancelo', 'último mes', 'no pago más',
                           'busco alternativas'],
                'value_multiplier': 0.5,
                'monthly_value': 100000
            }
        }
        
        # Correlation themes for analysis
        self.correlation_pairs = [
            ('precio', 'churn'),
            ('servicio_tecnico', 'satisfaccion'),
            ('velocidad', 'precio'),
            ('atencion_cliente', 'lealtad'),
            ('intermitencias', 'churn')
        ]
        
        # Alert thresholds
        self.alert_thresholds = {
            'sentiment_drop': {
                'threshold': -10,  # % drop
                'severity': 'critical',
                'action': 'immediate_management_review'
            },
            'churn_spike': {
                'threshold': 5,  # % increase
                'severity': 'high',
                'action': 'retention_campaign'
            },
            'competitor_mentions': {
                'threshold': 15,  # % of total
                'severity': 'medium',
                'action': 'competitive_analysis'
            },
            'p0_cases': {
                'threshold': 1,  # count
                'severity': 'critical',
                'action': 'emergency_response'
            }
        }
        
        # ROI metrics configuration
        self.roi_config = {
            'cost_per_churn': 500000,  # Gs - Cost of losing a customer
            'cost_per_complaint': 50000,  # Gs - Cost to handle complaint
            'value_per_promoter': 1000000,  # Gs - Value of a promoter (referrals)
            'improvement_cost': {
                'precio': 100000,
                'servicio_tecnico': 200000,
                'velocidad': 500000,
                'atencion_cliente': 150000
            }
        }
        
        # Entity patterns for NLP
        self.entity_patterns = {
            'person': r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Names
            'date': r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+de\s+\w+|\w+\s+pasado|hace\s+\d+\s+\w+)\b',
            'money': r'\b(\d+\.?\d*\s*(gs|guaraníes|mil|millones?))\b',
            'time': r'\b(\d+\s*(días?|semanas?|meses?|años?|horas?))\b',
            'location': r'\b(sucursal|oficina|centro|zona|barrio)\s+\w+\b',
            'product': r'\b(plan|paquete|servicio|internet|flow|router|modem)\s+\w+\b',
            'phone': r'\b(\d{4}[-\s]?\d{3,4}|\d{3}[-\s]?\d{3}[-\s]?\d{3})\b'
        }

    def calculate_enhanced_clv(self, text, sentiment, churn_risk):
        """Calculate enhanced Customer Lifetime Value indicators"""
        if pd.isna(text):
            return {
                'segment': 'unknown',
                'estimated_clv': 0,
                'risk_adjusted_clv': 0,
                'retention_priority': 'low'
            }
        
        text_lower = str(text).lower()
        
        # Determine CLV segment
        segment = 'bronze'  # default
        monthly_value = 150000
        multiplier = 1.0
        
        for seg, config in self.clv_indicators.items():
            if any(keyword in text_lower for keyword in config['keywords']):
                segment = seg
                monthly_value = config['monthly_value']
                multiplier = config['value_multiplier']
                break
        
        # Calculate base CLV (assuming 24-month average lifetime)
        base_clv = monthly_value * 24 * multiplier
        
        # Adjust for sentiment
        sentiment_adjustment = {
            'positivo': 1.2,
            'neutral': 1.0,
            'negativo': 0.7
        }.get(sentiment, 1.0)
        
        # Adjust for churn risk
        churn_adjustment = {
            'high': 0.3,
            'medium': 0.6,
            'low': 1.0
        }.get(churn_risk, 1.0)
        
        # Calculate risk-adjusted CLV
        risk_adjusted_clv = base_clv * sentiment_adjustment * churn_adjustment
        
        # Determine retention priority
        if segment in ['platinum', 'gold'] and churn_risk in ['high', 'medium']:
            retention_priority = 'critical'
        elif risk_adjusted_clv > 5000000:
            retention_priority = 'high'
        elif risk_adjusted_clv > 2000000:
            retention_priority = 'medium'
        else:
            retention_priority = 'low'
        
        return {
            'segment': segment,
            'estimated_clv': int(base_clv),
            'risk_adjusted_clv': int(risk_adjusted_clv),
            'retention_priority': retention_priority,
            'monthly_value': monthly_value
        }

    def analyze_correlations(self, data_points):
        """Analyze correlations between different metrics"""
        correlations = {}
        
        # Extract themes and sentiments from data points
        themes_sentiment = defaultdict(lambda: {'positivo': 0, 'neutral': 0, 'negativo': 0})
        themes_churn = defaultdict(lambda: {'high': 0, 'medium': 0, 'low': 0})
        
        for point in data_points:
            themes = point.get('themes', [])
            sentiment = point.get('sentiment', 'neutral')
            churn = point.get('churn_risk', 'low')
            
            for theme in themes:
                themes_sentiment[theme][sentiment] += 1
                themes_churn[theme][churn] += 1
        
        # Calculate correlations
        for theme in themes_sentiment:
            total = sum(themes_sentiment[theme].values())
            if total > 0:
                neg_ratio = themes_sentiment[theme]['negativo'] / total
                high_churn_ratio = themes_churn[theme].get('high', 0) / total
                
                # Correlation between theme negativity and churn
                correlation = min(1.0, (neg_ratio + high_churn_ratio) / 2)
                
                correlations[f'{theme}_negativity_churn'] = {
                    'value': round(correlation, 2),
                    'strength': 'strong' if correlation > 0.7 else 'moderate' if correlation > 0.4 else 'weak',
                    'insight': f"{theme} tiene {round(correlation*100)}% correlación con churn"
                }
        
        return correlations

    def calculate_roi_impact(self, analysis_results):
        """Calculate ROI and financial impact of improvements"""
        roi_analysis = {
            'current_state': {},
            'improvement_potential': {},
            'recommended_investments': []
        }
        
        # Current state costs
        total_comments = analysis_results.get('total', 1)
        negative_pct = analysis_results.get('negative_pct', 0) / 100
        churn_high = analysis_results.get('churn_analysis', {}).get('high_risk', 0)
        
        # Calculate current costs
        current_churn_cost = churn_high * self.roi_config['cost_per_churn']
        current_complaint_cost = int(total_comments * negative_pct * self.roi_config['cost_per_complaint'])
        total_current_cost = current_churn_cost + current_complaint_cost
        
        roi_analysis['current_state'] = {
            'churn_cost': current_churn_cost,
            'complaint_cost': current_complaint_cost,
            'total_cost': total_current_cost,
            'at_risk_revenue': churn_high * 150000 * 12  # Annual revenue at risk
        }
        
        # Calculate improvement potential
        # Assuming 30% reduction in negative sentiment and 50% reduction in high churn
        potential_churn_reduction = int(churn_high * 0.5)
        potential_complaint_reduction = int(total_comments * negative_pct * 0.3)
        
        potential_savings = (potential_churn_reduction * self.roi_config['cost_per_churn'] +
                           potential_complaint_reduction * self.roi_config['cost_per_complaint'])
        
        roi_analysis['improvement_potential'] = {
            'potential_churn_prevented': potential_churn_reduction,
            'potential_complaints_reduced': potential_complaint_reduction,
            'potential_savings': potential_savings,
            'roi_percentage': round((potential_savings / max(total_current_cost, 1)) * 100, 1)
        }
        
        # Recommend investments based on themes
        theme_counts = analysis_results.get('theme_counts', {})
        for theme, count in theme_counts.items():
            if count > 10:  # Significant theme
                investment_cost = self.roi_config['improvement_cost'].get(theme, 100000)
                expected_return = count * 50000  # Expected value per improvement
                roi = round((expected_return - investment_cost) / investment_cost * 100, 1)
                
                if roi > 0:
                    roi_analysis['recommended_investments'].append({
                        'area': theme,
                        'investment': investment_cost,
                        'expected_return': expected_return,
                        'roi_percentage': roi,
                        'priority': 'high' if roi > 100 else 'medium'
                    })
        
        # Sort investments by ROI
        roi_analysis['recommended_investments'].sort(key=lambda x: x['roi_percentage'], reverse=True)
        
        return roi_analysis

    def generate_alerts(self, current_results, previous_results=None):
        """Generate alerts based on threshold violations"""
        alerts = []
        
        # Check sentiment drop
        if previous_results:
            prev_negative = previous_results.get('negative_pct', 0)
            curr_negative = current_results.get('negative_pct', 0)
            sentiment_change = curr_negative - prev_negative
            
            if sentiment_change > abs(self.alert_thresholds['sentiment_drop']['threshold']):
                alerts.append({
                    'type': 'sentiment_drop',
                    'severity': 'critical',
                    'message': f'Sentimiento negativo aumentó {sentiment_change:.1f}%',
                    'action': 'Revisión inmediata de gerencia',
                    'metrics': {'previous': prev_negative, 'current': curr_negative}
                })
        
        # Check churn spike
        churn_high = current_results.get('churn_analysis', {}).get('high_risk', 0)
        total = current_results.get('total', 1)
        churn_pct = (churn_high / total * 100) if total > 0 else 0
        
        if churn_pct > self.alert_thresholds['churn_spike']['threshold']:
            alerts.append({
                'type': 'churn_spike',
                'severity': 'high',
                'message': f'{churn_high} clientes en alto riesgo de cancelación ({churn_pct:.1f}%)',
                'action': 'Activar campaña de retención inmediata',
                'metrics': {'high_risk_count': churn_high, 'percentage': churn_pct}
            })
        
        # Check competitor mentions
        comp_pct = current_results.get('competitor_analysis', {}).get('percentage', 0)
        if comp_pct > self.alert_thresholds['competitor_mentions']['threshold']:
            alerts.append({
                'type': 'competitor_threat',
                'severity': 'medium',
                'message': f'Competidores mencionados en {comp_pct:.1f}% de comentarios',
                'action': 'Análisis competitivo urgente',
                'metrics': {'percentage': comp_pct}
            })
        
        # Check P0 cases
        p0_cases = current_results.get('urgency_distribution', {}).get('P0', 0)
        if p0_cases >= self.alert_thresholds['p0_cases']['threshold']:
            alerts.append({
                'type': 'critical_issues',
                'severity': 'critical',
                'message': f'{p0_cases} casos críticos requieren atención inmediata',
                'action': 'Respuesta de emergencia requerida',
                'metrics': {'p0_count': p0_cases}
            })
        
        return alerts

    def extract_entities(self, text):
        """Extract named entities using pattern matching"""
        if pd.isna(text) or text == "":
            return {}
        
        entities = defaultdict(list)
        text_str = str(text)
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text_str, re.IGNORECASE)
            if matches:
                entities[entity_type].extend(matches)
        
        # Clean and deduplicate
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        return dict(entities)

    def predict_satisfaction_trend(self, historical_sentiments):
        """Predict future satisfaction trend based on historical data"""
        if len(historical_sentiments) < 3:
            return {
                'trend': 'insufficient_data',
                'prediction': None,
                'confidence': 0
            }
        
        # Simple moving average for trend
        positive_ratio = sum(1 for s in historical_sentiments if s == 'positivo') / len(historical_sentiments)
        negative_ratio = sum(1 for s in historical_sentiments if s == 'negativo') / len(historical_sentiments)
        
        # Determine trend
        if positive_ratio > 0.4:
            trend = 'improving'
            prediction = 'positive_outlook'
            confidence = min(95, positive_ratio * 100)
        elif negative_ratio > 0.3:
            trend = 'declining'
            prediction = 'negative_outlook'
            confidence = min(95, negative_ratio * 100)
        else:
            trend = 'stable'
            prediction = 'neutral_outlook'
            confidence = 70
        
        return {
            'trend': trend,
            'prediction': prediction,
            'confidence': round(confidence, 1),
            'positive_ratio': round(positive_ratio * 100, 1),
            'negative_ratio': round(negative_ratio * 100, 1)
        }

    def analyze_customer_cohorts(self, customer_data):
        """Analyze customer cohorts based on various attributes"""
        cohorts = {
            'new_customers': {
                'keywords': ['nuevo', 'recién', 'primer mes', 'acabo de'],
                'customers': [],
                'avg_satisfaction': 0,
                'common_issues': []
            },
            'loyal_customers': {
                'keywords': ['años', 'fiel', 'siempre', 'desde'],
                'customers': [],
                'avg_satisfaction': 0,
                'common_issues': []
            },
            'price_sensitive': {
                'keywords': ['caro', 'precio', 'costoso', 'barato'],
                'customers': [],
                'avg_satisfaction': 0,
                'common_issues': []
            },
            'tech_focused': {
                'keywords': ['velocidad', 'megas', 'router', 'técnico'],
                'customers': [],
                'avg_satisfaction': 0,
                'common_issues': []
            }
        }
        
        # Classify customers into cohorts
        for customer in customer_data:
            text = customer.get('text', '').lower()
            sentiment = customer.get('sentiment', 'neutral')
            themes = customer.get('themes', [])
            
            for cohort_name, cohort_data in cohorts.items():
                if any(keyword in text for keyword in cohort_data['keywords']):
                    cohort_data['customers'].append(customer)
                    cohort_data['common_issues'].extend(themes)
        
        # Calculate cohort metrics
        for cohort_name, cohort_data in cohorts.items():
            if cohort_data['customers']:
                # Calculate average satisfaction
                sentiments = [c.get('sentiment', 'neutral') for c in cohort_data['customers']]
                positive_pct = sum(1 for s in sentiments if s == 'positivo') / len(sentiments) * 100
                cohort_data['avg_satisfaction'] = round(positive_pct, 1)
                
                # Get most common issues
                issue_counts = Counter(cohort_data['common_issues'])
                cohort_data['common_issues'] = [issue for issue, _ in issue_counts.most_common(3)]
                
                # Add size
                cohort_data['size'] = len(cohort_data['customers'])
                
                # Remove actual customer data to save memory
                del cohort_data['customers']
        
        return cohorts

    def calculate_revenue_at_risk(self, analysis_results):
        """Calculate total revenue at risk from dissatisfied customers"""
        
        # Base monthly revenue per customer (average)
        avg_monthly_revenue = 150000  # Gs
        
        # Get risk metrics
        total = analysis_results.get('total', 0)
        high_churn = analysis_results.get('churn_analysis', {}).get('high_risk', 0)
        medium_churn = analysis_results.get('churn_analysis', {}).get('medium_risk', 0)
        negative_pct = analysis_results.get('negative_pct', 0) / 100
        
        # Calculate revenue at risk
        immediate_risk = high_churn * avg_monthly_revenue * 12  # Annual revenue
        medium_term_risk = medium_churn * avg_monthly_revenue * 6  # 6 months
        potential_risk = int(total * negative_pct * avg_monthly_revenue * 3)  # 3 months
        
        total_at_risk = immediate_risk + medium_term_risk + potential_risk
        
        return {
            'immediate_risk': immediate_risk,
            'medium_term_risk': medium_term_risk,
            'potential_risk': potential_risk,
            'total_at_risk': total_at_risk,
            'percentage_of_base': round((total_at_risk / (total * avg_monthly_revenue * 12) * 100), 1) if total > 0 else 0,
            'recommendations': self._generate_revenue_recommendations(total_at_risk)
        }
    
    def _generate_revenue_recommendations(self, total_at_risk):
        """Generate recommendations based on revenue at risk"""
        recommendations = []
        
        if total_at_risk > 100000000:  # > 100M Gs
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Reunión ejecutiva de emergencia',
                'timeline': 'Inmediato'
            })
        
        if total_at_risk > 50000000:  # > 50M Gs
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Activar programa de retención VIP',
                'timeline': '24 horas'
            })
        
        if total_at_risk > 10000000:  # > 10M Gs
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Campaña de satisfacción dirigida',
                'timeline': '1 semana'
            })
        
        return recommendations

    def generate_executive_summary(self, full_analysis):
        """Generate executive summary with key insights and recommendations"""
        
        summary = {
            'key_metrics': {},
            'critical_insights': [],
            'top_actions': [],
            'expected_outcomes': {}
        }
        
        # Extract key metrics
        summary['key_metrics'] = {
            'total_analyzed': full_analysis.get('total', 0),
            'satisfaction_score': 100 - full_analysis.get('negative_pct', 0),
            'nps': full_analysis.get('nps', {}).get('score', 0),
            'churn_risk': full_analysis.get('churn_analysis', {}).get('high_risk', 0),
            'revenue_at_risk': 0  # Will be calculated
        }
        
        # Generate critical insights
        if full_analysis.get('negative_pct', 0) > 30:
            summary['critical_insights'].append({
                'type': 'satisfaction',
                'message': 'Satisfacción crítica: >30% comentarios negativos',
                'impact': 'high'
            })
        
        if full_analysis.get('churn_analysis', {}).get('high_risk', 0) > 10:
            summary['critical_insights'].append({
                'type': 'churn',
                'message': f"{full_analysis.get('churn_analysis', {}).get('high_risk', 0)} clientes en riesgo inmediato de cancelación",
                'impact': 'critical'
            })
        
        if full_analysis.get('competitor_analysis', {}).get('percentage', 0) > 15:
            summary['critical_insights'].append({
                'type': 'competition',
                'message': 'Alta mención de competidores indica vulnerabilidad',
                'impact': 'high'
            })
        
        # Generate top actions
        if full_analysis.get('urgency_distribution', {}).get('P0', 0) > 0:
            summary['top_actions'].append({
                'priority': 1,
                'action': 'Resolver casos críticos P0 inmediatamente',
                'owner': 'Soporte Técnico',
                'timeline': 'Hoy'
            })
        
        if full_analysis.get('churn_analysis', {}).get('high_risk', 0) > 5:
            summary['top_actions'].append({
                'priority': 2,
                'action': 'Contactar clientes en alto riesgo de churn',
                'owner': 'Customer Success',
                'timeline': '24 horas'
            })
        
        # Expected outcomes
        summary['expected_outcomes'] = {
            'if_no_action': {
                'churn_expected': full_analysis.get('churn_analysis', {}).get('high_risk', 0),
                'revenue_loss': 'Calculando...',
                'nps_decline': -5
            },
            'with_recommended_actions': {
                'churn_prevented': int(full_analysis.get('churn_analysis', {}).get('high_risk', 0) * 0.6),
                'revenue_saved': 'Calculando...',
                'nps_improvement': 10
            }
        }
        
        return summary