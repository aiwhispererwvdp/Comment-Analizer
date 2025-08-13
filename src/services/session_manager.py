"""
Session Management Service for Personal Paraguay Comments Analysis Platform
Handles session state management and data persistence
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import pandas as pd


class SessionManager:
    """Service for managing session state and data persistence"""

    def __init__(self):
        self.session_state = st.session_state

    def store_uploaded_data(
        self, comments_df: pd.DataFrame, data_info: Dict, processing_info: Dict
    ):
        """Store uploaded data and metadata in session"""
        self.session_state["comments_data"] = comments_df
        self.session_state["data_info"] = data_info

        # Handle Excel-specific data
        if processing_info.get("is_multi_sheet", False):
            self.session_state["excel_sheets"] = processing_info["sheets"]
            self.session_state["current_sheet"] = processing_info["current_sheet"]
            self.session_state["is_multi_sheet"] = True
            self.session_state["uploaded_file_path"] = processing_info["temp_path"]
        else:
            self.session_state["is_multi_sheet"] = False

    def store_analysis_results(
        self,
        results: List[Dict],
        insights: Dict,
        recommendations: List[str],
        analyzed_comments: List[str],
    ):
        """Store analysis results with sheet-specific handling"""
        # Store current results
        self.session_state["analysis_results"] = results
        self.session_state["insights"] = insights
        self.session_state["recommendations"] = recommendations
        self.session_state["analyzed_comments"] = analyzed_comments

        # If multi-sheet Excel, also store with sheet-specific keys
        if self.session_state.get("is_multi_sheet", False):
            current_sheet = self.session_state.get("current_sheet", "Sheet1")
            self.session_state[f"analysis_results_{current_sheet}"] = results
            self.session_state[f"insights_{current_sheet}"] = insights
            self.session_state[f"recommendations_{current_sheet}"] = recommendations
            self.session_state[f"analyzed_comments_{current_sheet}"] = analyzed_comments

    def get_analysis_results(self, sheet_name: Optional[str] = None) -> Optional[Dict]:
        """Get analysis results for current or specific sheet"""
        if sheet_name:
            return {
                "results": self.session_state.get(f"analysis_results_{sheet_name}"),
                "insights": self.session_state.get(f"insights_{sheet_name}"),
                "recommendations": self.session_state.get(
                    f"recommendations_{sheet_name}"
                ),
                "analyzed_comments": self.session_state.get(
                    f"analyzed_comments_{sheet_name}"
                ),
            }
        else:
            return {
                "results": self.session_state.get("analysis_results"),
                "insights": self.session_state.get("insights"),
                "recommendations": self.session_state.get("recommendations"),
                "analyzed_comments": self.session_state.get("analyzed_comments"),
            }

    def switch_excel_sheet(self, new_sheet: str) -> bool:
        """Switch to different Excel sheet and load its data"""
        if not self.session_state.get("is_multi_sheet", False):
            return False

        try:
            # Update current sheet
            self.session_state["current_sheet"] = new_sheet

            # Check if we have cached analysis for this sheet
            sheet_analysis_key = f"analysis_results_{new_sheet}"
            if sheet_analysis_key in self.session_state:
                # Load existing analysis for this sheet
                self.session_state["analysis_results"] = self.session_state[
                    sheet_analysis_key
                ]
                self.session_state["insights"] = self.session_state.get(
                    f"insights_{new_sheet}", {}
                )
                self.session_state["recommendations"] = self.session_state.get(
                    f"recommendations_{new_sheet}", []
                )
                self.session_state["analyzed_comments"] = self.session_state.get(
                    f"analyzed_comments_{new_sheet}", []
                )
            else:
                # Clear current analysis results when switching to unanalyzed sheet
                for key in [
                    "analysis_results",
                    "insights",
                    "recommendations",
                    "analyzed_comments",
                ]:
                    if key in self.session_state:
                        del self.session_state[key]

            return True

        except Exception:
            return False

    def get_sheet_analysis_status(self) -> Dict[str, bool]:
        """Get analysis status for all Excel sheets"""
        if not self.session_state.get("is_multi_sheet", False):
            return {}

        sheets = self.session_state.get("excel_sheets", [])
        status = {}

        for sheet in sheets:
            sheet_analysis_key = f"analysis_results_{sheet}"
            status[sheet] = sheet_analysis_key in self.session_state

        return status

    def clear_sheet_results(self, sheet_name: str):
        """Clear analysis results for specific sheet"""
        keys_to_remove = [
            f"analysis_results_{sheet_name}",
            f"insights_{sheet_name}",
            f"recommendations_{sheet_name}",
            f"analyzed_comments_{sheet_name}",
        ]

        for key in keys_to_remove:
            if key in self.session_state:
                del self.session_state[key]

    def clear_all_analysis_results(self):
        """Clear all analysis results from session"""
        # Clear current results
        keys_to_remove = [
            "analysis_results",
            "insights",
            "recommendations",
            "analyzed_comments",
        ]

        for key in keys_to_remove:
            if key in self.session_state:
                del self.session_state[key]

        # Clear sheet-specific results if multi-sheet
        if self.session_state.get("is_multi_sheet", False):
            sheets = self.session_state.get("excel_sheets", [])
            for sheet in sheets:
                self.clear_sheet_results(sheet)

    def get_current_data(self) -> Optional[Dict]:
        """Get currently loaded data"""
        return {
            "comments_data": self.session_state.get("comments_data"),
            "data_info": self.session_state.get("data_info", {}),
            "is_multi_sheet": self.session_state.get("is_multi_sheet", False),
            "current_sheet": self.session_state.get("current_sheet"),
            "excel_sheets": self.session_state.get("excel_sheets", []),
        }

    def has_data_loaded(self) -> bool:
        """Check if data is currently loaded"""
        return (
            "comments_data" in self.session_state
            and self.session_state["comments_data"] is not None
        )

    def has_analysis_results(self, sheet_name: Optional[str] = None) -> bool:
        """Check if analysis results exist for current or specific sheet"""
        if sheet_name:
            return f"analysis_results_{sheet_name}" in self.session_state
        else:
            return "analysis_results" in self.session_state

    def store_optimization_settings(self, settings: Dict):
        """Store optimization settings"""
        self.session_state["optimization_settings"] = settings

    def get_optimization_settings(self) -> Dict:
        """Get optimization settings"""
        return self.session_state.get(
            "optimization_settings",
            {
                "deduplication": True,
                "prefiltering": True,
                "language_detection": True,
                "caching": True,
            },
        )

    def initialize_session(self, monitor=None):
        """Initialize session with monitoring if needed"""
        if "session_id" not in self.session_state and monitor:
            import streamlit as st

            try:
                user_agent = st.context.headers.get("user-agent", "Streamlit User")
                self.session_state["session_id"] = monitor.start_session(user_agent)
                self.session_state["monitor"] = monitor
            except Exception:
                # Fallback if context not available
                self.session_state["session_id"] = monitor.start_session(
                    "Unknown User Agent"
                )
                self.session_state["monitor"] = monitor

    def get_session_info(self) -> Dict:
        """Get session information"""
        return {
            "session_id": self.session_state.get("session_id"),
            "has_data": self.has_data_loaded(),
            "has_analysis": self.has_analysis_results(),
            "is_multi_sheet": self.session_state.get("is_multi_sheet", False),
            "current_sheet": self.session_state.get("current_sheet"),
        }
