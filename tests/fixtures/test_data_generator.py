"""
Test Data Generator for Personal Paraguay Fiber Comments Analysis
Generates realistic test data for various testing scenarios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from pathlib import Path
from typing import Dict, List, Optional


class DataGenerator:
    """Generate test data for various testing scenarios"""
    
    def __init__(self):
        """Initialize test data generator with sample content"""
        
        # Positive comments in Spanish
        self.positive_comments_es = [
            "Excelente servicio de fibra óptica, muy satisfecho con la velocidad",
            "La instalación fue rápida y profesional, muy buen servicio",
            "Internet súper rápido, no tengo quejas, funciona perfectamente",
            "Muy contento con el servicio, la velocidad es increíble",
            "El mejor internet que he tenido, lo recomiendo totalmente",
            "Servicio impecable, nunca se corta y siempre funciona bien",
            "Atención al cliente excelente, resolvieron mi problema rápidamente",
            "La fibra óptica cambió mi vida, puedo trabajar sin problemas",
            "Precio justo por la calidad del servicio, estoy muy satisfecho",
            "Instalación sin problemas y servicio estable, muy recomendable"
        ]
        
        # Negative comments in Spanish
        self.negative_comments_es = [
            "Terrible servicio, se corta constantemente y nadie responde",
            "Muy lento para lo que pago, estoy muy decepcionado",
            "Pésima atención al cliente, nunca resuelven nada",
            "El internet se cae todos los días, es un desastre",
            "No cumple con la velocidad prometida, muy mal servicio",
            "Llevo días sin internet y no me dan solución",
            "Cobran demasiado para la mala calidad que ofrecen",
            "Instalación desastrosa, dejaron todo mal hecho",
            "El peor servicio que he tenido, no lo recomiendo",
            "Problemas constantes, estoy pensando en cambiar de proveedor"
        ]
        
        # Neutral comments in Spanish
        self.neutral_comments_es = [
            "El servicio funciona normalmente sin problemas particulares",
            "Internet estándar, cumple con lo básico",
            "Sin comentarios especiales, funciona como debe",
            "Servicio regular, ni muy bueno ni muy malo",
            "Funciona bien la mayoría del tiempo",
            "Es un servicio de internet normal",
            "No tengo quejas pero tampoco estoy impresionado",
            "Cumple su función sin más",
            "Servicio aceptable para uso básico",
            "Normal, como cualquier otro proveedor"
        ]
        
        # Comments in Guaraní
        self.comments_gn = [
            "Iporãite pe servicio",
            "Ndaipóri problema",
            "Oĩ porã la conexión",
            "Che ahayhu ko servicio",
            "Heta problema oĩ"
        ]
        
        # Mixed language comments
        self.mixed_comments = [
            "Che servicio iporã pero un poco caro",
            "La velocidad oĩ porã pero a veces se corta",
            "Muy bueno che internet, ndaipóri problema",
            "Iporãite la instalación, muy profesionales"
        ]
        
        # Categories
        self.categories = [
            'Velocidad', 'Instalación', 'Atención al Cliente', 
            'Estabilidad', 'Precio', 'Calidad General'
        ]
        
        # Cities in Paraguay
        self.cities = [
            'Asunción', 'Ciudad del Este', 'San Lorenzo', 
            'Luque', 'Capiatá', 'Lambaré', 'Fernando de la Mora',
            'Limpio', 'Ñemby', 'Encarnación', 'Pedro Juan Caballero'
        ]
    
    def generate_small_dataset(self, num_rows: int = 10) -> pd.DataFrame:
        """Generate a small dataset for quick testing"""
        comments = []
        
        for i in range(num_rows):
            if i < num_rows // 3:
                comment = random.choice(self.positive_comments_es)
                rating = random.randint(4, 5)
            elif i < 2 * num_rows // 3:
                comment = random.choice(self.negative_comments_es)
                rating = random.randint(1, 2)
            else:
                comment = random.choice(self.neutral_comments_es)
                rating = 3
            
            comments.append({
                'Comentario': comment,
                'Fecha': datetime.now() - timedelta(days=random.randint(1, 30)),
                'Nota': rating,
                'Categoría': random.choice(self.categories),
                'Ciudad': random.choice(self.cities)
            })
        
        return pd.DataFrame(comments)
    
    def generate_medium_dataset(self, num_rows: int = 100) -> pd.DataFrame:
        """Generate a medium dataset for standard testing"""
        comments = []
        
        for i in range(num_rows):
            # Mix different types of comments
            comment_type = random.choices(
                ['positive', 'negative', 'neutral', 'guarani', 'mixed'],
                weights=[0.3, 0.3, 0.2, 0.1, 0.1]
            )[0]
            
            if comment_type == 'positive':
                comment = random.choice(self.positive_comments_es)
                rating = random.randint(4, 5)
            elif comment_type == 'negative':
                comment = random.choice(self.negative_comments_es)
                rating = random.randint(1, 2)
            elif comment_type == 'neutral':
                comment = random.choice(self.neutral_comments_es)
                rating = 3
            elif comment_type == 'guarani':
                comment = random.choice(self.comments_gn)
                rating = random.randint(3, 5)
            else:  # mixed
                comment = random.choice(self.mixed_comments)
                rating = random.randint(2, 4)
            
            comments.append({
                'Comentario': comment,
                'Fecha': datetime.now() - timedelta(days=random.randint(1, 90)),
                'Nota': rating,
                'Categoría': random.choice(self.categories),
                'Ciudad': random.choice(self.cities),
                'Usuario_ID': f'USER_{i:04d}'
            })
        
        return pd.DataFrame(comments)
    
    def generate_large_dataset(self, num_rows: int = 1000) -> pd.DataFrame:
        """Generate a large dataset for performance testing"""
        # Use numpy for faster generation
        np.random.seed(42)  # For reproducibility
        
        # Generate comment indices
        positive_idx = np.random.randint(0, len(self.positive_comments_es), num_rows // 3)
        negative_idx = np.random.randint(0, len(self.negative_comments_es), num_rows // 3)
        neutral_idx = np.random.randint(0, len(self.neutral_comments_es), num_rows - 2 * (num_rows // 3))
        
        # Build comments list
        comments = (
            [self.positive_comments_es[i] for i in positive_idx] +
            [self.negative_comments_es[i] for i in negative_idx] +
            [self.neutral_comments_es[i] for i in neutral_idx]
        )
        
        # Shuffle comments
        random.shuffle(comments)
        
        # Generate other columns
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=365),
            end=datetime.now(),
            periods=num_rows
        )
        
        ratings = np.concatenate([
            np.random.randint(4, 6, num_rows // 3),
            np.random.randint(1, 3, num_rows // 3),
            np.full(num_rows - 2 * (num_rows // 3), 3)
        ])
        np.random.shuffle(ratings)
        
        return pd.DataFrame({
            'Comentario': comments,
            'Fecha': dates,
            'Nota': ratings,
            'Categoría': np.random.choice(self.categories, num_rows),
            'Ciudad': np.random.choice(self.cities, num_rows),
            'Usuario_ID': [f'USER_{i:05d}' for i in range(num_rows)],
            'Sesión_ID': [f'SESSION_{i:08d}' for i in range(num_rows)]
        })
    
    def generate_edge_cases_dataset(self) -> pd.DataFrame:
        """Generate dataset with edge cases for testing"""
        edge_cases = [
            # Empty comment
            {'Comentario': '', 'Nota': 3},
            # Very short comment
            {'Comentario': 'Ok', 'Nota': 3},
            # Very long comment
            {'Comentario': 'Este es un comentario extremadamente largo ' * 50, 'Nota': 3},
            # Special characters
            {'Comentario': '¡¿Qué tal?! @#$%^&*()', 'Nota': 3},
            # Numbers only
            {'Comentario': '12345 67890', 'Nota': 3},
            # Emojis
            {'Comentario': '😀 Excelente servicio! 👍', 'Nota': 5},
            # HTML/Script injection attempt
            {'Comentario': '<script>alert("test")</script>', 'Nota': 1},
            # SQL injection attempt
            {'Comentario': "'; DROP TABLE comments; --", 'Nota': 1},
            # Unicode characters
            {'Comentario': '这是中文评论 これは日本語です', 'Nota': 3},
            # Mixed case
            {'Comentario': 'ExCeLenTe SeRvIcIo', 'Nota': 4},
            # Repeated characters
            {'Comentario': 'Muuuuuuy bueeeeeeno!!!!!!', 'Nota': 5},
            # All caps
            {'Comentario': 'TERRIBLE SERVICIO NO FUNCIONA', 'Nota': 1},
            # Null/None values
            {'Comentario': None, 'Nota': None},
            # Whitespace only
            {'Comentario': '   \n\t   ', 'Nota': 3},
        ]
        
        df = pd.DataFrame(edge_cases)
        df['Fecha'] = datetime.now()
        df['Categoría'] = 'Edge Case'
        df['Ciudad'] = 'Test City'
        
        return df
    
    def generate_multi_sheet_excel(self, output_path: str) -> str:
        """Generate Excel file with multiple sheets for testing"""
        output_path = Path(output_path)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Small dataset
            small_df = self.generate_small_dataset(20)
            small_df.to_excel(writer, sheet_name='Enero', index=False)
            
            # Sheet 2: Medium dataset
            medium_df = self.generate_medium_dataset(50)
            medium_df.to_excel(writer, sheet_name='Febrero', index=False)
            
            # Sheet 3: Edge cases
            edge_df = self.generate_edge_cases_dataset()
            edge_df.to_excel(writer, sheet_name='Edge_Cases', index=False)
            
            # Sheet 4: Summary
            summary_df = pd.DataFrame({
                'Mes': ['Enero', 'Febrero'],
                'Total_Comentarios': [len(small_df), len(medium_df)],
                'Promedio_Nota': [small_df['Nota'].mean(), medium_df['Nota'].mean()]
            })
            summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        return str(output_path)
    
    def generate_csv_file(self, output_path: str, num_rows: int = 100) -> str:
        """Generate CSV file for testing"""
        df = self.generate_medium_dataset(num_rows)
        output_path = Path(output_path)
        df.to_csv(output_path, index=False, encoding='utf-8')
        return str(output_path)
    
    def generate_json_file(self, output_path: str, num_rows: int = 50) -> str:
        """Generate JSON file for testing"""
        df = self.generate_small_dataset(num_rows)
        output_path = Path(output_path)
        
        # Convert to JSON with proper date formatting
        json_data = df.to_dict('records')
        for record in json_data:
            if pd.notna(record.get('Fecha')):
                record['Fecha'] = record['Fecha'].isoformat()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return str(output_path)
    
    def generate_text_file(self, output_path: str, num_lines: int = 30) -> str:
        """Generate text file with one comment per line"""
        output_path = Path(output_path)
        
        comments = (
            random.choices(self.positive_comments_es, k=num_lines // 3) +
            random.choices(self.negative_comments_es, k=num_lines // 3) +
            random.choices(self.neutral_comments_es, k=num_lines - 2 * (num_lines // 3))
        )
        
        random.shuffle(comments)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for comment in comments:
                f.write(comment + '\n')
        
        return str(output_path)
    
    def generate_all_test_files(self, output_dir: str) -> Dict[str, str]:
        """Generate all types of test files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        # Generate different file types
        files['small_excel'] = self.generate_multi_sheet_excel(
            output_dir / 'test_small.xlsx'
        )
        files['medium_csv'] = self.generate_csv_file(
            output_dir / 'test_medium.csv', 
            num_rows=100
        )
        files['small_json'] = self.generate_json_file(
            output_dir / 'test_small.json',
            num_rows=20
        )
        files['small_text'] = self.generate_text_file(
            output_dir / 'test_small.txt',
            num_lines=30
        )
        
        # Generate different sizes
        for size, rows in [('tiny', 5), ('small', 50), ('medium', 500)]:
            df = self.generate_medium_dataset(rows) if rows > 10 else self.generate_small_dataset(rows)
            file_path = output_dir / f'test_{size}.xlsx'
            df.to_excel(file_path, index=False)
            files[f'{size}_excel'] = str(file_path)
        
        return files


# Convenience functions for direct use
def generate_test_dataframe(size: str = 'small') -> pd.DataFrame:
    """Generate test dataframe of specified size"""
    generator = DataGenerator()
    
    if size == 'small':
        return generator.generate_small_dataset(10)
    elif size == 'medium':
        return generator.generate_medium_dataset(100)
    elif size == 'large':
        return generator.generate_large_dataset(1000)
    elif size == 'edge':
        return generator.generate_edge_cases_dataset()
    else:
        raise ValueError(f"Unknown size: {size}. Use 'small', 'medium', 'large', or 'edge'")


def create_all_test_files(output_dir: str = 'tests/fixtures/test_files') -> Dict[str, str]:
    """Create all test files in the specified directory"""
    generator = DataGenerator()
    return generator.generate_all_test_files(output_dir)


if __name__ == '__main__':
    # Generate test files when run directly
    print("Generating test data files...")
    files = create_all_test_files()
    print(f"Generated {len(files)} test files:")
    for name, path in files.items():
        print(f"  - {name}: {path}")
    print("Test data generation complete!")