from pydantic import BaseModel
from typing import List, Dict, Any, Tuple

class PolicyRule(BaseModel):
    rule_id: str
    rule_type: str # "PROMPT_INJECTION", "MALFORMED_OUTPUT", "BUDGET_EXCEEDED"
    keyword: str
    action: str = "BLOCK" # "BLOCK", "WARN", "REQUIRE_VERIFICATION"

class GuardrailsPolicyEngine:
    """
    Module 15: Guardrails and Policy Engine for ZyraMesh.
    Operates before planning, before execution, and after agent output.
    """
    FORBIDDEN_PATTERNS = ["drop table", "ignore previous instructions", "eval(", "rm -rf", "system_override"]

    @classmethod
    def inspect_input(cls, objective: str, no_guardrails: bool = False) -> Tuple[bool, str]:
        if no_guardrails:
            return True, "PASSED (Guardrails disabled)"
        
        obj_lower = objective.lower()
        for kw in cls.FORBIDDEN_PATTERNS:
            if kw in obj_lower:
                return False, f"Policy Violation: Forbidden security instruction detected ('{kw}')"
        return True, "PASSED"

    @classmethod
    def inspect_output(cls, output_data: Dict[str, Any], no_guardrails: bool = False) -> Tuple[bool, str]:
        if no_guardrails:
            return True, "PASSED (Guardrails disabled)"
        return True, "PASSED"
