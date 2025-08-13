"""
Analysis Dashboard UI Components for Personal Paraguay Comments Analysis Platform
Handles UI rendering for the analysis dashboard functionality
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional, List

from theme import theme
from services.session_manager import SessionManager
from services.analysis_service import AnalysisService
from data_processing.comment_reader import CommentReader
from sentiment_analysis.openai_analyzer import OpenAIAnalyzer
from utils.exceptions import (
    ErrorHandler,
    ConfigurationError,
    APIConnectionError,
    AnalysisProcessingError,
)
from utils.validators import InputValidator, SecurityLogger
from config import validate_config


class AnalysisDashboardUI:
    """UI component for analysis dashboard interface"""

    def __init__(self):
        self.session_manager = SessionManager()
        self.analysis_service = AnalysisService()

    def render_dashboard(self):
        """Render the complete analysis dashboard with professional sections"""
        # Main dashboard header with professional styling
        st.markdown(
            theme.get_component_html(
                "header",
                "Analysis Dashboard",
                "Comprehensive analytics and insights for customer feedback",
                subtitle="Real-time sentiment analysis powered by advanced AI"
            ),
            unsafe_allow_html=True,
        )

        # Check if data is loaded
        if not self.session_manager.has_data_loaded():
            st.warning(
                "No data loaded. Please upload data first in the 'Data Upload' section."
            )
            return

        current_data = self.session_manager.get_current_data()
        comments_df = current_data["comments_data"]
        data_info = current_data.get("data_info", {})
        
        # Debug: Log data_info structure
        if not isinstance(data_info, dict):
            st.warning(f"Debug: data_info is not a dict, it's {type(data_info)}. Value: {data_info}")
            data_info = {}
        elif data_info is None:
            st.warning("Debug: data_info is None")
            data_info = {}

        # Check API configuration
        api_configured = self._check_api_configuration()

        # Create professional sections with tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "🤖 AI Analysis", 
            "📈 Statistics",
            "📁 Data Management"
        ])
        
        with tab1:
            self._render_overview_section(data_info, comments_df, api_configured)
            
        with tab2:
            self._render_ai_analysis_section(comments_df, api_configured)
            
        with tab3:
            self._render_statistics_section(comments_df)
            
        with tab4:
            self._render_data_management_section(current_data)

    def _check_api_configuration(self) -> bool:
        """Check if API is properly configured"""
        try:
            validate_config()
            return True
        except ValueError as e:
            ErrorHandler.handle_streamlit_error(
                ConfigurationError(str(e), "OPENAI_API_KEY"),
                "OpenAI API key not configured. Please set up API key in Settings.",
            )
            return False

    def _render_overview_section(self, data_info: Dict, comments_df: pd.DataFrame, api_configured: bool):
        """Render comprehensive overview section with key metrics and status"""
        # Section header
        st.markdown("### 📊 Data Overview")
        st.markdown("Key metrics and insights from your dataset")
        
        # Ensure data_info is not None
        if data_info is None:
            data_info = {}
        
        # Primary metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Get total comments from data_info or calculate from DataFrame
            try:
                total_comments = data_info.get('total_comments', len(comments_df))
            except (KeyError, TypeError, AttributeError):
                total_comments = len(comments_df)
            
            st.metric(
                "Total Comments", 
                f"{total_comments:,}",
                help="Total number of comments in the dataset"
            )

        with col2:
            # Get sources safely with default
            sources = data_info.get("sources", [])
            st.metric(
                "Data Sources", 
                len(sources),
                help="Number of data files loaded"
            )

        with col3:
            if self.session_manager.has_analysis_results():
                insights = self.session_manager.get_analysis_results()["insights"] or {}
                guarani_pct = insights.get("guarani_percentage", 0)
                st.metric(
                    "Guarani Content", 
                    f"{guarani_pct}%",
                    help="Percentage of comments containing Guarani language"
                )
            else:
                st.metric(
                    "Analysis Status", 
                    "Ready" if api_configured else "Setup Required",
                    help="Current system status"
                )
                
        with col4:
            # Calculate average comment length
            if len(comments_df) > 0 and 'comment' in comments_df.columns:
                avg_length = comments_df['comment'].astype(str).str.len().mean()
                st.metric(
                    "Avg Length",
                    f"{avg_length:.0f} chars",
                    help="Average comment length in characters"
                )
            else:
                st.metric("Data Quality", "Valid")
        
        # Data quality indicators
        st.markdown("---")
        st.markdown("### 🔍 Data Quality Indicators")
        
        quality_col1, quality_col2, quality_col3 = st.columns(3)
        
        with quality_col1:
            # Check for empty comments
            if 'comment' in comments_df.columns:
                empty_count = comments_df['comment'].isna().sum() + (comments_df['comment'].astype(str).str.strip() == '').sum()
                quality_score = 100 - (empty_count / len(comments_df) * 100) if len(comments_df) > 0 else 0
                st.metric(
                    "Data Completeness",
                    f"{quality_score:.1f}%",
                    help="Percentage of non-empty comments"
                )
            
        with quality_col2:
            # Show analysis readiness
            if api_configured:
                st.metric(
                    "AI Analysis",
                    "✅ Ready",
                    help="OpenAI API configured and ready"
                )
            else:
                st.metric(
                    "AI Analysis",
                    "⚠️ Setup Required",
                    help="Configure API key in Settings"
                )
                
        with quality_col3:
            # Show last update time
            if 'uploaded_at' in st.session_state:
                st.metric(
                    "Last Updated",
                    st.session_state['uploaded_at'],
                    help="When data was last uploaded"
                )
            else:
                st.metric(
                    "Session Status",
                    "Active",
                    help="Current session is active"
                )
                
        # Quick insights if analysis available
        if self.session_manager.has_analysis_results():
            st.markdown("---")
            st.markdown("### 💡 Quick Insights")
            
            results = self.session_manager.get_analysis_results()
            if results and results.get("summary"):
                summary = results["summary"]
                
                insight_cols = st.columns(3)
                
                with insight_cols[0]:
                    if "sentiment_distribution" in summary:
                        dist = summary["sentiment_distribution"]
                        dominant = max(dist, key=dist.get)
                        st.info(f"**Dominant Sentiment:** {dominant.title()} ({dist[dominant]:.1f}%)")
                        
                with insight_cols[1]:
                    if "top_themes" in summary and summary["top_themes"]:
                        top_theme = list(summary["top_themes"].keys())[0]
                        st.info(f"**Top Theme:** {top_theme}")
                        
                with insight_cols[2]:
                    if "analyzed_count" in summary:
                        st.info(f"**Analyzed:** {summary['analyzed_count']} comments")

    def _render_sheet_selection_section(self, current_data: Dict):
        """Render Excel sheet selection section if applicable"""
        if not current_data["is_multi_sheet"]:
            return

        st.markdown("---")
        st.subheader("Excel Sheet Selection")

        available_sheets = current_data["excel_sheets"]
        current_sheet = current_data["current_sheet"]

        col1, col2 = st.columns([2, 1])

        with col1:
            selected_sheet = st.selectbox(
                "Select sheet to analyze:",
                available_sheets,
                index=(
                    available_sheets.index(current_sheet)
                    if current_sheet in available_sheets
                    else 0
                ),
                key="sheet_selector",
            )

        with col2:
            # Enhanced sheet switch button
            st.markdown(
                theme.get_component_html(
                    "cta_button",
                    "Switch Sheet",
                    "",
                    action="secondary",
                    size="normal"
                ),
                unsafe_allow_html=True,
            )
            
            if st.button("Switch Sheet Action", type="primary", key="switch_sheet_action"):
                if selected_sheet != current_sheet:
                    self._handle_sheet_switch(selected_sheet)

        # Show current sheet info
        comments_df = current_data["comments_data"]
        st.info(f"Currently viewing: **{current_sheet}** ({len(comments_df)} comments)")

        # Show analysis status for each sheet
        self._render_sheet_analysis_status(available_sheets)

    def _handle_sheet_switch(self, selected_sheet: str):
        """Handle switching to a different Excel sheet"""
        try:
            # Use session manager to handle the switch
            success = self.session_manager.switch_excel_sheet(selected_sheet)

            if success:
                # Check if we need to reload data from file
                current_data = self.session_manager.get_current_data()
                temp_path = st.session_state.get("uploaded_file_path", "")

                if temp_path and Path(temp_path).exists():
                    reader = CommentReader()
                    new_comments_df = reader.read_excel_sheet(
                        Path(temp_path), selected_sheet
                    )

                    # Update session state with new data
                    data_info = reader.get_data_info()
                    processing_info = {
                        "temp_path": temp_path,
                        "file_extension": ".xlsx",
                        "is_multi_sheet": True,
                        "current_sheet": selected_sheet,
                        "sheets": current_data["excel_sheets"],
                    }

                    self.session_manager.store_uploaded_data(
                        new_comments_df, data_info, processing_info
                    )

                    st.success(f"Switched to sheet: {selected_sheet}")
                    st.rerun()
                else:
                    st.error("Original file not found. Please upload the file again.")
            else:
                st.error("Failed to switch sheets.")

        except Exception as e:
            ErrorHandler.handle_streamlit_error(e, "Failed to switch sheets")

    def _render_sheet_analysis_status(self, available_sheets: List[str]):
        """Render analysis status for all sheets"""
        with st.expander("Analysis Status by Sheet"):
            sheet_status = self.session_manager.get_sheet_analysis_status()

            for sheet in available_sheets:
                if sheet_status.get(sheet, False):
                    # Get analysis count for this sheet
                    sheet_results = self.session_manager.get_analysis_results(sheet)
                    analysis_count = (
                        len(sheet_results["results"]) if sheet_results["results"] else 0
                    )
                    st.success(f"{sheet}: {analysis_count} comments analyzed")
                else:
                    st.info(f"{sheet}: Not analyzed yet")

    def _render_ai_analysis_section(
        self, comments_df: pd.DataFrame, api_configured: bool
    ):
        """Render AI analysis section with organized subsections"""
        st.markdown("### 🤖 AI-Powered Analysis")
        st.markdown("Advanced sentiment analysis and insights using GPT-4")

        if api_configured:
            # Create subsections for better organization
            analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs([
                "Quick Analysis",
                "Batch Processing", 
                "Results & Insights"
            ])
            
            with analysis_tab1:
                st.markdown("#### Quick Comment Analysis")
                st.markdown("Analyze a sample of comments for rapid insights")
                self._render_analysis_controls(comments_df)
                
            with analysis_tab2:
                st.markdown("#### Full Dataset Processing")
                st.markdown("Process your entire dataset with optimized batch analysis")
                self._render_batch_processing_section(comments_df)
                
            with analysis_tab3:
                if self.session_manager.has_analysis_results():
                    self._render_analysis_results()
                else:
                    st.info("No analysis results yet. Run Quick Analysis or Batch Processing to see results.")
        else:
            st.warning("⚠️ **API Configuration Required**")
            st.info("Configure OpenAI API key in Settings to enable AI analysis.")
            
            # Provide quick setup guide
            with st.expander("Quick Setup Guide"):
                st.markdown("""
                1. Navigate to **Settings** in the sidebar
                2. Enter your OpenAI API key
                3. Click **Save Settings**
                4. Return here to start analyzing
                
                Don't have an API key? [Get one from OpenAI](https://platform.openai.com/api-keys)
                """)

    def _render_analysis_controls(self, comments_df: pd.DataFrame):
        """Render analysis controls section"""
        # Full width slider
        total_comments = len(comments_df)
        sample_size = st.slider(
            "Number of comments to analyze:", 
            1, 
            total_comments, 
            min(10, total_comments),
            help=f"Select how many comments to analyze (max: {total_comments:,} comments)"
        )
        
        # Button and progress info below the slider
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🔍 Analyze Comments", type="primary", key="analyze_comments_action", use_container_width=True):
                # Validate analysis parameters
                is_valid_params, param_message = (
                    InputValidator.validate_analysis_parameters(
                        sample_size, len(comments_df)
                    )
                )

                if not is_valid_params:
                    st.error(f"{param_message}")
                    return

                self.analysis_service.analyze_comments_with_ai(comments_df, sample_size)
        
        with col2:
            # Progress info and analysis details
            st.info(f"📊 Will analyze {sample_size:,} of {total_comments:,} comments ({(sample_size/total_comments)*100:.1f}%)")
            
            # Estimated cost and time
            estimated_tokens = sample_size * 100  # Rough estimate
            estimated_cost = (estimated_tokens / 1000) * 0.002  # GPT-4 pricing estimate
            estimated_time = sample_size * 0.5  # Rough time estimate in seconds
            
            if sample_size > 0:
                st.markdown(f"""
                <div style='font-size: 0.8rem; color: #888; margin-top: 4px;'>
                    ⏱️ Est. time: {estimated_time:.0f}s • 💰 Est. cost: ${estimated_cost:.3f}
                </div>
                """, unsafe_allow_html=True)
        
        # Show last analysis status if available
        if 'last_analysis_success' in st.session_state:
            success_info = st.session_state['last_analysis_success']
            import time
            time_ago = int(time.time() - success_info['timestamp'])
            
            if time_ago < 300:  # Show for 5 minutes
                st.success(f"""
                ✅ **Last Analysis Completed Successfully** ({time_ago}s ago)
                - **{success_info['comments_count']} comments** analyzed with **{success_info['analyzer_type']}**
                - **{success_info['insights_count']} themes** and **{success_info['recommendations_count']} recommendations** generated
                - Results available in 'Results & Insights' tab below
                """)
            else:
                # Clean up old success messages
                del st.session_state['last_analysis_success']

    def _render_batch_processing_section(self, comments_df: pd.DataFrame):
        """Render simplified batch processing section - always processes 10 comments in parallel"""
        # Processing overview
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info("**Optimized Processing:** Analyzes 10 comments in parallel for maximum efficiency")
            
        with col2:
            total_comments = len(comments_df)
            st.metric("Dataset Size", f"{total_comments:,} comments")
            
        with col3:
            # Calculate estimated time
            batches = (total_comments + 9) // 10
            est_time = batches * 2  # ~2 seconds per batch
            st.metric("Est. Time", f"~{est_time}s")
        
        # Processing controls
        st.markdown("---")
        process_col1, process_col2 = st.columns([3, 1])
        
        with process_col1:
            st.markdown("""
            **Batch Processing Features:**
            - ✅ Parallel processing of 10 comments simultaneously
            - ✅ Progress tracking with detailed status updates
            - ✅ Automatic retry on API errors
            - ✅ Results saved incrementally
            """)
            
        with process_col2:
            if st.button(
                "🚀 Start Full Analysis", 
                help=f"Process all {total_comments:,} comments", 
                key="process_all", 
                type="primary", 
                use_container_width=True
            ):
                # Always use 10 comments for parallel processing
                self.analysis_service.analyze_all_comments_batch(comments_df, batch_size=10)
                
        # Show processing tips
        with st.expander("Processing Tips"):
            st.markdown("""
            - **Large datasets:** Processing continues even if you navigate away
            - **API limits:** The system automatically handles rate limiting
            - **Cost estimate:** ~$0.01 per 10 comments (GPT-4)
            - **Resume:** If interrupted, you can resume from where it stopped
            """)

    def _render_analysis_results(self):
        """Render analysis results section"""
        from components.analysis_results_ui import AnalysisResultsUI
        
        results_ui = AnalysisResultsUI()
        results_ui.render_results()

    def _render_statistics_section(self, comments_df: pd.DataFrame):
        """Render enhanced basic statistics section with error handling"""
        st.markdown("### 📈 Statistical Analysis")
        st.markdown("Comprehensive statistical overview of your comment dataset")

        # Validate required columns exist
        if 'comment' not in comments_df.columns:
            st.error("❌ **Error:** No 'comment' column found in the dataset. Please check your data format.")
            return
            
        if len(comments_df) == 0:
            st.warning("⚠️ **No data available** for statistical analysis.")
            return

        try:
            # Create a copy to avoid modifying original data
            stats_df = comments_df.copy()
            
            # Safe comment length calculation with error handling
            stats_df["comment_length"] = stats_df["comment"].astype(str).str.len()
            
            # Remove any invalid entries
            stats_df = stats_df[stats_df["comment_length"] > 0]
            
            if len(stats_df) == 0:
                st.warning("⚠️ **No valid comments** found for analysis.")
                return

            # Compact statistics overview (horizontal metrics)
            self._render_enhanced_statistics_overview(stats_df)
            
            # Enhanced length distribution chart (full width)
            self._render_length_distribution(stats_df)
            
        except Exception as e:
            st.error(f"❌ **Statistics Error:** {str(e)}")
            st.info("Please check your data format and try again.")

    def _render_enhanced_statistics_overview(self, stats_df: pd.DataFrame):
        """Render enhanced statistics overview with key metrics in compact layout"""
        # Calculate key statistics
        total_comments = len(stats_df)
        avg_length = stats_df["comment_length"].mean()
        median_length = stats_df["comment_length"].median()
        min_length = stats_df["comment_length"].min()
        max_length = stats_df["comment_length"].max()
        
        # Compact horizontal metrics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Comments",
                value=f"{total_comments:,}",
                help="Total number of comments in dataset"
            )
            
        with col2:
            st.metric(
                label="Avg Length", 
                value=f"{avg_length:.0f}",
                help="Mean character count per comment"
            )
            
        with col3:
            st.metric(
                label="Median Length",
                value=f"{median_length:.0f}",
                help="Median character count per comment"
            )
            
        with col4:
            st.metric(
                label="Range",
                value=f"{min_length}-{max_length}",
                help="Shortest to longest comment length"
            )

    def _render_length_distribution(self, comments_df: pd.DataFrame):
        """Render enhanced interactive comment length distribution chart"""
        st.markdown("### Length Distribution")

        try:
            if len(comments_df) == 0:
                st.warning("No data available for length distribution.")
                return

            # Create smart bins based on data distribution
            max_length = comments_df["comment_length"].max()
            min_length = comments_df["comment_length"].min()
            
            # Define meaningful length categories with better colors
            if max_length <= 50:
                bins = [0, 10, 25, max_length + 1]
                labels = ["Very Short (0-10)", f"Short (11-25)", f"Medium (26-{max_length})"]
                colors = ["#ef4444", "#f97316", "#eab308"]  # Red to amber gradient
            elif max_length <= 200:
                bins = [0, 25, 100, max_length + 1]
                labels = ["Short (0-25)", "Medium (26-100)", f"Long (101-{max_length})"]
                colors = ["#ef4444", "#f97316", "#22c55e"]  # Red to green gradient
            else:
                bins = [0, 50, 200, max_length + 1]
                labels = ["Short (0-50)", "Medium (51-200)", f"Long (201-{max_length})"]
                colors = ["#ef4444", "#eab308", "#22c55e"]  # Red to green spectrum

            # Ensure we have valid bins
            bins = sorted(list(set(bins)))
            if len(bins) < 2:
                st.info("All comments have similar lengths.")
                return

            # Create categories with proper error handling
            try:
                # Create length categories
                length_cats = pd.cut(
                    comments_df["comment_length"],
                    bins=bins,
                    labels=labels[:len(bins)-1],
                    include_lowest=True
                )
                
                # Count comments in each category
                length_counts = length_cats.value_counts().sort_index()

                if len(length_counts) == 0:
                    st.warning("No valid length categories found.")
                    return

                # Create enhanced interactive chart with Plotly
                import plotly.express as px
                import plotly.graph_objects as go
                
                chart_data = pd.DataFrame({
                    "Category": [str(cat) for cat in length_counts.index],
                    "Count": length_counts.values,
                    "Percentage": [(count / len(comments_df)) * 100 for count in length_counts.values]
                })

                # Create enhanced bar chart with custom colors
                fig = px.bar(
                    chart_data, 
                    x="Category", 
                    y="Count",
                    title="Comment Length Distribution",
                    color="Count",
                    color_continuous_scale=["#1e293b", "#4299e1", "#38b2ac"],
                    text="Count",
                    hover_data={"Percentage": ":.1f"}
                )
                
                # Enhance the chart styling
                fig.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    textfont_size=12,
                    marker_line_color='#1e293b',
                    marker_line_width=1
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    title_font_size=16,
                    title_font_color='#ffffff',
                    xaxis=dict(
                        title="Comment Length Categories",
                        title_font_color='#e2e8f0',
                        tickfont_color='#e2e8f0',
                        gridcolor='#4a5568',
                        showgrid=True
                    ),
                    yaxis=dict(
                        title="Number of Comments",
                        title_font_color='#e2e8f0',
                        tickfont_color='#e2e8f0',
                        gridcolor='#4a5568',
                        showgrid=True
                    ),
                    height=350,
                    showlegend=False
                )

                # Display the interactive chart
                st.plotly_chart(fig, use_container_width=True)

                # Enhanced category breakdown with better styling
                st.markdown("### 📊 Category Breakdown")
                
                # Create a styled container for categories
                category_container = st.container()
                with category_container:
                    for idx, (cat, count, pct) in enumerate(zip(chart_data["Category"], chart_data["Count"], chart_data["Percentage"])):
                        # Add spacing between items
                        if idx > 0:
                            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                        
                        # Create a visually appealing layout
                        col1, col2, col3 = st.columns([3, 1.5, 1.5])
                        
                        with col1:
                            # Category name with icon
                            category_icon = "📁" if idx == 0 else "📂" if idx == 1 else "📄"
                            st.markdown(f"""
                            <div style='display: flex; align-items: center;'>
                                <span style='font-size: 1.1em; margin-right: 8px;'>{category_icon}</span>
                                <strong style='font-size: 1.05em;'>{cat}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Comment count with better formatting
                            st.markdown(f"""
                            <div style='text-align: center; padding: 4px; background: rgba(102, 126, 234, 0.1); 
                            border-radius: 6px; border: 1px solid rgba(102, 126, 234, 0.2);'>
                                <strong>{count:,}</strong> comments
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            # Use Streamlit's native progress bar with proper height
                            st.progress(pct/100, text=f"{pct:.1f}%")
                    
                    # Add summary statistics
                    st.markdown("<div style='margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
                    summary_cols = st.columns(3)
                    
                    with summary_cols[0]:
                        st.metric("Total Categories", len(chart_data))
                    with summary_cols[1]:
                        st.metric("Largest Category", chart_data.iloc[0]["Category"])
                    with summary_cols[2]:
                        st.metric("Distribution", f"{chart_data['Percentage'].std():.1f}% std dev")

            except Exception as chart_error:
                st.error(f"Chart creation error: {str(chart_error)}")
                
                # Fallback: enhanced metrics display
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Length", f"{comments_df['comment_length'].mean():.0f} chars")
                with col2:
                    st.metric("Shortest", f"{min_length} chars")
                with col3:
                    st.metric("Longest", f"{max_length} chars")
                
        except Exception as e:
            st.error(f"Length distribution error: {str(e)}")
            st.info("Unable to generate length distribution chart.")

    def _render_data_management_section(self, current_data: Dict):
        """Render data management section with sheet controls and export options"""
        st.markdown("### 📁 Data Management")
        st.markdown("Manage your data sources, sheets, and export options")
        
        # Sheet selection if multi-sheet Excel
        if current_data["is_multi_sheet"]:
            self._render_sheet_selection_section(current_data)
        
        # Data source information
        st.markdown("---")
        st.markdown("### 📄 Current Data Source")
        
        source_col1, source_col2 = st.columns([2, 1])
        
        with source_col1:
            if current_data.get("data_info", {}).get("sources"):
                sources = current_data["data_info"]["sources"]
                for source in sources:
                    st.info(f"**File:** {source}")
            else:
                st.info("**File:** Uploaded data")
                
        with source_col2:
            file_info = current_data.get("processing_info", {})
            if file_info.get("file_extension"):
                st.metric("Format", file_info["file_extension"].upper())
            else:
                st.metric("Format", "CSV/Excel")
                
        # Export options
        st.markdown("---")
        st.markdown("### 💾 Export Options")
        
        export_cols = st.columns(4)
        
        with export_cols[0]:
            if st.button("Export to Excel", key="export_excel_dm", type="secondary", use_container_width=True):
                st.info("Export functionality available in Analysis Results")
                
        with export_cols[1]:
            if st.button("Export to CSV", key="export_csv_dm", type="secondary", use_container_width=True):
                st.info("Export functionality available in Analysis Results")
                
        with export_cols[2]:
            if st.button("Export Report", key="export_report_dm", type="secondary", use_container_width=True):
                st.info("Generate comprehensive report in Analysis Results")
                
        with export_cols[3]:
            if st.button("Clear Data", key="clear_data_dm", type="secondary", use_container_width=True):
                if st.checkbox("Confirm clear all data?"):
                    self.session_manager.clear_session()
                    st.success("Data cleared. Please upload new data.")
                    st.rerun()
                    
        # Session information
        if st.expander("Session Information"):
            st.json({
                "Total Comments": current_data.get("data_info", {}).get("total_comments", 0),
                "Is Multi-Sheet": current_data.get("is_multi_sheet", False),
                "Current Sheet": current_data.get("current_sheet", "N/A"),
                "Available Sheets": current_data.get("excel_sheets", []),
                "Has Analysis Results": self.session_manager.has_analysis_results(),
                "API Configured": self._check_api_configuration()
            })
