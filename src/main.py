"""
Main entry point for Personal Paraguay Fiber Comments Analysis System
"""

import streamlit as st
import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np
import os

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

# Set environment file path
env_path = project_root / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Import app modules
from config import Config, validate_config
from api.monitoring import get_monitor
from utils.validators import InputValidator, ValidationError, SecurityLogger
from utils.exceptions import (
    ErrorHandler, FileProcessingError, DataValidationError, 
    APIConnectionError, ConfigurationError, AnalysisProcessingError,
    raise_if_missing_config
)
from theme import theme
from services.session_manager import SessionManager

# Import components directly
from components.file_upload_ui import FileUploadUI
from components.analysis_dashboard_ui import AnalysisDashboardUI
from components.enhanced_results_ui import EnhancedResultsUI

def main():
    """Main application entry point"""
    
    st.set_page_config(
        page_title=Config.DASHBOARD_TITLE,
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply professional theme
    st.markdown(theme.get_main_css(), unsafe_allow_html=True)
    
    # Initialize monitoring
    if 'session_id' not in st.session_state:
        monitor = get_monitor()
        user_agent = st.context.headers.get("user-agent", "Streamlit User")
        st.session_state['session_id'] = monitor.start_session(user_agent)
        st.session_state['monitor'] = monitor
    
    # Enhanced professional header with improved typography
    st.markdown(
        theme.get_component_html(
            "header",
            Config.DASHBOARD_TITLE,
            "Advanced AI-powered sentiment analysis and business intelligence platform for telecommunications customer feedback",
            subtitle="Real-time insights • Multi-language support • Enterprise-grade security"
        ),
        unsafe_allow_html=True
    )
    
    # Initialize components
    file_upload_ui = FileUploadUI()
    dashboard_ui = AnalysisDashboardUI()
    results_ui = EnhancedResultsUI()
    session_manager = SessionManager()
    
    # Sidebar information
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>Personal Paraguay</h2>
            <p>Comment Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show statistics if data is loaded
        if session_manager.has_data_loaded():
            current_data = session_manager.get_current_data()
            if current_data and 'comments_data' in st.session_state:
                comments_count = len(st.session_state['comments_data'])
                st.metric("Total Comments", f"{comments_count:,}")
                if 'data_info' in st.session_state:
                    data_info = st.session_state['data_info']
                    if 'file_name' in data_info:
                        st.info(f"📄 {data_info['file_name']}")
    
    # Main content area - Single page application
    # File Upload Section
    with st.container():
        st.header("📁 Upload Data")
        file_upload_ui.render_upload_interface()
    
    # Show analysis section only if data is loaded
    if session_manager.has_data_loaded():
        st.markdown("---")
        
        # Analysis Dashboard Section
        with st.container():
            st.header("🔬 Analysis Dashboard")
            dashboard_ui.render_dashboard()
        
        # Results Section
        if session_manager.has_analysis_results():
            st.markdown("---")
            with st.container():
                st.header("📊 Results & Insights")
                results_ui.render_results()



if __name__ == "__main__":
    main()