# 📊 Multi-Agent Financial Research Assistant

An AI-powered investment research system that automatically generates professional equity research reports using a multi-agent architecture.

## 🎯 Overview

This tool orchestrates multiple specialized AI agents to:
- 🔍 **Fetch latest news** from financial sources via Tavily API
- 📈 **Analyze financial metrics** using Yahoo Finance data
- 💭 **Assess market sentiment** from news coverage
- 📝 **Generate structured reports** with investment recommendations

Perfect for demonstrating multi-agent system design, full-stack development skills, and practical AI applications in finance.

## ✨ Features

- **Multi-Agent Architecture**: 4 specialized agents working in sequence (CrewAI)
- **Real-time Data**: Live news and financial data from external APIs
- **Professional Reports**: Markdown-formatted investment research suitable for institutional investors
- **REST API**: FastAPI backend with automatic OpenAPI documentation
- **Interactive UI**: Clean Streamlit interface with report download capability
- **Australian Market Support**: Works with ASX tickers (e.g., TLS.AX, CBA.AX)

## 🏗️ Architecture

```
┌─────────────┐
│  Streamlit   │  ← User Interface
│    Frontend  │
└──────┬──────┘
       │ HTTP POST /research
       ▼
┌─────────────┐
│   FastAPI    │  ← Backend API
│   Server     │
└──────┬──────┘
       │ Orchestrates
       ▼
┌─────────────┐
│   CrewAI     │  ← Agent Orchestration
│    Crew      │
└──┬──┬──┬──┬──┘
   │  │  │  │
   ▼  ▼  ▼  ▼
┌────┐┌────┐┌────┐┌────┐
│News││Fin ││Sent││Rpt │  ← Specialized Agents
│Agent│Agent│Agent│Agent│
└─┬──┘└─┬──┘└────┘└────┘
  │     │
  ▼     ▼
┌────┐┌──────┐
│Tavily││Yahoo │  ← External Tools/APIs
│ API  ││Finance│
└────┘└──────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- API keys for:
  - **Tavily API** (news search): Get free key at https://tavily.com
  - **Google Gemini API** (LLM): Get free key at https://makersuite.google.com

### Installation

1. **Clone the repository**
   ```bash
   cd /home/fakhera/Development/marketintel-ai-engine
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # TAVILY_API_KEY=your_actual_key_here
   # GEMINI_API_KEY=your_actual_key_here
   ```

### Running the Application

You need to run **both** the backend API and frontend UI:

**Terminal 1 - Start FastAPI Backend:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run ui/app.py
```

Open your browser to `http://localhost:8501` and start generating reports!

## 📖 Usage Example

1. Enter a company name or ticker (e.g., "Telstra" or "TLS.AX")
2. Click "Generate Research Report"
3. Wait 30-60 seconds while agents work
4. View and download the generated report

### Sample Companies to Try

- **Australian**: Telstra (TLS.AX), Commonwealth Bank (CBA.AX), BHP (BHP.AX)
- **US**: Apple (AAPL), Tesla (TSLA), Microsoft (MSFT)

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

## 📁 Project Structure

```
marketintel-ai-engine/
├── agents/                 # CrewAI agent definitions
│   ├── news_agent.py      # News fetching agent
│   ├── financials_agent.py # Financial analysis agent
│   ├── sentiment_agent.py  # Sentiment analysis agent
│   └── report_agent.py    # Report writing agent
├── tools/                  # Custom tool wrappers
│   ├── search_tool.py     # Tavily API integration
│   └── finance_tool.py    # Yahoo Finance integration
├── config/                 # Configuration management
│   └── llm_config.py      # Flexible LLM configuration
├── api/                    # FastAPI backend
│   ├── main.py            # API endpoints
│   └── schemas.py         # Pydantic models
├── crew/                   # CrewAI orchestrator
│   └── research_crew.py   # Crew configuration
├── ui/                     # Streamlit frontend
│   └── app.py             # Web interface
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create from .env.example)
└── README.md              # This file
```

