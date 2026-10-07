import math
from typing import List, Dict, Any, Tuple, Optional
from app.models.agent import AgentModel

class CrossGraphMatcher:
    """
    Module 7: 2-Stage Cross-Graph Matcher for ZyraMesh.
    Matches TDG task requirements against ACTG candidate agents.
    
    Stage 1: Hard Filtering (Capability, Tool, Permission, Budget, Latency SLA, Availability).
    Stage 2: Soft Ranking using Conservative Trust Formulation:
             conservative_trust = trust_mean - k * trust_uncertainty
    """
    def __init__(self, k_uncertainty: float = 0.5, strategy: str = "ZYRAMESH", ablation_config: Optional[Dict[str, bool]] = None):
        self.k_uncertainty = k_uncertainty
        self.strategy = strategy.upper()
        self.ablation_config = ablation_config or {}

    def hard_filter(
        self,
        task: Dict[str, Any],
        agents: List[AgentModel],
        max_budget: Optional[float] = None,
        max_latency_ms: Optional[int] = None
    ) -> Tuple[List[AgentModel], List[Dict[str, Any]]]:
        
        req_caps = set(task.get("required_capabilities", []))
        req_tools = set(task.get("required_tools", []))
        rejection_reasons = []
        eligible_agents = []

        for agent in agents:
            # Availability & status check
            if agent.status not in ["ACTIVE", "DEGRADED"]:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Status '{agent.status}' is not active."})
                continue
            if agent.availability in ["OFFLINE", "UNAVAILABLE"]:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Availability '{agent.availability}' is unavailable."})
                continue

            # Required capability check
            agent_caps = set(agent.capabilities or [])
            if req_caps and not req_caps.intersection(agent_caps) and self.strategy not in ["REPUTATION_ONLY"]:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Missing required capabilities: {req_caps - agent_caps}"})
                continue

            # Required tool check
            agent_tools = {t.get("name") if isinstance(t, dict) else t for t in (agent.tools or [])}
            if req_tools and not req_tools.intersection(agent_tools) and self.strategy not in ["REPUTATION_ONLY"]:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Missing required tools: {req_tools - agent_tools}"})
                continue

            # Latency SLA check
            if max_latency_ms and agent.avg_latency_ms > max_latency_ms:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Latency {agent.avg_latency_ms}ms exceeds max SLA {max_latency_ms}ms"})
                continue

            # Cost check
            if max_budget and agent.cost_per_1k_tokens > max_budget:
                rejection_reasons.append({"agent_id": agent.agent_id, "reason": f"Cost ${agent.cost_per_1k_tokens} exceeds budget ${max_budget}"})
                continue

            eligible_agents.append(agent)

        return eligible_agents, rejection_reasons

    def soft_rank(
        self,
        task: Dict[str, Any],
        eligible_agents: List[AgentModel],
        prior_agent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        
        req_caps = set(task.get("required_capabilities", []))
        prop_risk = task.get("propagation_risk", 0.5)
        ranked_candidates = []

        no_uncert = self.ablation_config.get("no_uncertainty_penalty", False)
        no_collab = self.ablation_config.get("no_collaboration_memory", False)
        global_only = self.ablation_config.get("global_trust_only", False)

        for agent in eligible_agents:
            agent_caps = set(agent.capabilities or [])
            cap_match_ratio = len(req_caps.intersection(agent_caps)) / max(1, len(req_caps)) if req_caps else 1.0

            # Conservative trust calculation: conservative_trust = trust_mean - k * trust_uncertainty
            if global_only:
                t_mean = agent.global_trust
                t_var = agent.trust_uncertainty
            else:
                cap_trusts = [(agent.capability_specific_trust or {}).get(c, {}).get("mean", agent.trust_mean) for c in req_caps]
                t_mean = sum(cap_trusts) / max(1, len(cap_trusts)) if cap_trusts else agent.trust_mean
                t_var = agent.trust_uncertainty

            uncert_k = 0.0 if no_uncert else self.k_uncertainty
            conservative_trust = max(0.01, min(0.99, t_mean - uncert_k * t_var))

            # Pairwise handoff synergy
            collab_synergy = 1.0
            if prior_agent_id and not no_collab:
                collab_hist = agent.collaboration_history or {}
                collab_synergy = collab_hist.get(prior_agent_id, {}).get("success_rate", 0.85)

            # Normalized cost and latency scores
            norm_cost_score = max(0.0, 1.0 - (agent.cost_per_1k_tokens / 0.01))
            norm_latency_score = max(0.0, 1.0 - (agent.avg_latency_ms / 1000.0))

            # Composite multi-objective score
            composite_score = (
                0.35 * cap_match_ratio +
                0.35 * conservative_trust +
                0.15 * collab_synergy +
                0.10 * norm_latency_score +
                0.05 * norm_cost_score
            ) * (1.0 + 0.20 * prop_risk)

            explanation = (
                f"Agent '{agent.name}' selected with score {round(composite_score, 4)}: "
                f"Capability Fit={round(cap_match_ratio*100, 0)}%, "
                f"Conservative Trust={round(conservative_trust, 3)} (Mean={round(t_mean, 3)}, Var={round(t_var, 3)}), "
                f"Collaboration Synergy={round(collab_synergy*100, 0)}%, Latency={agent.avg_latency_ms}ms."
            )

            ranked_candidates.append({
                "agent": agent,
                "score": round(composite_score, 4),
                "conservative_trust": round(conservative_trust, 4),
                "trust_mean": round(t_mean, 4),
                "trust_uncertainty": round(t_var, 4),
                "collaboration_synergy": round(collab_synergy, 4),
                "explanation": explanation
            })

        ranked_candidates.sort(key=lambda x: x["score"], reverse=True)
        return ranked_candidates
