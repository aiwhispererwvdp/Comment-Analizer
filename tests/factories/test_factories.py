"""
Test factories for generating test data and objects
Using the Factory pattern for flexible test data creation
"""

import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
import json
from pathlib import Path


class BaseFactory:
    """Base factory class for all test factories"""
    
    _sequence = 0
    
    @classmethod
    def reset_sequence(cls):
        """Reset the sequence counter"""
        cls._sequence = 0
    
    @classmethod
    def next_sequence(cls) -> int:
        """Get next sequence number"""
        cls._sequence += 1
        return cls._sequence
    
    @classmethod
    def build(cls, **kwargs) -> Any:
        """Build an instance with given attributes"""
        raise NotImplementedError
    
    @classmethod
    def build_batch(cls, size: int, **kwargs) -> List[Any]:
        """Build multiple instances"""
        return [cls.build(**kwargs) for _ in range(size)]
    
    @classmethod
    def create(cls, **kwargs) -> Any:
        """Create and persist an instance"""
        instance = cls.build(**kwargs)
        # Override to add persistence logic
        return instance
    
    @classmethod
    def create_batch(cls, size: int, **kwargs) -> List[Any]:
        """Create and persist multiple instances"""
        return [cls.create(**kwargs) for _ in range(size)]


class CommentFactory(BaseFactory):
    """Factory for generating test comments"""
    
    # Comment templates by sentiment
    POSITIVE_TEMPLATES = [
        "Excelente servicio de fibra óptica, muy {adjective}",
        "Estoy muy {adjective} con la velocidad de internet",
        "La instalación fue {adjective}, lo recomiendo",
        "{adjective} experiencia con el servicio",
        "Internet {adjective}, sin problemas"
    ]
    
    NEGATIVE_TEMPLATES = [
        "Terrible servicio, muy {adjective}",
        "Internet {adjective}, no funciona bien",
        "Estoy {adjective} con el servicio",
        "La conexión es {adjective}, no lo recomiendo",
        "{adjective} experiencia, cambiaré de proveedor"
    ]
    
    NEUTRAL_TEMPLATES = [
        "El servicio es {adjective}",
        "Internet {adjective}, sin quejas particulares",
        "Funciona de manera {adjective}",
        "Servicio {adjective} para uso básico",
        "La conexión es {adjective}"
    ]
    
    POSITIVE_ADJECTIVES = ["satisfecho", "contento", "feliz", "impresionado", "agradecido",
                           "rápida", "excelente", "perfecta", "increíble", "maravillosa"]
    
    NEGATIVE_ADJECTIVES = ["insatisfecho", "decepcionado", "frustrado", "molesto", "enojado",
                           "lenta", "horrible", "pésima", "terrible", "mala"]
    
    NEUTRAL_ADJECTIVES = ["normal", "regular", "aceptable", "estándar", "básica",
                         "promedio", "común", "ordinaria", "típica", "corriente"]
    
    @classmethod
    def build(cls, 
              sentiment: str = None,
              language: str = 'es',
              length: str = 'medium',
              with_emoji: bool = False,
              with_punctuation: bool = True,
              **kwargs) -> Dict[str, Any]:
        """Build a comment with specified characteristics"""
        
        # Auto-determine sentiment if not provided
        if sentiment is None:
            sentiment = random.choice(['positive', 'negative', 'neutral'])
        
        # Select template and adjectives based on sentiment
        if sentiment == 'positive':
            template = random.choice(cls.POSITIVE_TEMPLATES)
            adjective = random.choice(cls.POSITIVE_ADJECTIVES)
            rating = random.randint(4, 5)
            confidence = random.uniform(0.7, 0.95)
        elif sentiment == 'negative':
            template = random.choice(cls.NEGATIVE_TEMPLATES)
            adjective = random.choice(cls.NEGATIVE_ADJECTIVES)
            rating = random.randint(1, 2)
            confidence = random.uniform(0.7, 0.95)
        else:
            template = random.choice(cls.NEUTRAL_TEMPLATES)
            adjective = random.choice(cls.NEUTRAL_ADJECTIVES)
            rating = 3
            confidence = random.uniform(0.4, 0.7)
        
        # Generate comment text
        text = template.format(adjective=adjective)
        
        # Add length variations
        if length == 'short':
            text = text.split(',')[0] if ',' in text else text[:30]
        elif length == 'long':
            text = f"{text}. " * random.randint(3, 5)
        
        # Add emoji if requested
        if with_emoji:
            emojis = {
                'positive': ['😀', '👍', '⭐', '✨', '🎉'],
                'negative': ['😞', '👎', '😠', '😤', '💔'],
                'neutral': ['😐', '🤷', '➖', '↔️', '〰️']
            }
            text += f" {random.choice(emojis.get(sentiment, ['']))}"
        
        # Add punctuation variations
        if not with_punctuation:
            text = text.replace('.', '').replace(',', '').replace('!', '')
        elif random.random() < 0.3:
            text += random.choice(['!', '!!', '...', '?'])
        
        return {
            'id': cls.next_sequence(),
            'text': text,
            'sentiment': sentiment,
            'confidence': confidence,
            'rating': rating,
            'language': language,
            'date': datetime.now() - timedelta(days=random.randint(0, 30)),
            'user_id': f"user_{random.randint(1000, 9999)}",
            **kwargs
        }
    
    @classmethod
    def build_spanish_comment(cls, **kwargs) -> Dict[str, Any]:
        """Build a Spanish comment"""
        return cls.build(language='es', **kwargs)
    
    @classmethod
    def build_guarani_comment(cls, **kwargs) -> Dict[str, Any]:
        """Build a Guaraní comment"""
        guarani_phrases = [
            "Iporãite pe servicio",
            "Ndaipóri problema",
            "Oĩ porã la conexión",
            "Heta problema oĩ",
            "Che ahayhu ko servicio"
        ]
        comment = cls.build(language='gn', **kwargs)
        comment['text'] = random.choice(guarani_phrases)
        return comment
    
    @classmethod
    def build_mixed_language_comment(cls, **kwargs) -> Dict[str, Any]:
        """Build a mixed language comment"""
        mixed_templates = [
            "Che servicio iporã pero {issue}",
            "La velocidad oĩ porã but {issue}",
            "Muy bueno che internet, ndaipóri problema"
        ]
        issues = ["un poco caro", "sometimes slow", "necesita mejoras"]
        
        comment = cls.build(language='mixed', **kwargs)
        comment['text'] = random.choice(mixed_templates).format(issue=random.choice(issues))
        return comment


