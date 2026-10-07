import datetime
import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.agent import AgentModel
from app.models.trust import TrustObservationModel

class TrustEngine:
    """
    Evidence-based Bayesian Trust Calibration Engine for ZyraMesh.
    Updates capability-specific trust distributions:
      Mean: \mu_{new} = \mu + \alpha (evidence - \mu)
      Uncertainty: \sigma_{new}^2 = (1 - \beta) \sigma^2
    """
    def record_observation_and_update(
        self,
        db: Session,
        agent_id: str,
        capability: str,
        success: bool,
        verifier_agreement: Optional[float],
        schema_validity: bool,
        tool_success: bool,
        handoff_success: bool,
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        evidence_source: str = "execution_runtime"
    ) -> TrustObservationModel:
        
        # 1. Create Observation record
        obs = TrustObservationModel(
            observation_id=f"obs_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            workflow_id=workflow_id,
            execution_id=execution_id,
            capability=capability,
            success=success,
            verifier_agreement=verifier_agreement,
            schema_validity=schema_validity,
            tool_success=tool_success,
            handoff_success=handoff_success,
            timestamp=datetime.datetime.utcnow(),
            evidence_source=evidence_source
        )
        db.add(obs)

        # 2. Retrieve Agent
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        if agent:
            # Composite Evidence Score E in [0, 1]
            s_val = 1.0 if success else 0.0
            v_val = verifier_agreement if verifier_agreement is not None else (1.0 if success else 0.0)
            sc_val = 1.0 if schema_validity else 0.0
            t_val = 1.0 if tool_success else 0.0
            h_val = 1.0 if handoff_success else 0.0

            evidence_score = 0.35 * s_val + 0.25 * v_val + 0.15 * sc_val + 0.15 * t_val + 0.10 * h_val
            
            # Bayesian update step
            alpha = 0.15 # Learning rate
            beta = 0.05  # Variance decay rate (reduction of uncertainty with more observations)

            curr_trust_dict = dict(agent.capability_specific_trust or {})
            cap_data = curr_trust_dict.get(capability, {"mean": agent.trust_mean, "var": agent.trust_uncertainty})

            old_mean = cap_data.get("mean", agent.trust_mean)
            old_var = cap_data.get("var", agent.trust_uncertainty)

            new_mean = round(old_mean + alpha * (evidence_score - old_mean), 4)
            new_var = round(max(0.01, old_var * (1.0 - beta)), 4)

            cap_data["mean"] = new_mean
            cap_data["var"] = new_var
            curr_trust_dict[capability] = cap_data

            agent.capability_specific_trust = curr_trust_dict

            # Update overall agent trust mean & uncertainty
            all_means = [v["mean"] for v in curr_trust_dict.values()]
            all_vars = [v["var"] for v in curr_trust_dict.values()]

            agent.trust_mean = round(sum(all_means) / len(all_means), 4)
            agent.trust_uncertainty = round(sum(all_vars) / len(all_vars), 4)
            agent.updated_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(obs)
        return obs
