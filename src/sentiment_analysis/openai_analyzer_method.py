"""
OpenAI Analysis Method Module
Provides OpenAI implementation of the analysis method
"""

from typing import List, Dict
from interfaces.analysis import AnalysisMethod
from sentiment_analysis.openai_analyzer import OpenAIAnalyzer

class OpenAIAnalysisMethod(AnalysisMethod):
    """OpenAI-based implementation of the analysis method"""
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def description(self) -> str:
        return "Analyze comments using OpenAI's API for sentiment analysis and pattern detection"
    
    def __init__(self, use_cache: bool = True):
        """Initialize the OpenAI analyzer"""
        self.analyzer = OpenAIAnalyzer(use_cache=use_cache)
    
    def analyze_batch(self, comments: List[str], **kwargs) -> List[Dict]:
        """
        Analyze a batch of comments using OpenAI
        
        Args:
            comments: List of text comments to analyze
            **kwargs: Additional parameters like model_name
            
        Returns:
            List of dictionaries containing analysis results
        """
        return self.analyzer.analyze_comments_batch(comments)
    
    def get_insights(self, results: List[Dict]) -> Dict:
        """Generate insights from analysis results"""
        return self.analyzer.get_overall_insights(results)
    
    def get_recommendations(self, insights: Dict) -> List[str]:
        """Generate recommendations based on insights"""
        return self.analyzer.generate_recommendations(insights) 