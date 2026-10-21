from app.adapters.llm_base import BaseLLMAdapter
from app.adapters.mock_llm_adapter import MockLLMAdapter
from app.adapters.ollama_adapter import OllamaAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.adapters.nvidia_adapter import NvidiaAdapter
from app.config import settings

def get_llm_adapter(provider_name: str = None) -> BaseLLMAdapter:
    provider = (provider_name or settings.DEFAULT_LLM_PROVIDER or "").lower()
    
    if "gemini" in provider:
        return GeminiAdapter()
    elif "nvidia" in provider:
        return NvidiaAdapter()
    elif "ollama" in provider:
        return OllamaAdapter()
    elif provider == "mock":
        return MockLLMAdapter()
    else:
        # Default fallback: If Gemini API key is configured, use Gemini
        if settings.GEMINI_API_KEY:
            return GeminiAdapter()
        return MockLLMAdapter()

