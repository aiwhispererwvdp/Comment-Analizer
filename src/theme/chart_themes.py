"""
Chart and Data Visualization Themes for Dark Theme
Enhances Plotly and Streamlit charts with dark theme styling
"""

def get_dark_plotly_theme() -> dict:
    """Get enhanced Plotly theme configuration for dark mode with improved contrast"""
    return {
        'layout': {
            'paper_bgcolor': '#1e2a3a',  # Enhanced card background
            'plot_bgcolor': '#0f1419',  # Deeper plot background
            'font': {
                'color': '#e2e8f0',      # Improved text contrast
                'family': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                'size': 14               # Larger base font size
            },
            'colorway': [
                '#4299e1',  # Enhanced primary blue
                '#48bb78',  # Enhanced success green  
                '#ed8936',  # Enhanced warning orange
                '#e53e3e',  # Enhanced error red
                '#9f7aea',  # Enhanced purple
                '#38b2ac',  # Enhanced teal
                '#f093fb',  # Enhanced pink
                '#4fd1c7'   # Enhanced cyan
            ],
            'xaxis': {
                'gridcolor': '#4a5568',     # More visible grid
                'linecolor': '#718096',     # Stronger axis lines
                'tickcolor': '#a0aec0',     # More visible ticks
                'title': {
                    'font': {'color': '#e2e8f0', 'size': 16},
                    'standoff': 20
                },
                'tickfont': {'color': '#cbd5e1', 'size': 12},
                'showgrid': True,
                'zeroline': True,
                'zerolinecolor': '#718096'
            },
            'yaxis': {
                'gridcolor': '#4a5568',     # More visible grid
                'linecolor': '#718096',     # Stronger axis lines
                'tickcolor': '#a0aec0',     # More visible ticks
                'title': {
                    'font': {'color': '#e2e8f0', 'size': 16},
                    'standoff': 20
                },
                'tickfont': {'color': '#cbd5e1', 'size': 12},
                'showgrid': True,
                'zeroline': True,
                'zerolinecolor': '#718096'
            },
            'legend': {
                'font': {'color': '#e2e8f0', 'size': 13},
                'bgcolor': 'rgba(30, 42, 58, 0.9)',
                'bordercolor': '#718096',
                'borderwidth': 1,
                'borderradius': 8,
                'itemsizing': 'constant'
            },
            'title': {
                'font': {'color': '#ffffff', 'size': 20, 'family': 'Inter'},
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top'
            },
            'margin': {'l': 60, 'r': 40, 't': 80, 'b': 60},
            'showlegend': True
        }
    }

def get_chart_css() -> str:
    """Get enhanced CSS for better chart styling addressing visual critique"""
    return """
    <style>
    /* === ENHANCED CHART CONTAINERS === */
    .stPlotlyChart {
        background: linear-gradient(135deg, #1e2a3a 0%, #253344 100%) !important;
        border: 1px solid #4a5568;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stPlotlyChart::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4299e1, #38b2ac, #9f7aea);
        border-radius: 0.75rem 0.75rem 0 0;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.5);
        transform: translateY(-4px);
        border-color: #4299e1;
    }
    
    /* === BAR CHART IMPROVEMENTS === */
    .stBarChart {
        background: #1e293b !important;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* === LINE CHART IMPROVEMENTS === */
    .stLineChart {
        background: #1e293b !important;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* === AREA CHART IMPROVEMENTS === */
    .stAreaChart {
        background: #1e293b !important;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* === METRIC VISUALIZATION === */
    .metric-chart {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .metric-chart::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #60a5fa, #4ade80, #fbbf24);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* === DATA TABLE ENHANCEMENTS === */
    .stDataFrame table {
        background: #1e293b !important;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 1rem 0.75rem !important;
        border-bottom: 2px solid #60a5fa !important;
    }
    
    .stDataFrame td {
        background: #1e293b !important;
        color: #f1f5f9 !important;
        padding: 0.75rem !important;
        border-bottom: 1px solid #334155 !important;
        transition: background-color 0.2s ease;
    }
    
    .stDataFrame tr:hover td {
        background: #334155 !important;
    }
    
    .stDataFrame tr:nth-child(even) td {
        background: rgba(51, 65, 85, 0.3) !important;
    }
    
    /* === PROGRESS BAR ENHANCEMENTS === */
    .stProgress {
        background: #334155 !important;
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #3b82f6, #60a5fa, #3b82f6) !important;
        background-size: 200% 100%;
        animation: progressFlow 2s ease-in-out infinite;
        border-radius: 1rem;
        position: relative;
    }
    
    .stProgress > div > div > div::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: progressShine 2s ease-in-out infinite;
    }
    
    @keyframes progressFlow {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    @keyframes progressShine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* === KPI CARDS === */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #60a5fa, #4ade80);
    }
    
    .kpi-value {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-label {
        font-size: 1rem;
        color: #cbd5e1;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-change {
        font-size: 0.875rem;
        margin-top: 0.5rem;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        display: inline-block;
    }
    
    .kpi-change.positive {
        background: rgba(74, 222, 128, 0.2);
        color: #4ade80;
    }
    
    .kpi-change.negative {
        background: rgba(248, 113, 113, 0.2);
        color: #f87171;
    }
    
    /* === CHART LEGEND IMPROVEMENTS === */
    .plotly .legend {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid #475569 !important;
        border-radius: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* === TOOLTIP STYLING === */
    .plotly .hoverlabel {
        background: #1e293b !important;
        border: 1px solid #60a5fa !important;
        border-radius: 0.5rem;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    
    /* === STATUS CHARTS === */
    .status-chart {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .status-item {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .status-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    
    .status-item.success {
        border-left: 4px solid #4ade80;
    }
    
    .status-item.warning {
        border-left: 4px solid #fbbf24;
    }
    
    .status-item.error {
        border-left: 4px solid #f87171;
    }
    
    .status-item.info {
        border-left: 4px solid #38bdf8;
    }
    
    /* === RESPONSIVE CHART SIZING === */
    @media (max-width: 768px) {
        .stPlotlyChart {
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .kpi-card {
            padding: 1rem;
        }
        
        .kpi-value {
            font-size: 2rem;
        }
        
        .status-chart {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """