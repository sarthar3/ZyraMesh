from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime

class ExecutionResponse(BaseModel):
    execution_id: str
    workflow_id: str
    task_id: str
    agent_id: str
    agent_name: Optional[str] = None
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    uncertainty_score: Optional[float] = None
    schema_valid: Optional[bool] = None
    verifier_agreement: Optional[float] = None
    evidence_score: Optional[float] = None
    tool_trace: List[Dict[str, Any]] = []
    policy_status: str = "PASSED"
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    status: str

    class Config:
        from_attributes = True
