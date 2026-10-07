import math
from typing import Dict, Any
from app.core.config import settings

class UncertaintyGate:
    """
    Module 10: Multi-Signal Uncertainty Evaluation Engine for ZyraMesh.
    Combines aleatoric output entropy, epistemic agent trust variance, schema validity,
    and task propagation risk to compute a calibrated uncertainty score and risk classification.
    
    Risk Levels & Actions:
      - LOW (< 0.25): ACCEPT
      - MEDIUM (0.25 - 0.40): VERIFY (Invoke Verification System)
      - HIGH (0.40 - 0.65): RETRY / REASSIGN
      - CRITICAL (>= 0.65): REORCHESTRATE / HUMAN REVIEW
    """
    def __init__(self, threshold: float = None):
        self.threshold = threshold or settings.UNCERTAINTY_VERIFICATION_THRESHOLD

    def evaluate(
        self,
        task: Dict[str, Any],
        agent_trust_uncertainty: float,
        confidence_score: float = 0.90,
        schema_valid: bool = True,
        tool_success: bool = True,
        no_uncertainty_penalty: bool = False
    ) -> Dict[str, Any]:
        
        if no_uncertainty_penalty:
            uncertainty = 0.05
            risk_level = "LOW"
            action = "ACCEPT"
        else:
            # 1. Aleatoric Entropy
            entropy = - (confidence_score * math.log2(confidence_score + 1e-9) + (1 - confidence_score) * math.log2(1 - confidence_score + 1e-9))
            
            # 2. Schema and Tool Failures
            schema_penalty = 0.0 if schema_valid else 0.35
            tool_penalty = 0.0 if tool_success else 0.20
            
            # 3. Task Criticality and Propagation Risk
            prop_risk = task.get("propagation_risk", 0.5)

            # Composite Uncertainty Score
            uncertainty = (
                0.35 * agent_trust_uncertainty +
                0.25 * entropy +
                0.20 * prop_risk +
                schema_penalty +
                tool_penalty
            )
            uncertainty = max(0.01, min(0.99, round(uncertainty, 4)))

            # Classification
            if uncertainty >= 0.65:
                risk_level = "CRITICAL"
                action = "REORCHESTRATE"
            elif uncertainty >= self.threshold:
                risk_level = "HIGH"
                action = "REASSIGN"
            elif uncertainty >= 0.25 or task.get("verification_required") == "ALWAYS":
                risk_level = "MEDIUM"
                action = "VERIFY"
            else:
                risk_level = "LOW"
                action = "ACCEPT"

        return {
            "confidence_score": round(confidence_score, 4),
            "uncertainty_score": uncertainty,
            "risk_level": risk_level,
            "recommended_action": action,
            "requires_verification": action in ["VERIFY", "REASSIGN", "REORCHESTRATE"]
        }
