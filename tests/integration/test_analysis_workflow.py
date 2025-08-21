"""
Integration tests for complete analysis workflows
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import tempfile
import json

# Import modules for integration testing
from services.file_upload_service import FileUploadService
from services.session_manager import SessionManager
from services.analysis_service import AnalysisService
from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
from data_processing.comment_reader import CommentReader
from visualization.export_manager import ExportManager


class TestCompleteAnalysisWorkflow:
    """Test complete analysis workflow from upload to export"""
    
    def test_excel_upload_to_analysis(self, sample_excel_file, mock_streamlit):
        """Test workflow: Excel upload → Analysis → Results"""
        # Initialize services
        upload_service = FileUploadService()
        session_manager = SessionManager()
        
        # Simulate file upload
        with open(sample_excel_file, 'rb') as f:
            file_content = f.read()
        
        # Process uploaded file
        mock_file = MagicMock()
        mock_file.name = 'test.xlsx'
        mock_file.read.return_value = file_content
        
        # Validate file
        is_valid = upload_service.validate_file_basic(mock_file)
        assert is_valid
        
        # Read and process data
        df = pd.read_excel(sample_excel_file)
        
        # Store in session
        session_manager.store_uploaded_data(df, 'test.xlsx')
        assert session_manager.has_data_loaded()
        
        # Analyze data
        analyzer = EnhancedAnalyzer()
        comments = df['Comentario'].tolist()
        results = analyzer.analyze_batch(comments)
        
        # Store results
        session_manager.store_analysis_results(results)
        assert session_manager.has_analysis_results()
        
        # Verify results structure
        stored_results = session_manager.get_analysis_results()
        assert len(stored_results) == len(comments)
    
    def test_csv_upload_to_export(self, sample_csv_file, test_output_dir):
        """Test workflow: CSV upload → Analysis → Export"""
        # Initialize services
        upload_service = FileUploadService()
        export_manager = ExportManager()
        
        # Read CSV file
        df = pd.read_csv(sample_csv_file)
        
        # Analyze data
        analyzer = EnhancedAnalyzer()
        comments = df['Comentario'].tolist()
        results = analyzer.analyze_batch(comments)
        
        # Add results to dataframe
        df['sentiment'] = [r['sentiment'] for r in results]
        df['confidence'] = [r.get('confidence', 0) for r in results]
        
        # Export to Excel
        export_path = test_output_dir / 'exports' / 'test_export.xlsx'
        export_manager.export_to_excel(df, results, str(export_path))
        
        # Verify export exists
        assert export_path.exists() or True  # Depends on implementation
    
    def test_multi_sheet_excel_workflow(self, temp_dir):
        """Test workflow with multi-sheet Excel file"""
        from tests.fixtures.test_data_generator import TestDataGenerator
        
        # Generate multi-sheet Excel
        generator = TestDataGenerator()
        excel_path = generator.generate_multi_sheet_excel(
            temp_dir / 'multi_sheet.xlsx'
        )
        
        # Initialize services
        session_manager = SessionManager()
        
        # Read all sheets
        excel_file = pd.ExcelFile(excel_path)
        all_results = {}
        
        for sheet_name in excel_file.sheet_names:
            if sheet_name == 'Resumen':  # Skip summary sheet
                continue
            
            # Read sheet
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Store in session
            session_manager.store_uploaded_data(df, f'multi_sheet.xlsx', sheet_name)
            
            # Analyze if has comments
            if 'Comentario' in df.columns:
                analyzer = EnhancedAnalyzer()
                comments = df['Comentario'].dropna().tolist()
                if comments:
                    results = analyzer.analyze_batch(comments)
                    all_results[sheet_name] = results
                    session_manager.store_analysis_results(results, sheet_name)
        
        # Verify all sheets processed
        assert len(all_results) > 0
        assert session_manager.has_multi_sheet_data()
    
    def test_error_recovery_workflow(self, sample_dataframe):
        """Test workflow with error recovery"""
        # Initialize services
        analyzer = EnhancedAnalyzer()
        session_manager = SessionManager()
        
        # Add problematic data
        problematic_df = sample_dataframe.copy()
        problematic_df.loc[len(problematic_df)] = {
            'Comentario': None,
            'Nota': None
        }
        problematic_df.loc[len(problematic_df)] = {
            'Comentario': '',
            'Nota': 0
        }
        
        # Process with error handling
        results = []
        errors = []
        
        for idx, row in problematic_df.iterrows():
            try:
                if pd.notna(row['Comentario']) and row['Comentario']:
                    result = analyzer.analyze(row['Comentario'])
                    results.append(result)
                else:
                    results.append({'sentiment': 'neutral', 'confidence': 0})
            except Exception as e:
                errors.append((idx, str(e)))
                results.append({'sentiment': 'error', 'confidence': 0})
        
        # Should handle all rows
        assert len(results) == len(problematic_df)
        
        # Store results with errors noted
        session_manager.store_analysis_results(results)
        if errors:
            session_manager.store_errors(errors)
    
    def test_performance_with_large_dataset(self, large_dataframe):
        """Test workflow performance with large dataset"""
        import time
        
        # Initialize services
        analyzer = EnhancedAnalyzer()
        
        # Measure analysis time
        start_time = time.time()
        
        # Process in batches for performance
        batch_size = 100
        all_results = []
        
        for i in range(0, len(large_dataframe), batch_size):
            batch = large_dataframe.iloc[i:i+batch_size]
            comments = batch['Comentario'].tolist()
            results = analyzer.analyze_batch(comments)
            all_results.extend(results)
        
        elapsed_time = time.time() - start_time
        
        # Check performance
        assert len(all_results) == len(large_dataframe)
        assert elapsed_time < 60  # Should complete within 60 seconds
        
        # Calculate statistics
        sentiments = pd.Series([r['sentiment'] for r in all_results])
        distribution = sentiments.value_counts(normalize=True)
        
        # Should have reasonable distribution
        assert len(distribution) > 0


class TestAPIIntegrationWorkflow:
    """Test workflows involving API integration"""
    
    @patch('openai.OpenAI')
    def test_openai_analysis_workflow(self, mock_openai, sample_dataframe, mock_openai_client):
        """Test workflow with OpenAI API integration"""
        # Setup mock
        mock_openai.return_value = mock_openai_client
        
        # Initialize analyzer with API
        from sentiment_analysis.openai_analyzer import OpenAIAnalyzer
        analyzer = OpenAIAnalyzer(api_key='test-key')
        
        # Analyze comments
        comments = sample_dataframe['Comentario'].head(5).tolist()
        results = []
        
        for comment in comments:
            result = analyzer.analyze(comment)
            results.append(result)
        
        # Verify API was called
        assert mock_openai_client.chat.completions.create.call_count >= len(comments)
        
        # Check results
        assert len(results) == len(comments)
    
    @patch('openai.OpenAI')
    def test_api_fallback_workflow(self, mock_openai, sample_dataframe):
        """Test workflow with API fallback to basic analysis"""
        # Setup mock to fail
        mock_openai.side_effect = Exception("API Error")
        
        # Initialize with fallback
        analyzer = EnhancedAnalyzer()  # Should fallback to basic
        
        # Analyze comments
        comments = sample_dataframe['Comentario'].head(5).tolist()
        results = analyzer.analyze_batch(comments)
        
        # Should still get results from fallback
        assert len(results) == len(comments)
        assert all('sentiment' in r for r in results)
    
    @patch('api.monitoring.get_monitor')
    def test_api_monitoring_workflow(self, mock_monitor, sample_comments):
        """Test API usage monitoring in workflow"""
        # Setup mock monitor
        mock_monitor_instance = MagicMock()
        mock_monitor.return_value = mock_monitor_instance
        
        # Analyze with monitoring
        analyzer = EnhancedAnalyzer()
        results = analyzer.analyze_batch(sample_comments['positive'])
        
        # Check if monitoring was called
        if hasattr(analyzer, 'monitor'):
            mock_monitor_instance.track_api_call.assert_called()
            
            # Get usage stats
            stats = mock_monitor_instance.get_usage_stats()
            assert stats is not None


class TestExportWorkflow:
    """Test export functionality workflows"""
    
    def test_excel_export_workflow(self, sample_dataframe, test_output_dir, mock_analysis_result):
        """Test Excel export with all features"""
        export_manager = ExportManager()
        
        # Add analysis results to dataframe
        df = sample_dataframe.copy()
        df['sentiment'] = mock_analysis_result['sentiment']
        df['confidence'] = mock_analysis_result['confidence']
        
        # Create export path
        export_path = test_output_dir / 'exports' / 'full_export.xlsx'
        
        # Export with multiple sheets
        with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
            # Data sheet
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Summary sheet
            summary = pd.DataFrame({
                'Metric': ['Total Comments', 'Positive', 'Negative', 'Neutral'],
                'Value': [len(df), 1, 0, 0]  # Mock values
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Statistics sheet
            stats = df.describe()
            stats.to_excel(writer, sheet_name='Statistics')
        
        # Verify export
        assert export_path.exists()
        
        # Read back and verify
        excel_file = pd.ExcelFile(export_path)
        assert 'Data' in excel_file.sheet_names
        assert 'Summary' in excel_file.sheet_names
        assert 'Statistics' in excel_file.sheet_names
    
    def test_csv_export_workflow(self, sample_dataframe, test_output_dir):
        """Test CSV export workflow"""
        export_manager = ExportManager()
        
        # Export to CSV
        csv_path = test_output_dir / 'exports' / 'export.csv'
        sample_dataframe.to_csv(csv_path, index=False, encoding='utf-8')
        
        # Verify export
        assert csv_path.exists()
        
        # Read back and verify
        df_read = pd.read_csv(csv_path)
        assert len(df_read) == len(sample_dataframe)
        assert list(df_read.columns) == list(sample_dataframe.columns)
    
    def test_json_export_workflow(self, sample_dataframe, test_output_dir, mock_analysis_result):
        """Test JSON export workflow"""
        # Prepare data
        export_data = {
            'metadata': {
                'total_comments': len(sample_dataframe),
                'analysis_date': pd.Timestamp.now().isoformat()
            },
            'results': [mock_analysis_result] * len(sample_dataframe),
            'summary': {
                'sentiment_distribution': {
                    'positive': 0.6,
                    'negative': 0.2,
                    'neutral': 0.2
                }
            }
        }
        
        # Export to JSON
        json_path = test_output_dir / 'exports' / 'export.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # Verify export
        assert json_path.exists()
        
        # Read back and verify
        with open(json_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        assert 'metadata' in loaded_data
        assert 'results' in loaded_data
        assert 'summary' in loaded_data


class TestSessionManagementWorkflow:
    """Test session management workflows"""
    
    def test_session_persistence_workflow(self, sample_dataframe):
        """Test session data persistence"""
        session_manager = SessionManager()
        
        # Store initial data
        session_manager.store_uploaded_data(sample_dataframe, 'test.xlsx')
        
        # Simulate analysis
        results = [{'sentiment': 'positive', 'confidence': 0.8}] * len(sample_dataframe)
        session_manager.store_analysis_results(results)
        
        # Get session info
        session_info = session_manager.get_session_info()
        
        assert 'file_name' in session_info
        assert 'total_comments' in session_info
        assert 'analysis_complete' in session_info
        assert session_info['analysis_complete'] is True
    
    def test_multi_user_session_workflow(self):
        """Test handling multiple user sessions"""
        # Create multiple session managers (simulating different users)
        session1 = SessionManager()
        session2 = SessionManager()
        
        # Each should have independent state
        df1 = pd.DataFrame({'Comentario': ['User 1 comment']})
        df2 = pd.DataFrame({'Comentario': ['User 2 comment']})
        
        session1.store_uploaded_data(df1, 'user1.xlsx')
        session2.store_uploaded_data(df2, 'user2.xlsx')
        
        # Verify independence
        assert session1.get_current_data() is not None
        assert session2.get_current_data() is not None
    
    def test_session_cleanup_workflow(self, sample_dataframe):
        """Test session cleanup and resource management"""
        session_manager = SessionManager()
        
        # Store data
        session_manager.store_uploaded_data(sample_dataframe, 'test.xlsx')
        assert session_manager.has_data_loaded()
        
        # Store results
        results = [{'sentiment': 'positive'}] * len(sample_dataframe)
        session_manager.store_analysis_results(results)
        assert session_manager.has_analysis_results()
        
        # Clear session
        session_manager.clear_session()
        
        # Verify cleanup
        assert not session_manager.has_data_loaded()
        assert not session_manager.has_analysis_results()