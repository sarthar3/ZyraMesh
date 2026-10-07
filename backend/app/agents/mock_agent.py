import time
from typing import Dict, Any
from app.agents.base_agent import BaseAgent, AgentResult
from app.adapters.mock_llm_adapter import MockLLMAdapter

class MockAgent(BaseAgent):
    """Deterministic Mock Agent ensuring fast, zero-dependency offline execution."""
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name, model_backend="mock")
        self.mock_adapter = MockLLMAdapter()

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        output_str = await self.mock_adapter.generate(task.get("description", ""), json_mode=True)
        elapsed_ms = int((time.time() - start_time) * 1000)

        return AgentResult(
            success=True,
            output={"result": output_str, "agent": self.name},
            confidence=0.94,
            uncertainty=0.06,
            evidence={"source": "MockDeterministicProvider"},
            tool_trace=[{"tool": "mock_tool", "status": "SUCCESS"}],
            schema_valid=True,
            latency_ms=elapsed_ms,
            cost=0.0005,
            errors=[]
        )
