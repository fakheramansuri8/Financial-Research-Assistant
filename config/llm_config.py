"""
Centralized LLM configuration for all agents.
Supports cloud providers (Gemini, OpenAI, etc.) and local models (Ollama, LM Studio).
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_config():
    """
    Get LLM configuration from environment variables.
    
    Returns:
        dict: Configuration dictionary with provider, model, API key, and base URL
    """
    provider = os.getenv("AICALL_AI_PROVIDER", "gemini")
    model = os.getenv("AICALL_AI_MODEL", "gemini/gemini-1.5-flash")
    api_key = os.getenv("AICALL_AI_API_KEY", "")
    base_url = os.getenv("AICALL_AI_BASE_URL", "")
    
    # Build LiteLLM model string
    # Format: provider/model_name or just model_name if it already includes provider
    if "/" not in model and provider:
        litellm_model = f"{provider}/{model}"
    else:
        litellm_model = model
    
    config = {
        "model": litellm_model,
        "api_key": api_key if api_key else None,
        "base_url": base_url if base_url else None,
    }
    
    return config


def create_llm_instance():
    """
    Create a LiteLLM instance with configured settings.
    
    Returns:
        str: LiteLLM model string ready to use with CrewAI
    """
    config = get_llm_config()
    
    # For CrewAI, we pass the model string directly
    # LiteLLM will handle the routing based on the model prefix
    return config["model"]


def get_llm_info():
    """
    Get human-readable info about current LLM configuration.
    
    Returns:
        str: Formatted string with LLM details
    """
    config = get_llm_config()
    
    provider = config["model"].split("/")[0] if "/" in config["model"] else "unknown"
    model_name = config["model"].split("/")[-1] if "/" in config["model"] else config["model"]
    
    info = f"""
LLM Configuration:
  Provider: {provider}
  Model: {model_name}
  Full Model String: {config['model']}
  Base URL: {config['base_url'] or 'Default'}
  API Key: {'Set' if config['api_key'] else 'Not set'}
    """.strip()
    
    return info


if __name__ == "__main__":
    print(get_llm_info())
