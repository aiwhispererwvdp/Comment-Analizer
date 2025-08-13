"""
Responsive Main Application for Personal Paraguay Comments Analysis
Features mobile-first design and adaptive layouts
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

# Import utilities and config
from config import Config
from utils.responsive_utils import ResponsiveUI, ResponsiveCards
from services.session_manager import SessionManager

# Import page components
from components.responsive_file_upload_ui import ResponsiveFileUploadUI
from components.responsive_analysis_dashboard_ui import ResponsiveAnalysisDashboardUI
from components.responsive_cost_optimization_ui import ResponsiveCostOptimizationUI


def initialize_app():
    """Initialize app configuration and state"""
    st.set_page_config(
        page_title="Personal Paraguay - Comments Analysis",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="collapsed" if ResponsiveUI.estimate_screen_size() == "mobile" else "expanded"
    )
    
    # Apply responsive theme
    ResponsiveUI.apply_responsive_theme()
    
    # Initialize session state
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.now().isoformat()
        st.session_state.session_start = datetime.now()
        st.session_state.selected_page = "Upload Data"


def render_responsive_header():
    """Render responsive header"""
    screen = ResponsiveUI.estimate_screen_size()
    
    if screen == 'mobile':
        # Compact mobile header
        st.markdown("""
        <div style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <h2 style="margin: 0; font-size: 1.2rem;">🔬 Personal Paraguay</h2>
            <p style="margin: 0; font-size: 0.8rem; color: #888;">Comments Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Full desktop header
        st.markdown("""
        <div style="padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <h1 style="margin: 0; font-size: 1.8rem;">🔬 Personal Paraguay - Comments Analysis Platform</h1>
            <p style="margin: 0.25rem 0 0 0; color: #888;">AI-powered sentiment analysis for telecommunications feedback</p>
        </div>
        """, unsafe_allow_html=True)


def render_responsive_navigation():
    """Render responsive navigation"""
    screen = ResponsiveUI.estimate_screen_size()
    
    nav_options = [
        ("📤", "Upload Data"),
        ("📊", "Analysis Dashboard"),
        ("💰", "Cost Optimization")
    ]
    
    if screen == 'mobile':
        # Horizontal tab bar for mobile
        tab_cols = st.columns(3)
        for idx, (icon, name) in enumerate(nav_options):
            with tab_cols[idx]:
                if st.button(
                    f"{icon}",
                    key=f"nav_{name}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_page == name else "secondary",
                    help=name
                ):
                    st.session_state.selected_page = name
                    st.rerun()
    else:
        # Sidebar navigation for tablet/desktop
        with st.sidebar:
            st.markdown("### 🧭 Navigation")
            for icon, name in nav_options:
                if st.button(
                    f"{icon} {name}",
                    key=f"nav_{name}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_page == name else "secondary"
                ):
                    st.session_state.selected_page = name
                    st.rerun()
            
            # Quick stats in sidebar (desktop only)
            if screen == 'desktop':
                render_sidebar_stats()


def render_sidebar_stats():
    """Render statistics in sidebar"""
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    if "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Comments", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        
        # Session duration
        if 'session_start' in st.session_state:
            duration = datetime.now() - st.session_state.session_start
            st.metric("Session", f"{int(duration.total_seconds() / 60)}m")
    else:
        st.info("No data loaded")


def render_responsive_content():
    """Render main content based on selected page"""
    page = st.session_state.selected_page
    
    # Show breadcrumb on mobile/tablet
    screen = ResponsiveUI.estimate_screen_size()
    if screen in ['mobile', 'tablet']:
        st.markdown(f"""
        <div style="padding: 0.5rem; background: rgba(255,255,255,0.03); 
        border-radius: 6px; margin: 0.5rem 0; font-size: 0.85rem;">
            📍 {page}
        </div>
        """, unsafe_allow_html=True)
    
    # Render selected page
    if page == "Upload Data":
        upload_ui = ResponsiveFileUploadUI()
        upload_ui.render()
    elif page == "Analysis Dashboard":
        dashboard_ui = ResponsiveAnalysisDashboardUI()
        dashboard_ui.render()
    elif page == "Cost Optimization":
        cost_ui = ResponsiveCostOptimizationUI()
        cost_ui.render()


def main():
    """Main application entry point"""
    initialize_app()
    render_responsive_header()
    render_responsive_navigation()
    render_responsive_content()


if __name__ == "__main__":
    main()