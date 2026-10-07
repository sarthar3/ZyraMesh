from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime

class BenchmarkRunRequest(BaseModel):
    num_samples: int = 10
    strategies: List[str] = ["SINGLE_GENERALIST", "FIXED_MULTI_AGENT", "CAPABILITY_ONLY", "REPUTATION_ONLY", "DYNAMIC_BASELINE", "ZYRAMESH"]
    ablations: List[str] = ["NONE", "NO_TDG", "GLOBAL_TRUST_ONLY", "NO_UNCERTAINTY_PENALTY", "NO_COLLABORATION_MEMORY", "NO_GUARDRAILS", "NO_REORCHESTRATION"]

class BenchmarkMetricResponse(BaseModel):
    metric_id: str
    run_id: str
    strategy: str
    ablation: str
    workflow_success_rate: float
    failure_propagation_rate: float
    expected_calibration_error: float
    avg_latency_ms: float
    total_cost: float
    verification_frequency: float
    rerouting_success_rate: float
    policy_violations_count: int
    sample_size: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True
