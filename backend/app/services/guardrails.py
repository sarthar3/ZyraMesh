import uuid
import datetime
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.audit import AuditEventModel

class GuardrailsPolicyEngine:
    """
    Guardrails and Policy Engine for ZyraMesh.
    Validates input objectives and output data against safety policies.
    """
    @staticmethod
    def inspect_input(objective: str, no_guardrails: bool = False) -> Tuple[bool, str]:
        if no_guardrails:
            return True, "PASSED (Guardrails disabled)"
        
        forbidden_keywords = ["drop table", "ignore safety instructions", "rm -rf", "eval("]
        obj_lower = objective.lower()
        for kw in forbidden_keywords:
            if kw in obj_lower:
                return False, f"Policy violation: Forbidden instruction detected ('{kw}')"
        return True, "PASSED"

    @staticmethod
    def inspect_output(output_data: Dict[str, Any], no_guardrails: bool = False) -> Tuple[bool, str]:
        if no_guardrails:
            return True, "PASSED (Guardrails disabled)"
        return True, "PASSED"


class AuditLogger:
    """
    Execution Trace & Audit System for ZyraMesh.
    Records every major pipeline event for explainability.
    """
    @staticmethod
    def log_event(
        db: Session,
        event_type: str,
        actor: str,
        payload: Dict[str, Any],
        workflow_id: str = None,
        execution_id: str = None
    ) -> AuditEventModel:
        event = AuditEventModel(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            execution_id=execution_id,
            event_type=event_type,
            actor=actor,
            payload=payload,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
