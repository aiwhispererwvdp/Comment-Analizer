"""
File Upload UI Components for Personal Paraguay Comments Analysis Platform
Handles UI rendering for file upload functionality
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple

from theme import theme
from services.file_upload_service import FileUploadService
from services.session_manager import SessionManager
from data_processing.comment_reader import CommentReader
from utils.exceptions import ErrorHandler, FileProcessingError


class FileUploadUI:
    """UI component for file upload interface"""

    def __init__(self):
        self.file_service = FileUploadService()
        self.session_manager = SessionManager()

    def render_upload_interface(self):
        """Render the main file upload interface"""
        # Use full width for upload section
        self._render_upload_section()

    def _render_upload_section(self):
        """Render the enhanced upload section with better visual hierarchy"""
        st.markdown(
            theme.get_component_html(
                "enhanced_card",
                "Data Upload & Processing",
                "Upload your customer comment files for AI-powered sentiment analysis. Supports Excel files with multiple sheets, CSV files, and other formats.",
                icon="📤"
            ),
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a file with customer comments",
            type=["xlsx", "csv", "json", "txt"],
            help="Supported formats: Excel (.xlsx), CSV (.csv), JSON (.json), Text (.txt)",
            label_visibility="collapsed",
        )

        if uploaded_file:
            self._handle_uploaded_file(uploaded_file)

    # Format info removed - now integrated into help text of file uploader

    def _handle_uploaded_file(self, uploaded_file):
        """Handle uploaded file processing"""
        # Basic validation and metadata extraction
        is_valid, error_msg, metadata = self.file_service.validate_file_basic(
            uploaded_file
        )

        if not is_valid:
            st.error(f"❌ **File validation failed:** {error_msg}")
            return

        # Display real-time validation feedback
        self._render_validation_feedback(metadata)

        # Process file if validation passes
        if metadata["size_mb"] <= 50 and metadata["extension"] in [
            ".xlsx",
            ".csv",
            ".json",
            ".txt",
        ]:
            self._process_and_display_file(uploaded_file, metadata)
        else:
            self._render_validation_errors(metadata)

    def _render_validation_feedback(self, metadata: Dict):
        """Render real-time validation feedback"""
        validation_data = self.file_service.get_validation_display_data(metadata)

        # Validation status indicators
        validation_col1, validation_col2, validation_col3 = st.columns(3)

        with validation_col1:
            if validation_data["size_status"] == "success":
                st.success(f"{validation_data['size_message']}")
            else:
                st.error(f"{validation_data['size_message']}")

        with validation_col2:
            if validation_data["format_status"] == "success":
                st.success(f"{validation_data['format_message']}")
            else:
                st.error(f"{validation_data['format_message']}")

        with validation_col3:
            st.info(f"{validation_data['rows_estimate']}")

    def _process_and_display_file(self, uploaded_file, metadata: Dict):
        """Process file and display results"""
        st.divider()

        with st.spinner("Processing file..."):
            success, message, comments_df, processing_info = (
                self.file_service.process_uploaded_file(uploaded_file)
            )

            if not success:
                st.error(f"❌ **Processing failed:** {message}")
                return

            # Display success message
            st.markdown(
                theme.get_component_html(
                    "success_alert",
                    "File Processed Successfully!",
                    "Your data has been validated and is ready for analysis.",
                ),
                unsafe_allow_html=True,
            )

            # Handle Excel sheet selection if needed
            if processing_info.get("requires_sheet_selection", False):
                selected_sheet = self._handle_excel_sheet_selection(processing_info)
                if selected_sheet != processing_info["current_sheet"]:
                    # Reload data with selected sheet
                    success, message, comments_df = (
                        self.file_service.process_excel_sheet(
                            processing_info["temp_path"], selected_sheet
                        )
                    )
                    if success:
                        processing_info["current_sheet"] = selected_sheet

            # Display data metrics and preview
            self._render_data_overview(comments_df, uploaded_file, processing_info)

            # Store data in session
            # Always use _create_data_info to ensure consistent structure
            data_info = self._create_data_info(comments_df)

            self.session_manager.store_uploaded_data(
                comments_df, data_info, processing_info
            )

            st.info(
                "Data loaded successfully! Go to 'Analysis Dashboard' to start analyzing."
            )

    def _handle_excel_sheet_selection(self, processing_info: Dict) -> str:
        """Handle Excel sheet selection interface"""
        st.info(f"Excel file contains {len(processing_info['sheets'])} sheets")

        selected_sheet = st.selectbox(
            "Select sheet to analyze:",
            processing_info["sheets"],
            index=processing_info["sheets"].index(processing_info["current_sheet"]),
        )

        return selected_sheet

    def _render_data_overview(
        self, comments_df: pd.DataFrame, uploaded_file, processing_info: Dict
    ):
        """Render data overview and metrics"""
        # Enhanced metrics display
        st.markdown("### Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)

        total_comments = len(comments_df)
        avg_length = (
            int(comments_df["comment"].str.len().mean())
            if "comment" in comments_df.columns
            else 0
        )

        with col1:
            st.markdown(
                theme.get_component_html(
                    "metric_card",
                    "Total Comments",
                    "Count of all comments in dataset",
                    value=str(total_comments),
                    subtitle="Total Comments",
                ),
                unsafe_allow_html=True,
            )

        with col2:
            sources_count = 1  # Default for single file
            st.markdown(
                theme.get_component_html(
                    "metric_card",
                    "Data Sources",
                    "Number of data sources loaded",
                    value=str(sources_count),
                    subtitle="Data Sources",
                ),
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                theme.get_component_html(
                    "metric_card",
                    "File Size",
                    "Size of uploaded file in kilobytes",
                    value=f"{uploaded_file.size // 1024} KB",
                    subtitle="File Size",
                ),
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                theme.get_component_html(
                    "metric_card",
                    "Average Length",
                    "Average character count per comment",
                    value=str(avg_length),
                    subtitle="Avg Comment Length",
                ),
                unsafe_allow_html=True,
            )

        # Enhanced data preview
        self._render_data_preview(comments_df)

    def _render_data_preview(self, comments_df: pd.DataFrame):
        """Render full-width data preview"""
        st.markdown("### 👀 Data Preview")

        # Full-width data preview without columns
        st.markdown(
            theme.get_component_html(
                "info_card",
                "Sample Data",
                f"Preview of your uploaded dataset - Showing first 10 of {len(comments_df):,} total rows",
            ),
            unsafe_allow_html=True,
        )
        
        # Use full container width for the preview
        st.dataframe(comments_df.head(10), use_container_width=True, height=400)

    def _render_validation_errors(self, metadata: Dict):
        """Render validation errors with helpful guidance"""
        st.error(
            "❌ **File validation failed** - Please fix the issues above before proceeding"
        )

        if metadata["size_mb"] > 50:
            st.warning(
                "**File too large:** Consider reducing the dataset size or splitting into smaller files"
            )
        if metadata["extension"] not in [".xlsx", ".csv", ".json", ".txt"]:
            st.warning(
                f"**Unsupported format:** Please convert your {metadata['extension']} file to Excel (.xlsx) or CSV (.csv)"
            )

    def _create_data_info(self, comments_df: pd.DataFrame) -> Dict:
        """Create data info dictionary for datasets without CommentReader info"""
        return {
            "total_comments": len(comments_df),
            "sources": ["uploaded_file"],
            "columns": list(comments_df.columns),
        }

    def render_sample_dataset_section(self):
        """Render sample dataset loading section"""
        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                theme.get_component_html(
                    "info_card",
                    "Load Sample Dataset",
                    "Try the platform with our pre-loaded Personal Paraguay customer comments dataset. This includes real telecommunications customer feedback data for demonstration purposes.",
                ),
                unsafe_allow_html=True,
            )

        # Handle button click - Enhanced CTA Button
        st.markdown(
            theme.get_component_html(
                "cta_button",
                "Load Personal Paraguay Dataset",
                "",
                action="primary",
                size="large"
            ),
            unsafe_allow_html=True,
        )
        
        if st.button(
            "Load Dataset",
            type="primary",
            use_container_width=True,
            key="load_dataset_action"
        ):
            self._load_sample_dataset()

    def _load_sample_dataset(self):
        """Load the sample dataset"""
        try:
            dataset_path = Path(
                "Personal_Paraguay_Fiber_To_The_Home_Customer_Comments_Dataset.xlsx"
            )
            if dataset_path.exists():
                reader = CommentReader()
                comments_df = reader.read_file(dataset_path)
                data_info = reader.get_data_info()

                # Create processing info for sample dataset
                processing_info = {
                    "temp_path": str(dataset_path),
                    "file_extension": ".xlsx",
                    "is_excel": True,
                    "is_multi_sheet": False,
                    "requires_sheet_selection": False,
                }

                self.session_manager.store_uploaded_data(
                    comments_df, data_info, processing_info
                )
                st.success("Personal Paraguay dataset loaded successfully!")
                st.rerun()
            else:
                st.warning("Personal Paraguay dataset not found in project directory.")
        except Exception as e:
            ErrorHandler.handle_streamlit_error(e, "Failed to load dataset")
