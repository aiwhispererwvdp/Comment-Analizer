"""
Analysis Service Package
Provides a decoupled service layer for text analysis operations
"""

from interfaces.analysis import AnalysisMethod
from .service import AnalysisService, get_analysis_service

__all__ = ['AnalysisMethod', 'AnalysisService', 'get_analysis_service'] 