## 🔧 Configuration

### API Keys

Get your free API keys:

1. **Tavily API** (1000 searches/month free):
   - Sign up at https://tavily.com
   - Copy your API key to `.env`

2. **Gemini API** (free tier available):
   - Sign up at https://makersuite.google.com
   - Create API key and add to `.env`

### LLM Configuration (Flexible & Changeable!)

The system supports **100+ LLM providers** including cloud and local models. All configuration is done via environment variables - **no code changes needed!**

Edit `.env` to switch models:

```bash
# Default: Google Gemini (Free)
AICALL_AI_PROVIDER=gemini
AICALL_AI_MODEL=gemini/gemini-1.5-flash
AICALL_AI_API_KEY=your_gemini_key
AICALL_AI_BASE_URL=

# Switch to Ollama (Local, Free)
AICALL_AI_PROVIDER=ollama
AICALL_AI_MODEL=llama3.2
AICALL_AI_API_KEY=
AICALL_AI_BASE_URL=http://localhost:11434

# Switch to LM Studio (Local)
AICALL_AI_PROVIDER=openai
AICALL_AI_MODEL=qwen2.5-7b-instruct
AICALL_AI_API_KEY=sk-dummy-key
AICALL_AI_BASE_URL=http://localhost:1234/v1

# Switch to Custom Endpoint (Your Example)
AICALL_AI_PROVIDER=openai
AICALL_AI_MODEL=qwen2.5-72b-instruct
AICALL_AI_API_KEY=sk-V6Tu6Vo5R9CQ0WzCAcruOw
AICALL_AI_BASE_URL=http://45.195.82.195:4000/v1
```

**Supported Providers:**
- ✅ **Cloud:** Gemini, OpenAI, Anthropic Claude, Azure, AWS Bedrock
- ✅ **Local:** Ollama, LM Studio, vLLM, Text Generation WebUI
- ✅ **Aggregators:** OpenRouter (100+ models), Together AI
- ✅ **Custom:** Any OpenAI-compatible endpoint

See `LLM_CONFIG_GUIDE.md` for detailed setup instructions for each provider.

### Optional: Use Different Models Per Agent

By default, all agents use the same LLM. You can customize individual agents by editing the agent files in `agents/` directory.

## 🌐 Deployment

### Deploy to Render (Free Tier)

1. Push code to GitHub
2. Connect repository to Render
3. Add environment variables in Render dashboard
4. Deploy!

See `render.yaml` in the plan for configuration details.

### Deploy to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Choose "Streamlit" as SDK
3. Upload your code
4. Add secrets (API keys) in Space settings

## 🎓 What This Demonstrates

This project showcases:

1. **Multi-Agent System Design**: Practical CrewAI implementation with task delegation
2. **Tool Integration**: Custom wrappers for external APIs (Tavily, yfinance)
3. **Full-Stack Development**: FastAPI backend + Streamlit frontend
4. **Production Practices**: Error handling, environment config, testing, deployment readiness
5. **Business Acumen**: Solves real-world problem (investment research automation)
6. **Live Demo Capability**: Type "Telstra" → watch agents work → get professional report

Perfect for portfolio projects and technical interviews in fintech/AI roles!

## 🛠️ Tech Stack

- **Agent Framework**: CrewAI
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **LLM Routing**: LiteLLM (supports 100+ providers)
- **Data Sources**: Tavily API (news), Yahoo Finance (financials)
- **Testing**: pytest

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

- `GET /health` - Health check
- `POST /research` - Generate research report

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - feel free to use this for learning, portfolio projects, or commercial applications.

## 🙏 Acknowledgments

- CrewAI team for the excellent agent orchestration framework
- Tavily for providing powerful search API
- Yahoo Finance for free financial data access
- Google Gemini for fast, cost-effective LLM inference

---

**Built with ❤️ for the Australian fintech community**

For questions or feedback, please open an issue on GitHub.
