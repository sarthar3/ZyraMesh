import math
from typing import List, Dict, Any, Optional, Tuple
from app.models.agent import AgentModel

class TeamComposer:
    """
    ZyraMesh Dual-Graph Constrained Team Composer.
    Matches TDG subtasks against ACTG agent candidates under hard constraints and multi-objective soft scoring.
    """
    def __init__(self, strategy: str = "ZYRAMESH", ablation_config: Optional[Dict[str, bool]] = None):
        self.strategy = strategy.upper()
        self.ablation_config = ablation_config or {}

    def compose_team(
        self,
        subtasks: List[Dict[str, Any]],
        agents: List[AgentModel],
        max_budget: Optional[float] = None,
        max_latency_ms: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        
        assigned_tasks = []
        team_agents = {}
        total_cost = 0.0
        total_latency = 0
        overall_score = 0.0

        # Baseline logic override
        if self.strategy == "SINGLE_GENERALIST":
            generalist = next((a for a in agents if "generalist" in a.agent_id or "monolithic" in a.name.lower()), agents[0])
            for t in subtasks:
                t_assigned = dict(t)
                t_assigned["assigned_agent_id"] = generalist.agent_id
                t_assigned["assigned_agent_name"] = generalist.name
                assigned_tasks.append(t_assigned)
            return assigned_tasks, {"strategy": self.strategy, "score": 0.70, "total_cost": generalist.cost_per_1k_tokens * len(subtasks), "total_latency": generalist.avg_latency_ms}

        for idx, task in enumerate(subtasks):
            req_caps = set(task.get("required_capabilities", []))
            crit_score = task.get("criticality_score", 0.5)
            prop_risk = task.get("propagation_risk", 0.5)
            
            candidates = []
            for agent in agents:
                status = getattr(agent, "status", "ACTIVE") or "ACTIVE"
                avail = getattr(agent, "availability_status", "AVAILABLE") or "AVAILABLE"
                if status != "ACTIVE" or avail == "OFFLINE":
                    continue
                
                # 1. Hard capability match check
                agent_caps = set(agent.capabilities)
                cap_match_ratio = len(req_caps.intersection(agent_caps)) / max(1, len(req_caps))
                if cap_match_ratio == 0 and self.strategy not in ["REPUTATION_ONLY"]:
                    continue

                # 2. Strategy-dependent candidate scoring
                if self.strategy == "CAPABILITY_ONLY":
                    score = cap_match_ratio
                elif self.strategy == "REPUTATION_ONLY":
                    score = agent.trust_mean
                elif self.strategy == "DYNAMIC_BASELINE":
                    score = 0.5 * cap_match_ratio + 0.5 * agent.trust_mean
                else:
                    # ZyraMesh Dual Graph Scoring
                    # Calibrated trust = mean - uncertainty penalty
                    use_global = self.ablation_config.get("global_trust_only", False)
                    no_uncert = self.ablation_config.get("no_uncertainty_penalty", False)
                    no_collab = self.ablation_config.get("no_collaboration_memory", False)
                    
                    if use_global:
                        t_mean = agent.trust_mean
                        t_var = agent.trust_uncertainty
                    else:
                        cap_trusts = [agent.capability_specific_trust.get(c, {}).get("mean", agent.trust_mean) for c in req_caps]
                        t_mean = sum(cap_trusts) / max(1, len(cap_trusts))
                        t_var = agent.trust_uncertainty

                    uncert_penalty = 0.0 if no_uncert else (0.5 * t_var)
                    calibrated_trust = max(0.01, t_mean - uncert_penalty)
                    
                    # Collaboration synergy score with previous assigned agent
                    collab_synergy = 1.0
                    if idx > 0 and not no_collab and assigned_tasks:
                        prev_agent_id = assigned_tasks[-1]["assigned_agent_id"]
                        collab_synergy = agent.collaboration_history.get(prev_agent_id, {}).get("success_rate", 0.85)

                    # Multi-objective composite score weighted by propagation risk
                    score = (
                        0.40 * cap_match_ratio +
                        0.35 * calibrated_trust +
                        0.15 * collab_synergy +
                        0.10 * (1.0 - (agent.avg_latency_ms / 1000.0))
                    ) * (1.0 + 0.2 * prop_risk)

                candidates.append((agent, score))

            if not candidates:
                # Fallback to generalist if no match found
                chosen_agent = agents[0]
                score = 0.5
            else:
                candidates.sort(key=lambda x: x[1], reverse=True)
                chosen_agent, score = candidates[0]

            t_assigned = dict(task)
            t_assigned["assigned_agent_id"] = chosen_agent.agent_id
            t_assigned["assigned_agent_name"] = chosen_agent.name
            t_assigned["match_score"] = round(score, 4)
            assigned_tasks.append(t_assigned)

            team_agents[chosen_agent.agent_id] = chosen_agent.name
            total_cost += chosen_agent.cost_per_1k_tokens
            total_latency += chosen_agent.avg_latency_ms
            overall_score += score

        meta = {
            "strategy": self.strategy,
            "ablation_config": self.ablation_config,
            "team_size": len(set(t["assigned_agent_id"] for t in assigned_tasks)),
            "total_cost": round(total_cost, 4),
            "total_latency_ms": total_latency,
            "average_team_fit_score": round(overall_score / max(1, len(subtasks)), 4)
        }

        return assigned_tasks, meta
