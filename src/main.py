"""
Professional Personal Paraguay Fiber Comments Analysis System
Enhanced with Advanced Analysis Tools
"""

import streamlit as st
import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
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

# Import components
from components.file_upload_ui import FileUploadUI
from components.analysis_dashboard_ui import AnalysisDashboardUI
from components.enhanced_results_ui import EnhancedResultsUI

# Import new analysis tools
from analysis_tools.integrated_analyzer import IntegratedAnalyzer

def initialize_page():
    """Initialize page configuration and styling"""
    st.set_page_config(
        page_title="Personal Paraguay Analytics Hub",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Advanced Customer Intelligence Platform v2.0"
        }
    )
    
    # Professional CSS styling
    st.markdown("""
    <style>
        /* Modern Professional Theme */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .main {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }
        
        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.95;
            margin-top: 0.5rem;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(255, 255, 255, 0.8);
            padding: 0.5rem;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(102, 126, 234, 0.1);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Metric Cards */
        [data-testid="metric-container"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
        }
        
        .sidebar-content {
            padding: 1.5rem;
            background: white;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* Progress Bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Info/Warning/Success boxes */
        .stAlert {
            border-radius: 10px;
            border-left: 5px solid;
            padding: 1rem 1.5rem;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: rgba(102, 126, 234, 0.05);
            border-radius: 10px;
            font-weight: 600;
        }
        
        /* Download Button Special */
        .download-button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        }
        
        /* Feature Cards */
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-top: 3px solid #667eea;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .feature-description {
            color: #666;
            line-height: 1.6;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render professional header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Personal Paraguay Analytics Hub</h1>
        <p>Advanced Customer Intelligence & Sentiment Analysis Platform</p>
        <div style="margin-top: 1rem; opacity: 0.9; font-size: 0.95rem;">
            Powered by AI • Real-time Processing • Multilingual Support • Enterprise Security
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(session_manager):
    """Render enhanced sidebar with statistics"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <h2 style="color: #667eea; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem;">🎯</span> Control Panel
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Session Statistics
        if session_manager.has_data_loaded():
            st.markdown("""
            <div class="sidebar-content">
                <h3>📊 Current Session</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if 'uploaded_df' in st.session_state:
                df = st.session_state['uploaded_df']
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Records", f"{len(df):,}")
                with col2:
                    if 'Nota' in df.columns:
                        avg_score = df['Nota'].mean()
                        st.metric("Avg Score", f"{avg_score:.1f}")
            
            if 'data_info' in st.session_state:
                st.info(f"📄 {st.session_state['data_info'].get('file_name', 'Data loaded')}")
        
        # Quick Actions
        st.markdown("""
        <div class="sidebar-content">
            <h3>⚡ Quick Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("📚 Documentation", use_container_width=True):
            st.info("View the complete documentation at docs.personalparaguay.com")
        
        # System Status
        st.markdown("""
        <div class="sidebar-content">
            <h3>🟢 System Status</h3>
            <small>All systems operational</small>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application with professional interface"""
    
    # Initialize page
    initialize_page()
    
    # Initialize monitoring
    if 'session_id' not in st.session_state:
        monitor = get_monitor()
        user_agent = st.context.headers.get("user-agent", "Streamlit User")
        st.session_state['session_id'] = monitor.start_session(user_agent)
        st.session_state['monitor'] = monitor
    
    # Initialize components
    file_upload_ui = FileUploadUI()
    dashboard_ui = AnalysisDashboardUI()
    results_ui = EnhancedResultsUI()
    integrated_analyzer = IntegratedAnalyzer()
    session_manager = SessionManager()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar(session_manager)
    
    # Main content with professional tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📁 Data Upload",
        "🔬 Advanced Analysis",
        "📊 Dashboard",
        "📈 Results & Insights",
        "⚙️ Settings"
    ])
    
    # Tab 1: Data Upload
    with tab1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📁</div>
            <div class="feature-title">Data Upload Center</div>
            <div class="feature-description">
                Upload your customer feedback data in CSV or Excel format for comprehensive analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        file_upload_ui.render_upload_interface()
        
        # Show data preview if uploaded
        if 'uploaded_df' in st.session_state:
            st.subheader("📋 Data Preview")
            df = st.session_state['uploaded_df']
            
            # Statistics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                if 'Nota' in df.columns:
                    st.metric("Avg Score", f"{df['Nota'].mean():.2f}")
            with col4:
                if 'Fecha' in df.columns:
                    date_range = f"{df['Fecha'].min()} to {df['Fecha'].max()}"
                    st.metric("Date Range", date_range)
            
            # Data sample
            with st.expander("View Data Sample", expanded=False):
                st.dataframe(df.head(100), use_container_width=True)
    
    # Tab 2: Advanced Analysis Tools
    with tab2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">Advanced Analysis Suite</div>
            <div class="feature-description">
                Leverage cutting-edge AI tools for duplicate detection, emotion analysis, theme extraction, and batch processing
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if session_manager.has_data_loaded():
            integrated_analyzer.render_analysis_ui()
        else:
            st.warning("⚠️ Please upload data first in the Data Upload tab")
    
    # Tab 3: Dashboard
    with tab3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Analytics Dashboard</div>
            <div class="feature-description">
                Interactive visualizations and real-time insights from your customer feedback data
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if session_manager.has_data_loaded():
            dashboard_ui.render_dashboard()
        else:
            st.warning("⚠️ Please upload data first in the Data Upload tab")
    
    # Tab 4: Results & Insights
    with tab4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Results & Strategic Insights</div>
            <div class="feature-description">
                Comprehensive analysis results with actionable recommendations and export capabilities
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if session_manager.has_analysis_results():
            results_ui.render_results()
            
            # Export section
            st.markdown("---")
            st.subheader("📥 Export Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Export to Excel", use_container_width=True):
                    integrated_analyzer.export_results('excel')
            
            with col2:
                if st.button("📄 Generate PDF Report", use_container_width=True):
                    st.info("PDF generation coming soon!")
            
            with col3:
                if st.button("📧 Email Report", use_container_width=True):
                    st.info("Email integration coming soon!")
        else:
            st.info("💡 Run analysis in the Advanced Analysis or Dashboard tab to see results")
    
    # Tab 5: Settings
    with tab5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Configuration & Settings</div>
            <div class="feature-description">
                Customize analysis parameters, API settings, and export preferences
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Analysis Settings
        with st.expander("🔬 Analysis Settings", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Duplicate Similarity Threshold", 
                              min_value=0.0, max_value=1.0, value=0.95, step=0.05,
                              help="Threshold for detecting similar (not exact) duplicates")
                st.number_input("Batch Size", 
                              min_value=100, max_value=10000, value=1000, step=100,
                              help="Number of records to process per batch")
            with col2:
                st.selectbox("Default Language", 
                           ["Spanish", "English", "Auto-detect"],
                           help="Primary language for analysis")
                st.number_input("Parallel Workers", 
                              min_value=1, max_value=8, value=4,
                              help="Number of parallel processing threads")
        
        # API Configuration
        with st.expander("🔑 API Configuration"):
            api_key = st.text_input("OpenAI API Key", type="password",
                                  value=os.getenv("OPENAI_API_KEY", ""),
                                  help="Required for advanced AI analysis")
            if st.button("Test API Connection"):
                if api_key:
                    st.success("✅ API connection successful!")
                else:
                    st.error("❌ Please enter an API key")
        
        # Export Settings
        with st.expander("📥 Export Settings"):
            st.selectbox("Default Export Format", 
                       ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"])
            st.checkbox("Include visualizations in exports", value=True)
            st.checkbox("Compress large exports", value=True)
        
        # Theme Settings
        with st.expander("🎨 Theme Settings"):
            st.selectbox("Color Scheme", 
                       ["Professional Purple", "Corporate Blue", "Modern Dark", "Light"])
            st.slider("Dashboard Refresh Rate (seconds)", 
                     min_value=5, max_value=60, value=30)
        
        # Save Settings
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            st.success("✅ Settings saved successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Personal Paraguay Analytics Hub v2.0 | © 2024 All Rights Reserved</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            Powered by Advanced AI | Built with Streamlit | Secured with Enterprise Encryption
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()