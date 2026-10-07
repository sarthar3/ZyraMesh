import json
import random
import hashlib
from typing import Optional
from app.adapters.llm_base import BaseLLMAdapter

class MockLLMAdapter(BaseLLMAdapter):
    """
    Deterministic mock provider ensuring zero-dependency local testing.
    Responds with context-aware JSON or text based on objective keywords.
    """
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        prompt_lower = prompt.lower()
        
        # 1. Task Decomposition Prompt
        if "decompose" in prompt_lower or "subtask" in prompt_lower or "objective" in prompt_lower:
            if json_mode:
                return json.dumps({
                    "subtasks": [
                        {
                            "subtask_index": 1,
                            "description": "Analyze input requirements and validate data schema",
                            "required_capabilities": ["data_analysis", "schema_validation"],
                            "required_tools": ["schema_checker"],
                            "sensitivity_score": 0.2,
                            "criticality_score": 0.8,
                            "propagation_risk": 0.7,
                            "dependencies": []
                        },
                        {
                            "subtask_index": 2,
                            "description": "Fetch target dataset and preprocess records",
                            "required_capabilities": ["data_retrieval", "preprocessing"],
                            "required_tools": ["db_query_tool"],
                            "sensitivity_score": 0.5,
                            "criticality_score": 0.7,
                            "propagation_risk": 0.6,
                            "dependencies": [1]
                        },
                        {
                            "subtask_index": 3,
                            "description": "Execute main analysis / transformation model",
                            "required_capabilities": ["code_execution", "machine_learning"],
                            "required_tools": ["python_interpreter"],
                            "sensitivity_score": 0.3,
                            "criticality_score": 0.9,
                            "propagation_risk": 0.8,
                            "dependencies": [2]
                        },
                        {
                            "subtask_index": 4,
                            "description": "Perform security audit and compliance verification",
                            "required_capabilities": ["security_audit", "policy_verification"],
                            "required_tools": ["guardrail_scanner"],
                            "sensitivity_score": 0.9,
                            "criticality_score": 0.95,
                            "propagation_risk": 0.9,
                            "dependencies": [3]
                        },
                        {
                            "subtask_index": 5,
                            "description": "Synthesize final report with recommendations",
                            "required_capabilities": ["report_synthesis", "summarization"],
                            "required_tools": ["markdown_formatter"],
                            "sensitivity_score": 0.1,
                            "criticality_score": 0.5,
                            "propagation_risk": 0.2,
                            "dependencies": [4]
                        }
                    ]
                })

        # 2. General agent execution output
        if json_mode:
            return json.dumps({
                "status": "SUCCESS",
                "summary": "Completed step execution cleanly with calibrated evidence.",
                "data": {"result_code": 200, "confidence": 0.94, "processed_items": 42},
                "confidence_score": 0.92,
                "tool_calls": [{"tool": "default_verifier", "status": "OK"}]
            })
            
        return "Executed subtask successfully using deterministic mock adapter. All checks passed with confidence = 0.94."

    async def get_embedding(self, text: str) -> list[float]:
        # Hash text into deterministic 128-float vector for embedding
        hash_digest = hashlib.sha256(text.encode("utf-8")).digest()
        vector = []
        for i in range(128):
            byte_val = hash_digest[i % len(hash_digest)]
            vector.append((byte_val / 255.0) * 2.0 - 1.0)
        return vector
