"""
Animation and Interaction Enhancements for Dark Theme
Adds smooth transitions, loading states, and micro-interactions
"""

def get_animation_css() -> str:
    """Get additional CSS for smooth animations and micro-interactions"""
    return """
    <style>
    /* === SMOOTH TRANSITIONS === */
    * {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* === LOADING STATES === */
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
    
    .loading-skeleton {
        display: inline-block;
        height: 1em;
        position: relative;
        overflow: hidden;
        background-color: #334155;
    }
    
    .loading-skeleton::after {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        transform: translateX(-100%);
        background-image: linear-gradient(
            90deg,
            rgba(255, 255, 255, 0) 0,
            rgba(255, 255, 255, 0.1) 20%,
            rgba(255, 255, 255, 0.2) 60%,
            rgba(255, 255, 255, 0)
        );
        animation: shimmer 2s infinite;
        content: '';
    }
    
    /* === PULSE ANIMATION === */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* === FADE IN ANIMATIONS === */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Apply animations to components */
    .main-header {
        animation: fadeIn 0.6s ease-out;
    }
    
    .info-card {
        animation: fadeIn 0.4s ease-out;
        animation-fill-mode: both;
    }
    
    .info-card:nth-child(1) { animation-delay: 0.1s; }
    .info-card:nth-child(2) { animation-delay: 0.2s; }
    .info-card:nth-child(3) { animation-delay: 0.3s; }
    
    [data-testid="stSidebar"] {
        animation: slideInLeft 0.4s ease-out;
    }
    
    .stSelectbox, .stButton {
        animation: slideInRight 0.3s ease-out;
    }
    
    /* === HOVER EFFECTS === */
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    
    .metric-container:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) scale(1.02);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* === FOCUS STATES === */
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {
        transform: scale(1.01);
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.3);
    }
    
    /* === LOADING SPINNERS === */
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(96, 165, 250, 0.3);
        border-radius: 50%;
        border-top-color: #60a5fa;
        animation: spin 1s ease-in-out infinite;
    }
    
    /* === PROGRESS BAR ANIMATIONS === */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #60a5fa, #3b82f6);
        background-size: 200% 100%;
        animation: progressShine 2s ease-in-out infinite;
    }
    
    @keyframes progressShine {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }
    
    /* === DATA TABLE ANIMATIONS === */
    .stDataFrame tbody tr {
        transition: background-color 0.2s ease;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #334155 !important;
    }
    
    /* === ALERT ANIMATIONS === */
    .stAlert {
        animation: slideInRight 0.3s ease-out;
        border-left: 4px solid;
    }
    
    .stSuccess {
        border-left-color: #4ade80;
    }
    
    .stWarning {
        border-left-color: #fbbf24;
    }
    
    .stError {
        border-left-color: #f87171;
    }
    
    .stInfo {
        border-left-color: #38bdf8;
    }
    
    /* === UPLOAD AREA ANIMATIONS === */
    .upload-section {
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        transform: scale(1.01);
    }
    
    .stFileUploader:hover {
        transform: scale(1.01);
    }
    
    /* === METRIC ANIMATIONS === */
    .stMetric [data-testid="metric-value"] {
        transition: all 0.3s ease;
    }
    
    .stMetric:hover [data-testid="metric-value"] {
        transform: scale(1.05);
        color: #60a5fa !important;
    }
    
    /* === TAB ANIMATIONS === */
    .stTabs [data-baseweb="tab"] {
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(96, 165, 250, 0.1) !important;
    }
    
    .stTabs [aria-selected="true"] {
        transform: translateY(-1px);
    }
    
    /* === EXPANDER ANIMATIONS === */
    .streamlit-expanderHeader {
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #475569 !important;
        transform: translateX(2px);
    }
    
    /* === SIDEBAR ANIMATIONS === */
    [data-testid="stSidebar"] .stSelectbox:hover {
        transform: translateX(2px);
    }
    
    /* === SCROLL ANIMATIONS === */
    @keyframes scrollGlow {
        0% { box-shadow: inset 0 0 5px rgba(96, 165, 250, 0.3); }
        50% { box-shadow: inset 0 0 10px rgba(96, 165, 250, 0.5); }
        100% { box-shadow: inset 0 0 5px rgba(96, 165, 250, 0.3); }
    }
    
    ::-webkit-scrollbar-thumb:active {
        animation: scrollGlow 0.3s ease-in-out;
    }
    
    /* === TYPING ANIMATION === */
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    .typing-animation {
        overflow: hidden;
        border-right: 2px solid #60a5fa;
        white-space: nowrap;
        margin: 0 auto;
        animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #60a5fa; }
    }
    
    /* === STATUS INDICATOR ANIMATIONS === */
    .status-indicator {
        animation: fadeIn 0.4s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .status-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .status-indicator:hover::before {
        left: 100%;
    }
    
    /* === ENHANCED BUTTON RIPPLE === */
    .stButton > button {
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    /* === REDUCED MOTION SUPPORT === */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* === DARK MODE SPECIFIC GLOW EFFECTS === */
    .main-header {
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(96, 165, 250, 0.1);
    }
    
    .info-card:hover {
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(96, 165, 250, 0.1);
    }
    
    .stButton > button:hover {
        box-shadow: 
            0 5px 15px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(59, 130, 246, 0.3);
    }
    </style>
    """