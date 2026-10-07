import networkx as nx
from typing import List, Dict, Any, Tuple, Optional
from app.core.exceptions import OrchestrationException

class TDGBuilder:
    """
    Module 5: Task Dependency Graph (TDG) Builder using NetworkX.
    Provides DAG validation, topological sorting, dependency resolution, and ready-task detection.
    """
    @staticmethod
    def build_tdg(subtasks: List[Dict[str, Any]]) -> Tuple[nx.DiGraph, Dict[str, Any]]:
        graph = nx.DiGraph()

        for s in subtasks:
            task_id = s.get("task_id") or f"task_{s['subtask_index']}"
            graph.add_node(task_id, **s)

        for s in subtasks:
            node_id = s.get("task_id") or f"task_{s['subtask_index']}"
            for parent_idx in s.get("dependencies", []):
                parent_id = f"task_{parent_idx}" if isinstance(parent_idx, int) else parent_idx
                if graph.has_node(parent_id):
                    graph.add_edge(parent_id, node_id)

        # DAG Validation
        if not nx.is_directed_acyclic_graph(graph):
            raise OrchestrationException("Task Dependency Graph contains cycles and is not a valid DAG.")

        tdg_json = {
            "is_valid_dag": True,
            "nodes": [{"id": n, **graph.nodes[n]} for n in graph.nodes()],
            "edges": [{"source": u, "target": v} for u, v in graph.edges()],
            "topological_order": list(nx.topological_sort(graph))
        }

        return graph, tdg_json

    @staticmethod
    def get_ready_tasks(graph: nx.DiGraph, completed_task_ids: set) -> List[str]:
        """Detect tasks whose dependencies have all been completed."""
        ready = []
        for node in graph.nodes():
            if node in completed_task_ids:
                continue
            parents = set(graph.predecessors(node))
            if parents.issubset(completed_task_ids):
                ready.append(node)
        return ready
