import streamlit as st
import os
from dotenv import load_dotenv
from crew.research_crew import create_research_crew

# Load environment variables
load_dotenv()

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
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 10px 14px;
    }
    .stButton > button {
        background-color: #4a90e2;
        color: white;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 500;
        width: 100%;
    }
    .report-container {
        background-color: #fafbfc;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Financial Research Assistant")
st.markdown("""
    Generate professional investment research reports using AI agents.
    *Powered by CrewAI, Tavily, and Google Gemini.*
""")

# Check for API Keys in environment (Hugging Face Secrets)
tavily_key = os.getenv("TAVILY_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not tavily_key or not gemini_key:
    st.warning("⚠️ **API Keys Missing**: Please set `TAVILY_API_KEY` and `GEMINI_API_KEY` in your environment variables or Hugging Face Secrets.")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    company = st.text_input("Company Name or Ticker", placeholder="e.g., Apple, AAPL, Tesla")
with col2:
    ticker = st.text_input("Ticker (Optional)", placeholder="AAPL")

if st.button("Generate Research Report", type="primary"):
    if not (tavily_key and gemini_key):
        st.error("Cannot proceed without API keys.")
    elif not company:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("AI agents are researching... This usually takes 45-60 seconds."):
            try:
                # Initialize Crew directly (Bypassing FastAPI for deployment simplicity)
                crew = create_research_crew()
                
                inputs = {"company": company}
                if ticker:
                    inputs["ticker"] = ticker
                
                # Run the crew
                result = crew.kickoff(inputs=inputs)
                report_text = str(result)
                
                # Display Results
                st.success(f"Analysis complete for {company}!")
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown("### Investment Research Report")
                st.markdown("---")
                st.markdown(report_text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="Download Report (.md)",
                    data=report_text,
                    file_name=f"{company.lower().replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 How it works")
    st.info("""
    This app uses **CrewAI** to orchestrate 4 specialized agents:
    1. **Search Agent**: Finds latest news.
    2. **Finance Agent**: Pulls market data.
    3. **Analyst Agent**: Evaluates sentiment.
    4. **Writer Agent**: Compiles the final report.
    """)
    st.markdown("---")
    st.caption("Built with ❤️ for the Fintech Community")
