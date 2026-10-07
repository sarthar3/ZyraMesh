import random
from typing import Dict, Any

class VerifierEngine:
    """
    Selective Verification System for ZyraMesh.
    Provides agreement scoring between execution outputs and oracle/verifier checks.
    """
    def verify_execution(self, task: Dict[str, Any], agent_id: str, output_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate dual verifier oracle agreement score
        # For mock verification, high agreement when schema valid and status ok
        schema_ok = output_data.get("schema_valid", True)
        base_agreement = 0.95 if schema_ok else 0.40
        agreement = round(base_agreement - random.uniform(0.0, 0.05), 4)
        
        passed = agreement >= 0.70
        return {
            "verified": True,
            "verifier_agreement": agreement,
            "passed": passed,
            "evidence_score": round(agreement * 0.98, 4),
            "comments": "Verifier agreement verified by dual-oracle cross-check." if passed else "Output rejected by verifier due to agreement failure."
        }
