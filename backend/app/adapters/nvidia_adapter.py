import httpx
from typing import Optional, List
from app.adapters.llm_base import BaseLLMAdapter
from app.core.config import settings
from app.adapters.mock_llm_adapter import MockLLMAdapter
from app.core.logging import logger

class NvidiaAdapter(BaseLLMAdapter):
    """
    NVIDIA NIM API Adapter (meta/llama-3.1-70b-instruct, nvidia/nemotron).
    Provides frontier teacher inference and enterprise multi-agent execution.
    Falls back gracefully to MockLLMAdapter if offline or key is missing.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.NVIDIA_DEFAULT_MODEL
        self.api_key = settings.NVIDIA_API_KEY
        self.base_url = settings.NVIDIA_BASE_URL.rstrip('/')
        self.fallback = MockLLMAdapter()

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        if not self.api_key:
            return await self.fallback.generate(prompt, system_prompt, json_mode)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 1024,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    logger.warning(f"NVIDIA NIM API responded with status {res.status_code}: {res.text}. Falling back.")
                    return await self.fallback.generate(prompt, system_prompt, json_mode)
        except Exception as e:
            logger.warning(f"NVIDIA NIM invocation error: {e}. Falling back gracefully.")
            return await self.fallback.generate(prompt, system_prompt, json_mode)

    async def get_embedding(self, text: str) -> List[float]:
        return await self.fallback.get_embedding(text)