class UserFactory(BaseFactory):
    """Factory for generating test users"""
    
    FIRST_NAMES = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "José", "Laura", "Pedro", "Sofia"]
    LAST_NAMES = ["González", "Rodríguez", "López", "Martínez", "García", "Fernández", "Pérez", "Sánchez"]
    CITIES = ["Asunción", "Ciudad del Este", "San Lorenzo", "Luque", "Capiatá", "Lambaré", "Fernando de la Mora"]
    
    @classmethod
    def build(cls, 
              user_type: str = 'customer',
              active: bool = True,
              **kwargs) -> Dict[str, Any]:
        """Build a user with specified characteristics"""
        
        user_id = cls.next_sequence()
        first_name = random.choice(cls.FIRST_NAMES)
        last_name = random.choice(cls.LAST_NAMES)
        
        return {
            'id': user_id,
            'username': f"{first_name.lower()}.{last_name.lower()}{user_id}",
            'email': f"{first_name.lower()}.{last_name.lower()}{user_id}@example.com",
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'user_type': user_type,
            'active': active,
            'city': random.choice(cls.CITIES),
            'created_at': datetime.now() - timedelta(days=random.randint(30, 365)),
            'last_login': datetime.now() - timedelta(days=random.randint(0, 7)),
            **kwargs
        }


