from typing import List, Dict, Any, Tuple, Optional
from app.models.agent import AgentModel
from app.matching.cross_matcher import CrossGraphMatcher

class ConstrainedTeamComposer:
    """
    Module 8: Constrained Team Composer.
    Solves multi-objective team formation for TDG tasks under hard SLA/budget constraints
    and soft multi-objective optimization (quality, cost, latency, risk, redundancy, synergy).
    """
    def __init__(self, strategy: str = "ZYRAMESH", ablation_config: Optional[Dict[str, bool]] = None):
        self.strategy = strategy.upper()
        self.ablation_config = ablation_config or {}
        self.matcher = CrossGraphMatcher(strategy=self.strategy, ablation_config=self.ablation_config)

    def compose_team(
        self,
        subtasks: List[Dict[str, Any]],
        agents: List[AgentModel],
        max_budget: Optional[float] = None,
        max_latency_ms: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        
        assigned_subtasks = []
        total_cost = 0.0
        total_latency = 0
        overall_fit_score = 0.0
        prior_agent_id = None

        # Strategy override: SINGLE_GENERALIST baseline
        if self.strategy == "SINGLE_GENERALIST":
            generalist = next((a for a in agents if "generalist" in a.agent_id or "general" in a.category), agents[0])
            for t in subtasks:
                t_assigned = dict(t)
                t_assigned["assigned_agent_id"] = generalist.agent_id
                t_assigned["assigned_agent_name"] = generalist.name
                t_assigned["match_score"] = 0.70
                t_assigned["explanation"] = f"Assigned to monolithic generalist baseline '{generalist.name}'."
                assigned_subtasks.append(t_assigned)
            return assigned_subtasks, {
                "strategy": self.strategy,
                "team_size": 1,
                "total_cost": generalist.cost_per_1k_tokens * len(subtasks),
                "total_latency_ms": generalist.avg_latency_ms,
                "average_team_fit_score": 0.70
            }

        for idx, task in enumerate(subtasks):
            # Stage 1: Hard Filter
            eligible, rejections = self.matcher.hard_filter(
                task, agents, max_budget=max_budget, max_latency_ms=max_latency_ms
            )

            if not eligible:
                # Fallback to top general agent if no candidate satisfies hard constraints
                chosen_agent = agents[0]
                match_score = 0.50
                explanation = f"Fallback assignment to '{chosen_agent.name}' (no eligible candidates passed Stage 1 hard filter)."
            else:
                # Stage 2: Soft Rank
                ranked = self.matcher.soft_rank(task, eligible, prior_agent_id=prior_agent_id)
                top_candidate = ranked[0]
                chosen_agent = top_candidate["agent"]
                match_score = top_candidate["score"]
                explanation = top_candidate["explanation"]

            t_assigned = dict(task)
            t_assigned["assigned_agent_id"] = chosen_agent.agent_id
            t_assigned["assigned_agent_name"] = chosen_agent.name
            t_assigned["match_score"] = match_score
            t_assigned["explanation"] = explanation
            assigned_subtasks.append(t_assigned)

            prior_agent_id = chosen_agent.agent_id
            total_cost += chosen_agent.cost_per_1k_tokens
            total_latency += chosen_agent.avg_latency_ms
            overall_fit_score += match_score

        meta = {
            "strategy": self.strategy,
            "ablation_config": self.ablation_config,
            "team_size": len(set(t["assigned_agent_id"] for t in assigned_subtasks)),
            "total_cost": round(total_cost, 5),
            "total_latency_ms": total_latency,
            "average_team_fit_score": round(overall_fit_score / max(1, len(subtasks)), 4)
        }

        return assigned_subtasks, meta
