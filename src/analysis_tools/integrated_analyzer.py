"""
Integrated Analysis Tool
Combines all analysis tools into a unified interface for the main application
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from .duplicate_cleaner import DuplicateCleaner
from .emotion_analyzer import EmotionAnalyzer
from .theme_analyzer import ThemeAnalyzer
from .batch_processor import BatchProcessor

logger = logging.getLogger(__name__)

class IntegratedAnalyzer:
    """Unified interface for all analysis tools"""
    
    def __init__(self):
        """Initialize integrated analyzer with all tools"""
        self.duplicate_cleaner = DuplicateCleaner()
        self.emotion_analyzer = EmotionAnalyzer()
        self.theme_analyzer = ThemeAnalyzer()
        self.batch_processor = BatchProcessor()
        
        self.current_results = {}
        self.processed_df = None
        
    def render_analysis_ui(self):
        """Render the analysis tools UI in Streamlit"""
        st.title("🔬 Advanced Analysis Tools")
        
        # Analysis type selection
        col1, col2 = st.columns([2, 1])
        with col1:
            analysis_types = st.multiselect(
                "Select Analysis Types",
                ["Duplicate Detection", "Emotion Analysis", "Theme Analysis", "Batch Processing"],
                default=["Duplicate Detection", "Emotion Analysis", "Theme Analysis"]
            )
        
        with col2:
            if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                if 'uploaded_df' in st.session_state and st.session_state.uploaded_df is not None:
                    self.run_comprehensive_analysis(st.session_state.uploaded_df, analysis_types)
                else:
                    st.error("Please upload a file first!")
        
        # Display results
        if self.current_results:
            self.display_results()
    
    def run_comprehensive_analysis(self, df: pd.DataFrame, analysis_types: List[str]):
        """Run selected analyses on the dataframe"""
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_steps = len(analysis_types)
        current_step = 0
        
        try:
            # Duplicate Detection
            if "Duplicate Detection" in analysis_types:
                status_text.text("Analyzing duplicates...")
                self.current_results['duplicates'] = self._run_duplicate_analysis(df)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            # Emotion Analysis
            if "Emotion Analysis" in analysis_types:
                status_text.text("Analyzing emotions...")
                self.current_results['emotions'] = self._run_emotion_analysis(df)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            # Theme Analysis
            if "Theme Analysis" in analysis_types:
                status_text.text("Analyzing themes...")
                self.current_results['themes'] = self._run_theme_analysis(df)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            # Batch Processing (for large files)
            if "Batch Processing" in analysis_types:
                status_text.text("Running batch processing...")
                self.current_results['batch'] = self._run_batch_processing(df)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            progress_bar.progress(1.0)
            status_text.text("Analysis complete!")
            st.success("✅ Analysis completed successfully!")
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            logger.error(f"Analysis error: {e}")
    
    def _run_duplicate_analysis(self, df: pd.DataFrame) -> Dict:
        """Run duplicate analysis"""
        report = self.duplicate_cleaner.generate_duplicate_report(df)
        self.processed_df = self.duplicate_cleaner.remove_duplicates(
            df, keep='highest_score', track_frequency=True
        )
        return report
    
    def _run_emotion_analysis(self, df: pd.DataFrame) -> Dict:
        """Run emotion analysis"""
        df_to_analyze = self.processed_df if self.processed_df is not None else df
        report = self.emotion_analyzer.generate_emotion_report(df_to_analyze)
        
        # Add timeline if date column exists
        if 'Fecha' in df_to_analyze.columns:
            report['timeline'] = self.emotion_analyzer.analyze_emotion_trends(df_to_analyze)
        
        return report
    
    def _run_theme_analysis(self, df: pd.DataFrame) -> Dict:
        """Run theme analysis"""
        df_to_analyze = self.processed_df if self.processed_df is not None else df
        report = self.theme_analyzer.generate_theme_report(df_to_analyze)
        
        # Add timeline if date column exists
        if 'Fecha' in df_to_analyze.columns:
            report['timeline'] = self.theme_analyzer.analyze_theme_trends(df_to_analyze)
        
        return report
    
    def _run_batch_processing(self, df: pd.DataFrame) -> Dict:
        """Run batch processing analysis"""
        # For demonstration, we'll process the existing dataframe in batches
        # In production, this would read from file directly
        temp_file = "temp_batch_data.csv"
        df.to_csv(temp_file, index=False)
        
        try:
            results = self.batch_processor.process_file(
                temp_file,
                analyses=['duplicates', 'emotions', 'themes'],
                parallel=True
            )
        finally:
            # Clean up temp file
            if Path(temp_file).exists():
                Path(temp_file).unlink()
        
        return results
    
    def display_results(self):
        """Display analysis results in organized tabs"""
        tabs = []
        tab_names = []
        
        if 'duplicates' in self.current_results:
            tab_names.append("📋 Duplicates")
            tabs.append(None)
        
        if 'emotions' in self.current_results:
            tab_names.append("😊 Emotions")
            tabs.append(None)
        
        if 'themes' in self.current_results:
            tab_names.append("🎯 Themes")
            tabs.append(None)
        
        if 'batch' in self.current_results:
            tab_names.append("⚡ Batch Results")
            tabs.append(None)
        
        if tab_names:
            tabs = st.tabs(tab_names)
            tab_index = 0
            
            # Duplicate Results Tab
            if 'duplicates' in self.current_results:
                with tabs[tab_index]:
                    self._display_duplicate_results(self.current_results['duplicates'])
                tab_index += 1
            
            # Emotion Results Tab
            if 'emotions' in self.current_results:
                with tabs[tab_index]:
                    self._display_emotion_results(self.current_results['emotions'])
                tab_index += 1
            
            # Theme Results Tab
            if 'themes' in self.current_results:
                with tabs[tab_index]:
                    self._display_theme_results(self.current_results['themes'])
                tab_index += 1
            
            # Batch Results Tab
            if 'batch' in self.current_results:
                with tabs[tab_index]:
                    self._display_batch_results(self.current_results['batch'])
                tab_index += 1
    
    def _display_duplicate_results(self, results: Dict):
        """Display duplicate analysis results"""
        st.header("Duplicate Analysis Results")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Comments", results['summary']['total_comments'])
        with col2:
            st.metric("Unique Comments", results['summary']['unique_comments'])
        with col3:
            st.metric("Duplicates", results['summary']['total_duplicates'])
        with col4:
            st.metric("Duplication Rate", f"{results['summary']['duplication_rate']}%")
        
        # Most repeated comments
        if results.get('most_repeated'):
            st.subheader("Most Repeated Comments")
            
            repeated_df = pd.DataFrame(results['most_repeated'])
            if not repeated_df.empty:
                fig = px.bar(
                    repeated_df.head(10),
                    x='frequency',
                    y=repeated_df.head(10).index,
                    orientation='h',
                    title="Top 10 Most Repeated Comments",
                    labels={'frequency': 'Frequency', 'index': 'Comment Index'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show details in expander
                with st.expander("View Comment Details"):
                    for idx, item in enumerate(results['most_repeated'][:5]):
                        st.write(f"**Comment {idx + 1}** (Repeated {item['frequency']} times)")
                        st.write(f"Text: {item['text']}")
                        if item.get('avg_score'):
                            st.write(f"Average Score: {item['avg_score']:.1f}")
                        st.divider()
        
        # Download cleaned data
        if self.processed_df is not None:
            st.subheader("Cleaned Data")
            st.write(f"Original: {results['summary']['total_comments']} → Cleaned: {len(self.processed_df)} comments")
            
            csv = self.processed_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Cleaned Data",
                csv,
                "cleaned_comments.csv",
                "text/csv"
            )
    
    def _display_emotion_results(self, results: Dict):
        """Display emotion analysis results"""
        st.header("Emotion Analysis Results")
        
        # Emotion balance metrics
        if 'summary' in results and 'emotion_balance' in results['summary']:
            balance = results['summary']['emotion_balance']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", f"{balance['positive']}%", 
                         delta=f"{balance['positive'] - balance['negative']:.1f}%")
            with col2:
                st.metric("Negative", f"{balance['negative']}%")
            with col3:
                st.metric("Neutral", f"{balance['neutral']}%")
        
        # Emotion distribution chart
        if 'summary' in results and 'emotion_percentages' in results['summary']:
            emotions = results['summary']['emotion_percentages']
            
            # Pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(emotions.keys()),
                values=[e['percentage'] for e in emotions.values()],
                marker=dict(colors=[e['color'] for e in emotions.values()]),
                hole=0.3
            )])
            fig.update_layout(title="Emotion Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Bar chart with intensity
            emotion_df = pd.DataFrame([
                {
                    'Emotion': emotion,
                    'Percentage': data['percentage'],
                    'Intensity': data.get('avg_intensity', 0) * 100
                }
                for emotion, data in emotions.items()
            ])
            
            if not emotion_df.empty:
                fig2 = px.bar(
                    emotion_df.sort_values('Percentage', ascending=True),
                    x='Percentage',
                    y='Emotion',
                    orientation='h',
                    color='Intensity',
                    color_continuous_scale='RdYlGn',
                    title="Emotion Percentages with Intensity"
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Insights
        if 'insights' in results:
            st.subheader("📊 Key Insights")
            for insight in results['insights']:
                st.info(f"• {insight}")
        
        # Recommendations
        if 'recommendations' in results:
            st.subheader("💡 Recommendations")
            for rec in results['recommendations']:
                st.warning(f"• {rec}")
    
    def _display_theme_results(self, results: Dict):
        """Display theme analysis results"""
        st.header("Theme Analysis Results")
        
        # Theme distribution
        if 'predefined_themes' in results and 'theme_distribution' in results['predefined_themes']:
            themes = results['predefined_themes']['theme_distribution']
            
            # Summary metrics
            if 'summary' in results['predefined_themes']:
                summary = results['predefined_themes']['summary']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Technical Focus", f"{summary.get('technical_focus', 0)}%")
                with col2:
                    st.metric("Service Focus", f"{summary.get('service_focus', 0)}%")
                with col3:
                    st.metric("Business Focus", f"{summary.get('business_focus', 0)}%")
            
            # Theme distribution chart
            theme_df = pd.DataFrame([
                {
                    'Theme': theme.replace('_', ' ').title(),
                    'Percentage': data['percentage'],
                    'Count': data['count']
                }
                for theme, data in themes.items()
                if data['percentage'] > 0
            ])
            
            if not theme_df.empty:
                fig = px.treemap(
                    theme_df,
                    path=['Theme'],
                    values='Percentage',
                    title="Theme Distribution Treemap",
                    color='Percentage',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Bar chart
                fig2 = px.bar(
                    theme_df.sort_values('Percentage', ascending=False).head(10),
                    x='Percentage',
                    y='Theme',
                    orientation='h',
                    title="Top 10 Themes"
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Theme combinations
        if 'predefined_themes' in results and 'theme_combinations' in results['predefined_themes']:
            combos = results['predefined_themes']['theme_combinations']
            if combos:
                st.subheader("Common Theme Combinations")
                combo_df = pd.DataFrame(combos)
                if not combo_df.empty:
                    combo_df['themes_str'] = combo_df['themes'].apply(lambda x: ' + '.join(x))
                    fig = px.bar(
                        combo_df.head(5),
                        x='percentage',
                        y='themes_str',
                        orientation='h',
                        title="Top Theme Combinations"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Discovered topics (if available)
        if 'discovered_topics' in results and results['discovered_topics']:
            topics = results['discovered_topics'].get('discovered_topics', [])
            if topics:
                st.subheader("🔍 Discovered Topics (AI-Generated)")
                for topic in topics[:5]:
                    with st.expander(f"Topic {topic['topic_id'] + 1}"):
                        st.write("**Keywords:**", ", ".join(topic['words']))
                        st.write("**Weights:**", topic['weights'])
        
        # Recommendations
        if 'recommendations' in results:
            st.subheader("💡 Recommendations")
            for rec in results['recommendations']:
                st.info(f"• {rec}")
    
    def _display_batch_results(self, results: Dict):
        """Display batch processing results"""
        st.header("Batch Processing Results")
        
        # Processing summary
        if 'summary' in results:
            summary = results['summary']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{summary['total_records']:,}")
            with col2:
                st.metric("Total Batches", summary['total_batches'])
            with col3:
                st.metric("Processing Time", f"{summary.get('processing_time', 0):.2f}s")
        
        # Aggregated results
        st.subheader("Aggregated Analysis")
        
        # Duplicates
        if 'duplicates' in results:
            st.write("**Duplicate Analysis:**")
            dup = results['duplicates']
            st.write(f"- Total Duplicates: {dup['total_duplicates']:,}")
            st.write(f"- Duplication Rate: {dup['overall_duplication_rate']}%")
        
        # Emotions
        if 'emotions' in results:
            st.write("**Emotion Analysis:**")
            emotions = results['emotions']
            top_emotions = sorted(emotions.items(), 
                                key=lambda x: x[1]['avg_percentage'], 
                                reverse=True)[:5]
            for emotion, data in top_emotions:
                st.write(f"- {emotion.capitalize()}: {data['avg_percentage']}%")
        
        # Themes
        if 'themes' in results:
            st.write("**Theme Analysis:**")
            themes = results['themes']
            top_themes = sorted(themes.items(), 
                              key=lambda x: x[1]['avg_percentage'], 
                              reverse=True)[:5]
            for theme, data in top_themes:
                theme_name = theme.replace('_', ' ').title()
                st.write(f"- {theme_name}: {data['avg_percentage']}%")
    
    def export_results(self, format: str = 'excel'):
        """Export analysis results to file"""
        if not self.current_results:
            st.warning("No results to export")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'excel':
            output_file = f"analysis_results_{timestamp}.xlsx"
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Export each result type to a separate sheet
                if 'duplicates' in self.current_results:
                    dup_df = pd.DataFrame([self.current_results['duplicates']['summary']])
                    dup_df.to_excel(writer, sheet_name='Duplicates', index=False)
                
                if 'emotions' in self.current_results:
                    if 'summary' in self.current_results['emotions']:
                        emotions = self.current_results['emotions']['summary']['emotion_percentages']
                        emo_df = pd.DataFrame([
                            {'Emotion': k, **v} for k, v in emotions.items()
                        ])
                        emo_df.to_excel(writer, sheet_name='Emotions', index=False)
                
                if 'themes' in self.current_results:
                    if 'predefined_themes' in self.current_results['themes']:
                        themes = self.current_results['themes']['predefined_themes']['theme_distribution']
                        theme_df = pd.DataFrame([
                            {'Theme': k, **v} for k, v in themes.items()
                        ])
                        theme_df.to_excel(writer, sheet_name='Themes', index=False)
            
            st.success(f"Results exported to {output_file}")
            
            # Provide download button
            with open(output_file, 'rb') as f:
                st.download_button(
                    "📥 Download Results",
                    f.read(),
                    output_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )