"""
Optimized Main Application with Enhanced Sidebar and Space-Efficient Layout
Personal Paraguay Fiber Comments Analysis System
"""

import streamlit as st
import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np
import os
from datetime import datetime

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

# Import optimized components
from components.optimized_file_upload_ui import OptimizedFileUploadUI

# Import existing page modules (we'll optimize these next)
from pages.analysis_dashboard_page import render_analysis_dashboard_page
from pages.cost_optimization_page import render_cost_optimization_page


def main():
    """Optimized main application with enhanced sidebar"""
    
    st.set_page_config(
        page_title=Config.DASHBOARD_TITLE,
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply professional theme with custom CSS for optimization
    custom_css = """
    <style>
    /* Compact header */
    .main-header {
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    /* Enhanced sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }
    
    .sidebar-stats {
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }
    
    .sidebar-stat-item {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;
        font-size: 0.85rem;
    }
    
    .sidebar-stat-value {
        font-weight: 600;
        color: #667eea;
    }
    
    /* Quick actions */
    .quick-actions {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .quick-action-btn {
        width: 100%;
        padding: 8px;
        margin: 4px 0;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 6px;
        color: #667eea;
        text-align: left;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-action-btn:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateX(2px);
    }
    
    /* Floating action button */
    .floating-cta {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 24px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .floating-cta:hover {
        transform: scale(1.05);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .sidebar-content {
            padding: 0.5rem;
        }
    }
    </style>
    """
    
    st.markdown(theme.get_main_css() + custom_css, unsafe_allow_html=True)
    
    # Initialize monitoring
    if 'session_id' not in st.session_state:
        monitor = get_monitor()
        user_agent = st.context.headers.get("user-agent", "Streamlit User")
        st.session_state['session_id'] = monitor.start_session(user_agent)
        st.session_state['monitor'] = monitor
        st.session_state['session_start'] = datetime.now()
    
    # Compact header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 1.8rem;">🔬 Personal Paraguay - Comments Analysis</h1>
        <p style="margin: 0; color: #888; font-size: 0.9rem;">AI-powered sentiment analysis platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options
    nav_options = [
        ("📤", "Upload Data"),
        ("📊", "Analysis Dashboard"), 
        ("💰", "Cost Optimization")
    ]
    
    # Initialize page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Upload Data"
    
    # Enhanced sidebar with useful information
    with st.sidebar:
        # Compact branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <h2 style="margin: 0; font-size: 1.2rem;">Personal Paraguay</h2>
            <p style="margin: 0; font-size: 0.8rem; color: #888;">Analysis Platform v2.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation section
        st.markdown("### 🧭 Navigation")
        for icon, option in nav_options:
            if st.button(
                f"{icon} {option}",
                key=f"nav_{option}",
                use_container_width=True,
                type="primary" if st.session_state.selected_page == option else "secondary"
            ):
                st.session_state.selected_page = option
                st.rerun()
        
        # Current status section
        st.markdown("### 📈 Current Status")
        st.markdown('<div class="sidebar-stats">', unsafe_allow_html=True)
        
        # Show data status
        if "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            st.markdown(f"""
            <div class="sidebar-stat-item">
                <span>Dataset:</span>
                <span class="sidebar-stat-value">Loaded ✓</span>
            </div>
            <div class="sidebar-stat-item">
                <span>Comments:</span>
                <span class="sidebar-stat-value">{len(df):,}</span>
            </div>
            <div class="sidebar-stat-item">
                <span>Columns:</span>
                <span class="sidebar-stat-value">{len(df.columns)}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sidebar-stat-item">
                <span>Dataset:</span>
                <span style="color: #ffa500;">Not loaded</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Session info
        if 'session_start' in st.session_state:
            duration = datetime.now() - st.session_state.session_start
            minutes = int(duration.total_seconds() / 60)
            st.markdown(f"""
            <div class="sidebar-stat-item">
                <span>Session:</span>
                <span class="sidebar-stat-value">{minutes}m</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick actions section
        st.markdown("### ⚡ Quick Actions")
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        
        if st.button("🔄 Clear Data", use_container_width=True, help="Clear all uploaded data"):
            for key in ['uploaded_data', 'analysis_results', 'upload_step']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        if st.button("📥 Export Results", use_container_width=True, help="Export analysis results"):
            if "analysis_results" in st.session_state:
                st.download_button(
                    label="Download CSV",
                    data=st.session_state.analysis_results.to_csv(index=False),
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No results to export")
        
        if st.button("❓ Help", use_container_width=True):
            st.info("Visit docs.anthropic.com for help")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.75rem; color: #666;">
            <p>© 2024 Personal Paraguay</p>
            <p>Powered by OpenAI GPT-4</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area based on selection
    page = st.session_state.selected_page
    
    # Show current page with breadcrumb
    st.markdown(f"""
    <div style="padding: 8px 16px; background: rgba(255,255,255,0.03); 
    border-radius: 8px; margin-bottom: 1rem; font-size: 0.9rem;">
        📍 <strong>{page}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "Upload Data":
        upload_ui = OptimizedFileUploadUI()
        upload_ui.render_upload_interface()
    elif page == "Analysis Dashboard":
        render_analysis_dashboard_page()
    elif page == "Cost Optimization":
        render_cost_optimization_page()
    
    # Floating CTA button (only show on upload page when data is loaded)
    if page == "Upload Data" and "uploaded_data" in st.session_state:
        st.markdown("""
        <div class="floating-cta" onclick="document.querySelector('[key=nav_Analysis Dashboard]').click()">
            🚀 Start Analysis →
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()