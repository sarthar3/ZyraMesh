import math
import random
from typing import Dict, Any, Tuple
from app.config import settings

class UncertaintyGate:
    """
    Uncertainty-Gated Controller for ZyraMesh.
    Calculates output uncertainty using confidence variance, schema validity, and propagation risk.
    Determines if selective verification or re-orchestration is needed.
    """
    def __init__(self, threshold: float = None):
        self.threshold = threshold or settings.UNCERTAINTY_VERIFICATION_THRESHOLD

    def evaluate_output(
        self,
        task: Dict[str, Any],
        agent_trust_uncertainty: float,
        raw_output: str,
        confidence_score: float = 0.90,
        schema_valid: bool = True,
        no_uncertainty_penalty: bool = False
    ) -> Dict[str, Any]:
        
        if no_uncertainty_penalty:
            uncertainty = 0.05
        else:
            # Epistemic uncertainty from agent trust variance + aleatoric entropy from model confidence
            entropy = - (confidence_score * math.log2(confidence_score + 1e-9) + (1 - confidence_score) * math.log2(1 - confidence_score + 1e-9))
            propagation_risk = task.get("propagation_risk", 0.5)
            schema_penalty = 0.0 if schema_valid else 0.4

            uncertainty = 0.4 * agent_trust_uncertainty + 0.3 * entropy + 0.2 * propagation_risk + schema_penalty
            uncertainty = max(0.01, min(0.99, round(uncertainty, 4)))

        requires_verification = (uncertainty >= self.threshold) or (task.get("verification_requirement") == "ALWAYS")
        
        return {
            "confidence_score": confidence_score,
            "uncertainty_score": uncertainty,
            "schema_valid": schema_valid,
            "requires_verification": requires_verification,
            "risk_level": "HIGH" if uncertainty > 0.6 else ("MEDIUM" if uncertainty > 0.3 else "LOW")
        }
