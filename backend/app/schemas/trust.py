from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime

class TrustObservationResponse(BaseModel):
    observation_id: str
    agent_id: str
    workflow_id: Optional[str] = None
    execution_id: Optional[str] = None
    capability: str
    success: bool
    verifier_agreement: Optional[float] = None
    schema_validity: bool
    tool_success: bool
    handoff_success: bool
    timestamp: datetime.datetime
    evidence_source: str

    class Config:
        from_attributes = True

class AgentTrustLeaderboardItem(BaseModel):
    agent_id: str
    name: str
    trust_mean: float
    trust_uncertainty: float
    capability_trust: Dict[str, Dict[str, float]]
    total_executions: int
    success_rate: float
