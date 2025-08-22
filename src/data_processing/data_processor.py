"""
Data processor module for handling data operations
"""

import pandas as pd
from typing import Iterator, List


class DataProcessor:
    """Simple data processor for testing"""
    
    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size
    
    def chunk_data(self, df: pd.DataFrame) -> Iterator[pd.DataFrame]:
        """Chunk dataframe into smaller pieces"""
        for i in range(0, len(df), self.chunk_size):
            yield df.iloc[i:i + self.chunk_size]