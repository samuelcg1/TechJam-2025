"""
Streamlit Web Application for Geo-Compliance Analysis

This module provides a user-friendly web interface for uploading CSV files
and analyzing features for geo-specific compliance requirements.
"""

import streamlit as st
import pandas as pd
import os
import tempfile
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from compliance_analyzer import ComplianceAnalyzer


def main():
    """
    Main Streamlit application function.
    """
    st.set_page_config(
        page_title="Geo-Compliance Analysis Tool",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Geo-Compliance Analysis Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze features for geo-specific compliance requirements using AI</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. You can also set it as an environment variable OPENAI_API_KEY."
        )
        
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        # Model selection
        model = st.selectbox(
            "LLM Model",
            ["gpt-4", "gpt-3.5-turbo"],
            help="Select the OpenAI model to use for analysis"
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        use_rule_based = st.checkbox("Enable Rule-Based Analysis", value=True, help="Use keyword-based analysis as backup")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, help="Minimum confidence for automatic decisions")
        
        # Information
        st.subheader("ℹ️ About")
        st.info("""
        This tool analyzes features to determine if they require geo-specific compliance logic.
        
        **Supported Regulations:**
        - DSA (Digital Services Act - EU)
        - COPPA (Children's Online Privacy Protection Act - US)
        - GDPR (General Data Protection Regulation - EU)
        - California Protecting Our Kids Act
        - Florida Online Protections for Minors
        - Utah Social Media Regulation Act
        - NCMEC reporting requirements
        - CCPA (California Consumer Privacy Act)
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Features")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with columns: Title, Description, Documents (optional)"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)
                
                # Display preview
                st.subheader("📋 Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
                # Validate columns
                required_columns = ['Title', 'Description']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {missing_columns}")
                    st.info("Your CSV must contain at least 'Title' and 'Description' columns.")
                else:
                    st.success(f"✅ CSV file loaded successfully! Found {len(df)} features to analyze.")
                    
                    # Analysis button
                    if st.button("🚀 Start Analysis", type="primary"):
                        if not api_key:
                            st.error("❌ OpenAI API key is required. Please enter it in the sidebar.")
                        else:
                            with st.spinner("🔍 Analyzing features..."):
                                try:
                                    # Initialize analyzer
                                    analyzer = ComplianceAnalyzer(api_key=api_key)
                                    
                                    # Save uploaded file temporarily
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                                        df.to_csv(tmp_file.name, index=False)
                                        
                                        # Analyze the CSV
                                        results_df = analyzer.analyze_csv(tmp_file.name)
                                        
                                        # Clean up temporary file
                                        os.unlink(tmp_file.name)
                                    
                                    # Display results
                                    st.success("✅ Analysis completed!")
                                    
                                    # Show results
                                    st.subheader("📊 Analysis Results")
                                    st.dataframe(results_df, use_container_width=True)
                                    
                                    # Download results
                                    csv_data = results_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Results",
                                        data=csv_data,
                                        file_name="compliance_analysis_results.csv",
                                        mime="text/csv"
                                    )
                                    
                                    # Summary statistics
                                    st.subheader("📈 Summary Statistics")
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        yes_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'Yes'])
                                        st.metric("Features Needing Compliance", yes_count)
                                    
                                    with col2:
                                        no_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'No'])
                                        st.metric("Features Not Needing Compliance", no_count)
                                    
                                    with col3:
                                        review_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'Needs Review'])
                                        st.metric("Features Needing Review", review_count)
                                    
                                    # Detailed breakdown
                                    st.subheader("🔍 Detailed Breakdown")
                                    
                                    # Features needing compliance
                                    if yes_count > 0:
                                        st.markdown("**Features Requiring Geo-Compliance Logic:**")
                                        yes_features = results_df[results_df['Needs Geo-Compliance Logic?'] == 'Yes']
                                        for _, row in yes_features.iterrows():
                                            with st.expander(f"🔴 {row['Title']}"):
                                                st.write(f"**Reasoning:** {row['Reasoning']}")
                                                if row['Related Regulations']:
                                                    st.write(f"**Related Regulations:** {', '.join(eval(row['Related Regulations'])) if isinstance(row['Related Regulations'], str) else ', '.join(row['Related Regulations'])}")
                                                if row['Rule-Based Keywords']:
                                                    st.write(f"**Keywords Found:** {row['Rule-Based Keywords']}")
                                    
                                    # Features needing review
                                    if review_count > 0:
                                        st.markdown("**Features Needing Manual Review:**")
                                        review_features = results_df[results_df['Needs Geo-Compliance Logic?'] == 'Needs Review']
                                        for _, row in review_features.iterrows():
                                            with st.expander(f"🟡 {row['Title']}"):
                                                st.write(f"**Reasoning:** {row['Reasoning']}")
                                                if row['Related Regulations']:
                                                    st.write(f"**Related Regulations:** {', '.join(eval(row['Related Regulations'])) if isinstance(row['Related Regulations'], str) else ', '.join(row['Related Regulations'])}")
                                    
                                except Exception as e:
                                    st.error(f"❌ Analysis failed: {str(e)}")
                                    st.info("Please check your API key and try again.")
                
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
    
    with col2:
        st.header("📝 Sample CSV Format")
        
        # Create sample data
        sample_data = {
            'Title': [
                'Age Verification System',
                'Location-Based Content Filtering',
                'User Profile Management',
                'Live Streaming Feature',
                'E-commerce Integration'
            ],
            'Description': [
                'Implement age gates for users under 18 to comply with COPPA and state regulations',
                'Block content based on user location to meet regional compliance requirements',
                'Basic user profile creation and management functionality',
                'Allow users to stream live video content to their followers',
                'Enable users to purchase products directly through the platform'
            ],
            'Documents': [
                'age_verification_specs.pdf',
                'geo_blocking_requirements.txt',
                '',
                'live_streaming_policy.pdf',
                'ecommerce_compliance.pdf'
            ]
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        
        # Download sample
        sample_csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=sample_csv,
            file_name="sample_features.csv",
            mime="text/csv"
        )
        
        st.markdown("""
        **Required Columns:**
        - **Title**: Feature name
        - **Description**: Detailed feature description
        
        **Optional Columns:**
        - **Documents**: Path to PDF files or additional text
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built for TikTok TechJam 2025 | Geo-Compliance Analysis Tool</p>
        <p>This tool helps identify features that require geo-specific compliance logic based on various regulations.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
