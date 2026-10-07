from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.simulation import simulation_manager

router = APIRouter(prefix="/simulations", tags=["Failure Simulation & Demo Mode"])

class FailureInjectRequest(BaseModel):
    agent_id: Optional[str] = "SpecificationAgent-A"
    failure_type: str = "SCHEMA_FAILURE" # SCHEMA_FAILURE, TIMEOUT, UNCERTAINTY, VERIFIER_DISAGREEMENT, TOOL_FAILURE, UNAVAILABLE
    target_task_index: Optional[int] = None
    enabled: bool = True

@router.post("/inject-failure")
def inject_failure(req: FailureInjectRequest):
    return simulation_manager.set_failure_injection(
        agent_id=req.agent_id,
        failure_type=req.failure_type,
        target_task_index=req.target_task_index,
        enabled=req.enabled
    )

@router.get("/state")
def get_simulation_state():
    return simulation_manager.get_simulation_state()

@router.post("/reset")
def reset_simulation():
    return simulation_manager.set_failure_injection(enabled=False)
