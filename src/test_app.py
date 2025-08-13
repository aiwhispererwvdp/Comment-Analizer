"""
Test minimal Streamlit app to check basic functionality
"""

import streamlit as st
import pandas as pd

def main():
    st.set_page_config(
        page_title="Personal Paraguay Comments Analysis",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Personal Paraguay Fiber Comments Analysis")
    
    # Simple sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Data Upload", "Analysis Dashboard", "Settings", "About"]
    )
    
    if page == "Data Upload":
        st.header("Data Upload")
        st.write("Upload your Excel or CSV file here")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['xlsx', 'csv', 'json', 'txt'],
            help="Upload Excel (.xlsx), CSV (.csv), JSON (.json), or text (.txt) files"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
    elif page == "Analysis Dashboard":
        st.header("Analysis Dashboard")
        st.write("This is where analysis results will be shown")
        
    elif page == "Settings":
        st.header("Settings")
        st.write("Configuration options")
        
    elif page == "About":
        st.header("About")
        st.write("Personal Paraguay Fiber Comments Analysis System")

if __name__ == "__main__":
    main()