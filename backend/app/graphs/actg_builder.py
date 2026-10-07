import networkx as nx
from typing import List, Dict, Any, Tuple
from app.models.agent import AgentModel

class ACTGBuilder:
    """
    Module 6: Agent Capability-Trust Graph (ACTG) Builder using NetworkX.
    Nodes: Agent IDs, Capability tags, Tool names.
    Edges:
      - Agent -> Capability (weight = capability-specific trust mean)
      - Agent -> Agent (weight = pairwise collaboration handoff compatibility rate)
    Supports cold-start agents with conservative trust and higher uncertainty variance.
    """
    @staticmethod
    def build_actg(agents: List[AgentModel]) -> Tuple[nx.Graph, Dict[str, Any]]:
        g = nx.Graph()

        for agent in agents:
            # Cold-start detection: 0 successful executions
            is_cold_start = (getattr(agent, "successful_executions", 0) == 0) and (getattr(agent, "failed_executions", 0) == 0)
            
            trust_mean = agent.trust_mean if not is_cold_start else 0.50
            trust_var = agent.trust_uncertainty if not is_cold_start else 0.50

            g.add_node(
                agent.agent_id,
                type="agent",
                name=agent.name,
                category=getattr(agent, "category", "general"),
                trust_mean=trust_mean,
                trust_uncertainty=trust_var,
                is_cold_start=is_cold_start,
                cost=agent.cost_per_1k_tokens,
                latency=agent.avg_latency_ms,
                status=agent.status,
                permissions=agent.permissions or []
            )

            # Capability edges
            for cap in (agent.capabilities or []):
                cap_node = f"cap_{cap}"
                if not g.has_node(cap_node):
                    g.add_node(cap_node, type="capability", name=cap)

                cap_trust = (agent.capability_specific_trust or {}).get(cap, {}).get("mean", trust_mean)
                g.add_edge(agent.agent_id, cap_node, weight=cap_trust, relation="HAS_CAPABILITY")

            # Tool edges
            for t in (agent.tools or []):
                tool_name = t.get("name") if isinstance(t, dict) else t
                tool_node = f"tool_{tool_name}"
                if not g.has_node(tool_node):
                    g.add_node(tool_node, type="tool", name=tool_name)
                g.add_edge(agent.agent_id, tool_node, relation="HAS_TOOL")

            # Pairwise Collaboration edges
            collab_hist = agent.collaboration_history or {}
            for partner_id, hist in collab_hist.items():
                if any(a.agent_id == partner_id for a in agents):
                    collab_rate = hist.get("success_rate", 0.85)
                    g.add_edge(
                        agent.agent_id,
                        partner_id,
                        weight=collab_rate,
                        relation="COLLABORATION_HISTORY",
                        handoff_success=collab_rate,
                        schema_compatibility=0.95
                    )

        actg_json = {
            "nodes": [
                {
                    "id": n,
                    "type": g.nodes[n].get("type"),
                    "label": g.nodes[n].get("name", n),
                    "trust_mean": g.nodes[n].get("trust_mean"),
                    "trust_uncertainty": g.nodes[n].get("trust_uncertainty"),
                    "is_cold_start": g.nodes[n].get("is_cold_start", False),
                    "cost": g.nodes[n].get("cost"),
                    "latency": g.nodes[n].get("latency")
                }
                for n in g.nodes()
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "weight": g.edges[u, v].get("weight", 1.0),
                    "relation": g.edges[u, v].get("relation", "")
                }
                for u, v in g.edges()
            ]
        }

        return g, actg_json
