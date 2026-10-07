import time
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class AgentResult(BaseModel):
    success: bool
    output: Any
    confidence: float = 0.90
    uncertainty: float = 0.10
    evidence: Optional[Dict[str, Any]] = None
    tool_trace: List[Dict[str, Any]] = Field(default_factory=list)
    schema_valid: bool = True
    latency_ms: int = 0
    cost: float = 0.0
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, model_backend: str = "mock", timeout_sec: float = 30.0):
        self.agent_id = agent_id
        self.name = name
        self.model_backend = model_backend
        self.timeout_sec = timeout_sec

    @abstractmethod
    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """Universal agent execution protocol method."""
        pass
