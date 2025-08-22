"""
Data cleaner module for handling missing data
"""

import pandas as pd


class DataCleaner:
    """Simple data cleaner for testing"""
    
    def __init__(self, missing_strategy: str = "drop"):
        self.missing_strategy = missing_strategy
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe based on strategy"""
        if self.missing_strategy == "drop":
            return df.dropna()
        elif self.missing_strategy == "fill":
            return df.fillna("Unknown")
        elif self.missing_strategy == "skip":
            return df
        else:
            return df