from typing import Optional
from app.adapters.llm_base import BaseLLMAdapter
from app.config import settings
from app.adapters.mock_llm_adapter import MockLLMAdapter

class GeminiAdapter(BaseLLMAdapter):
    """
    Gemini LLM provider using google-genai SDK.
    Falls back gracefully to MockLLMAdapter if API key is not configured or fails.
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.GEMINI_DEFAULT_MODEL
        self.api_key = settings.GEMINI_API_KEY
        self.fallback = MockLLMAdapter()

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        if not self.api_key:
            return await self.fallback.generate(prompt, system_prompt, json_mode)
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            res = client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
            )
            return res.text
        except Exception:
            return await self.fallback.generate(prompt, system_prompt, json_mode)

    async def get_embedding(self, text: str) -> list[float]:
        return await self.fallback.get_embedding(text)
