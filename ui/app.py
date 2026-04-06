import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Financial Research Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional light theme
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4a90e2;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 12px 24px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #357abd;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
    }
    
    /* Report container */
    .report-container {
        background-color: #fafbfc;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        margin-top: 20px;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 6px;
        padding: 12px 16px;
    }
    
    /* Error messages */
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        border-radius: 6px;
        padding: 12px 16px;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
        border-radius: 6px;
        padding: 12px 16px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e1e4e8;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 500;
    }
    
    .stDownloadButton > button:hover {
        background-color: #218838;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4a90e2 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Financial Research Assistant")
st.markdown("""
    Generate professional investment research reports using AI agents.
    
    Enter a company name or ticker symbol below to begin analysis.
""")

# API base URL (change this if deploying)
API_BASE_URL = "http://localhost:8000"

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    company = st.text_input(
        "Company Name or Ticker",
        placeholder="e.g., Apple, AAPL, Telstra, TLS.AX",
        help="Enter either the company name or stock ticker symbol"
    )
with col2:
    ticker = st.text_input(
        "Ticker (Optional)",
        placeholder="AAPL",
        help="Specific ticker symbol if known"
    )

# Research button
if st.button("Generate Research Report", type="primary", use_container_width=True):
    if not company:
        st.warning("Please enter a company name or ticker.")
    else:
        with st.spinner("AI agents are researching... This may take 30-60 seconds."):
            try:
                # Prepare request payload
                payload = {"company": company}
                if ticker:
                    payload["ticker"] = ticker
                
                # Call API
                response = requests.post(
                    f"{API_BASE_URL}/research",
                    json=payload,
                    timeout=120  # 2 minute timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display success message
                    st.success(f"Research completed for {result.get('company', company)}")
                    
                    # Display report in a styled container
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown("### Investment Research Report")
                    st.markdown("---")
                    
                    # Render the markdown report
                    report_text = result.get('report', 'No report generated.')
                    st.markdown(report_text)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add download button
                    st.download_button(
                        label="Download Report",
                        data=report_text,
                        file_name=f"{company.replace(' ', '_')}_research_report.md",
                        mime="text/markdown"
                    )
                    
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Error: {error_detail}")
                    
            except requests.exceptions.Timeout:
                st.error("Request timed out. The research is taking longer than expected. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the API server. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

# Sidebar with information
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
        This tool uses a multi-agent architecture:
        
        - **News Agent**: Fetches latest financial news
        - **Financials Agent**: Analyzes key metrics
        - **Sentiment Agent**: Assesses market sentiment
        - **Report Agent**: Generates professional research report
    """)
    
    st.markdown("---")
    st.markdown("### Links")
    st.markdown("[API Documentation](http://localhost:8000/docs)")

# Footer
st.markdown("---")
st.markdown(
    "<center><small>Built with CrewAI, FastAPI, and Streamlit</small></center>",
    unsafe_allow_html=True
)
