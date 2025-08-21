"""
Theme package for Personal Paraguay Comments Analysis Platform
Provides centralized styling and UI components with enhanced modern dark design
"""

from .modern_theme import ModernProfessionalTheme, modern_theme
from .enhanced_dark_theme import EnhancedDarkTheme, enhanced_dark_theme
from .styles import ProfessionalTheme

# Use enhanced dark theme as default
theme = enhanced_dark_theme
# Alias for backwards compatibility
dark_theme = enhanced_dark_theme
DarkProfessionalTheme = EnhancedDarkTheme

__all__ = [
    'DarkProfessionalTheme', 
    'ModernProfessionalTheme', 
    'EnhancedDarkTheme',
    'ProfessionalTheme', 
    'theme', 
    'dark_theme', 
    'modern_theme',
    'enhanced_dark_theme'
]