import datetime
import uuid
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.agent import AgentModel
from app.models.trust import TrustObservationModel

class TrustEngine:
    """
    Module 13: Evidence-Driven Bayesian Trust Update Engine for ZyraMesh.
    Updates capability-specific trust distributions:
      Mean: \mu_{new} = \mu + \alpha (evidence - \mu)
      Uncertainty Variance: \sigma_{new}^2 = \sigma^2 (1 - \beta)
    Persists auditable records in trust_observations table.
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
        
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        old_trust = agent.trust_mean if agent else 0.50

        # Composite Evidence Score E in [0, 1]
        s_val = 1.0 if success else 0.0
        v_val = verifier_agreement if verifier_agreement is not None else (1.0 if success else 0.0)
        sc_val = 1.0 if schema_validity else 0.0
        t_val = 1.0 if tool_success else 0.0
        h_val = 1.0 if handoff_success else 0.0

        evidence_score = 0.35 * s_val + 0.25 * v_val + 0.15 * sc_val + 0.15 * t_val + 0.10 * h_val
        
        alpha = 0.15 # Bayesian learning rate
        beta = 0.05  # Uncertainty variance reduction rate

        new_trust = old_trust
        if agent:
            curr_trust_dict = dict(agent.capability_specific_trust or {})
            cap_data = curr_trust_dict.get(capability, {"mean": agent.trust_mean, "var": agent.trust_uncertainty})

            old_cap_mean = cap_data.get("mean", agent.trust_mean)
            old_cap_var = cap_data.get("var", agent.trust_uncertainty)

            new_cap_mean = round(old_cap_mean + alpha * (evidence_score - old_cap_mean), 4)
            new_cap_var = round(max(0.01, old_cap_var * (1.0 - beta)), 4)

            cap_data["mean"] = new_cap_mean
            cap_data["var"] = new_cap_var
            curr_trust_dict[capability] = cap_data

            agent.capability_specific_trust = curr_trust_dict

            all_means = [v["mean"] for v in curr_trust_dict.values()]
            all_vars = [v["var"] for v in curr_trust_dict.values()]

            new_trust = round(sum(all_means) / len(all_means), 4)
            agent.trust_mean = new_trust
            agent.global_trust = new_trust
            agent.trust_uncertainty = round(sum(all_vars) / len(all_vars), 4)

            if success:
                agent.successful_executions = getattr(agent, "successful_executions", 0) + 1
            else:
                agent.failed_executions = getattr(agent, "failed_executions", 0) + 1

            agent.updated_at = datetime.datetime.utcnow()

        # Create Observation Audit Log
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
            old_trust=old_trust,
            new_trust=new_trust,
            timestamp=datetime.datetime.utcnow(),
            evidence_source=evidence_source
        )
        db.add(obs)
        db.commit()
        db.refresh(obs)
        return obs
