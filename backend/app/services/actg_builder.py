import networkx as nx
from typing import List, Dict, Any, Tuple
from app.models.agent import AgentModel

class ACTGBuilder:
    """
    Builds and manages the Agent Capability-Trust Graph (ACTG) in NetworkX.
    Nodes: Agent IDs, Capability tags.
    Edges: 
      - Agent -> Capability (weight = capability-specific trust mean)
      - Agent -> Agent (weight = pairwise collaboration success rate)
    """
    @staticmethod
    def build_actg(agents: List[AgentModel]) -> Tuple[nx.Graph, Dict[str, Any]]:
        g = nx.Graph()

        # Add nodes
        for agent in agents:
            g.add_node(
                agent.agent_id,
                type="agent",
                name=agent.name,
                trust_mean=agent.trust_mean,
                trust_uncertainty=agent.trust_uncertainty,
                cost=agent.cost_per_1k_tokens,
                latency=agent.avg_latency_ms,
                status=agent.status
            )
            # Capability edges
            for cap in agent.capabilities:
                cap_node = f"cap_{cap}"
                if not g.has_node(cap_node):
                    g.add_node(cap_node, type="capability", name=cap)
                
                cap_trust = agent.capability_specific_trust.get(cap, {}).get("mean", agent.trust_mean)
                g.add_edge(agent.agent_id, cap_node, weight=cap_trust, relation="HAS_CAPABILITY")

            # Collaboration edges
            collab_hist = agent.collaboration_history or {}
            for partner_id, hist in collab_hist.items():
                if any(a.agent_id == partner_id for a in agents):
                    collab_rate = hist.get("success_rate", 0.5)
                    g.add_edge(agent.agent_id, partner_id, weight=collab_rate, relation="COLLABORATION_HISTORY")

        actg_json = {
            "nodes": [
                {
                    "id": n,
                    "type": g.nodes[n].get("type"),
                    "label": g.nodes[n].get("name", n),
                    "trust_mean": g.nodes[n].get("trust_mean"),
                    "trust_uncertainty": g.nodes[n].get("trust_uncertainty"),
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
