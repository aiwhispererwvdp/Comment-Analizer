"""
Enhanced Analysis Module for Personal Paraguay
Includes advanced sentiment analysis, emotion detection, churn prediction, and more
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from datetime import datetime

class EnhancedAnalysis:
    def __init__(self):
        """Initialize enhanced analysis with all categorizations"""
        
        # Emotion categories in Spanish
        self.emotion_categories = {
            'frustracion': ['frustrado', 'harto', 'cansado', 'irritado', 'molesto', 'fastidiado', 'agotado'],
            'satisfaccion': ['satisfecho', 'contento', 'feliz', 'conforme', 'alegre', 'complacido', 'encantado'],
            'preocupacion': ['preocupado', 'inquieto', 'nervioso', 'dudoso', 'ansioso', 'intranquilo'],
            'enojo': ['enojado', 'furioso', 'indignado', 'rabioso', 'enfadado', 'iracundo'],
            'esperanza': ['espero', 'confío', 'ojalá', 'desearía', 'anhelo', 'aspiro', 'quisiera'],
            'decepcion': ['decepcionado', 'desilusionado', 'esperaba más', 'frustrado', 'desencantado']
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'muy': 1.5,
            'super': 2.0,
            'súper': 2.0,
            'extremadamente': 2.5,
            'totalmente': 2.0,
            'completamente': 2.0,
            'bastante': 1.3,
            'demasiado': 2.0,
            'increíblemente': 2.5,
            'absolutamente': 2.5,
            'un poco': 0.7,
            'algo': 0.8,
            'ligeramente': 0.6
        }
        
        # Extended themes with sub-themes
        self.extended_themes = {
            'precio': {
                'aumento_sin_aviso': ['sube sin avisar', 'aumenta sin consultar', 'alzaron sin decir', 
                                      'subió sin avisar', 'aumentó de repente', 'cambió el precio'],
                'precio_alto': ['caro', 'costoso', 'elevado', 'no puedo pagar', 'muy caro', 
                               'demasiado caro', 'carísimo', 'impagable'],
                'comparacion_competencia': ['tigo más barato', 'copaco mejor precio', 'claro cobra menos',
                                           'en tigo pago menos', 'competencia más barata'],
                'fidelidad_descuento': ['descuento por antigüedad', 'promoción cliente fiel', 
                                       'beneficio por años', 'premio fidelidad', 'cliente antiguo']
            },
            'servicio_tecnico': {
                'tiempo_respuesta': ['demora', 'tarda', 'no vienen', 'esperé semanas', 'nunca llegaron',
                                    'días esperando', 'sin respuesta', 'no responden'],
                'calidad_tecnico': ['técnico malo', 'no sabe', 'incompetente', 'no resuelve',
                                   'mal técnico', 'servicio técnico malo', 'no solucionó'],
                'disponibilidad': ['no hay servicio técnico', 'fin de semana', 'feriados',
                                  'horario limitado', 'no atienden', 'cerrado'],
                'solucion_efectiva': ['no resuelve', 'vuelve el problema', 'parche', 'temporal',
                                     'no funciona la solución', 'mismo problema', 'sigue fallando']
            },
            'calidad_conexion': {
                'velocidad_real': ['no llega', 'menos de lo contratado', 'prueba velocidad',
                                  'velocidad menor', 'no es lo prometido', 'engaño velocidad'],
                'estabilidad': ['se corta', 'intermitente', 'microcortes', 'inestable',
                               'se cae', 'cortes constantes', 'no es estable'],
                'horarios_pico': ['noche lento', 'fin de semana', 'horas pico', 'tarde lento',
                                 'mañana no funciona', 'horario saturado'],
                'clima_afecta': ['lluvia', 'viento', 'tormenta', 'mal tiempo',
                                'cuando llueve', 'clima afecta', 'temporal']
            }
        }
        
        # Churn indicators
        self.churn_indicators = {
            'high_risk': {
                'phrases': ['voy a cambiar', 'busco otro proveedor', 'me voy a tigo',
                           'doy de baja', 'cancelo el servicio', 'último mes',
                           'me cambio', 'termino contrato', 'no renuevo'],
                'score': 9
            },
            'medium_risk': {
                'phrases': ['evaluando opciones', 'viendo alternativas', 'comparando precios',
                           'no estoy satisfecho', 'pensando cambiar', 'considerando',
                           'analizando', 'no me convence', 'dudando'],
                'score': 6
            },
            'low_risk': {
                'phrases': ['mejorar o me voy', 'última oportunidad', 'si no mejora',
                           'espero mejoren', 'den solución', 'necesito que mejore'],
                'score': 3
            }
        }
        
        # Competitor mentions
        self.competitors = {
            'tigo': ['tigo', 'tigo mejor', 'tigo más barato', 'vuelvo a tigo', 'con tigo'],
            'copaco': ['copaco', 'copaco mejor', 'copaco más barato'],
            'claro': ['claro', 'claro tiene', 'claro ofrece', 'claro mejor'],
            'vox': ['vox', 'vox internet', 'vox fibra']
        }
        
        # Urgency levels
        self.urgency_levels = {
            'P0_critico': ['sin servicio', 'no funciona', 'no hay internet', 'completamente caído',
                          'urgente', 'emergencia', 'sin conexión', 'totalmente muerto'],
            'P1_urgente': ['muy lento', 'casi no funciona', 'problemas graves', 'afecta trabajo',
                          'no puedo trabajar', 'pérdidas', 'crítico', 'inaceptable'],
            'P2_importante': ['lento', 'a veces falla', 'intermitente', 'molesto',
                            'problemas', 'inconveniente', 'debería mejorar'],
            'P3_deseable': ['podría mejorar', 'sería bueno', 'sugerencia', 'me gustaría',
                          'recomiendo', 'opinión', 'idea']
        }

    def analyze_emotions(self, text):
        """Analyze granular emotions in text"""
        if pd.isna(text) or text == "":
            return {'dominant_emotion': 'neutral', 'all_emotions': {}, 'intensity': 0}
        
        text_lower = str(text).lower()
        emotion_scores = {}
        
        # Check for each emotion category
        for emotion, keywords in self.emotion_categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        else:
            dominant_emotion = 'neutral'
        
        # Calculate intensity
        intensity = self.calculate_intensity(text_lower)
        
        return {
            'dominant_emotion': dominant_emotion,
            'all_emotions': emotion_scores,
            'intensity': intensity
        }

    def calculate_intensity(self, text):
        """Calculate emotional intensity on scale 1-10"""
        base_intensity = 5
        
        # Check for intensity modifiers
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text:
                base_intensity = min(10, base_intensity * multiplier)
        
        # Check for exclamation marks (increase intensity)
        exclamation_count = text.count('!')
        base_intensity = min(10, base_intensity + exclamation_count * 0.5)
        
        # Check for caps (increase intensity)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:  # More than 30% caps
            base_intensity = min(10, base_intensity * 1.3)
        
        # Check for repeated characters (increase intensity)
        if re.search(r'(.)\1{2,}', text):  # Characters repeated 3+ times
            base_intensity = min(10, base_intensity * 1.2)
        
        return round(base_intensity, 1)

    def analyze_extended_themes(self, text):
        """Analyze text for extended themes and sub-themes"""
        if pd.isna(text) or text == "":
            return {}
        
        text_lower = str(text).lower()
        detected_themes = {}
        
        for main_theme, sub_themes in self.extended_themes.items():
            theme_data = {}
            for sub_theme, keywords in sub_themes.items():
                if any(keyword in text_lower for keyword in keywords):
                    theme_data[sub_theme] = True
            
            if theme_data:
                detected_themes[main_theme] = theme_data
        
        return detected_themes

    def predict_churn_risk(self, text):
        """Predict customer churn risk based on text"""
        if pd.isna(text) or text == "":
            return {'risk_level': 'low', 'score': 0, 'indicators': []}
        
        text_lower = str(text).lower()
        max_score = 0
        risk_level = 'low'
        found_indicators = []
        
        # Check each risk level
        for level, data in self.churn_indicators.items():
            for phrase in data['phrases']:
                if phrase in text_lower:
                    found_indicators.append(phrase)
                    if data['score'] > max_score:
                        max_score = data['score']
                        risk_level = level.replace('_risk', '')
        
        return {
            'risk_level': risk_level,
            'score': max_score,
            'indicators': found_indicators,
            'probability': min(100, max_score * 11.1)  # Convert to percentage
        }

    def analyze_competitors(self, text):
        """Analyze competitor mentions in text"""
        if pd.isna(text) or text == "":
            return {'mentioned': [], 'context': {}}
        
        text_lower = str(text).lower()
        mentioned_competitors = []
        context = {}
        
        for competitor, keywords in self.competitors.items():
            for keyword in keywords:
                if keyword in text_lower:
                    mentioned_competitors.append(competitor)
                    
                    # Extract context around competitor mention
                    # Find sentence containing the keyword
                    sentences = text_lower.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            context[competitor] = sentence.strip()
                            break
                    break
        
        return {
            'mentioned': list(set(mentioned_competitors)),
            'context': context
        }

    def determine_urgency(self, text):
        """Determine urgency level of the comment"""
        if pd.isna(text) or text == "":
            return 'P3'
        
        text_lower = str(text).lower()
        
        # Check from most urgent to least urgent
        for urgency_level, keywords in self.urgency_levels.items():
            if any(keyword in text_lower for keyword in keywords):
                return urgency_level.split('_')[0]  # Return P0, P1, P2, or P3
        
        return 'P3'  # Default to lowest urgency

    def calculate_nps_from_sentiment(self, sentiment, intensity=5):
        """Calculate NPS score based on sentiment and intensity"""
        if sentiment == 'positivo':
            # Promoter: 9-10
            return min(10, 8 + (intensity / 5))
        elif sentiment == 'negativo':
            # Detractor: 0-6
            return max(0, 7 - (intensity / 2))
        else:
            # Passive: 7-8
            return 7.5

    def analyze_sentiment_by_theme(self, comments_with_themes):
        """Analyze sentiment distribution for each theme"""
        theme_sentiments = defaultdict(lambda: {'positivo': 0, 'neutral': 0, 'negativo': 0})
        
        for comment_data in comments_with_themes:
            text = comment_data.get('text', '')
            sentiment = comment_data.get('sentiment', 'neutral')
            themes = comment_data.get('themes', {})
            
            for theme in themes:
                theme_sentiments[theme][sentiment] += 1
        
        # Calculate percentages
        result = {}
        for theme, sentiments in theme_sentiments.items():
            total = sum(sentiments.values())
            if total > 0:
                result[theme] = {
                    'positivo': round(sentiments['positivo'] / total * 100, 1),
                    'neutral': round(sentiments['neutral'] / total * 100, 1),
                    'negativo': round(sentiments['negativo'] / total * 100, 1),
                    'total_mentions': total
                }
        
        return result

    def generate_action_plan(self, analysis_results):
        """Generate action plan based on analysis results"""
        actions = []
        
        # Check churn risk - handle both dict and list formats
        churn_data = analysis_results.get('churn_analysis', {})
        if isinstance(churn_data, dict):
            # Handle dict format with high_risk key
            high_churn_count = churn_data.get('high_risk', 0)
            # Check if details is a list
            details = churn_data.get('details', [])
            if details and isinstance(details, list):
                # Recount from details if available
                high_churn_count = sum(1 for r in details 
                                     if isinstance(r, dict) and r.get('risk_level') == 'high')
        else:
            # Handle list format
            high_churn_count = sum(1 for r in churn_data 
                                  if isinstance(r, dict) and r.get('risk_level') == 'high')
        
        if high_churn_count > 5:
            actions.append({
                'priority': 'P0',
                'action': 'Campaña de retención urgente',
                'department': 'Customer Success',
                'timeline': '24 horas',
                'affected_customers': high_churn_count
            })
        
        # Check urgency levels - handle dict format
        urgency_data = analysis_results.get('urgency_distribution', {})
        if isinstance(urgency_data, dict):
            p0_count = urgency_data.get('P0', 0)
        else:
            p0_count = sum(1 for r in analysis_results.get('urgency_analysis', [])
                          if r == 'P0')
        
        if p0_count > 0:
            actions.append({
                'priority': 'P0',
                'action': 'Resolver problemas críticos de servicio',
                'department': 'Technical Support',
                'timeline': 'Inmediato',
                'affected_customers': p0_count
            })
        
        # Check negative sentiment themes
        theme_sentiments = analysis_results.get('theme_sentiments', {})
        for theme, sentiment_data in theme_sentiments.items():
            if sentiment_data.get('negativo', 0) > 50:  # More than 50% negative
                actions.append({
                    'priority': 'P1',
                    'action': f'Mejorar {theme}',
                    'department': self.get_department_for_theme(theme),
                    'timeline': '1 semana',
                    'affected_customers': sentiment_data.get('total_mentions', 0)
                })
        
        # Sort by priority
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        actions.sort(key=lambda x: priority_order.get(x['priority'], 99))
        
        return actions

    def get_department_for_theme(self, theme):
        """Map themes to responsible departments"""
        department_map = {
            'precio': 'Billing & Pricing',
            'servicio_tecnico': 'Technical Support',
            'calidad_conexion': 'Network Operations',
            'atencion_cliente': 'Customer Service',
            'instalacion': 'Field Operations',
            'cobertura': 'Network Planning'
        }
        return department_map.get(theme, 'General Management')

    def analyze_customer_value(self, text):
        """Analyze potential customer value indicators"""
        if pd.isna(text) or text == "":
            return {'value_segment': 'standard', 'indicators': []}
        
        text_lower = str(text).lower()
        
        value_indicators = {
            'high_value': ['años con ustedes', 'cliente fiel', 'desde el inicio',
                          'recomendé a varios', 'tengo todos los servicios',
                          'cliente antiguo', 'siempre pago', 'nunca me atraso'],
            'expansion_opportunity': ['me interesa flow', 'quiero más servicios', 
                                     'plan familiar', 'para mi negocio', 'internet empresa',
                                     'necesito más velocidad', 'upgrade'],
            'price_sensitive': ['por el precio', 'solo por costo', 'el más barato',
                               'no puedo pagar más', 'busco económico', 'muy caro',
                               'precio alto', 'costoso']
        }
        
        found_indicators = []
        value_segment = 'standard'
        
        for segment, keywords in value_indicators.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_indicators.append(keyword)
                    if segment == 'high_value':
                        value_segment = 'vip'
                    elif segment == 'expansion_opportunity' and value_segment != 'vip':
                        value_segment = 'growth'
                    elif segment == 'price_sensitive' and value_segment == 'standard':
                        value_segment = 'budget'
        
        return {
            'value_segment': value_segment,
            'indicators': found_indicators
        }

    def full_analysis(self, text):
        """Perform complete enhanced analysis on a single comment"""
        return {
            'emotions': self.analyze_emotions(text),
            'extended_themes': self.analyze_extended_themes(text),
            'churn_risk': self.predict_churn_risk(text),
            'competitors': self.analyze_competitors(text),
            'urgency': self.determine_urgency(text),
            'customer_value': self.analyze_customer_value(text)
        }