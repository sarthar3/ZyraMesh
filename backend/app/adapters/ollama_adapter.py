import httpx
from typing import Optional
from app.adapters.llm_base import BaseLLMAdapter
from app.config import settings
from app.adapters.mock_llm_adapter import MockLLMAdapter

class OllamaAdapter(BaseLLMAdapter):
    """
    Ollama local LLM provider supporting qwen2.5:1.5b-instruct.
    Falls back gracefully to MockLLMAdapter if server is unreachable.
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.OLLAMA_DEFAULT_MODEL
        self.base_url = settings.OLLAMA_BASE_URL
        self.fallback = MockLLMAdapter()

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                }
                if system_prompt:
                    payload["system"] = system_prompt
                if json_mode:
                    payload["format"] = "json"

                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
        except Exception:
            pass
        
        # Fallback to mock adapter
        return await self.fallback.generate(prompt, system_prompt, json_mode)

    async def get_embedding(self, text: str) -> list[float]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                payload = {"model": self.model_name, "prompt": text}
                response = await client.post(f"{self.base_url}/api/embeddings", json=payload)
                if response.status_code == 200:
                    return response.json().get("embedding", [])
        except Exception:
            pass
        return await self.fallback.get_embedding(text)
