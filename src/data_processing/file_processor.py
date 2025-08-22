"""
File processor module for handling different file formats
"""

import pandas as pd
from pathlib import Path
from typing import Union


class FileProcessor:
    """Simple file processor for testing"""
    
    def process_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Process a file and return DataFrame"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif file_path.suffix.lower() == '.json':
            return pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")