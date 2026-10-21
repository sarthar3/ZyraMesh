import asyncio
import logging
from typing import Optional
from app.adapters.llm_base import BaseLLMAdapter
from app.config import settings
from app.adapters.mock_llm_adapter import MockLLMAdapter

logger = logging.getLogger(__name__)

class GeminiAdapter(BaseLLMAdapter):
    """
    Gemini LLM provider using google-genai SDK.
    Executes in background thread pool and gracefully falls back to candidate models
    or MockLLMAdapter if API key is not configured or fails.
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.GEMINI_DEFAULT_MODEL or "gemini-flash-latest"
        self.api_key = settings.GEMINI_API_KEY
        self.fallback = MockLLMAdapter()

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        if not self.api_key:
            return await self.fallback.generate(prompt, system_prompt, json_mode)
        
        from google import genai
        client = genai.Client(api_key=self.api_key)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        # Candidate models to try in case of temporary provider maintenance or model deprecation
        candidate_models = [self.model_name, "gemini-flash-latest", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
        seen_models = set()
        
        for candidate in candidate_models:
            if not candidate or candidate in seen_models:
                continue
            seen_models.add(candidate)
            try:
                res = await asyncio.to_thread(
                    client.models.generate_content,
                    model=candidate,
                    contents=full_prompt,
                )
                if res and res.text:
                    return res.text
            except Exception as e:
                logger.warning(f"Gemini generation with {candidate} failed: {e}. Trying fallback...")
                continue

        logger.error("All Gemini candidate models failed. Falling back to deterministic mock.")
        return await self.fallback.generate(prompt, system_prompt, json_mode)

    async def get_embedding(self, text: str) -> list[float]:
        return await self.fallback.get_embedding(text)
