import pytest
from app.verification.uncertainty_gate import UncertaintyGate

def test_uncertainty_gate_classification():
    gate = UncertaintyGate(threshold=0.40)
    task = {"task_id": "t1", "propagation_risk": 0.8}

    # Low uncertainty case
    low_res = gate.evaluate(task, agent_trust_uncertainty=0.03, confidence_score=0.95, schema_valid=True)
    assert low_res["risk_level"] in ["LOW", "MEDIUM"]

    # High uncertainty case due to schema failure & high agent trust variance
    high_res = gate.evaluate(task, agent_trust_uncertainty=0.40, confidence_score=0.60, schema_valid=False)
    assert high_res["requires_verification"] is True
    assert high_res["risk_level"] in ["HIGH", "CRITICAL"]
