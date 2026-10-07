import pytest
import asyncio
from app.agents.mock_agent import MockAgent
from app.agents.local_llm_agent import LocalLLMAgent

@pytest.mark.asyncio
async def test_mock_agent_execution_protocol():
    agent = MockAgent("agent_test_mock", "Test Mock Agent")
    task = {"task_id": "task_1", "description": "Validate data schema"}
    context = {}

    res = await agent.execute(task, context)
    assert res.success is True
    assert res.output is not None
    assert res.confidence >= 0.90
    assert res.latency_ms >= 0
    assert res.schema_valid is True

@pytest.mark.asyncio
async def test_local_llm_agent_fallback():
    agent = LocalLLMAgent("agent_test_llm", "Test LLM Agent", timeout_sec=1.0)
    task = {"task_id": "task_2", "description": "Execute laptop search"}
    context = {}

    res = await agent.execute(task, context)
    assert res.output is not None
    assert isinstance(res.latency_ms, int)