class AnalysisResultFactory(BaseFactory):
    """Factory for generating test analysis results"""
    
    @classmethod
    def build(cls,
              sentiment: str = None,
              with_emotions: bool = True,
              with_themes: bool = True,
              with_entities: bool = False,
              **kwargs) -> Dict[str, Any]:
        """Build an analysis result"""
        
        if sentiment is None:
            sentiment = random.choice(['positive', 'negative', 'neutral'])
        
        # Base confidence based on sentiment
        base_confidence = {
            'positive': random.uniform(0.7, 0.95),
            'negative': random.uniform(0.7, 0.95),
            'neutral': random.uniform(0.4, 0.7)
        }
        
        result = {
            'id': cls.next_sequence(),
            'sentiment': sentiment,
            'confidence': base_confidence[sentiment],
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        # Add emotions if requested
        if with_emotions:
            emotions = {
                'joy': 0.0,
                'anger': 0.0,
                'sadness': 0.0,
                'fear': 0.0,
                'surprise': 0.0
            }
            
            if sentiment == 'positive':
                emotions['joy'] = random.uniform(0.6, 0.9)
                emotions['surprise'] = random.uniform(0.1, 0.3)
            elif sentiment == 'negative':
                emotions['anger'] = random.uniform(0.4, 0.7)
                emotions['sadness'] = random.uniform(0.3, 0.6)
                emotions['fear'] = random.uniform(0.1, 0.3)
            else:
                # Neutral - low values for all
                for emotion in emotions:
                    emotions[emotion] = random.uniform(0.0, 0.2)
            
            result['emotions'] = emotions
        
        # Add themes if requested
        if with_themes:
            theme_options = {
                'positive': ['good_service', 'fast_speed', 'reliable', 'professional', 'value_for_money'],
                'negative': ['poor_service', 'slow_speed', 'disconnections', 'bad_support', 'expensive'],
                'neutral': ['average_service', 'basic_features', 'standard_speed', 'normal_price']
            }
            
            themes = random.sample(theme_options[sentiment], k=random.randint(1, 3))
            result['themes'] = themes
        
        # Add entities if requested
        if with_entities:
            entities = []
            if random.random() < 0.5:
                entities.append({
                    'type': 'SERVICE',
                    'text': 'fibra óptica',
                    'confidence': random.uniform(0.8, 1.0)
                })
            if random.random() < 0.3:
                entities.append({
                    'type': 'COMPANY',
                    'text': 'Personal',
                    'confidence': random.uniform(0.7, 0.9)
                })
            result['entities'] = entities
        
        return result


class SessionFactory(BaseFactory):
    """Factory for generating test sessions"""
    
    @classmethod
    def build(cls,
              user_id: str = None,
              active: bool = True,
              with_data: bool = True,
              **kwargs) -> Dict[str, Any]:
        """Build a session"""
        
        session_id = f"session_{cls.next_sequence()}_{random.randint(1000, 9999)}"
        
        session = {
            'id': session_id,
            'user_id': user_id or f"user_{random.randint(1000, 9999)}",
            'active': active,
            'created_at': datetime.now() - timedelta(hours=random.randint(0, 24)),
            'last_activity': datetime.now() - timedelta(minutes=random.randint(0, 60)),
            'ip_address': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            **kwargs
        }
        
        if with_data:
            session['data'] = {
                'uploaded_file': f"test_file_{random.randint(1, 100)}.xlsx",
                'total_comments': random.randint(10, 1000),
                'analyzed_comments': random.randint(5, 500),
                'analysis_complete': random.choice([True, False]),
                'export_generated': random.choice([True, False])
            }
        
        return session


class DataFrameFactory(BaseFactory):
    """Factory for generating test DataFrames"""
    
    @classmethod
    def build(cls,
              rows: int = 10,
              include_comments: bool = True,
              include_dates: bool = True,
              include_ratings: bool = True,
              include_metadata: bool = False,
              **kwargs) -> pd.DataFrame:
        """Build a test DataFrame"""
        
        data = {}
        
        # Always include ID
        data['id'] = list(range(1, rows + 1))
        
        # Add comments if requested
        if include_comments:
            comment_factory = CommentFactory()
            comments = [comment_factory.build()['text'] for _ in range(rows)]
            data['Comentario'] = comments
        
        # Add dates if requested
        if include_dates:
            start_date = datetime.now() - timedelta(days=90)
            dates = pd.date_range(start=start_date, periods=rows, freq='D')
            data['Fecha'] = dates
        
        # Add ratings if requested
        if include_ratings:
            data['Nota'] = np.random.randint(1, 6, rows)
        
        # Add metadata if requested
        if include_metadata:
            data['Ciudad'] = [random.choice(UserFactory.CITIES) for _ in range(rows)]
            data['Usuario'] = [f"user_{i}" for i in range(rows)]
            data['Sesion'] = [f"session_{i}" for i in range(rows)]
        
        # Add any additional columns
        for key, value in kwargs.items():
            if isinstance(value, list) and len(value) == rows:
                data[key] = value
            else:
                data[key] = [value] * rows
        
        return pd.DataFrame(data)


class FileFactory(BaseFactory):
    """Factory for generating test files"""
    
    @classmethod
    def build(cls,
              file_type: str = 'xlsx',
              rows: int = 10,
              file_name: str = None,
              multi_sheet: bool = False,
              **kwargs) -> Path:
        """Build a test file"""
        
        import tempfile
        
        # Generate file name if not provided
        if file_name is None:
            file_name = f"test_file_{cls.next_sequence()}.{file_type}"
        
        # Create temp file
        temp_dir = Path(tempfile.gettempdir())
        file_path = temp_dir / file_name
        
        # Generate data
        df_factory = DataFrameFactory()
        
        if file_type in ['xlsx', 'xls']:
            if multi_sheet:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Create multiple sheets
                    for month in ['Enero', 'Febrero', 'Marzo']:
                        df = df_factory.build(rows=rows, **kwargs)
                        df.to_excel(writer, sheet_name=month, index=False)
            else:
                df = df_factory.build(rows=rows, **kwargs)
                df.to_excel(file_path, index=False)
        
        elif file_type == 'csv':
            df = df_factory.build(rows=rows, **kwargs)
            df.to_csv(file_path, index=False, encoding='utf-8')
        
        elif file_type == 'json':
            df = df_factory.build(rows=rows, **kwargs)
            df.to_json(file_path, orient='records', force_ascii=False, indent=2)
        
        elif file_type == 'txt':
            comment_factory = CommentFactory()
            comments = [comment_factory.build()['text'] for _ in range(rows)]
            file_path.write_text('\n'.join(comments), encoding='utf-8')
        
        return file_path


class MockResponseFactory(BaseFactory):
    """Factory for generating mock API responses"""
    
    @classmethod
    def build(cls,
              success: bool = True,
              api_type: str = 'openai',
              **kwargs) -> Dict[str, Any]:
        """Build a mock API response"""
        
        if api_type == 'openai':
            if success:
                return {
                    'id': f"chatcmpl-{cls.next_sequence()}",
                    'object': 'chat.completion',
                    'created': int(datetime.now().timestamp()),
                    'model': 'gpt-4',
                    'choices': [{
                        'index': 0,
                        'message': {
                            'role': 'assistant',
                            'content': json.dumps({
                                'sentiment': random.choice(['positive', 'negative', 'neutral']),
                                'confidence': random.uniform(0.7, 0.95),
                                'themes': ['service_quality', 'speed'],
                                'language': 'es'
                            })
                        },
                        'finish_reason': 'stop'
                    }],
                    'usage': {
                        'prompt_tokens': random.randint(50, 200),
                        'completion_tokens': random.randint(30, 100),
                        'total_tokens': random.randint(80, 300)
                    }
                }
            else:
                return {
                    'error': {
                        'message': 'API rate limit exceeded',
                        'type': 'rate_limit_error',
                        'code': 'rate_limit_exceeded'
                    }
                }
        
        elif api_type == 'azure':
            if success:
                return {
                    'documents': [{
                        'id': '1',
                        'sentiment': random.choice(['positive', 'negative', 'neutral']),
                        'confidenceScores': {
                            'positive': random.random(),
                            'neutral': random.random(),
                            'negative': random.random()
                        }
                    }]
                }
            else:
                return {
                    'error': {
                        'code': 'InvalidRequest',
                        'message': 'Invalid request'
                    }
                }
        
        return {}