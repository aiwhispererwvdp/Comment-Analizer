"""
Input Validation and Sanitization Module
Provides comprehensive validation for all user inputs to prevent security vulnerabilities
"""

import re
import html
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
import pandas as pd
import logging

# File type detection disabled to avoid dependency issues
HAS_MAGIC = False
magic = None

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class InputValidator:
    """Comprehensive input validation and sanitization"""
    
    # File validation constants
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'.xlsx', '.csv', '.json', '.txt'}
    ALLOWED_MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
        'application/json',
        'text/plain'
    }
    
    # Text validation constants
    MAX_COMMENT_LENGTH = 5000
    MAX_COMMENTS_PER_BATCH = 1000
    MIN_COMMENT_LENGTH = 1
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'(\'|(\'\')|(\;)|\b(or|and)\b.*?(\=|like|\<|\>))',
        r'(union|select|insert|delete|update|drop|create|alter)',
        r'(\-\-|\#|\/\*|\*\/)',
        r'(script|javascript|vbscript|onload|onerror)',
        r'(xp_|sp_|exec|execute)'
    ]
    
    @staticmethod
    def validate_file_upload(uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file for security and format compliance
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check file size
            if uploaded_file.size > InputValidator.MAX_FILE_SIZE:
                return False, f"File too large. Maximum size is {InputValidator.MAX_FILE_SIZE // (1024*1024)}MB"
            
            if uploaded_file.size == 0:
                return False, "File is empty"
            
            # Check file extension
            file_extension = Path(uploaded_file.name).suffix.lower()
            if file_extension not in InputValidator.ALLOWED_EXTENSIONS:
                return False, f"Unsupported file type. Allowed: {', '.join(InputValidator.ALLOWED_EXTENSIONS)}"
            
            # Check file content type (basic)
            if hasattr(uploaded_file, 'type') and uploaded_file.type:
                if uploaded_file.type not in InputValidator.ALLOWED_MIME_TYPES:
                    logger.warning(f"Suspicious MIME type: {uploaded_file.type}")
            
            # Check filename for suspicious content
            if not InputValidator._is_safe_filename(uploaded_file.name):
                return False, "Invalid filename. Use only letters, numbers, dots, hyphens, and underscores"
            
            return True, "Valid file"
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return False, "File validation failed"
    
    @staticmethod
    def validate_comment_text(comment: str) -> Tuple[bool, str]:
        """
        Validate and sanitize comment text
        
        Args:
            comment: Raw comment text
            
        Returns:
            Tuple[bool, str]: (is_valid, sanitized_comment_or_error)
        """
        try:
            if not comment or not isinstance(comment, str):
                return False, "Comment must be a non-empty string"
            
            # Check length
            if len(comment) < InputValidator.MIN_COMMENT_LENGTH:
                return False, "Comment too short"
            
            if len(comment) > InputValidator.MAX_COMMENT_LENGTH:
                return False, f"Comment too long. Maximum {InputValidator.MAX_COMMENT_LENGTH} characters"
            
            # Check for SQL injection patterns
            for pattern in InputValidator.SQL_INJECTION_PATTERNS:
                if re.search(pattern, comment.lower()):
                    logger.warning(f"Potential SQL injection attempt blocked: {pattern}")
                    return False, "Comment contains potentially harmful content"
            
            # Sanitize HTML/script tags
            sanitized = html.escape(comment)
            
            # Remove potential script tags
            sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove excessive whitespace
            sanitized = re.sub(r'\s+', ' ', sanitized).strip()
            
            return True, sanitized
            
        except Exception as e:
            logger.error(f"Comment validation error: {e}")
            return False, "Comment validation failed"
    
    @staticmethod
    def validate_comment_batch(comments: List[str]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a batch of comments
        
        Args:
            comments: List of comment strings
            
        Returns:
            Tuple[bool, List[str], List[str]]: (all_valid, sanitized_comments, errors)
        """
        if not comments or len(comments) == 0:
            return False, [], ["No comments provided"]
        
        if len(comments) > InputValidator.MAX_COMMENTS_PER_BATCH:
            return False, [], [f"Too many comments. Maximum {InputValidator.MAX_COMMENTS_PER_BATCH} per batch"]
        
        sanitized_comments = []
        errors = []
        all_valid = True
        
        for i, comment in enumerate(comments):
            is_valid, result = InputValidator.validate_comment_text(comment)
            
            if is_valid:
                sanitized_comments.append(result)
            else:
                sanitized_comments.append("")  # Keep position but mark as invalid
                errors.append(f"Comment {i+1}: {result}")
                all_valid = False
        
        return all_valid, sanitized_comments, errors
    
    @staticmethod
    def validate_analysis_parameters(sample_size: int, total_comments: int) -> Tuple[bool, str]:
        """
        Validate analysis parameters
        
        Args:
            sample_size: Number of comments to analyze
            total_comments: Total available comments
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if sample_size <= 0:
            return False, "Sample size must be positive"
        
        if sample_size > total_comments:
            return False, f"Sample size ({sample_size}) cannot exceed total comments ({total_comments})"
        
        if sample_size > InputValidator.MAX_COMMENTS_PER_BATCH:
            return False, f"Sample size too large. Maximum {InputValidator.MAX_COMMENTS_PER_BATCH} comments"
        
        return True, "Valid parameters"
    
    @staticmethod
    def sanitize_export_filename(filename: str) -> str:
        """
        Sanitize filename for export operations
        
        Args:
            filename: Proposed filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove path separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
        
        # Limit length
        if len(sanitized) > 100:
            name, ext = Path(sanitized).stem, Path(sanitized).suffix
            sanitized = name[:95] + ext
        
        # Ensure it's not empty
        if not sanitized or sanitized.isspace():
            sanitized = "export_file"
        
        return sanitized
    
    @staticmethod
    def validate_dataframe_content(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate DataFrame content for suspicious data
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check size limits
            if len(df) == 0:
                return False, "No data found in file"
            
            if len(df) > 20000:  # Updated limit per user requirement
                return False, "Dataset too large. Maximum 20,000 rows supported"
            
            # Check for suspicious column names
            suspicious_columns = ['password', 'token', 'secret', 'key', 'admin']
            for col in df.columns:
                if any(sus in col.lower() for sus in suspicious_columns):
                    logger.warning(f"Suspicious column name detected: {col}")
            
            # Validate text columns
            text_columns = df.select_dtypes(include=['object']).columns
            
            for col in text_columns[:3]:  # Check first 3 text columns
                sample_texts = df[col].dropna().head(10).astype(str)
                
                for text in sample_texts:
                    # Check for extremely long text (potential attack)
                    if len(text) > InputValidator.MAX_COMMENT_LENGTH * 2:
                        return False, f"Text in column '{col}' is suspiciously long"
                    
                    # Check for binary content
                    if any(ord(char) < 32 and char not in '\t\n\r' for char in text[:100]):
                        return False, f"Binary content detected in column '{col}'"
            
            return True, "Valid DataFrame content"
            
        except Exception as e:
            logger.error(f"DataFrame validation error: {e}")
            return False, "Content validation failed"
    
    @staticmethod
    def _is_safe_filename(filename: str) -> bool:
        """Check if filename is safe (no path traversal, etc.)"""
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False
        
        # Check for control characters
        if any(ord(char) < 32 for char in filename):
            return False
        
        # Check reasonable length
        if len(filename) > 255:
            return False
        
        # Check for dangerous patterns
        dangerous_patterns = ['con', 'prn', 'aux', 'nul', 'com1', 'lpt1']
        if Path(filename).stem.lower() in dangerous_patterns:
            return False
        
        return True

class SecurityLogger:
    """Centralized security event logging"""
    
    @staticmethod
    def log_validation_failure(event_type: str, details: str, user_info: str = "unknown"):
        """Log security validation failures"""
        logger.warning(f"SECURITY: {event_type} - {details} - User: {user_info}")
    
    @staticmethod
    def log_suspicious_activity(activity: str, details: str, user_info: str = "unknown"):
        """Log suspicious user activity"""
        logger.error(f"SECURITY ALERT: {activity} - {details} - User: {user_info}")

# Example usage and testing
if __name__ == "__main__":
    # Test comment validation
    test_comments = [
        "El servicio es excelente",
        "SELECT * FROM users",  # SQL injection attempt
        "<script>alert('xss')</script>",  # XSS attempt
        "A" * 6000,  # Too long
        "",  # Empty
        "Comentario normal en español"
    ]
    
    print("Testing comment validation:")
    for i, comment in enumerate(test_comments):
        is_valid, result = InputValidator.validate_comment_text(comment)
        print(f"Comment {i+1}: {'VALID' if is_valid else 'INVALID'} - {result[:50]}...")
    
    # Test batch validation
    all_valid, sanitized, errors = InputValidator.validate_comment_batch(test_comments)
    print(f"\nBatch validation: {'PASS' if all_valid else 'FAIL'}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"  - {error}")