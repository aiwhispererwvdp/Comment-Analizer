"""
Tests for FileUploadService
"""
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import io

from src.services.file_upload_service import FileUploadService


class TestFileUploadService:
    """Test cases for FileUploadService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = FileUploadService()
    
    def test_init(self):
        """Test service initialization"""
        assert self.service.supported_extensions == ['.xlsx', '.xls', '.csv', '.json', '.txt']
        assert self.service.max_file_size_mb == 50
        assert self.service.max_rows == 20000
    
    def test_validate_file_basic_valid_file(self):
        """Test basic file validation with valid file"""
        # Create mock uploaded file
        mock_file = Mock()
        mock_file.name = "test_file.csv"
        mock_file.size = 1024 * 1024  # 1MB
        
        is_valid, error_msg, metadata = self.service.validate_file_basic(mock_file)
        
        assert is_valid is True
        assert error_msg == ""
        assert metadata['extension'] == '.csv'
        assert metadata['size_mb'] == 1.0
        assert metadata['filename'] == "test_file.csv"
    
    def test_validate_file_basic_invalid_extension(self):
        """Test basic file validation with invalid extension"""
        mock_file = Mock()
        mock_file.name = "test_file.pdf"
        mock_file.size = 1024 * 1024
        
        is_valid, error_msg, metadata = self.service.validate_file_basic(mock_file)
        
        assert is_valid is False
        assert "Unsupported file format" in error_msg
    
    def test_validate_file_basic_too_large(self):
        """Test basic file validation with file too large"""
        mock_file = Mock()
        mock_file.name = "test_file.csv"
        mock_file.size = 60 * 1024 * 1024  # 60MB
        
        is_valid, error_msg, metadata = self.service.validate_file_basic(mock_file)
        
        assert is_valid is False
        assert "File size exceeds maximum limit" in error_msg
    
    def test_get_data_quality_metrics(self):
        """Test data quality metrics calculation"""
        # Create test DataFrame
        test_data = pd.DataFrame({
            'comment': ['Good service', 'Bad service', '', 'Good service', None],
            'rating': [5, 1, 3, 5, 2]
        })
        
        metrics = self.service.get_data_quality_metrics(test_data)
        
        assert metrics['total_rows'] == 5
        assert metrics['empty_comments'] == 2  # Empty string and None
        assert metrics['duplicate_comments'] == 1  # 'Good service' appears twice
        assert metrics['valid_entries'] == 3
        assert 'quality_score' in metrics
        assert 'quality_status' in metrics
    
    def test_get_validation_display_data(self):
        """Test validation display data generation"""
        metadata = {
            'extension': '.csv',
            'size_mb': 5.0,
            'filename': 'test.csv'
        }
        
        display_data = self.service.get_validation_display_data(metadata)
        
        assert display_data['size_status'] == 'success'
        assert 'Size: 5.0MB' in display_data['size_message']
        assert display_data['format_status'] == 'success'
        assert 'Format: .csv' in display_data['format_message']
        assert 'Est.' in display_data['rows_estimate']
    
    @patch('src.services.file_upload_service.InputValidator')
    @patch('src.services.file_upload_service.CommentReader')
    def test_process_uploaded_file_success(self, mock_reader_class, mock_validator):
        """Test successful file processing"""
        # Setup mocks
        mock_validator.validate_file_upload.return_value = (True, "")
        mock_validator.sanitize_export_filename.return_value = "safe_file.csv"
        mock_validator.validate_dataframe_content.return_value = (True, "")
        
        mock_reader = Mock()
        mock_reader_class.return_value = mock_reader
        mock_reader.read_file.return_value = pd.DataFrame({'comment': ['test']})
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("comment\ntest comment")
            temp_path = f.name
        
        try:
            mock_file = Mock()
            mock_file.getbuffer.return_value = b"comment\ntest comment"
            
            success, message, df, info = self.service.process_uploaded_file(mock_file)
            
            assert success is True
            assert "successfully" in message.lower()
            assert df is not None
            assert 'file_extension' in info
            
        finally:
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
    
    def test_estimate_rows_csv(self):
        """Test row estimation for CSV files"""
        metadata = {'extension': '.csv', 'size_mb': 2.0}
        estimate = self.service._estimate_rows(metadata)
        assert 'Est.' in estimate
    
    def test_estimate_rows_excel(self):
        """Test row estimation for Excel files"""
        metadata = {'extension': '.xlsx', 'size_mb': 2.0}
        estimate = self.service._estimate_rows(metadata)
        assert 'Excel detected' in estimate


class TestFileUploadServiceIntegration:
    """Integration tests for FileUploadService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = FileUploadService()
    
    def test_real_csv_file_processing(self):
        """Test processing a real CSV file"""
        # Create a real CSV file
        csv_content = "comment,rating\nGood service,5\nBad service,1\nOkay service,3"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            # Create mock file object
            mock_file = Mock()
            mock_file.name = "test.csv"
            mock_file.size = len(csv_content.encode())
            mock_file.getbuffer.return_value = csv_content.encode()
            
            # Basic validation should pass
            is_valid, error_msg, metadata = self.service.validate_file_basic(mock_file)
            assert is_valid is True
            
            # Validation display data should be correct
            display_data = self.service.get_validation_display_data(metadata)
            assert display_data['size_status'] == 'success'
            assert display_data['format_status'] == 'success'
            
        finally:
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)


# Pytest fixtures
@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing"""
    return pd.DataFrame({
        'comment': [
            'Excellent service',
            'Poor quality',
            '',
            'Excellent service',  # Duplicate
            'Average experience',
            None
        ],
        'rating': [5, 1, 3, 5, 3, 2]
    })


@pytest.fixture
def mock_uploaded_file():
    """Create a mock uploaded file"""
    mock_file = Mock()
    mock_file.name = "test_comments.csv"
    mock_file.size = 2048  # 2KB
    mock_file.getbuffer.return_value = b"comment,rating\nGood,5\nBad,1"
    return mock_file


# Parametrized tests
@pytest.mark.parametrize("file_extension,expected_valid", [
    ('.csv', True),
    ('.xlsx', True),
    ('.xls', True),
    ('.json', True),
    ('.txt', True),
    ('.pdf', False),
    ('.doc', False),
    ('.py', False),
])
def test_file_extension_validation(file_extension, expected_valid):
    """Test file extension validation with various formats"""
    service = FileUploadService()
    mock_file = Mock()
    mock_file.name = f"test{file_extension}"
    mock_file.size = 1024
    
    is_valid, _, _ = service.validate_file_basic(mock_file)
    assert is_valid == expected_valid


@pytest.mark.parametrize("file_size_mb,expected_valid", [
    (1, True),
    (25, True),
    (49, True),
    (50, True),
    (51, False),
    (100, False),
])
def test_file_size_validation(file_size_mb, expected_valid):
    """Test file size validation with various sizes"""
    service = FileUploadService()
    mock_file = Mock()
    mock_file.name = "test.csv"
    mock_file.size = file_size_mb * 1024 * 1024  # Convert to bytes
    
    is_valid, _, _ = service.validate_file_basic(mock_file)
    assert is_valid == expected_valid