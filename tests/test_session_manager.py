"""
Tests for SessionManager
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch

from src.services.session_manager import SessionManager


class TestSessionManager:
    """Test cases for SessionManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        with patch('streamlit.session_state', new={}):
            self.manager = SessionManager()
    
    @patch('streamlit.session_state', new={})
    def test_store_uploaded_data_single_sheet(self):
        """Test storing single sheet data"""
        manager = SessionManager()
        test_df = pd.DataFrame({'comment': ['test']})
        data_info = {'total_comments': 1, 'sources': ['test']}
        processing_info = {'is_multi_sheet': False}
        
        manager.store_uploaded_data(test_df, data_info, processing_info)
        
        assert 'comments_data' in manager.session_state
        assert 'data_info' in manager.session_state
        assert manager.session_state['is_multi_sheet'] is False
    
    @patch('streamlit.session_state', new={})
    def test_store_uploaded_data_multi_sheet(self):
        """Test storing multi-sheet data"""
        manager = SessionManager()
        test_df = pd.DataFrame({'comment': ['test']})
        data_info = {'total_comments': 1, 'sources': ['test']}
        processing_info = {
            'is_multi_sheet': True,
            'sheets': ['Sheet1', 'Sheet2'],
            'current_sheet': 'Sheet1',
            'temp_path': '/path/to/file.xlsx'
        }
        
        manager.store_uploaded_data(test_df, data_info, processing_info)
        
        assert manager.session_state['is_multi_sheet'] is True
        assert manager.session_state['excel_sheets'] == ['Sheet1', 'Sheet2']
        assert manager.session_state['current_sheet'] == 'Sheet1'
        assert manager.session_state['uploaded_file_path'] == '/path/to/file.xlsx'
    
    @patch('streamlit.session_state', new={})
    def test_store_analysis_results(self):
        """Test storing analysis results"""
        manager = SessionManager()
        results = [{'sentiment': 'positive'}]
        insights = {'positive_percentage': 75}
        recommendations = ['Improve customer service']
        analyzed_comments = ['Great service']
        
        manager.store_analysis_results(results, insights, recommendations, analyzed_comments)
        
        assert manager.session_state['analysis_results'] == results
        assert manager.session_state['insights'] == insights
        assert manager.session_state['recommendations'] == recommendations
        assert manager.session_state['analyzed_comments'] == analyzed_comments
    
    @patch('streamlit.session_state', new={})
    def test_store_analysis_results_multi_sheet(self):
        """Test storing analysis results for multi-sheet Excel"""
        manager = SessionManager()
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['current_sheet'] = 'Sheet1'
        
        results = [{'sentiment': 'positive'}]
        insights = {'positive_percentage': 75}
        recommendations = ['Improve customer service']
        analyzed_comments = ['Great service']
        
        manager.store_analysis_results(results, insights, recommendations, analyzed_comments)
        
        # Check current results
        assert manager.session_state['analysis_results'] == results
        
        # Check sheet-specific results
        assert manager.session_state['analysis_results_Sheet1'] == results
        assert manager.session_state['insights_Sheet1'] == insights
        assert manager.session_state['recommendations_Sheet1'] == recommendations
        assert manager.session_state['analyzed_comments_Sheet1'] == analyzed_comments
    
    @patch('streamlit.session_state', new={})
    def test_get_analysis_results_current(self):
        """Test getting current analysis results"""
        manager = SessionManager()
        test_results = [{'sentiment': 'positive'}]
        manager.session_state['analysis_results'] = test_results
        
        results = manager.get_analysis_results()
        
        assert results['results'] == test_results
    
    @patch('streamlit.session_state', new={})
    def test_get_analysis_results_specific_sheet(self):
        """Test getting analysis results for specific sheet"""
        manager = SessionManager()
        test_results = [{'sentiment': 'negative'}]
        manager.session_state['analysis_results_Sheet2'] = test_results
        
        results = manager.get_analysis_results('Sheet2')
        
        assert results['results'] == test_results
    
    @patch('streamlit.session_state', new={})
    def test_switch_excel_sheet_success(self):
        """Test successful sheet switching"""
        manager = SessionManager()
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['current_sheet'] = 'Sheet1'
        
        # Add existing analysis for Sheet2
        manager.session_state['analysis_results_Sheet2'] = [{'sentiment': 'positive'}]
        manager.session_state['insights_Sheet2'] = {'positive_percentage': 80}
        
        success = manager.switch_excel_sheet('Sheet2')
        
        assert success is True
        assert manager.session_state['current_sheet'] == 'Sheet2'
        assert manager.session_state['analysis_results'] == [{'sentiment': 'positive'}]
        assert manager.session_state['insights']['positive_percentage'] == 80
    
    @patch('streamlit.session_state', new={})
    def test_switch_excel_sheet_no_multi_sheet(self):
        """Test sheet switching when not multi-sheet"""
        manager = SessionManager()
        manager.session_state['is_multi_sheet'] = False
        
        success = manager.switch_excel_sheet('Sheet2')
        
        assert success is False
    
    @patch('streamlit.session_state', new={})
    def test_get_sheet_analysis_status(self):
        """Test getting analysis status for all sheets"""
        manager = SessionManager()
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['excel_sheets'] = ['Sheet1', 'Sheet2', 'Sheet3']
        manager.session_state['analysis_results_Sheet1'] = [{'test': 'data'}]
        # Sheet2 and Sheet3 have no analysis
        
        status = manager.get_sheet_analysis_status()
        
        assert status['Sheet1'] is True
        assert status['Sheet2'] is False
        assert status['Sheet3'] is False
    
    @patch('streamlit.session_state', new={})
    def test_clear_sheet_results(self):
        """Test clearing results for specific sheet"""
        manager = SessionManager()
        # Add some sheet-specific data
        manager.session_state['analysis_results_Sheet1'] = [{'test': 'data'}]
        manager.session_state['insights_Sheet1'] = {'test': 'insights'}
        manager.session_state['recommendations_Sheet1'] = ['test recommendation']
        manager.session_state['analyzed_comments_Sheet1'] = ['test comment']
        
        manager.clear_sheet_results('Sheet1')
        
        assert 'analysis_results_Sheet1' not in manager.session_state
        assert 'insights_Sheet1' not in manager.session_state
        assert 'recommendations_Sheet1' not in manager.session_state
        assert 'analyzed_comments_Sheet1' not in manager.session_state
    
    @patch('streamlit.session_state', new={})
    def test_clear_all_analysis_results(self):
        """Test clearing all analysis results"""
        manager = SessionManager()
        # Add current and sheet-specific data
        manager.session_state['analysis_results'] = [{'test': 'data'}]
        manager.session_state['insights'] = {'test': 'insights'}
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['excel_sheets'] = ['Sheet1', 'Sheet2']
        manager.session_state['analysis_results_Sheet1'] = [{'test': 'data1'}]
        manager.session_state['analysis_results_Sheet2'] = [{'test': 'data2'}]
        
        manager.clear_all_analysis_results()
        
        assert 'analysis_results' not in manager.session_state
        assert 'insights' not in manager.session_state
        assert 'analysis_results_Sheet1' not in manager.session_state
        assert 'analysis_results_Sheet2' not in manager.session_state
    
    @patch('streamlit.session_state', new={})
    def test_has_data_loaded(self):
        """Test checking if data is loaded"""
        manager = SessionManager()
        
        # No data loaded
        assert manager.has_data_loaded() is False
        
        # Data loaded
        manager.session_state['comments_data'] = pd.DataFrame({'comment': ['test']})
        assert manager.has_data_loaded() is True
        
        # Data is None
        manager.session_state['comments_data'] = None
        assert manager.has_data_loaded() is False
    
    @patch('streamlit.session_state', new={})
    def test_has_analysis_results(self):
        """Test checking if analysis results exist"""
        manager = SessionManager()
        
        # No results
        assert manager.has_analysis_results() is False
        assert manager.has_analysis_results('Sheet1') is False
        
        # Current results exist
        manager.session_state['analysis_results'] = [{'test': 'data'}]
        assert manager.has_analysis_results() is True
        
        # Sheet-specific results exist
        manager.session_state['analysis_results_Sheet1'] = [{'test': 'data'}]
        assert manager.has_analysis_results('Sheet1') is True
    
    @patch('streamlit.session_state', new={})
    def test_get_current_data(self):
        """Test getting current data summary"""
        manager = SessionManager()
        test_df = pd.DataFrame({'comment': ['test']})
        manager.session_state['comments_data'] = test_df
        manager.session_state['data_info'] = {'total_comments': 1}
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['current_sheet'] = 'Sheet1'
        manager.session_state['excel_sheets'] = ['Sheet1', 'Sheet2']
        
        data = manager.get_current_data()
        
        assert data['comments_data'].equals(test_df)
        assert data['data_info']['total_comments'] == 1
        assert data['is_multi_sheet'] is True
        assert data['current_sheet'] == 'Sheet1'
        assert data['excel_sheets'] == ['Sheet1', 'Sheet2']
    
    @patch('streamlit.session_state', new={})
    def test_optimization_settings(self):
        """Test optimization settings storage and retrieval"""
        manager = SessionManager()
        
        # Test default settings
        default_settings = manager.get_optimization_settings()
        assert default_settings['deduplication'] is True
        assert default_settings['caching'] is True
        
        # Test storing custom settings
        custom_settings = {
            'deduplication': False,
            'prefiltering': False,
            'language_detection': True,
            'caching': False
        }
        manager.store_optimization_settings(custom_settings)
        
        retrieved_settings = manager.get_optimization_settings()
        assert retrieved_settings == custom_settings
    
    @patch('streamlit.session_state', new={})
    def test_get_session_info(self):
        """Test getting session information summary"""
        manager = SessionManager()
        manager.session_state['session_id'] = 'test_session_123'
        manager.session_state['comments_data'] = pd.DataFrame({'comment': ['test']})
        manager.session_state['analysis_results'] = [{'test': 'data'}]
        manager.session_state['is_multi_sheet'] = True
        manager.session_state['current_sheet'] = 'Sheet1'
        
        info = manager.get_session_info()
        
        assert info['session_id'] == 'test_session_123'
        assert info['has_data'] is True
        assert info['has_analysis'] is True
        assert info['is_multi_sheet'] is True
        assert info['current_sheet'] == 'Sheet1'


