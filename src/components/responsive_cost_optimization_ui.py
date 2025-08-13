"""
Responsive Cost Optimization UI Component
Adaptive cost analysis and optimization interface
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List

from utils.responsive_utils import ResponsiveUI, ResponsiveCards
from services.session_manager import SessionManager
from api.api_optimizer import APICallOptimizer as APIOptimizer


class ResponsiveCostOptimizationUI:
    """Responsive cost optimization interface"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.api_optimizer = APIOptimizer()
    
    def render(self):
        """Render responsive cost optimization interface"""
        screen = ResponsiveUI.estimate_screen_size()
        
        st.markdown("### 💰 Cost Optimization")
        st.markdown("Optimize API usage and reduce analysis costs")
        
        # Check if data is loaded
        if not self.session_manager.has_data_loaded():
            st.warning("📊 No data loaded. Please upload data first.")
            return
        
        # Get current data
        current_data = self.session_manager.get_current_data()
        df = current_data["data"]
        
        # Render based on screen size
        if screen == 'mobile':
            self._render_mobile_layout(df)
        else:
            self._render_desktop_layout(df, screen)
    
    def _render_mobile_layout(self, df: pd.DataFrame):
        """Mobile-optimized layout with tabs"""
        tab1, tab2, tab3 = st.tabs(["💵 Costs", "⚡ Optimize", "📈 Savings"])
        
        with tab1:
            self._render_cost_overview(df, 'mobile')
        
        with tab2:
            self._render_optimization_controls(df, 'mobile')
        
        with tab3:
            self._render_savings_summary(df, 'mobile')
    
    def _render_desktop_layout(self, df: pd.DataFrame, screen: str):
        """Desktop/tablet layout with columns"""
        # Cost overview at top
        self._render_cost_overview(df, screen)
        
        # Main content in columns
        if screen == 'tablet':
            col1, col2 = st.columns(2)
        else:
            col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_optimization_controls(df, screen)
            self._render_cost_breakdown_chart(df, screen)
        
        with col2:
            self._render_savings_summary(df, screen)
            self._render_recommendations(df)
    
    def _render_cost_overview(self, df: pd.DataFrame, screen: str):
        """Render cost overview metrics"""
        st.markdown("#### 💵 Current Cost Analysis")
        
        # Calculate costs
        total_comments = len(df)
        avg_length = int(df['comment'].str.len().mean()) if 'comment' in df.columns else 100
        
        # Estimate tokens and costs
        total_tokens = total_comments * avg_length * 1.3  # Rough token estimate
        input_cost = (total_tokens / 1000) * 0.01  # $0.01 per 1K tokens
        output_cost = (total_tokens / 2000) * 0.03  # $0.03 per 1K tokens
        total_cost = input_cost + output_cost
        
        # Display metrics
        metrics = [
            ("Total Comments", f"{total_comments:,}", None),
            ("Est. Tokens", f"{int(total_tokens):,}", None),
            ("Input Cost", f"${input_cost:.2f}", None),
            ("Output Cost", f"${output_cost:.2f}", None),
            ("Total Cost", f"${total_cost:.2f}", None),
            ("Per Comment", f"${total_cost/total_comments:.4f}", None)
        ]
        
        if screen == 'mobile':
            # 2 columns on mobile
            cols = st.columns(2)
            for idx, metric in enumerate(metrics):
                with cols[idx % 2]:
                    st.metric(*metric)
        else:
            # Responsive grid
            ResponsiveUI.responsive_metrics(metrics[:4])
    
    def _render_optimization_controls(self, df: pd.DataFrame, screen: str):
        """Render optimization controls"""
        st.markdown("#### ⚡ Optimization Settings")
        
        with st.expander("Configure optimization parameters", expanded=True):
            if screen == 'mobile':
                # Stack controls vertically
                batch_size = st.slider("Batch size:", 10, 100, 50)
                cache_enabled = st.checkbox("Enable caching", value=True)
                compression = st.checkbox("Enable compression", value=True)
                sampling_rate = st.slider("Sampling rate (%):", 10, 100, 100)
            else:
                # Grid layout
                col1, col2 = st.columns(2)
                with col1:
                    batch_size = st.slider("Batch size:", 10, 100, 50)
                    cache_enabled = st.checkbox("Enable caching", value=True)
                with col2:
                    compression = st.checkbox("Enable compression", value=True)
                    sampling_rate = st.slider("Sampling rate (%):", 10, 100, 100)
            
            # Calculate optimized costs
            optimized_comments = int(len(df) * sampling_rate / 100)
            optimized_cost = (optimized_comments * 100 * 1.3 / 1000) * 0.02
            
            if cache_enabled:
                optimized_cost *= 0.7  # 30% reduction with caching
            if compression:
                optimized_cost *= 0.9  # 10% reduction with compression
            
            # Apply button
            if st.button("🚀 Apply Optimization", type="primary", use_container_width=True):
                st.success(f"✅ Optimization applied! New estimated cost: ${optimized_cost:.2f}")
                st.session_state.optimized_settings = {
                    'batch_size': batch_size,
                    'cache': cache_enabled,
                    'compression': compression,
                    'sampling': sampling_rate
                }
    
    def _render_cost_breakdown_chart(self, df: pd.DataFrame, screen: str):
        """Render cost breakdown chart"""
        st.markdown("#### 📊 Cost Breakdown")
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['API Calls', 'Processing', 'Storage', 'Transfer'],
            values=[45, 30, 15, 10],
            hole=.3,
            marker_colors=['#667eea', '#764ba2', '#f6ad55', '#68d391']
        )])
        
        fig.update_layout(
            height=250 if screen == 'mobile' else 350,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(
                orientation="h" if screen == 'mobile' else "v",
                yanchor="bottom" if screen == 'mobile' else "middle",
                y=-0.2 if screen == 'mobile' else 0.5,
                xanchor="center" if screen == 'mobile' else "left",
                x=0.5 if screen == 'mobile' else 1.02
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_savings_summary(self, df: pd.DataFrame, screen: str):
        """Render savings summary"""
        st.markdown("#### 📈 Potential Savings")
        
        # Calculate savings
        current_cost = len(df) * 0.0001  # Simplified calculation
        optimized_cost = current_cost * 0.6  # 40% savings
        savings = current_cost - optimized_cost
        savings_pct = (savings / current_cost) * 100
        
        # Savings card
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-radius: 12px; padding: 1.5rem; color: white; text-align: center;">
                <h2 style="margin: 0;">💰 ${savings:.2f}</h2>
                <p style="margin: 0.5rem 0 0 0;">Potential Monthly Savings</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem;">{savings_pct:.0f}% Reduction</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Breakdown
        st.markdown("**Savings Breakdown:**")
        savings_items = [
            ("Caching", 30),
            ("Batching", 25),
            ("Compression", 10),
            ("Sampling", 35)
        ]
        
        for item, pct in savings_items:
            st.markdown(
                ResponsiveCards.progress_card(item, pct, "#10b981"),
                unsafe_allow_html=True
            )
    
    def _render_recommendations(self, df: pd.DataFrame):
        """Render optimization recommendations"""
        st.markdown("#### 💡 Recommendations")
        
        recommendations = [
            ("Enable caching", "Save 30% on repeated analyses", "🔄"),
            ("Use batch processing", "Reduce API calls by 40%", "📦"),
            ("Implement sampling", "Analyze subset first", "📊"),
            ("Schedule off-peak", "Lower rates available", "🕐")
        ]
        
        for title, desc, icon in recommendations:
            st.markdown(
                ResponsiveCards.info_card(f"{icon} {title}", desc, ""),
                unsafe_allow_html=True
            )