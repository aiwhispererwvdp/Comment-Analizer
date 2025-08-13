"""
Simplified Personal Paraguay Comments Analysis
Clean, minimalist interface with real data analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from datetime import datetime
import numpy as np
from collections import Counter
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from services.session_manager import SessionManager
from services.file_upload_service import FileUploadService
from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer

# Page config
st.set_page_config(
    page_title="Personal Paraguay — Comments Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for simplified design
st.markdown("""
<style>
    /* Root colors matching HTML */
    :root {
        --bg: #0f1419;
        --card: #18202a;
        --ink: #e6edf3;
        --muted: #9aa6b2;
        --border: #243247;
        --ok: #16c784;
        --warn: #f4bf4f;
        --bad: #ff5e57;
        --brand: #4ea4ff;
    }
    
    /* Main app styling */
    .stApp {
        background: var(--bg);
    }
    
    /* Header styling */
    .main-header {
        background: #0e1520;
        border-bottom: 1px solid var(--border);
        padding: 12px 16px;
        margin: -1rem -1rem 1rem -1rem;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px;
        height: 100%;
    }
    
    .metric-label {
        font-size: 12px;
        color: var(--muted);
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--ink);
    }
    
    /* Progress bar */
    .progress-bar {
        height: 6px;
        background: #0c141f;
        border: 1px solid #1f2a3a;
        border-radius: 6px;
        overflow: hidden;
        margin-top: 6px;
    }
    
    .progress-fill {
        height: 100%;
        transition: width 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: #0f1a26;
        border: 1px solid var(--border);
        color: var(--ink);
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #1a2433;
        border-color: var(--brand);
    }
    
    /* Primary button */
    .primary-button > button {
        background: var(--brand) !important;
        border-color: transparent !important;
    }
    
    .primary-button > button:hover {
        background: #3d8fd9 !important;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #2b4060;
        border-radius: 10px;
        padding: 24px;
        background: transparent;
    }
    
    .stFileUploader:hover {
        border-color: var(--brand);
        background: #0f1a26;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px 8px 0 0;
        color: var(--ink);
    }
    
    .stTabs [aria-selected="true"] {
        background: #101a26;
        border-color: var(--border);
        border-bottom-color: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive grid */
    @media (max-width: 900px) {
        .summary-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()
    st.session_state.file_service = FileUploadService()
    st.session_state.analyzer = EnhancedAnalyzer()
    st.session_state.analysis_results = None
    st.session_state.raw_data = None
    st.session_state.themes_data = None

# Analysis Functions
def analyze_sentiment_simple(text):
    """Simple sentiment analysis based on keywords"""
    if pd.isna(text) or text == "":
        return "neutral"
    
    text_lower = str(text).lower()
    
    # Positive keywords
    positive_words = ['excelente', 'bueno', 'mejor', 'satisfecho', 'rapido', 'bien', 
                     'perfecto', 'genial', 'feliz', 'contento', 'funciona', 'estable']
    
    # Negative keywords  
    negative_words = ['malo', 'pesimo', 'lento', 'cae', 'corta', 'intermitencia', 
                     'problema', 'terrible', 'horrible', 'nunca', 'no funciona', 'peor']
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def extract_themes(texts):
    """Extract common themes from text"""
    themes = {
        'velocidad_lenta': ['lento', 'velocidad', 'lentitud', 'demora', 'tarda'],
        'intermitencias': ['cae', 'corta', 'intermitencia', 'inestable', 'interrumpe'],
        'atencion_cliente': ['atencion', 'servicio', 'cliente', 'respuesta', 'soporte'],
        'precio': ['caro', 'precio', 'costoso', 'tarifa', 'pago'],
        'cobertura': ['cobertura', 'señal', 'alcance', 'zona', 'area'],
        'instalacion': ['instalacion', 'tecnico', 'visita', 'demora', 'cita']
    }
    
    theme_counts = {theme: 0 for theme in themes}
    theme_examples = {theme: [] for theme in themes}
    
    for text in texts:
        if pd.isna(text):
            continue
        text_lower = str(text).lower()
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:  # Keep top 3 examples
                    theme_examples[theme].append(text[:100])  # First 100 chars
    
    return theme_counts, theme_examples

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract data"""
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Find comment column (look for common names)
        comment_cols = ['comment', 'comments', 'feedback', 'review', 'texto', 
                       'comentario', 'comentarios', 'respuesta', 'opinion']
        
        comment_col = None
        for col in df.columns:
            if any(name in col.lower() for name in comment_cols):
                comment_col = col
                break
        
        if comment_col is None and len(df.columns) > 0:
            # Use first text column if no comment column found
            for col in df.columns:
                if df[col].dtype == 'object':
                    comment_col = col
                    break
        
        if comment_col is None:
            st.error("No text column found in the file")
            return None
        
        # Analyze each comment
        comments = df[comment_col].dropna().tolist()
        sentiments = [analyze_sentiment_simple(comment) for comment in comments]
        
        # Calculate statistics
        total = len(comments)
        sentiment_counts = Counter(sentiments)
        
        positive_pct = (sentiment_counts['positive'] / total * 100) if total > 0 else 0
        neutral_pct = (sentiment_counts['neutral'] / total * 100) if total > 0 else 0
        negative_pct = (sentiment_counts['negative'] / total * 100) if total > 0 else 0
        
        # Extract themes
        theme_counts, theme_examples = extract_themes(comments)
        
        # Calculate file stats
        file_size_kb = uploaded_file.size / 1024
        avg_length = np.mean([len(str(c)) for c in comments]) if comments else 0
        
        return {
            'total': total,
            'positive_pct': round(positive_pct, 1),
            'neutral_pct': round(neutral_pct, 1),
            'negative_pct': round(negative_pct, 1),
            'positive_count': sentiment_counts['positive'],
            'neutral_count': sentiment_counts['neutral'],
            'negative_count': sentiment_counts['negative'],
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'file_size': round(file_size_kb, 1),
            'avg_length': round(avg_length),
            'comments': comments[:100],  # Keep first 100 for display
            'sentiments': sentiments[:100]
        }
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# Header
st.markdown("""
<div class="main-header">
    <strong style="font-size: 16px;">🔬 Personal Paraguay</strong> · 
    <span style="color: var(--muted);">Customer Comments Analysis</span>
</div>
""", unsafe_allow_html=True)

# Main container
container = st.container()

with container:
    # Summary metrics - Dynamic based on analysis
    col1, col2, col3, col4 = st.columns(4)
    
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value">{results['total']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Positive</div>
                <div class="metric-value" style="color: var(--ok);">{results['positive_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['positive_pct']}%; background: var(--ok);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Neutral</div>
                <div class="metric-value" style="color: var(--warn);">{results['neutral_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['neutral_pct']}%; background: var(--warn);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Negative</div>
                <div class="metric-value" style="color: var(--bad);">{results['negative_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['negative_pct']}%; background: var(--bad);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Default empty state
        for col in [col1, col2, col3, col4]:
            with col:
                labels = ["Total", "Positive", "Neutral", "Negative"]
                idx = [col1, col2, col3, col4].index(col)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{labels[idx]}</div>
                    <div class="metric-value">—</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload & Analyze section
    with st.container():
        st.markdown("## Upload & Analyze")
        
        uploaded_file = st.file_uploader(
            "Drop Excel/CSV here or click to browse",
            type=['xlsx', 'xls', 'csv'],
            help="Upload customer comments for analysis"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Quick Analysis", key="quick", use_container_width=True):
                if uploaded_file:
                    with st.spinner("Analyzing comments..."):
                        results = process_uploaded_file(uploaded_file)
                        if results:
                            st.session_state.analysis_results = results
                            st.success("✅ Analysis complete!")
                            st.rerun()
                else:
                    st.warning("Please upload a file first")
        
        with col2:
            if st.button("📦 Batch Process", key="batch", use_container_width=True):
                if uploaded_file:
                    with st.spinner("Processing in batch mode..."):
                        results = process_uploaded_file(uploaded_file)
                        if results:
                            st.session_state.analysis_results = results
                            st.info("Batch processing complete")
                            st.rerun()
                else:
                    st.warning("Please upload a file first")
        
        with col3:
            if st.button("📥 Load Sample Data", key="sample", use_container_width=True):
                # Create sample data
                sample_comments = [
                    'El servicio es excelente, muy satisfecho',
                    'La velocidad es muy lenta en las noches',
                    'Buena atención al cliente',
                    'El servicio cae mucho durante el día',
                    'Internet funciona perfecto',
                    'Pesimo servicio, siempre con problemas',
                    'Intermitencias constantes en horario pico',
                    'Muy contento con la estabilidad',
                    'No funciona bien, muy lento',
                    'Servicio regular, podría mejorar',
                    'Excelente velocidad y estabilidad',
                    'Terrible experiencia con soporte técnico',
                    'Funciona bien la mayoría del tiempo',
                    'Demasiadas interrupciones del servicio',
                    'Precio justo por la calidad'
                ] * 10  # Multiply to get more data
                
                # Create DataFrame
                sample_df = pd.DataFrame({'comments': sample_comments})
                
                # Process sample data
                sentiments = [analyze_sentiment_simple(c) for c in sample_comments]
                sentiment_counts = Counter(sentiments)
                total = len(sample_comments)
                
                theme_counts, theme_examples = extract_themes(sample_comments)
                
                st.session_state.analysis_results = {
                    'total': total,
                    'positive_pct': round(sentiment_counts['positive'] / total * 100, 1),
                    'neutral_pct': round(sentiment_counts['neutral'] / total * 100, 1),
                    'negative_pct': round(sentiment_counts['negative'] / total * 100, 1),
                    'positive_count': sentiment_counts['positive'],
                    'neutral_count': sentiment_counts['neutral'],
                    'negative_count': sentiment_counts['negative'],
                    'theme_counts': theme_counts,
                    'theme_examples': theme_examples,
                    'file_size': 15.3,
                    'avg_length': 45,
                    'comments': sample_comments[:100],
                    'sentiments': sentiments[:100]
                }
                st.success("Sample data loaded!")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Overview tabs
    tab1, tab2, tab3 = st.tabs(["📊 Sentiment", "📈 NPS", "📉 Trends"])
    
    with tab1:
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            col1, col2 = st.columns(2)
            
            with col1:
                # Sentiment distribution chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Positive', 'Neutral', 'Negative'], 
                        y=[results['positive_count'], results['neutral_count'], results['negative_count']],
                        marker_color=['#16c784', '#f4bf4f', '#ff5e57'],
                        text=[f"{results['positive_pct']}%", f"{results['neutral_pct']}%", f"{results['negative_pct']}%"],
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Sentiment Distribution",
                    plot_bgcolor='#0f1419',
                    paper_bgcolor='#18202a',
                    font=dict(color='#e6edf3'),
                    height=300,
                    showlegend=False,
                    yaxis_title="Count",
                    xaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top themes chart
                theme_data = results['theme_counts']
                top_themes = sorted(theme_data.items(), key=lambda x: x[1], reverse=True)[:5]
                
                if top_themes:
                    themes_fig = go.Figure(data=[
                        go.Bar(
                            x=[count for _, count in top_themes], 
                            y=[theme.replace('_', ' ').title() for theme, _ in top_themes],
                            orientation='h',
                            marker_color='#4ea4ff',
                            text=[count for _, count in top_themes],
                            textposition='auto'
                        )
                    ])
                    themes_fig.update_layout(
                        title="Top Themes",
                        plot_bgcolor='#0f1419',
                        paper_bgcolor='#18202a',
                        font=dict(color='#e6edf3'),
                        height=300,
                        showlegend=False,
                        xaxis_title="Mentions",
                        yaxis_title=""
                    )
                    st.plotly_chart(themes_fig, use_container_width=True)
                else:
                    st.info("No themes detected yet")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.info("📊 Sentiment distribution will appear here after analysis")
            with col2:
                st.info("📊 Top themes will appear here after analysis")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### NPS by Theme")
            if st.session_state.analysis_results:
                st.info("NPS calculation based on sentiment mapping")
                # Simple NPS estimation from sentiment
                results = st.session_state.analysis_results
                promoters = results['positive_count']
                passives = results['neutral_count']
                detractors = results['negative_count']
                total = results['total']
                nps = ((promoters - detractors) / total * 100) if total > 0 else 0
                st.metric("Estimated NPS Score", f"{nps:.1f}")
            else:
                st.info("Upload data to see NPS analysis")
        
        with col2:
            st.markdown("### Promoters / Passives / Detractors")
            if st.session_state.analysis_results:
                results = st.session_state.analysis_results
                fig = go.Figure(data=[go.Pie(
                    labels=['Promoters', 'Passives', 'Detractors'],
                    values=[results['positive_count'], results['neutral_count'], results['negative_count']],
                    hole=.3,
                    marker_colors=['#16c784', '#f4bf4f', '#ff5e57']
                )])
                fig.update_layout(
                    plot_bgcolor='#0f1419',
                    paper_bgcolor='#18202a',
                    font=dict(color='#e6edf3'),
                    height=250,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload data to see customer categorization")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Week-over-Week Sentiment")
            st.info("Historical trend analysis requires time-series data")
        with col2:
            st.markdown("### Pain Point Trends")
            st.info("Pain point evolution requires historical data")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Themes & Pain Points
    with st.container():
        st.markdown("## Themes & Pain Points")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            theme_data = results['theme_counts']
            theme_examples = results['theme_examples']
            
            # Get top 3 themes
            top_themes = sorted(theme_data.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if top_themes:
                cols = st.columns(3)
                for idx, (theme, count) in enumerate(top_themes):
                    with cols[idx]:
                        theme_display = theme.replace('_', ' ').title()
                        if st.button(f"{theme_display} ({count})", key=f"theme_{idx}", use_container_width=True):
                            with st.expander("Examples", expanded=True):
                                examples = theme_examples.get(theme, [])
                                if examples:
                                    for example in examples[:3]:
                                        st.write(f"• {example}")
                                else:
                                    st.write("No examples available")
            else:
                st.info("No themes detected. Upload data to see theme analysis.")
        else:
            col1, col2, col3 = st.columns(3)
            for col in [col1, col2, col3]:
                with col:
                    st.button("—", disabled=True, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendations
    with st.container():
        st.markdown("## Recommendations")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Generate recommendations based on analysis
            recommendations = []
            
            # Check sentiment distribution
            if results['negative_pct'] > 30:
                recommendations.append("**Customer Experience (P1):** High negative sentiment detected. Immediate action needed to address customer concerns.")
            
            # Check themes
            theme_counts = results['theme_counts']
            if theme_counts.get('velocidad_lenta', 0) > 10:
                recommendations.append("**Network Ops (P1):** Speed issues reported frequently. Network optimization required.")
            
            if theme_counts.get('intermitencias', 0) > 10:
                recommendations.append("**Technical (P1):** Service interruptions detected. Infrastructure stability review needed.")
            
            if theme_counts.get('atencion_cliente', 0) > 5:
                recommendations.append("**Customer Care (P2):** Customer service improvements needed based on feedback.")
            
            if not recommendations:
                if results['positive_pct'] > 60:
                    recommendations.append("**Continue Current Strategy:** High customer satisfaction detected.")
                else:
                    recommendations.append("**Monitor Trends:** Continue monitoring customer feedback for emerging issues.")
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.markdown("""
            - **Upload data** to receive AI-generated recommendations
            - **Analyze patterns** in customer feedback
            - **Get actionable insights** for improvement
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Stats
    with st.container():
        st.markdown("## Data Stats")
        
        col1, col2, col3 = st.columns(3)
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            with col1:
                st.metric("File Size", f"{results['file_size']} KB")
            
            with col2:
                st.metric("Total Records", results['total'])
            
            with col3:
                st.metric("Avg Length", f"{results['avg_length']} chars")
        else:
            with col1:
                st.metric("File Size", "—")
            
            with col2:
                st.metric("Total Records", "—")
            
            with col3:
                st.metric("Avg Length", "—")