# Pytest fixtures
@pytest.fixture
def sample_session_manager():
    """Create a SessionManager with sample data"""
    with patch('streamlit.session_state', new={}):
        manager = SessionManager()
        # Add some sample data
        manager.session_state['comments_data'] = pd.DataFrame({
            'comment': ['Great service', 'Poor quality', 'Average experience']
        })
        manager.session_state['data_info'] = {
            'total_comments': 3,
            'sources': ['test_file.csv']
        }
        return manager


# Integration tests
class TestSessionManagerIntegration:
    """Integration tests for SessionManager"""
    
    @patch('streamlit.session_state', new={})
    def test_full_workflow_single_sheet(self):
        """Test complete workflow for single sheet file"""
        manager = SessionManager()
        
        # 1. Store uploaded data
        test_df = pd.DataFrame({'comment': ['test comment']})
        data_info = {'total_comments': 1, 'sources': ['test.csv']}
        processing_info = {'is_multi_sheet': False}
        
        manager.store_uploaded_data(test_df, data_info, processing_info)
        
        # 2. Store analysis results
        results = [{'sentiment': 'positive', 'confidence': 0.95}]
        insights = {'positive_percentage': 100}
        recommendations = ['Keep up the good work']
        analyzed_comments = ['test comment']
        
        manager.store_analysis_results(results, insights, recommendations, analyzed_comments)
        
        # 3. Verify data integrity
        assert manager.has_data_loaded()
        assert manager.has_analysis_results()
        
        current_data = manager.get_current_data()
        assert current_data['is_multi_sheet'] is False
        
        analysis_results = manager.get_analysis_results()
        assert analysis_results['results'] == results
        assert analysis_results['insights'] == insights
    
    @patch('streamlit.session_state', new={})
    def test_full_workflow_multi_sheet(self):
        """Test complete workflow for multi-sheet file"""
        manager = SessionManager()
        
        # 1. Store multi-sheet data
        test_df = pd.DataFrame({'comment': ['sheet1 comment']})
        data_info = {'total_comments': 1, 'sources': ['test.xlsx']}
        processing_info = {
            'is_multi_sheet': True,
            'sheets': ['Sheet1', 'Sheet2'],
            'current_sheet': 'Sheet1',
            'temp_path': '/path/to/test.xlsx'
        }
        
        manager.store_uploaded_data(test_df, data_info, processing_info)
        
        # 2. Analyze Sheet1
        results_sheet1 = [{'sentiment': 'positive'}]
        insights_sheet1 = {'positive_percentage': 100}
        recommendations_sheet1 = ['Good work on Sheet1']
        comments_sheet1 = ['sheet1 comment']
        
        manager.store_analysis_results(results_sheet1, insights_sheet1, recommendations_sheet1, comments_sheet1)
        
        # 3. Switch to Sheet2 and analyze
        manager.switch_excel_sheet('Sheet2')
        
        results_sheet2 = [{'sentiment': 'negative'}]
        insights_sheet2 = {'negative_percentage': 100}
        recommendations_sheet2 = ['Improve Sheet2']
        comments_sheet2 = ['sheet2 complaint']
        
        manager.store_analysis_results(results_sheet2, insights_sheet2, recommendations_sheet2, comments_sheet2)
        
        # 4. Verify sheet-specific data
        sheet_status = manager.get_sheet_analysis_status()
        assert sheet_status['Sheet1'] is True
        assert sheet_status['Sheet2'] is True
        
        # 5. Switch back to Sheet1 and verify data persistence
        manager.switch_excel_sheet('Sheet1')
        current_results = manager.get_analysis_results()
        assert current_results['results'] == results_sheet1
        
        # 6. Clear all and verify cleanup
        manager.clear_all_analysis_results()
        assert not manager.has_analysis_results()
        assert not manager.has_analysis_results('Sheet1')
        assert not manager.has_analysis_results('Sheet2')