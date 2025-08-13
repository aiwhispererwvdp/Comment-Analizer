"""
Responsive File Upload UI Component
Mobile-first design with adaptive layouts
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

from utils.responsive_utils import ResponsiveUI, ResponsiveCards
from services.file_upload_service import FileUploadService
from services.session_manager import SessionManager
from data_processing.comment_reader import CommentReader
from utils.exceptions import ErrorHandler


class ResponsiveFileUploadUI:
    """Responsive file upload interface"""
    
    def __init__(self):
        self.file_service = FileUploadService()
        self.session_manager = SessionManager()
    
    def render(self):
        """Render responsive upload interface"""
        screen = ResponsiveUI.estimate_screen_size()
        
        # Progress tracker
        self._render_progress_tracker()
        
        # Main upload section
        self._render_upload_section(screen)
        
        # Data preview if available
        if "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
            self._render_data_preview(screen)
    
    def _render_progress_tracker(self):
        """Render responsive progress tracker"""
        steps = ["Upload", "Validate", "Preview", "Analyze"]
        current = st.session_state.get("upload_step", 0)
        
        # Use responsive columns
        cols = ResponsiveUI.responsive_columns('metrics')
        
        for idx, (col, step) in enumerate(zip(cols[:len(steps)], steps)):
            with col:
                if idx <= current:
                    st.success(f"✓ {step}")
                else:
                    st.info(f"{idx+1}. {step}")
    
    def _render_upload_section(self, screen: str):
        """Render upload section with responsive layout"""
        st.markdown("### 📤 Upload Your Data")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["xlsx", "csv", "json", "txt"],
            help="Excel, CSV, JSON or Text files (max 50MB)",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            self._handle_file_upload(uploaded_file, screen)
        else:
            # Sample data option
            with st.expander("💡 Try with sample data"):
                st.write("Load our Personal Paraguay telecommunications dataset")
                if st.button("Load Sample Dataset", type="primary", use_container_width=True):
                    self._load_sample_data()
    
    def _handle_file_upload(self, uploaded_file, screen: str):
        """Handle file upload with responsive feedback"""
        # Validate
        is_valid, error_msg, metadata = self.file_service.validate_file_basic(uploaded_file)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        # Show validation status
        if screen == 'mobile':
            # Stack vertically on mobile
            st.success(f"✓ Format: {metadata['extension'].upper()}")
            st.success(f"✓ Size: {metadata['size_mb']:.1f}MB")
            st.info(f"Rows: ~{metadata.get('rows_estimate', 'Unknown')}")
        else:
            # Horizontal layout for larger screens
            cols = st.columns(3)
            with cols[0]:
                st.success(f"✓ {metadata['extension'].upper()}")
            with cols[1]:
                st.success(f"✓ {metadata['size_mb']:.1f}MB")
            with cols[2]:
                st.info(f"~{metadata.get('rows_estimate', 'Unknown')} rows")
        
        # Process file
        with st.spinner("Processing..."):
            success, message, comments_df, processing_info = self.file_service.process_uploaded_file(uploaded_file)
            
            if not success:
                st.error(f"Failed: {message}")
                return
            
            # Handle Excel sheets
            if processing_info.get("requires_sheet_selection"):
                sheet = st.selectbox("Select sheet:", processing_info["sheets"])
                if sheet != processing_info.get("current_sheet"):
                    success, message, comments_df = self.file_service.process_excel_sheet(
                        processing_info["temp_path"], sheet
                    )
            
            # Store data
            st.session_state.uploaded_data = comments_df
            st.session_state.upload_step = 3
            
            # Success message
            st.success(f"✅ Loaded {len(comments_df):,} comments successfully!")
            
            # Store in session manager
            data_info = {
                "total_comments": len(comments_df),
                "sources": ["uploaded_file"],
                "columns": list(comments_df.columns)
            }
            self.session_manager.store_uploaded_data(comments_df, data_info, processing_info)
    
    def _render_data_preview(self, screen: str):
        """Render responsive data preview"""
        df = st.session_state.uploaded_data
        
        st.markdown("---")
        st.markdown("### 👀 Data Preview")
        
        # Responsive metrics
        metrics = [
            ("Total Comments", f"{len(df):,}", None),
            ("Columns", len(df.columns), None),
            ("Avg Length", f"{int(df['comment'].str.len().mean()) if 'comment' in df.columns else 0} chars", None),
            ("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB", None)
        ]
        
        ResponsiveUI.responsive_metrics(metrics)
        
        # Control row
        col1, col2 = st.columns([3, 1]) if screen != 'mobile' else (st.container(), st.container())
        
        with col1:
            preview_rows = st.slider(
                "Rows to display:",
                5, 
                min(100, len(df)),
                min(20 if screen == 'desktop' else 10, len(df))
            )
        
        with col2:
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                st.session_state.selected_page = "Analysis Dashboard"
                st.rerun()
        
        # Responsive dataframe display
        if screen == 'mobile':
            # Show fewer columns on mobile
            essential_cols = ['comment'] if 'comment' in df.columns else df.columns[:2]
            display_df = df[essential_cols].head(preview_rows)
            height = 300
        elif screen == 'tablet':
            # Show more columns on tablet
            cols_to_show = min(4, len(df.columns))
            display_df = df.iloc[:preview_rows, :cols_to_show]
            height = 400
        else:
            # Show all on desktop
            display_df = df.head(preview_rows)
            height = 500
        
        st.dataframe(display_df, use_container_width=True, height=height)
        
        # Data info
        st.info(f"Showing {len(display_df)} of {len(df):,} rows • {len(display_df.columns)} of {len(df.columns)} columns")
    
    def _load_sample_data(self):
        """Load sample dataset"""
        try:
            path = Path("Personal_Paraguay_Fiber_To_The_Home_Customer_Comments_Dataset.xlsx")
            if path.exists():
                reader = CommentReader()
                df = reader.read_file(path)
                st.session_state.uploaded_data = df
                st.session_state.upload_step = 3
                st.success("✅ Sample dataset loaded!")
                st.rerun()
            else:
                st.warning("Sample dataset not found")
        except Exception as e:
            st.error(f"Error: {str(e)}")