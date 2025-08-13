"""
Analysis Results UI Components for Personal Paraguay Comments Analysis Platform
Handles UI rendering for analysis results display and export functionality
"""

import streamlit as st
import pandas as pd
from typing import Dict, List

from theme import theme
from services.session_manager import SessionManager
from visualization.export_manager import ExportManager


class AnalysisResultsUI:
    """UI component for analysis results display"""

    def __init__(self):
        self.session_manager = SessionManager()
        self.export_manager = ExportManager()

    def render_results(self):
        """Render the complete analysis results interface"""
        if not self.session_manager.has_analysis_results():
            st.warning("No analysis results available. Please run analysis first.")
            return

        analysis_data = self.session_manager.get_analysis_results()
        results = analysis_data["results"]
        insights = analysis_data["insights"]
        recommendations = analysis_data["recommendations"]
        analyzed_comments = analysis_data["analyzed_comments"]

        # Render all sections
        self._render_sentiment_overview(results, insights)
        self._render_themes_and_pain_points(insights)
        self._render_recommendations(recommendations)
        self._render_export_section()
        self._render_detailed_results(results, analyzed_comments)

    def _render_sentiment_overview(self, results: List[Dict], insights: Dict):
        """Render sentiment analysis overview"""
        # Build title with sheet info
        title = f"Sentiment Analysis Results (Sample Size: {len(results)} comments)"
        if st.session_state.get("is_multi_sheet", False):
            current_sheet = st.session_state.get("current_sheet", "Unknown")
            title += f" - Sheet: {current_sheet}"

        st.subheader(title)

        # Sentiment metrics
        col1, col2, col3 = st.columns(3)
        sentiment_dist = insights.get("sentiment_percentages", {})

        with col1:
            positive_pct = sentiment_dist.get("positive", 0)
            st.metric("Positive", f"{positive_pct}%", delta=None, delta_color="normal")

        with col2:
            neutral_pct = sentiment_dist.get("neutral", 0)
            st.metric("Neutral", f"{neutral_pct}%")

        with col3:
            negative_pct = sentiment_dist.get("negative", 0)
            st.metric(
                "Negative", f"{negative_pct}%", delta=None, delta_color="inverse"
            )

    def _render_themes_and_pain_points(self, insights: Dict):
        """Render themes and pain points analysis"""
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Themes")
            top_themes = insights.get("top_themes", {})
            if top_themes:
                themes_df = pd.DataFrame(
                    list(top_themes.items()), columns=["Theme", "Count"]
                )
                st.bar_chart(themes_df.set_index("Theme"))
            else:
                st.write("No themes detected")

        with col2:
            st.subheader("Top Pain Points")
            top_pain_points = insights.get("top_pain_points", {})
            if top_pain_points:
                pain_points_df = pd.DataFrame(
                    list(top_pain_points.items()), columns=["Pain Point", "Count"]
                )
                st.bar_chart(pain_points_df.set_index("Pain Point"))
            else:
                st.write("No pain points detected")

    def _render_recommendations(self, recommendations: List[str]):
        """Render AI recommendations"""
        st.subheader("AI Recommendations")
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.info("No specific recommendations generated")

    def _render_export_section(self):
        """Render export options"""
        st.markdown("---")
        st.subheader("Export Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Export Excel", help="Export complete analysis to Excel"):
                self._export_analysis_results("excel")

        with col2:
            if st.button("Export CSV", help="Export detailed results to CSV"):
                self._export_analysis_results("csv")

        with col3:
            if st.button("Summary Report", help="Export executive summary"):
                self._export_analysis_results("summary")

        with col4:
            if st.button("Export JSON", help="Export data for further processing"):
                self._export_analysis_results("json")

        # Show download links if files were exported
        self._render_download_links()

    def _render_download_links(self):
        """Render download links for exported files"""
        if "export_files" in st.session_state and st.session_state["export_files"]:
            st.subheader("Download Files")
            for file_info in st.session_state["export_files"]:
                st.markdown(file_info["link"], unsafe_allow_html=True)

    def _render_detailed_results(self, results: List[Dict], analyzed_comments: List[str]):
        """Render detailed analysis results table"""
        with st.expander("Detailed Analysis Results"):
            if results:
                results_df = pd.DataFrame(results)

                # Add original comments if available
                if analyzed_comments and len(analyzed_comments) == len(results_df):
                    results_df["original_comment"] = analyzed_comments

                st.dataframe(results_df, use_container_width=True)
            else:
                st.info("No detailed results available")

    def _export_analysis_results(self, export_type: str):
        """Export analysis results in specified format"""
        try:
            # Get current analysis data
            analysis_data = self.session_manager.get_analysis_results()
            results = analysis_data["results"]
            insights = analysis_data["insights"]
            recommendations = analysis_data["recommendations"]
            analyzed_comments = analysis_data["analyzed_comments"]

            if not results:
                st.error("No analysis results to export")
                return

            # Prepare export data
            export_data = {
                "results": results,
                "insights": insights,
                "recommendations": recommendations,
                "analyzed_comments": analyzed_comments,
                "metadata": {
                    "total_analyzed": len(results),
                    "export_timestamp": pd.Timestamp.now().isoformat(),
                    "is_multi_sheet": st.session_state.get("is_multi_sheet", False),
                    "current_sheet": st.session_state.get("current_sheet", "N/A"),
                },
            }

            # Export using export manager
            with st.spinner(f"Exporting {export_type.upper()} file..."):
                success, message, file_info = self.export_manager.export_analysis_results(
                    export_data, export_type
                )

                if success:
                    st.success(message)

                    # Store file info for download links
                    if "export_files" not in st.session_state:
                        st.session_state["export_files"] = []

                    # Add to export files list (keep only last 5 exports)
                    st.session_state["export_files"].append(file_info)
                    if len(st.session_state["export_files"]) > 5:
                        st.session_state["export_files"] = st.session_state[
                            "export_files"
                        ][-5:]

                    st.rerun()
                else:
                    st.error(message)

        except Exception as e:
            st.error(f"Export failed: {str(e)}")

    def render_export_only(self, results: List[Dict], insights: Dict, 
                          recommendations: List[str], analyzed_comments: List[str]):
        """Render only export functionality for use in other components"""
        st.markdown("---")
        st.subheader("Export Results")

        col1, col2, col3, col4 = st.columns(4)

        # Prepare export data
        export_data = {
            "results": results,
            "insights": insights,
            "recommendations": recommendations,
            "analyzed_comments": analyzed_comments,
            "metadata": {
                "total_analyzed": len(results),
                "export_timestamp": pd.Timestamp.now().isoformat(),
                "is_multi_sheet": st.session_state.get("is_multi_sheet", False),
                "current_sheet": st.session_state.get("current_sheet", "N/A"),
            },
        }

        with col1:
            if st.button("Export Excel", help="Export complete analysis to Excel", key="export_excel_inline"):
                self._handle_inline_export(export_data, "excel")

        with col2:
            if st.button("Export CSV", help="Export detailed results to CSV", key="export_csv_inline"):
                self._handle_inline_export(export_data, "csv")

        with col3:
            if st.button("Summary Report", help="Export executive summary", key="export_summary_inline"):
                self._handle_inline_export(export_data, "summary")

        with col4:
            if st.button("Export JSON", help="Export data for further processing", key="export_json_inline"):
                self._handle_inline_export(export_data, "json")

    def _handle_inline_export(self, export_data: Dict, export_type: str):
        """Handle export for inline use"""
        try:
            with st.spinner(f"Exporting {export_type.upper()} file..."):
                success, message, file_info = self.export_manager.export_analysis_results(
                    export_data, export_type
                )

                if success:
                    st.success(message)
                    # Show download link immediately
                    st.markdown(file_info["link"], unsafe_allow_html=True)
                else:
                    st.error(message)

        except Exception as e:
            st.error(f"Export failed: {str(e)}")

    def get_results_summary(self) -> Dict:
        """Get a summary of current analysis results"""
        if not self.session_manager.has_analysis_results():
            return {"has_results": False}

        analysis_data = self.session_manager.get_analysis_results()
        results = analysis_data["results"] or []
        insights = analysis_data["insights"] or {}

        return {
            "has_results": True,
            "total_analyzed": len(results),
            "sentiment_distribution": insights.get("sentiment_percentages", {}),
            "top_themes_count": len(insights.get("top_themes", {})),
            "top_pain_points_count": len(insights.get("top_pain_points", {})),
            "recommendations_count": len(analysis_data["recommendations"] or []),
            "current_sheet": st.session_state.get("current_sheet", "N/A"),
            "is_multi_sheet": st.session_state.get("is_multi_sheet", False),
        }