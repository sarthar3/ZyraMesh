from app.adapters.llm_base import BaseLLMAdapter
from app.adapters.mock_llm_adapter import MockLLMAdapter
from app.adapters.ollama_adapter import OllamaAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.adapters.nvidia_adapter import NvidiaAdapter
from app.config import settings

def get_llm_adapter(provider_name: str = None) -> BaseLLMAdapter:
    provider = (provider_name or settings.DEFAULT_LLM_PROVIDER).lower()
    if provider == "ollama":
        return OllamaAdapter()
    elif provider == "gemini":
        return GeminiAdapter()
    elif provider == "nvidia":
        return NvidiaAdapter()
    else:
        return MockLLMAdapter()

