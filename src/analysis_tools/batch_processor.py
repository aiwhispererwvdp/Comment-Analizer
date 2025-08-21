"""
Batch Processing Tool
Handles large-scale comment analysis with memory optimization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Generator, Any
from pathlib import Path
import logging
import gc
import json
from datetime import datetime
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# Import analysis tools
from .duplicate_cleaner import DuplicateCleaner
from .emotion_analyzer import EmotionAnalyzer
from .theme_analyzer import ThemeAnalyzer

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Batch processing tool for efficient large-scale analysis"""
    
    def __init__(self, batch_size: int = 1000, n_workers: int = None):
        """
        Initialize batch processor
        
        Args:
            batch_size: Number of records to process per batch
            n_workers: Number of parallel workers (None for auto)
        """
        self.batch_size = batch_size
        self.n_workers = n_workers or min(4, mp.cpu_count())
        
        # Initialize analyzers
        self.duplicate_cleaner = DuplicateCleaner()
        self.emotion_analyzer = EmotionAnalyzer()
        self.theme_analyzer = ThemeAnalyzer()
        
        # Processing statistics
        self.processing_stats = {
            'total_processed': 0,
            'batches_completed': 0,
            'processing_time': 0,
            'memory_usage': []
        }
        
        # Results storage
        self.batch_results = []
        self.aggregated_results = {}
        
    def read_file_in_chunks(self, file_path: str, 
                           chunk_size: int = None) -> Generator[pd.DataFrame, None, None]:
        """
        Read large file in chunks for memory efficiency
        
        Args:
            file_path: Path to input file
            chunk_size: Size of each chunk
            
        Yields:
            DataFrame chunks
        """
        chunk_size = chunk_size or self.batch_size
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension == '.csv':
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    yield chunk
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
                for i in range(0, len(df), chunk_size):
                    yield df.iloc[i:i + chunk_size]
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise
    
    def process_batch(self, batch_df: pd.DataFrame, 
                     batch_id: int,
                     analyses: List[str] = None) -> Dict:
        """
        Process a single batch of data
        
        Args:
            batch_df: DataFrame batch to process
            batch_id: Batch identifier
            analyses: List of analyses to perform
            
        Returns:
            Dictionary with batch results
        """
        if analyses is None:
            analyses = ['duplicates', 'emotions', 'themes']
        
        results = {
            'batch_id': batch_id,
            'batch_size': len(batch_df),
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Duplicate analysis
            if 'duplicates' in analyses:
                dup_report = self.duplicate_cleaner.generate_duplicate_report(batch_df)
                results['duplicates'] = {
                    'total_duplicates': dup_report['summary']['total_duplicates'],
                    'duplication_rate': dup_report['summary']['duplication_rate'],
                    'unique_count': dup_report['summary']['unique_comments']
                }
            
            # Emotion analysis
            if 'emotions' in analyses:
                emotion_report = self.emotion_analyzer.analyze_emotion_percentages(batch_df)
                results['emotions'] = {
                    'distribution': emotion_report['emotion_percentages'],
                    'balance': emotion_report['emotion_balance'],
                    'dominant': emotion_report['dominant_emotion']
                }
            
            # Theme analysis
            if 'themes' in analyses:
                theme_report = self.theme_analyzer.analyze_themes(batch_df)
                results['themes'] = {
                    'distribution': theme_report['theme_distribution'],
                    'dominant': theme_report['dominant_theme'],
                    'combinations': theme_report['theme_combinations'][:3]  # Top 3
                }
            
            # Memory usage
            results['memory_mb'] = self._get_memory_usage()
            
        except Exception as e:
            logger.error(f"Error processing batch {batch_id}: {e}")
            results['error'] = str(e)
        
        return results
    
    def process_file(self, file_path: str, 
                    output_dir: str = None,
                    analyses: List[str] = None,
                    parallel: bool = True) -> Dict:
        """
        Process entire file in batches
        
        Args:
            file_path: Path to input file
            output_dir: Directory for output files
            analyses: List of analyses to perform
            parallel: Whether to use parallel processing
            
        Returns:
            Aggregated results dictionary
        """
        start_time = datetime.now()
        
        if analyses is None:
            analyses = ['duplicates', 'emotions', 'themes']
        
        logger.info(f"Starting batch processing of {file_path}")
        logger.info(f"Analyses to perform: {analyses}")
        logger.info(f"Batch size: {self.batch_size}, Workers: {self.n_workers}")
        
        # Reset results
        self.batch_results = []
        batch_id = 0
        
        try:
            # Process in batches
            if parallel and self.n_workers > 1:
                self._process_parallel(file_path, analyses)
            else:
                self._process_sequential(file_path, analyses)
            
            # Aggregate results
            self.aggregated_results = self._aggregate_batch_results()
            
            # Save results if output directory specified
            if output_dir:
                self._save_results(output_dir)
            
            # Update processing stats
            self.processing_stats['processing_time'] = (datetime.now() - start_time).total_seconds()
            self.processing_stats['avg_batch_time'] = (
                self.processing_stats['processing_time'] / 
                max(1, self.processing_stats['batches_completed'])
            )
            
            logger.info(f"Batch processing completed in {self.processing_stats['processing_time']:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            raise
        
        return self.aggregated_results
    
    def _process_sequential(self, file_path: str, analyses: List[str]):
        """Process file sequentially"""
        batch_id = 0
        
        for chunk in self.read_file_in_chunks(file_path):
            logger.info(f"Processing batch {batch_id + 1}")
            
            result = self.process_batch(chunk, batch_id, analyses)
            self.batch_results.append(result)
            
            self.processing_stats['total_processed'] += len(chunk)
            self.processing_stats['batches_completed'] += 1
            
            batch_id += 1
            
            # Garbage collection
            if batch_id % 5 == 0:
                gc.collect()
    
    def _process_parallel(self, file_path: str, analyses: List[str]):
        """Process file in parallel"""
        # Load all chunks first
        chunks = list(self.read_file_in_chunks(file_path))
        
        with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
            futures = []
            
            for batch_id, chunk in enumerate(chunks):
                future = executor.submit(self.process_batch, chunk, batch_id, analyses)
                futures.append(future)
            
            # Collect results
            for future in futures:
                result = future.result()
                self.batch_results.append(result)
                self.processing_stats['total_processed'] += result['batch_size']
                self.processing_stats['batches_completed'] += 1
    
    def _aggregate_batch_results(self) -> Dict:
        """Aggregate results from all batches"""
        if not self.batch_results:
            return {}
        
        aggregated = {
            'summary': {
                'total_records': self.processing_stats['total_processed'],
                'total_batches': self.processing_stats['batches_completed'],
                'processing_time': self.processing_stats['processing_time']
            }
        }
        
        # Aggregate duplicates
        if 'duplicates' in self.batch_results[0]:
            total_dups = sum(r.get('duplicates', {}).get('total_duplicates', 0) 
                           for r in self.batch_results)
            total_unique = sum(r.get('duplicates', {}).get('unique_count', 0) 
                             for r in self.batch_results)
            
            aggregated['duplicates'] = {
                'total_duplicates': total_dups,
                'total_unique': total_unique,
                'overall_duplication_rate': round(
                    (total_dups / self.processing_stats['total_processed'] * 100) 
                    if self.processing_stats['total_processed'] > 0 else 0, 2
                )
            }
        
        # Aggregate emotions
        if 'emotions' in self.batch_results[0]:
            emotion_totals = {}
            
            for result in self.batch_results:
                emotions = result.get('emotions', {}).get('distribution', {})
                for emotion, data in emotions.items():
                    if emotion not in emotion_totals:
                        emotion_totals[emotion] = {'count': 0, 'percentage_sum': 0}
                    emotion_totals[emotion]['count'] += data.get('count', 0)
                    emotion_totals[emotion]['percentage_sum'] += data.get('percentage', 0)
            
            # Calculate weighted averages
            aggregated['emotions'] = {}
            for emotion, totals in emotion_totals.items():
                avg_percentage = totals['percentage_sum'] / max(1, len(self.batch_results))
                aggregated['emotions'][emotion] = {
                    'total_count': totals['count'],
                    'avg_percentage': round(avg_percentage, 2)
                }
        
        # Aggregate themes
        if 'themes' in self.batch_results[0]:
            theme_totals = {}
            
            for result in self.batch_results:
                themes = result.get('themes', {}).get('distribution', {})
                for theme, data in themes.items():
                    if theme not in theme_totals:
                        theme_totals[theme] = {'count': 0, 'percentage_sum': 0}
                    theme_totals[theme]['count'] += data.get('count', 0)
                    theme_totals[theme]['percentage_sum'] += data.get('percentage', 0)
            
            # Calculate weighted averages
            aggregated['themes'] = {}
            for theme, totals in theme_totals.items():
                avg_percentage = totals['percentage_sum'] / max(1, len(self.batch_results))
                aggregated['themes'][theme] = {
                    'total_count': totals['count'],
                    'avg_percentage': round(avg_percentage, 2)
                }
        
        return aggregated
    
    def _save_results(self, output_dir: str):
        """Save processing results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save aggregated results as JSON
        json_path = output_path / f'batch_results_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.aggregated_results, f, indent=2, ensure_ascii=False)
        
        # Save detailed batch results
        batch_df = pd.DataFrame(self.batch_results)
        excel_path = output_path / f'batch_details_{timestamp}.xlsx'
        batch_df.to_excel(excel_path, index=False)
        
        # Create summary report
        self._create_summary_report(output_path / f'summary_{timestamp}.txt')
        
        logger.info(f"Results saved to {output_path}")
    
    def _create_summary_report(self, file_path: Path):
        """Create text summary report"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("BATCH PROCESSING SUMMARY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Processing stats
            f.write("PROCESSING STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Records: {self.processing_stats['total_processed']:,}\n")
            f.write(f"Total Batches: {self.processing_stats['batches_completed']}\n")
            f.write(f"Batch Size: {self.batch_size}\n")
            f.write(f"Processing Time: {self.processing_stats.get('processing_time', 0):.2f} seconds\n")
            f.write(f"Avg Batch Time: {self.processing_stats.get('avg_batch_time', 0):.2f} seconds\n\n")
            
            # Duplicate analysis
            if 'duplicates' in self.aggregated_results:
                f.write("DUPLICATE ANALYSIS\n")
                f.write("-" * 30 + "\n")
                dup = self.aggregated_results['duplicates']
                f.write(f"Total Duplicates: {dup['total_duplicates']:,}\n")
                f.write(f"Unique Comments: {dup['total_unique']:,}\n")
                f.write(f"Duplication Rate: {dup['overall_duplication_rate']}%\n\n")
            
            # Emotion analysis
            if 'emotions' in self.aggregated_results:
                f.write("EMOTION ANALYSIS\n")
                f.write("-" * 30 + "\n")
                emotions = self.aggregated_results['emotions']
                sorted_emotions = sorted(emotions.items(), 
                                       key=lambda x: x[1]['avg_percentage'], 
                                       reverse=True)
                for emotion, data in sorted_emotions[:5]:
                    f.write(f"{emotion.capitalize()}: {data['avg_percentage']}%\n")
                f.write("\n")
            
            # Theme analysis
            if 'themes' in self.aggregated_results:
                f.write("THEME ANALYSIS\n")
                f.write("-" * 30 + "\n")
                themes = self.aggregated_results['themes']
                sorted_themes = sorted(themes.items(), 
                                     key=lambda x: x[1]['avg_percentage'], 
                                     reverse=True)
                for theme, data in sorted_themes[:5]:
                    theme_name = theme.replace('_', ' ').title()
                    f.write(f"{theme_name}: {data['avg_percentage']}%\n")
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def optimize_batch_size(self, file_path: str, 
                          target_memory_mb: float = 500) -> int:
        """
        Automatically determine optimal batch size based on memory constraints
        
        Args:
            file_path: Path to input file
            target_memory_mb: Target memory usage in MB
            
        Returns:
            Recommended batch size
        """
        # Sample the file
        sample_size = 100
        sample_df = pd.read_csv(file_path, nrows=sample_size) if file_path.endswith('.csv') else pd.read_excel(file_path, nrows=sample_size)
        
        # Estimate memory per record
        memory_per_record = sample_df.memory_usage(deep=True).sum() / len(sample_df) / 1024 / 1024
        
        # Calculate optimal batch size
        optimal_size = int(target_memory_mb / (memory_per_record * 2))  # Factor of 2 for processing overhead
        optimal_size = max(100, min(optimal_size, 10000))  # Bounds
        
        logger.info(f"Recommended batch size: {optimal_size} records")
        return optimal_size