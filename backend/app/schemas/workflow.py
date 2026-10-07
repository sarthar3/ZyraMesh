from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import datetime

class WorkflowSubmitRequest(BaseModel):
    raw_user_objective: str
    execution_strategy: str = "ZYRAMESH" # SINGLE_GENERALIST, FIXED_MULTI_AGENT, CAPABILITY_ONLY, REPUTATION_ONLY, DYNAMIC_BASELINE, ZYRAMESH
    ablation_config: Dict[str, bool] = {
        "no_tdg": False,
        "global_trust_only": False,
        "no_uncertainty_penalty": False,
        "no_collaboration_memory": False,
        "no_guardrails": False,
        "no_reorchestration": False
    }
    max_budget: Optional[float] = None
    max_latency_ms: Optional[int] = None
    required_security_tier: Optional[str] = "STANDARD"

class SubtaskSchema(BaseModel):
    task_id: str
    subtask_index: int
    description: str
    required_capabilities: List[str]
    required_tools: List[str] = []
    sensitivity_score: float = 0.0
    criticality_score: float = 0.5
    propagation_risk: float = 0.5
    verification_requirement: str = "AUTO"
    dependencies: List[str] = []
    assigned_agent_id: Optional[str] = None
    assigned_agent_name: Optional[str] = None
    status: str = "PENDING"

class WorkflowResponse(BaseModel):
    workflow_id: str
    raw_user_objective: str
    status: str
    execution_strategy: str
    ablation_config: Dict[str, Any]
    tdg_structure: Optional[Dict[str, Any]] = None
    tasks: List[SubtaskSchema] = []
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
