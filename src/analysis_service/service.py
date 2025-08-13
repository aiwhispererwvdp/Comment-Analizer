"""
Analysis Service Implementation
Provides the core service functionality for analysis methods
"""

from typing import List, Dict, Any, Optional, Type
import logging
import time
from interfaces.analysis import AnalysisMethod
from config import Config

logger = logging.getLogger(__name__)

class AnalysisService:
    """
    Service layer for text analysis operations
    Decouples analysis logic from UI code
    """
    
    def __init__(self):
        """Initialize analysis service with available methods"""
        self.available_methods: Dict[str, Type[AnalysisMethod]] = {}
        self._register_methods()
    
    def _register_methods(self):
        """Register available analysis methods"""
        # Import here to avoid circular imports
        from sentiment_analysis.openai_analyzer_method import OpenAIAnalysisMethod
        from sentiment_analysis.basic_analyzer import BasicAnalysisMethod
        
        # Register built-in methods
        self.available_methods[OpenAIAnalysisMethod().name] = OpenAIAnalysisMethod
        self.available_methods[BasicAnalysisMethod().name] = BasicAnalysisMethod
        
        # Add dynamic method discovery here in the future
        # This could scan directories for classes that extend AnalysisMethod
    
    def get_available_methods(self) -> List[Dict]:
        """
        Get information about available analysis methods
        
        Returns:
            List of dicts with method info
        """
        methods = []
        for method_name, method_class in self.available_methods.items():
            instance = method_class()
            methods.append({
                "name": method_name,
                "description": instance.description
            })
        return methods
    
    def create_method(self, method_name: str, **kwargs) -> Optional[AnalysisMethod]:
        """
        Create an instance of the requested analysis method
        
        Args:
            method_name: Name of the analysis method to create
            **kwargs: Parameters to pass to the method constructor
            
        Returns:
            Instance of the requested analysis method or None if not found
        """
        if method_name not in self.available_methods:
            logger.error(f"Analysis method '{method_name}' not found")
            return None
            
        try:
            method_class = self.available_methods[method_name]
            return method_class(**kwargs)
        except Exception as e:
            logger.error(f"Error creating analysis method '{method_name}': {e}")
            return None
    
    def analyze_comments(self, comments: List[str], method_name: str = "openai", **kwargs) -> Dict[str, Any]:
        """
        Analyze comments using the specified method
        
        Args:
            comments: List of text comments to analyze
            method_name: Name of the analysis method to use
            **kwargs: Additional parameters for the analysis
            
        Returns:
            Dictionary with analysis results, insights, and recommendations
        """
        try:
            # Create analysis method
            method = self.create_method(method_name, **kwargs)
            if not method:
                return {
                    "success": False,
                    "error": f"Analysis method '{method_name}' not available"
                }
            
            # Perform analysis
            start_time = time.time()
            results = method.analyze_batch(comments, **kwargs)
            
            # Generate insights and recommendations
            insights = method.get_insights(results)
            recommendations = method.get_recommendations(insights)
            
            elapsed_time = time.time() - start_time
            
            return {
                "success": True,
                "results": results,
                "insights": insights,
                "recommendations": recommendations,
                "stats": {
                    "total_comments": len(comments),
                    "elapsed_time": elapsed_time,
                    "comments_per_second": len(comments) / elapsed_time if elapsed_time > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing comments: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance
_service = None

def get_analysis_service() -> AnalysisService:
    """Get or create the analysis service singleton"""
    global _service
    if _service is None:
        _service = AnalysisService()
    return _service 