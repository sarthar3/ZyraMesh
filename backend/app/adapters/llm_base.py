from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLMAdapter(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        """Generate response from backend LLM"""
        pass
    
    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        """Generate text embedding vector"""
        pass
