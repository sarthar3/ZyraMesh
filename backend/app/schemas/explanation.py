from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentSelectionExplanation(BaseModel):
    task_id: str
    subtask_description: str
    candidate_agent_id: str
    candidate_agent_name: str
    capability_fit: float = Field(..., description="Capability match score (0.0 - 1.0)")
    conservative_trust: float = Field(..., description="Trust mean - k * uncertainty")
    uncertainty: float = Field(..., description="Agent trust uncertainty variance")
    cost: float = Field(..., description="Cost per execution in USD")
    latency_ms: int = Field(..., description="Expected latency in milliseconds")
    compatibility_score: float = Field(..., description="Pairwise collaboration handoff score")
    policy_risk: float = Field(..., description="Policy violation risk penalty")
    final_score: float = Field(..., description="Composite match score")
    selected: bool = Field(..., description="Whether this candidate was chosen")
    decision_reason: str = Field(..., description="Human-readable decision explanation")

class UncertaintyExplanation(BaseModel):
    task_id: str
    agent_id: str
    confidence_score: float
    aleatoric_entropy: float
    verifier_disagreement: float
    schema_validity: bool
    evidence_score: float
    criticality: float
    propagation_risk: float
    total_uncertainty: float
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    final_action: str  # ACCEPT, VERIFY, RETRY, REORCHESTRATE
    decision_reason: str

class ReOrchestrationExplanation(BaseModel):
    workflow_id: str
    failed_task_id: str
    failed_agent_id: str
    failed_agent_name: str
    failure_reason: str
    trigger_type: str  # TIMEOUT, SCHEMA_FAILURE, VERIFIER_REJECTION, HIGH_UNCERTAINTY, ERROR
    replacement_candidates: List[Dict[str, Any]]
    selected_replacement_id: Optional[str]
    selected_replacement_name: Optional[str]
    decision_reason: str

class TrustUpdateExplanation(BaseModel):
    agent_id: str
    capability: str
    old_trust: float
    new_trust: float
    delta: float
    evidence_source: str
    verifier_result: str
    decision_reason: str
