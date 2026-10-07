from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
import datetime

class AgentBase(BaseModel):
    name: str
    description: str
    category: str = "general"
    capabilities: List[str] = []
    tools: List[Dict[str, Any]] = []
    model_backend: str = "ollama"
    model_name: str = "qwen2.5:1.5b-instruct"
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}
    cost_per_execution: float = 0.001
    cost_per_1k_tokens: float = 0.001
    expected_latency: int = 150
    avg_latency_ms: int = 150
    availability: str = "AVAILABLE"
    availability_status: str = "AVAILABLE"
    permissions: List[str] = ["standard"]
    provenance: Dict[str, Any] = {"registered_by": "system"}
    status: str = "ACTIVE"

class AgentCreate(AgentBase):
    agent_id: Optional[str] = None
    global_trust: float = 0.5
    trust_mean: float = 0.5
    trust_uncertainty: float = 0.5

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    capabilities: Optional[List[str]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    availability: Optional[str] = None
    status: Optional[str] = None
    cost_per_execution: Optional[float] = None
    expected_latency: Optional[int] = None

class AgentResponse(AgentBase):
    model_config = ConfigDict(from_attributes=True)

    agent_id: str
    global_trust: float = 0.5
    trust_mean: float = 0.5
    trust_uncertainty: float = 0.5
    capability_specific_trust: Dict[str, Dict[str, float]] = {}
    successful_executions: int = 0
    failed_executions: int = 0
    verifier_agreement: float = 0.90
    schema_validity: float = 0.95
    tool_success: float = 0.95
    recent_performance: float = 0.85
    historical_performance: float = 0.85
    collaboration_history: Dict[str, Dict[str, Any]] = {}
    created_at: datetime.datetime
    updated_at: datetime.datetime
