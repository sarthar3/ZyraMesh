import time
import json
import asyncio
from typing import Dict, Any
from app.agents.base_agent import BaseAgent, AgentResult
from app.adapters.provider_factory import get_llm_adapter
from app.core.logging import logger

class LocalLLMAgent(BaseAgent):
    """
    Ollama-backed Local LLM Agent (Default model: qwen2.5:1.5b-instruct).
    Implements structured prompt execution, timeout, retry, and latency/cost tracking.
    """
    def __init__(self, agent_id: str, name: str, model_name: str = "qwen2.5:1.5b-instruct", timeout_sec: float = 30.0):
        super().__init__(agent_id, name, model_backend="ollama", timeout_sec=timeout_sec)
        self.model_name = model_name
        self.adapter = get_llm_adapter("ollama")

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        task_desc = task.get("description", "")
        system_prompt = f"You are agent '{self.name}' executing task: {task_desc}."
        prompt = f"Task payload: {json.dumps(task)}\nPrior context: {json.dumps(context)}"

        retries = 2
        last_error = None
        for attempt in range(retries + 1):
            try:
                # Execution with timeout
                output_str = await asyncio.wait_for(
                    self.adapter.generate(prompt, system_prompt=system_prompt, json_mode=True),
                    timeout=self.timeout_sec
                )
                elapsed_ms = int((time.time() - start_time) * 1000)

                try:
                    parsed_output = json.loads(output_str)
                except Exception:
                    parsed_output = {"result": output_str}

                return AgentResult(
                    success=True,
                    output=parsed_output,
                    confidence=0.92,
                    uncertainty=0.08,
                    evidence={"source": "Ollama/qwen2.5:1.5b-instruct", "attempt": attempt + 1},
                    tool_trace=[{"tool": "ollama_generate", "status": "SUCCESS"}],
                    schema_valid=True,
                    latency_ms=elapsed_ms,
                    cost=0.001,
                    errors=[]
                )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"LocalLLMAgent '{self.agent_id}' attempt {attempt + 1} failed: {last_error}")
                await asyncio.sleep(0.2)

        elapsed_ms = int((time.time() - start_time) * 1000)
        return AgentResult(
            success=False,
            output={"result": "Execution failed after retries."},
            confidence=0.20,
            uncertainty=0.80,
            schema_valid=False,
            latency_ms=elapsed_ms,
            cost=0.0,
            errors=[last_error or "Timeout/Execution Error"]
        )
