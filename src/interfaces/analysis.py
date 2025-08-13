"""
Analysis Interface Module
Defines the abstract base class for all analysis methods
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AnalysisMethod(ABC):
    """Abstract base class for analysis methods"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the analysis method"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the analysis method does"""
        pass
    
    @abstractmethod
    def analyze_batch(self, comments: List[str], **kwargs) -> List[Dict]:
        """
        Analyze a batch of comments
        
        Args:
            comments: List of text comments to analyze
            **kwargs: Additional parameters for the analysis
            
        Returns:
            List of dictionaries containing analysis results
        """
        pass
    
    @abstractmethod
    def get_insights(self, results: List[Dict]) -> Dict:
        """
        Generate insights from analysis results
        
        Args:
            results: List of analysis results
            
        Returns:
            Dictionary of insights
        """
        pass
    
    @abstractmethod
    def get_recommendations(self, insights: Dict) -> List[str]:
        """
        Generate recommendations based on insights
        
        Args:
            insights: Dictionary of insights
            
        Returns:
            List of recommendation strings
        """
        pass 