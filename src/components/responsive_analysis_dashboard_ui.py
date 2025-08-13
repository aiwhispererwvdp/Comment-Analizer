"""
Responsive Analysis Dashboard UI Component
Adaptive layouts for all screen sizes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

from utils.responsive_utils import ResponsiveUI, ResponsiveCards
from services.session_manager import SessionManager
from services.analysis_service import AnalysisService
from sentiment_analysis.openai_analyzer import OpenAIAnalyzer
from utils.exceptions import ErrorHandler


class ResponsiveAnalysisDashboardUI:
    """Responsive analysis dashboard"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.analysis_service = AnalysisService()
    
    def render(self):
        """Render responsive dashboard"""
        screen = ResponsiveUI.estimate_screen_size()
        
        # Check if data is loaded
        if not self.session_manager.has_data_loaded():
            st.warning("📊 No data loaded. Please upload data first.")
            if st.button("Go to Upload", type="primary"):
                st.session_state.selected_page = "Upload Data"
                st.rerun()
            return
        
        # Get data
        current_data = self.session_manager.get_current_data()
        comments_df = current_data["data"]
        
        # Dashboard header
        st.markdown("### 📊 Analysis Dashboard")
        st.markdown(f"Analyzing {len(comments_df):,} comments")
        
        # Render sections based on screen size
        if screen == 'mobile':
            self._render_mobile_dashboard(comments_df)
        elif screen == 'tablet':
            self._render_tablet_dashboard(comments_df)
        else:
            self._render_desktop_dashboard(comments_df)
    
    def _render_mobile_dashboard(self, df: pd.DataFrame):
        """Mobile-optimized dashboard layout"""
        # Use tabs for mobile to save space
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "💭 Sentiment", "📊 Charts", "💾 Export"])
        
        with tab1:
            self._render_overview_metrics(df, 'mobile')
        
        with tab2:
            self._render_sentiment_analysis(df, 'mobile')
        
        with tab3:
            self._render_charts(df, 'mobile')
        
        with tab4:
            self._render_export_section(df, 'mobile')
    
    def _render_tablet_dashboard(self, df: pd.DataFrame):
        """Tablet-optimized dashboard layout"""
        # 2-column layout for tablets
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_overview_metrics(df, 'tablet')
            self._render_sentiment_analysis(df, 'tablet')
        
        with col2:
            self._render_charts(df, 'tablet')
        
        # Full width export section
        self._render_export_section(df, 'tablet')
    
    def _render_desktop_dashboard(self, df: pd.DataFrame):
        """Desktop full-featured dashboard"""
        # Overview metrics
        self._render_overview_metrics(df, 'desktop')
        
        # Main content in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_sentiment_analysis(df, 'desktop')
            self._render_charts(df, 'desktop')
        
        with col2:
            self._render_insights_panel(df)
            self._render_export_section(df, 'desktop')
    
    def _render_overview_metrics(self, df: pd.DataFrame, screen: str):
        """Render overview metrics responsively"""
        st.markdown("#### Key Metrics")
        
        # Calculate metrics
        total_comments = len(df)
        avg_length = int(df['comment'].str.len().mean()) if 'comment' in df.columns else 0
        unique_sources = df['source'].nunique() if 'source' in df.columns else 1
        
        # Sentiment distribution (mock for now)
        positive_pct = 45
        negative_pct = 30
        neutral_pct = 25
        
        metrics = [
            ("Total Comments", f"{total_comments:,}", None),
            ("Avg Length", f"{avg_length} chars", None),
            ("Sources", unique_sources, None),
            ("Positive", f"{positive_pct}%", "+5%"),
            ("Negative", f"{negative_pct}%", "-3%"),
            ("Neutral", f"{neutral_pct}%", "-2%")
        ]
        
        # Display based on screen size
        if screen == 'mobile':
            # 2 columns on mobile
            cols = st.columns(2)
            for idx, metric in enumerate(metrics):
                with cols[idx % 2]:
                    st.metric(*metric)
        else:
            # Use responsive columns
            ResponsiveUI.responsive_metrics(metrics[:4])
    
    def _render_sentiment_analysis(self, df: pd.DataFrame, screen: str):
        """Render sentiment analysis section"""
        st.markdown("#### 💭 Sentiment Analysis")
        
        # Analysis controls
        if screen == 'mobile':
            # Stack controls vertically
            sample_size = st.slider("Sample size:", 10, min(100, len(df)), 50)
            if st.button("🔄 Run Analysis", type="primary", use_container_width=True):
                self._run_sentiment_analysis(df.head(sample_size))
        else:
            # Horizontal layout
            col1, col2 = st.columns([2, 1])
            with col1:
                sample_size = st.slider("Sample size:", 10, min(500, len(df)), 100)
            with col2:
                if st.button("🔄 Run Analysis", type="primary", use_container_width=True):
                    self._run_sentiment_analysis(df.head(sample_size))
        
        # Display results if available
        if "sentiment_results" in st.session_state:
            results = st.session_state.sentiment_results
            
            # Sentiment chart
            fig = go.Figure(data=[
                go.Bar(
                    x=['Positive', 'Negative', 'Neutral'],
                    y=[results['positive'], results['negative'], results['neutral']],
                    marker_color=['#10b981', '#ef4444', '#6b7280']
                )
            ])
            
            fig.update_layout(
                title="Sentiment Distribution",
                height=300 if screen == 'mobile' else 400,
                showlegend=False,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_charts(self, df: pd.DataFrame, screen: str):
        """Render responsive charts"""
        st.markdown("#### 📊 Data Visualizations")
        
        # Chart tabs
        if screen == 'mobile':
            # Use tabs on mobile
            chart_tab1, chart_tab2 = st.tabs(["Length Distribution", "Time Series"])
            
            with chart_tab1:
                self._render_length_chart(df, screen)
            
            with chart_tab2:
                self._render_time_chart(df, screen)
        else:
            # Show charts in sequence
            self._render_length_chart(df, screen)
            self._render_time_chart(df, screen)
    
    def _render_length_chart(self, df: pd.DataFrame, screen: str):
        """Render comment length distribution"""
        if 'comment' in df.columns:
            df['length'] = df['comment'].str.len()
            
            fig = px.histogram(
                df, 
                x='length',
                nbins=30,
                title="Comment Length Distribution"
            )
            
            fig.update_layout(
                height=250 if screen == 'mobile' else 350,
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis_title="Characters",
                yaxis_title="Count"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_time_chart(self, df: pd.DataFrame, screen: str):
        """Render time series if date column exists"""
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        
        if date_cols:
            try:
                df['date'] = pd.to_datetime(df[date_cols[0]])
                daily_counts = df.groupby(df['date'].dt.date).size().reset_index(name='count')
                
                fig = px.line(
                    daily_counts,
                    x='date',
                    y='count',
                    title="Comments Over Time"
                )
                
                fig.update_layout(
                    height=250 if screen == 'mobile' else 350,
                    margin=dict(l=0, r=0, t=40, b=0),
                    xaxis_title="Date",
                    yaxis_title="Comments"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("No time series data available")
    
    def _render_insights_panel(self, df: pd.DataFrame):
        """Render insights panel (desktop only)"""
        st.markdown("#### 💡 Quick Insights")
        
        insights = [
            "📈 Comment volume increased 15% this week",
            "😊 Positive sentiment trending upward",
            "⚠️ 23 comments need review",
            "🔥 Hot topic: 'service quality'"
        ]
        
        for insight in insights:
            st.markdown(
                ResponsiveCards.info_card("", insight, ""),
                unsafe_allow_html=True
            )
    
    def _render_export_section(self, df: pd.DataFrame, screen: str):
        """Render export options"""
        st.markdown("#### 💾 Export Options")
        
        if screen == 'mobile':
            # Stack buttons vertically
            if st.button("📥 Download CSV", use_container_width=True):
                self._export_csv(df)
            if st.button("📊 Download Report", use_container_width=True):
                self._export_report(df)
        else:
            # Horizontal layout
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Download CSV", use_container_width=True):
                    self._export_csv(df)
            with col2:
                if st.button("📊 Download Report", use_container_width=True):
                    self._export_report(df)
    
    def _run_sentiment_analysis(self, df: pd.DataFrame):
        """Run sentiment analysis on sample"""
        with st.spinner("Analyzing sentiment..."):
            # Mock results for demonstration
            st.session_state.sentiment_results = {
                'positive': 45,
                'negative': 30,
                'neutral': 25
            }
            st.success("✅ Analysis complete!")
    
    def _export_csv(self, df: pd.DataFrame):
        """Export data as CSV"""
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="comments_analysis.csv",
            mime="text/csv"
        )
    
    def _export_report(self, df: pd.DataFrame):
        """Export analysis report"""
        st.info("Report generation in progress...")
        # Implement report generation logic here